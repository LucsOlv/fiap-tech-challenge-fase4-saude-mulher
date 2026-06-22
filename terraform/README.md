# Terraform — Infraestrutura Azure do Tech Challenge Fase 4

**Tempo de deploy:** ~5 minutos  
**Custo mensal:** R$ 0 com tier gratuito + R$ 5-15 OpenAI (uso leve)  
**Custo com Azure for Students:** R$ 0 (créditos de $100)

## Pré-requisitos

```bash
# 1. Instalar Azure CLI
brew install azure-cli      # macOS
# ou: https://docs.microsoft.com/cli/azure/install-azure-cli

# 2. Instalar Terraform
brew install terraform       # macOS
# ou: https://developer.hashicorp.com/terraform/downloads

# 3. Login na Azure
az login
# ↑ abre navegador pra autenticar com sua conta FIAP
```

## Deploy (3 comandos)

```bash
cd terraform/

# 1. Inicializar
terraform init

# 2. Ver o que vai ser criado (sem deploy)
terraform plan

# 3. Criar tudo
terraform apply -auto-approve
```

Depois de ~5 minutos, o Terraform vai exibir o `.env` completo pra você copiar.

## Gerar o .env do projeto

```bash
# Extrai as chaves e gera o .env automaticamente
terraform output -raw env_file_template > ../.env
```

## 💰 Custos

| Recurso | SKU | Custo/mês |
|---------|-----|:---------:|
| Cognitive Services (Speech + Vision) | F0 (grátis) | R$ 0 |
| Azure OpenAI | S0 | ~R$ 5-15 |
| Storage Account (5 GB) | Standard LRS | ~R$ 0,50 |
| Key Vault | Standard | ~R$ 1 |
| **Total** | | **~R$ 6-16** |

### Otimizações pra economizar:

1. **Azure for Students**: ganha $100 crédito → custo real R$ 0
2. Mudar `openai_model` pra `gpt-4o-mini` já está como default (10x mais barato)
3. Mudar `cognitive_sku` pra `F0` em `terraform.tfvars` (grátis)
4. Só deployar OpenAI quando for realmente usar

## O que é criado

| Recurso | Nome | Propósito |
|---------|------|-----------|
| Resource Group | `rg-fiap-saude-mulher` | Agrupa tudo |
| Cognitive Services | `cog-fiap-saude-mulher` | Speech-to-Text + Computer Vision |
| Azure OpenAI | `oai-fiap-saude-mulher` | GPT-4o-mini pra sumarização e NLP |
| Storage Account | `stfiapsaudemulher` | Blob Storage pra vídeos/áudios |
| Key Vault | `kv-fiap-saude-mulher` | Secrets e chave de criptografia |

## Destruir tudo (quando não precisar mais)

```bash
terraform destroy
# ⚠️ Isso apaga TODOS os recursos. Dados não são recuperáveis.
```

## Troubleshooting

**Erro: `quota exceeded`**  
→ OpenAI tem cota limitada por subscription. Peça aumento no portal Azure.

**Erro: `name already in use`**  
→ Mude os nomes dos recursos em `main.tf` (são globais pra storage/key vault).

**Erro: `sku F0 not available in brazilsouth`**  
→ Troque `location` pra `eastus` no `terraform.tfvars`.
