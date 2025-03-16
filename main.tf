locals {
  default_tags = merge(
    var.tags,
    {
      Environment = var.environment
      Terraform   = "true"
      Module      = "ec2-start-stop-scheduled"
    }
  )
}

resource "aws_iam_role" "start_stop_lambda" {
  name = "ec2-${var.prefix}-${var.region}-${var.instance_state}-lambda-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF

  tags = local.default_tags
}

data "archive_file" "start_stop_lambda" {
  type        = "zip"
  source_dir  = "${path.module}/src/start_stop_lambda"
  output_path = "${path.module}/src/start_stop_lambda.zip"
}

resource "aws_iam_policy" "start_stop_lambda" {
  name        = "ec2-${var.prefix}-${var.region}-${var.instance_state}-lambda-policy"
  path        = "/"
  description = "Lambda Policy to Start or Stop Ec2 Instances"
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource" : "arn:aws:logs:*:*:*"
      },
      {
        "Effect" : "Allow",
        "Action" : [
          "ec2:Describe*",
          "ec2:Start*",
          "ec2:Stop*"
        ],
        "Resource" : "*"
      }
  ] })
}

resource "aws_iam_role_policy_attachment" "start_stop_lambda_policy_attachment" {
  policy_arn = aws_iam_policy.start_stop_lambda.arn
  role       = aws_iam_role.start_stop_lambda.name
}

resource "aws_lambda_function" "start_stop_lambda" {
  function_name    = "ec2-${var.prefix}-${var.region}-${var.instance_state}-lambda"
  description      = "${var.instance_state} instances with Tag:Name ${var.tag_key} and Tag:Value ${var.tag_value}"
  role             = aws_iam_role.start_stop_lambda.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.9"
  timeout          = 300
  filename         = data.archive_file.start_stop_lambda.output_path
  source_code_hash = data.archive_file.start_stop_lambda.output_base64sha256
  
  environment {
    variables = {
      "TAG_KEY"     = var.tag_key
      "TAG_VALUE"   = var.tag_value
      "INST_STATE"  = var.instance_state
      "INST_REGION" = var.region
    }
  }

  tags = local.default_tags
}

resource "aws_cloudwatch_event_rule" "start_stop_lambda_cw_event_rule" {
  name                = "ec2-${var.prefix}-${var.region}-${var.instance_state}-lambda-cw-event"
  description         = "Schedule to ${var.instance_state} ec2 instances"
  schedule_expression = var.cron_schedule
  
  tags = local.default_tags
}

resource "aws_cloudwatch_event_target" "start_stop_lambda" {
  rule      = aws_cloudwatch_event_rule.start_stop_lambda_cw_event_rule.name
  target_id = aws_lambda_function.start_stop_lambda.id
  arn       = aws_lambda_function.start_stop_lambda.arn
}

resource "aws_lambda_permission" "start_stop_lambda" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.start_stop_lambda.arn
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.start_stop_lambda_cw_event_rule.arn
}
