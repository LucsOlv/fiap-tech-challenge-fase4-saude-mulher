# AGENTS.md - FIAP Tech Challenge Fase 4

## Project Context

- **Course:** 8IADT at FIAP
- **Phase:** Fase 4 - Tech Challenge (weight: 90% of all courses this phase)
- **Repository:** `fiap-tech-challenge-fase4-saude-mulher` (public)
- **Owner:** LucsOlv
- **Language:** Python (primary), with shell scripts for automation

## Project Description

Multimodal AI system for continuous women's health monitoring. The system
processes video (surgeries, consultations), audio (voice recordings), and text
(medical reports, prescriptions) to detect early risk signals and alert
specialized medical teams in real time.

## Core Architecture

```
Video (YOLOv8) ──┐
Audio (NLP/ML) ──┼── Fusion Engine ──► Dashboard/Alerts
Text (NLP) ──────┘
Azure Cognitive Services (cloud layer)
```

## Technology Stack

- **Video Analysis:** YOLOv8 (custom training), OpenCV, PyTorch
- **Audio Analysis:** Whisper/Speech-to-Text, wav2vec 2.0, librosa
- **Text Analysis:** NLP with GPT/Azure OpenAI, spaCy (Portuguese)
- **Cloud:** Azure Cognitive Services, Azure Blob Storage
- **Dashboard:** Streamlit or FastAPI + React
- **Security:** LGPD compliance, Azure Key Vault, data encryption

## Key Deliverables (from PDF)

1. **Git repository** with complete source code
2. **Technical report** describing:
   - Multimodal flow
   - Models used for each data type
   - Results and examples of detected anomalies
3. **Video demo** (up to 15 min, YouTube/Vimeo) showing:
   - Audio and video analysis in practice
   - Anomaly detection and response
   - Azure integration
   - Final alert flow to medical team

## Mandatory Requirements

### 1. Video Analysis (YOLOv8 custom)
- Process: surgeries, consultations, physiotherapy, domestic violence screening
- Custom YOLOv8 for one of: surgical instruments, critical areas (uterus,
  ovaries, breasts), anomalous bleeding, self-harm indicators
- Auto reports: obstetric deviations, surgical complications, psychological
  discomfort indicators, domestic violence alerts

### 2. Audio Analysis
- Process: gynecological consultations, prenatal follow-up, post-partum
  consultations, domestic violence victim care
- Detect: voice tone, symptom reporting hesitation, gestational anxiety,
  post-partum depression, trauma voice patterns

### 3. Multimodal Fusion
- Fuse text + audio + video into unified risk assessment
- Real-time anomaly detection (vital signs, fetal heartbeats, hormonal
  prescriptions, clinical evolution)

### 4. Azure Cloud Integration
- Azure Cognitive Services for scalable processing
- Highest privacy and security standards for sensitive data

## Student Decisions Required

The PDF specifies "choose at least 2" features and "choose at least 3"
objectives. The team must decide:
- Which video features (2+ from 4 options)
- Which objectives (3+ from 5 options)
- Which YOLOv8 detection target (1 from 4 options or custom)

## Build & Run

```bash
# Setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run dashboard
streamlit run src/dashboard/app.py
```

## Code Style

- Python with type hints wherever practical
- Docstrings in English for critical functions
- Config via environment variables (.env.example provided)
- All sensitive credentials via Azure Key Vault or env vars
