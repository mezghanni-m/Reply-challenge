data "azurerm_client_config" "current" {}

locals {
  fixedcodespacename = "code-391ff5ac-6576-460f-ba4d-7e03433c68b6"
}

data "azurerm_subscription" "current" {
}

data "azurerm_resource_group" "existing_rg" {
  name = var.resource_group_name
}

data "azurerm_storage_account" "existing_storageaccount" {
  resource_group_name = data.azurerm_resource_group.existing_rg
  name = var.storage_account_name

}
resource "azurerm_key_vault" "key_vault" {
  name                        = "keyvault"
  location                    = data.azurerm_resource_group.existing_rg.location
  resource_group_name         = data.azurerm_resource_group.existing_rg.name
  tenant_id                   = var.tenant_id

  sku_name = "standard"

}

resource "azurerm_machine_learning_workspace" "ml" {
  
  name = var.name
  location                = data.azurerm_resource_group.existing_rg.location
  resource_group_name     = var.resource_group_name
  application_insights_id = var.application_insights_id
  key_vault_id            = azurerm_key_vault.key_vault.id
  storage_account_id      = data.azurerm_storage_account.existing_storageaccount.id
  container_registry_id   = var.container_registry_id

  public_network_access_enabled = true

  identity {
    type = "UserAssigned"
  }


}


resource "time_sleep" "wait_30_seconds" {
  depends_on = [azurerm_machine_learning_workspace.ml]

  create_duration = "60s"
}

resource "null_resource" "waitazureml" {
  depends_on = [time_sleep.wait_30_seconds]
}

data "azurerm_storage_share" "existing_share" {
  name                 = local.fixedcodespacename
  storage_account_name = module.tfdp-bs-az-storageaccount-module.storage_account.name
  depends_on           = [azurerm_machine_learning_workspace.ml, null_resource.waitazureml]
}

resource "azurerm_storage_share_directory" "train_folder" {
  name                 = "training_experiment"
  share_name           = data.azurerm_storage_share.existing_share.name
  storage_account_name = module.tfdp-bs-az-storageaccount-module.storage_account.name

  depends_on           = [data.azurerm_storage_share.existing_share]
}

resource "azurerm_storage_share_file" "storageaccountfileshare" {
  name             = "train_dbscan.py"
  path             = "training_experiment"
  storage_share_id = data.azurerm_storage_share.existing_share.id
  source           = "${path.root}/train_dbscan.py"

  depends_on           = [azurerm_storage_share_directory.train_folder]
}