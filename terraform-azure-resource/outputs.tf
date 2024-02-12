output "tenant_id" {
  value = var.tenant_id
}

output "subscription_id" {
  value = var.subscription_id
}

output "spn_user_id" {
  value = var.spn_user_id
}

output "azurerm_container_registry" {
  sensitive = true
  value = azurerm_container_registry.acr
}


output "azurerm_log_analytics_workspace" {
  sensitive = true
  value = azurerm_log_analytics_workspace.law
}

output "azurerm_application_insights" {
  sensitive = true
  value = azurerm_application_insights.appi
}

output "azurerm_machine_learning_workspace" {
  value = module.aml.azurerm_machine_learning_workspace
}