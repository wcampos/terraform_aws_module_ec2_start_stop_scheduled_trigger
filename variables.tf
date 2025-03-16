variable "region" {
  type        = string
  default     = ""
  description = "EC2 Instances Region"
}

variable "prefix" {
  type = string
  default = ""
  description = "Prefix will be append to elements name"
}

variable "tag_key" {
  type        = string
  default     = ""
  description = "Name of the Tag:Key used on ec2 filter"
}

variable "tag_value" {
  type        = string
  default     = ""
  description = "Value for the Tag:Value used for ec2 filter"
}

variable "instance_state" {
  type        = string
  default     = ""
  description = "Desire state for Ec2s. Available options: [ 'Start', 'Stop']"
}

variable "cron_schedule" {
  type        = string
  default     = "cron(0 12 * * ? *)"
  description = "Cron Expression to Start or Stop EC2s. Format for cron cron(0 12 * * ? *)"
}

variable "tags" {
  description = "A map of tags to add to all resources"
  type        = map(string)
  default     = {}
}

variable "environment" {
  description = "Environment name for the resources"
  type        = string
  default     = "prod"
}