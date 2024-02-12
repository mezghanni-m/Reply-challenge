output "azureml_workspace_name" {
  #value = "none"
  value = azurerm_machine_learning_workspace.ml.name
}

output "azurerm_machine_learning_workspace" {
  #value = "none"
  value = azurerm_machine_learning_workspace.ml
}