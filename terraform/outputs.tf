# ═══════════════════════════════════════════════════════════
# Outputs — copie e cole no .env do projeto
# ═══════════════════════════════════════════════════════════

output "instructions" {
  value = <<-EOT



  ╔═══════════════════════════════════════════════════════╗
  ║   AZURE PROVISIONADO!                                ║
  ║   Copie os valores abaixo para seu arquivo .env:     ║
  ╚═══════════════════════════════════════════════════════╝

  EOT
}

output "env_file_template" {
  value = templatefile("${path.module}/.env.tftpl", {
    speech_endpoint = "https://${azurerm_cognitive_account.speech_vision.custom_subdomain_name}.cognitiveservices.azure.com/"
    speech_key      = azurerm_cognitive_account.speech_vision.primary_access_key
    speech_region   = var.location

    vision_endpoint = "https://${azurerm_cognitive_account.speech_vision.custom_subdomain_name}.cognitiveservices.azure.com/"
    vision_key      = azurerm_cognitive_account.speech_vision.primary_access_key

    openai_endpoint  = "https://${azurerm_cognitive_account.openai.custom_subdomain_name}.openai.azure.com/"
    openai_key       = azurerm_cognitive_account.openai.primary_access_key
    openai_deployment = azurerm_cognitive_deployment.gpt4o.name

    storage_connection = azurerm_storage_account.saude_mulher.primary_connection_string
    storage_container  = azurerm_storage_container.dados.name

    key_vault_url = azurerm_key_vault.saude_mulher.vault_uri

    encryption_key = random_string.encryption_key.result
  })
  sensitive = true
}

# ─── Outputs individuais (pra debug/verificação) ──────────

output "resource_group" {
  value = azurerm_resource_group.saude_mulher.name
}

output "cognitive_services_endpoint" {
  value = "https://${azurerm_cognitive_account.speech_vision.custom_subdomain_name}.cognitiveservices.azure.com/"
}

output "openai_endpoint" {
  value = "https://${azurerm_cognitive_account.openai.custom_subdomain_name}.openai.azure.com/"
}

output "openai_deployment" {
  value = azurerm_cognitive_deployment.gpt4o.name
}

output "storage_account_name" {
  value = azurerm_storage_account.saude_mulher.name
}

output "key_vault_uri" {
  value = azurerm_key_vault.saude_mulher.vault_uri
}
