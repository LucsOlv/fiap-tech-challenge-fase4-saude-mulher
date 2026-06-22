variable "location" {
  description = "Região Azure"
  type        = string
  default     = "brazilsouth"
}

variable "cognitive_sku" {
  description = "SKU do Cognitive Services (Speech + Vision)"
  type        = string
  default     = "S0" # Standard. Gratuito: F0 (mas sem SLA)
  validation {
    condition     = contains(["F0", "S0"], var.cognitive_sku)
    error_message = "SKU deve ser F0 (gratuito) ou S0 (standard)."
  }
}

variable "openai_sku" {
  description = "SKU do Azure OpenAI"
  type        = string
  default     = "S0"
}

variable "openai_model" {
  description = "Modelo OpenAI a deployar"
  type        = string
  default     = "gpt-4o-mini" # Mais barato (~1/10 do custo do gpt-4o)
  validation {
    condition     = contains(["gpt-4o", "gpt-4o-mini", "gpt-4", "gpt-35-turbo"], var.openai_model)
    error_message = "Modelo deve ser gpt-4o, gpt-4o-mini, gpt-4, ou gpt-35-turbo."
  }
}

variable "openai_model_version" {
  description = "Versão do modelo OpenAI"
  type        = string
  default     = "2024-07-18"
}

variable "environment" {
  description = "Ambiente (dev / prod)"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Nome do projeto (usado em tags)"
  type        = string
  default     = "fiap-saude-mulher"
}
