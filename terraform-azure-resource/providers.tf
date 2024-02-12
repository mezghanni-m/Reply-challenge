terraform {
  required_version = ">= 1.3.6"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "= 3.72.0"
    }

    time = {
      source  = "hashicorp/time"
      version = "= 0.9.1"
    }

    null = {
      source  = "hashicorp/null"
      version = "= 3.2.1"
    }
  }
}
