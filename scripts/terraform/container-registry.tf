#
# Creates a container registry on Azure so that we can publish Docker images.
#
resource "azurerm_container_registry" "container_registry" {
  name                = var.app_name
  resource_group_name = azurerm_resource_group.bmzk1.name
  location            = var.location
  admin_enabled       = true
  sku                 = "Basic"
}