#
# Creates a resource group for our two services in Azure account.
#
resource "azurerm_resource_group" "bmzk1" {
  name     = var.app_name
  location = var.location
}
