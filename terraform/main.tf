# ─── FIAP Tech Challenge Fase 4 ───
# Infraestrutura Azure (Terraform)
#
# Pré-requisitos:
#   1. Azure CLI:  brew install azure-cli
#   2. Login:      az login
#   3. Terraform:  brew install terraform  (v1.5+)
#
# Custo mensal estimado (tiers Standard + free): ~R$ 0-30
# Com free tier do Azure Students: R$ 0

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy    = false
      recover_soft_deleted_key_vaults = true
    }
    cognitive_account {
      purge_soft_delete_on_destroy = true
    }
  }
}

# ─── Resource Group ─────────────────────────────────────────

resource "azurerm_resource_group" "saude_mulher" {
  name     = "rg-fiap-saude-mulher"
  location = var.location
}

# ─── Cognitive Services (Speech + Vision) ───────────────────
# Usamos uma conta multi-service pra Speech-to-Text e Computer Vision

resource "azurerm_cognitive_account" "speech_vision" {
  name                = "cog-fiap-saude-mulher"
  location            = azurerm_resource_group.saude_mulher.location
  resource_group_name = azurerm_resource_group.saude_mulher.name
  kind                = "CognitiveServices" # multi-service: Speech + Vision
  sku_name            = var.cognitive_sku

  custom_subdomain_name = "cog-fiap-saude-mulher"

  network_acls {
    default_action = "Allow" # Prod: mudar pra Deny + IPs da rede hospitalar
  }
}

# ─── Azure OpenAI ───────────────────────────────────────────

resource "azurerm_cognitive_account" "openai" {
  name                = "oai-fiap-saude-mulher"
  location            = azurerm_resource_group.saude_mulher.location
  resource_group_name = azurerm_resource_group.saude_mulher.name
  kind                = "OpenAI"
  sku_name            = var.openai_sku

  custom_subdomain_name = "oai-fiap-saude-mulher"
}

# Deployment do modelo GPT-4o (ou GPT-4o-mini pra economizar)

resource "azurerm_cognitive_deployment" "gpt4o" {
  name                 = "gpt-4o"
  cognitive_account_id = azurerm_cognitive_account.openai.id

  model {
    format  = "OpenAI"
    name    = var.openai_model
    version = var.openai_model_version
  }

  scale {
    type     = "Standard"
    capacity = 10 # 10K TPM
  }
}

# ─── Storage Account (Blob) ─────────────────────────────────

resource "azurerm_storage_account" "saude_mulher" {
  name                     = "stfiapsaudemulher"
  resource_group_name      = azurerm_resource_group.saude_mulher.name
  location                 = azurerm_resource_group.saude_mulher.location
  account_tier             = "Standard"
  account_replication_type = "LRS" # Local - barato. Mudar pra GRS em prod.
  account_kind             = "StorageV2"

  min_tls_version           = "TLS1_2"
  enable_https_traffic_only = true

  blob_properties {
    versioning_enabled       = true
    change_feed_enabled      = true
    last_access_time_enabled = true

    delete_retention_policy {
      days = 30
    }

    container_delete_retention_policy {
      days = 30
    }
  }
}

resource "azurerm_storage_container" "dados" {
  name                  = "saude-mulher-data"
  storage_account_id    = azurerm_storage_account.saude_mulher.id
  container_access_type = "private"
}

resource "azurerm_storage_container" "videos" {
  name                  = "saude-mulher-videos"
  storage_account_id    = azurerm_storage_account.saude_mulher.id
  container_access_type = "private"
}

resource "azurerm_storage_container" "audio" {
  name                  = "saude-mulher-audio"
  storage_account_id    = azurerm_storage_account.saude_mulher.id
  container_access_type = "private"
}

# ─── Key Vault ──────────────────────────────────────────────

data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "saude_mulher" {
  name                       = "kv-fiap-saude-mulher"
  location                   = azurerm_resource_group.saude_mulher.location
  resource_group_name        = azurerm_resource_group.saude_mulher.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  soft_delete_retention_days = 30
  enable_rbac_authorization  = true

  network_acls {
    default_action = "Allow"
    bypass         = "AzureServices"
  }
}

# ─── Secrets no Key Vault ───────────────────────────────────

resource "azurerm_key_vault_secret" "speech_key" {
  name         = "azure-speech-key"
  value        = azurerm_cognitive_account.speech_vision.primary_access_key
  key_vault_id = azurerm_key_vault.saude_mulher.id
}

resource "azurerm_key_vault_secret" "vision_key" {
  name         = "azure-vision-key"
  value        = azurerm_cognitive_account.speech_vision.primary_access_key
  key_vault_id = azurerm_key_vault.saude_mulher.id
}

resource "azurerm_key_vault_secret" "openai_key" {
  name         = "azure-openai-key"
  value        = azurerm_cognitive_account.openai.primary_access_key
  key_vault_id = azurerm_key_vault.saude_mulher.id
}

resource "azurerm_key_vault_secret" "storage_connection" {
  name         = "azure-storage-connection-string"
  value        = azurerm_storage_account.saude_mulher.primary_connection_string
  key_vault_id = azurerm_key_vault.saude_mulher.id
}

# ─── Encryption key para dados em repouso (LGPD) ────────────

resource "random_string" "encryption_key" {
  length  = 32
  special = true
}

resource "azurerm_key_vault_secret" "encryption_key" {
  name         = "data-encryption-key"
  value        = random_string.encryption_key.result
  key_vault_id = azurerm_key_vault.saude_mulher.id
}
