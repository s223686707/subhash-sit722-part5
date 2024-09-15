provider "azurerm" {
  features {}

  subscription_id = var.subscription_id
  client_id       = var.client_id
  client_secret   = var.client_secret
  tenant_id       = var.tenant_id
}

# Sets global variables for this Terraform project.
variable "app_name" {
  description = "The name of the application"
}

variable "location" {
  default = "australiasoutheast"
}

variable "kubernetes_version" {
  description = "The version of Kubernetes to use"
}

# Creates a resource group for our two services in Azure account.
resource "azurerm_resource_group" "bmok1" {
  name     = var.app_name
  location = var.location
}

# Creates a managed Kubernetes cluster on Azure.
resource "azurerm_kubernetes_cluster" "cluster" {
  name                = var.app_name
  location            = var.location
  resource_group_name = azurerm_resource_group.bmok1.name
  dns_prefix          = var.app_name
  kubernetes_version  = var.kubernetes_version

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_D2s_v3"
  }

  identity {
    type = "SystemAssigned"
  }
}

# Creates a container registry on Azure so that we can publish Docker images.
resource "azurerm_container_registry" "container_registry" {
  name                = var.app_name
  resource_group_name = azurerm_resource_group.bmok1.name
  location            = var.location
  admin_enabled       = true
  sku                 = "Basic"
}