output "lambda_function_arn" {
  description = "The ARN of the Lambda function"
  value       = aws_lambda_function.start_stop_lambda.arn
}

output "lambda_function_name" {
  description = "The name of the Lambda function"
  value       = aws_lambda_function.start_stop_lambda.function_name
}

output "cloudwatch_event_rule_arn" {
  description = "The ARN of the CloudWatch Event Rule"
  value       = aws_cloudwatch_event_rule.start_stop_lambda_cw_event_rule.arn
}

output "iam_role_arn" {
  description = "The ARN of the IAM role"
  value       = aws_iam_role.start_stop_lambda.arn
} 