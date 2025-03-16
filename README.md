# AWS EC2 Start/Stop Scheduled Trigger Terraform Module

This Terraform module creates an AWS Lambda function that can start or stop EC2 instances based on tags and a schedule.

## Features

- Automatically start/stop EC2 instances based on tags
- Configurable schedule using CloudWatch Events (EventBridge)
- Customizable through variables
- Includes proper IAM roles and permissions
- Supports resource tagging

## Usage

```hcl
module "ec2_start_stop" {
  source = "github.com/wcampos/terraform_aws_module_ec2_start_stop_scheduled_trigger"

  region         = "us-west-2"
  prefix         = "prod"
  tag_key        = "Environment"
  tag_value      = "Production"
  instance_state = "Stop"
  cron_schedule  = "cron(0 20 ? * MON-FRI *)" # Stop at 8 PM on weekdays

  tags = {
    Project     = "CostOptimization"
    ManagedBy   = "Terraform"
  }
}
```

## Requirements

- Terraform >= 1.0
- AWS Provider >= 4.0
- Python 3.9 (for Lambda function)

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| region | EC2 Instances Region | string | - | yes |
| prefix | Prefix will be append to elements name | string | - | yes |
| tag_key | Name of the Tag:Key used on ec2 filter | string | - | yes |
| tag_value | Value for the Tag:Value used for ec2 filter | string | - | yes |
| instance_state | Desire state for Ec2s. Available options: [ 'Start', 'Stop'] | string | - | yes |
| cron_schedule | Cron Expression to Start or Stop EC2s | string | "cron(0 12 * * ? *)" | no |
| tags | A map of tags to add to all resources | map(string) | {} | no |
| environment | Environment name for the resources | string | "prod" | no |

## Outputs

| Name | Description |
|------|-------------|
| lambda_function_arn | The ARN of the Lambda function |
| lambda_function_name | The name of the Lambda function |
| cloudwatch_event_rule_arn | The ARN of the CloudWatch Event Rule |
| iam_role_arn | The ARN of the IAM role |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT Licensed. See LICENSE for full details.