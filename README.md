# FIAP 8IADT - Tech Challenge Fase 4: Sistema Multimodal de IA para Saúde da Mulher

**Repositório:** `fiap-tech-challenge-fase4-saude-mulher`
**Curso:** 8IADT - FIAP
**Fase:** 4 - Tech Challenge

## 📋 Descrição

Sistema multimodal de inteligência artificial para monitoramento contínuo da saúde da mulher, integrando análise de vídeo, áudio e texto para detecção precoce de riscos. O sistema utiliza modelos de deep learning (YOLOv8), processamento de linguagem natural e Azure Cognitive Services para apoiar decisões clínicas em tempo real.

## 🎯 Objetivos

- Detectar precocemente riscos em saúde materna e ginecológica
- Identificar sinais de violência doméstica ou abuso
- Monitorar bem-estar psicológico feminino
- Utilizar serviços em nuvem (Azure) para processamento especializado
- Aplicar técnicas de detecção de anomalias em tempo real

## 🧩 Funcionalidades Principais

### Análise de Vídeo (YOLOv8)
- Detecção de instrumentos cirúrgicos ginecológicos e áreas críticas
- Análise de sangramento anômalo em procedimentos
- Identificação de sinais não-verbais de desconforto ou medo
- Triagem de linguagem corporal indicativa de abuso

### Análise de Áudio
- Processamento de voz em consultas ginecológicas
- Detecção de ansiedade gestacional e depressão pós-parto
- Identificação de padrões vocais indicativos de trauma
- Hesitação e tom de voz na comunicação de sintomas

### Integração Azure
- Azure Cognitive Services (Speech-to-Text, Video Indexer, Computer Vision)
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
- [Issues do Projeto](https://github.com/LucsOlv/fiap-tech-challenge-fase4-saude-mulher/issues)
