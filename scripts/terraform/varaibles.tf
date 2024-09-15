variable "subscription_id" {
  type        = string
  description = "The subscription ID for the Azure account"
}

variable "client_id" {
  type        = string
  description = "The client ID of the Azure service principal"
}

variable "client_secret" {
  type        = string
  description = "The client secret of the Azure service principal"
  sensitive   = true
}

variable "tenant_id" {
  type        = string
  description = "The tenant ID for the Azure account"
}