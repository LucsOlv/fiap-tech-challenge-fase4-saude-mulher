# FIAP 8IADT - Tech Challenge Fase 4: Sistema Multimodal de IA para Saúde da Mulher

**Repositório:** `fiap-tech-challenge-fase4-saude-mulher`
**Curso:** 8IADT - FIAP
**Fase:** 4 - Tech Challenge

## 📋 Descrição

Sistema multimodal de inteligência artificial para monitoramento contínuo da saúde da mulher, integrando análise de vídeo, áudio e texto para detecção precoce de riscos. O sistema utiliza modelos de deep learning (YOLOv8), processamento de linguagem natural e Azure Cognitive Services para apoiar decisões clínicas em tempo real.

## 🎯 Escopo Definido (Issue #1)

### Funcionalidades escolhidas (4 de 4):
- [x] Analisar vídeos de partos, cirurgias ginecológicas, fisioterapia pós-parto e consultas
- [x] Processar gravações de voz de pacientes (depressão pós-parto, ansiedade, violência doméstica)
- [x] Detectar anomalias em sinais vitais (pressão arterial, batimentos fetais, prescrições)
- [x] Integrar com Azure Cognitive Services (Speech, Video Indexer, Computer Vision, OpenAI)

### Objetivos escolhidos (5 de 5):
- [x] Detectar precocemente riscos em saúde materna e ginecológica
- [x] Identificar sinais de violência doméstica ou abuso
- [x] Monitorar bem-estar psicológico feminino
- [x] Utilizar serviços em nuvem (Azure) para processamento especializado
- [x] Aplicar técnicas de detecção de anomalias em tempo real

### Alvo do YOLOv8:
- [x] **Sangramento anômalo durante procedimentos** — detecção visual de hemorragia em vídeos cirúrgicos

## 🧩 Funcionalidades Principais

### Análise de Vídeo (YOLOv8)
- Detecção de sangramento anômalo em procedimentos cirúrgicos ginecológicos
- Análise de áreas críticas (útero, ovários, mamas)
- Identificação de sinais não-verbais de desconforto ou medo
- Triagem de linguagem corporal indicativa de abuso

### Análise de Áudio
- Processamento de voz em consultas ginecológicas
- Detecção de ansiedade gestacional e depressão pós-parto
- Identificação de padrões vocais indicativos de trauma
- Hesitação e tom de voz na comunicação de sintomas

### Integração Azure
- Azure Cognitive Services (Speech-to-Text, Video Indexer, Computer Vision, OpenAI)
- Processamento escalável em nuvem
- Padrões elevados de privacidade e segurança (LGPD)

## 📦 Entregáveis

| Item | Descrição |
|------|-----------|
| **Código-fonte** | Solução completa com todos os módulos |
| **Relatório Técnico** | Fluxo multimodal, modelos, resultados, exemplos |
| **Vídeo Demo** | Até 15 min no YouTube/Vimeo demonstrando o sistema |

## 🚀 Estrutura do Projeto

```
.
├── docs/               # Documentação e relatório técnico
├── src/
│   ├── video/          # Módulo de análise de vídeo (YOLOv8)
│   ├── audio/          # Módulo de análise de áudio
│   ├── text/           # Módulo de análise de texto
│   ├── fusion/         # Fusão multimodal
│   ├── azure/          # Integração Azure Cognitive Services
│   └── dashboard/      # Interface de alertas
├── notebooks/          # Jupyter notebooks exploratórios
├── tests/              # Testes unitários e de integração
└── data/               # Datasets (não versionados)
```

## 🔗 Links

- [Tech Challenge - Fase 4 (PDF)](./docs/8IADT%20-%20Fase%204%20-%20Tech%20challenge%20Secretaria.pdf)
- [Relatório Técnico](./docs/relatorio-tecnico.md)
- [Issues do Projeto](https://github.com/LucsOlv/fiap-tech-challenge-fase4-saude-mulher/issues)
- [PRs do Projeto](https://github.com/LucsOlv/fiap-tech-challenge-fase4-saude-mulher/pulls)

## 🚀 Instalação Rápida

```bash
git clone https://github.com/LucsOlv/fiap-tech-challenge-fase4-saude-mulher.git
cd fiap-tech-challenge-fase4-saude-mulher
bash setup.sh
source venv/bin/activate
```

### Executar testes
```bash
pytest tests/ -v          # 121 testes
pytest --cov=src tests/   # Com cobertura
```

### Executar Dashboard
```bash
streamlit run src/dashboard/app.py
```

### Configurar Azure
Copie `.env.example` para `.env` e preencha suas credenciais Azure.

## 📊 Status do Projeto

| Métrica | Valor |
|---------|-------|
| **Módulos** | 7 (video, audio, text, fusion, azure, security, dashboard) |
| **Arquivos de código** | 40 |
| **Testes** | 121 (100% passando) |
| **Issues criadas** | 17 |
| **PRs merged** | 2 |
| **Cobertura** | Testes unitários + integração |

## 🛡️ Stack Tecnológica

| Categoria | Tecnologia |
|-----------|-----------|
| **Linguagem** | Python 3.10+ |
| **Deep Learning** | PyTorch, Ultralytics YOLOv8, Transformers |
| **Áudio** | Librosa, Whisper, SoundFile |
| **NLP** | spaCy, scikit-learn |
| **Cloud** | Azure Cognitive Services |
| **Dashboard** | Streamlit, Plotly |
| **Segurança** | Cryptography (AES), TLS 1.3 |
| **Testes** | Pytest |
| **LGPD** | Anonimização, criptografia, auditoria |
