#
# Creates a managed Kubernetes cluster on Azure.
#
resource "azurerm_kubernetes_cluster" "cluster" {
    name                = var.app_name
    location            = var.location
    resource_group_name = azurerm_resource_group.bmzk1.name
    dns_prefix          = var.app_name
    kubernetes_version  = var.kubernetes_version

    default_node_pool {
        name            = "default"
        node_count      = 1
        vm_size         = "Standard_D2s_v3"
    }

    
    identity {
        type = "SystemAssigned"
    }    
}


