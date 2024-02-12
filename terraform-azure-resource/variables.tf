# Subscription

variable "tenant_id" {
  type = string
}

variable "subscription_id" {
  type = string
}

# SPN Credentials

variable "spn_user_id" {
  type = string
}

variable "spn_user_secret" {
  type = string
}

variable "resource_group_name" {
  type = string
}

variable "storage_account_id" {
  type = string
}
variable "storage_account_name" {
  type = string
}