
# Terraform Module to Start and Stop EC2 Instances based on schedule

This module requires a tag:key and tag:value to query aws ec2 instances and apply the schedule to stop or start

**Scheduled events are managed by a Cron, the format can be found: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html**

## How to use

Example:
```bash
module "stop_jenkins" {
  source = "git::https://github.com/wcampos/terraform_aws_module_ec2_start_stop_scheduled_trigger.git"

  region         = "us-east-1"
  prefix         = "test"
  tag_key        = "Name"
  tag_value      = "MyMachineName"
  instance_state = "Stop"
  cron_schedule  = "cron(0 12 * * ? *)"

}
```

<!-- BEGIN_TF_DOCS -->
## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_archive"></a> [archive](#provider\_archive) | n/a |
| <a name="provider_aws"></a> [aws](#provider\_aws) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_cloudwatch_event_rule.start_stop_lambda_cw_event_rule](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_rule) | resource |
| [aws_cloudwatch_event_target.start_stop_lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_target) | resource |
| [aws_iam_policy.start_stop_lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_role.start_stop_lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.start_stop_lambda_policy_attachment](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_lambda_function.start_stop_lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_permission.start_stop_lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_permission) | resource |
| [archive_file.start_stop_lambda](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_cron_schedule"></a> [cron\_schedule](#input\_cron\_schedule) | Cron Expression to Start or Stop EC2s | `string` | `""` | no |
| <a name="input_instance_state"></a> [instance\_state](#input\_instance\_state) | Desire state for Ec2s. Available options: [ 'Start', 'Stop'] | `string` | `""` | no |
| <a name="input_region"></a> [region](#input\_region) | EC2 Instances Region | `string` | `""` | no |
| <a name="input_tag_key"></a> [tag\_key](#input\_tag\_key) | Name of the Tag:Key used on ec2 filter | `string` | `""` | no |
| <a name="input_tag_value"></a> [tag\_value](#input\_tag\_value) | Value for the Tag:Value used for ec2 filter | `string` | `""` | no |

## Outputs

No outputs.
<!-- END_TF_DOCS -->