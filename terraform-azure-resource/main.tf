
provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy    = true
      recover_soft_deleted_key_vaults = true
    }
  }

  skip_provider_registration = true

  tenant_id       = var.tenant_id
  subscription_id = var.subscription_id
  client_id       = var.spn_user_id
  client_secret   = var.spn_user_secret
}



data "azurerm_subscription" "current" {
}

data "azurerm_resource_group" "existing_rg" {
  name = var.resource_group_name
}


# prerequisites: container registry

resource "azurerm_container_registry" "acr" {


  name = "crazureml"

  resource_group_name = data.azurerm_resource_group.existing_rg.name
  location            = data.azurerm_resource_group.existing_rg.location

  sku           = "free"
  admin_enabled = false

  public_network_access_enabled = false
  anonymous_pull_enabled        = false

}


resource "azurerm_log_analytics_workspace" "law" {

  name = "lawazureml"

  location            = data.azurerm_resource_group.existing_rg.location
  resource_group_name = data.azurerm_resource_group.existing_rg.name
  sku                 = "Free"

}

resource "azurerm_application_insights" "appi" {

  name = "appiazureml"

  location            = data.azurerm_resource_group.existing_rg.location
  resource_group_name = data.azurerm_resource_group.existing_rg.name
  workspace_id        = azurerm_log_analytics_workspace.law.id
  application_type    = "web"

  depends_on           = [azurerm_log_analytics_workspace.law]
}


module "aml" {
  source = "./aml"

  name = "azureml"

  resource_group_name = data.azurerm_resource_group.existing_rg.name


  application_insights_id    = azurerm_application_insights.appi.id
  container_registry_id      = azurerm_container_registry.acr.id

 
  storage_account_id = var.storage_account_id
  storage_account_name = var.storage_account_name
  tenant_id = var.tenant_id
}