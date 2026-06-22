#!/bin/bash
set -e
echo "=== FIAP Tech Challenge Fase 4 - Setup ==="

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download pt_core_news_sm 2>/dev/null || echo "spaCy model: install manually if needed"

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ".env file created from template. Edit with your Azure credentials."
fi

mkdir -p data/raw data/processed data/samples models
echo ""
echo "Setup complete! Activate with: source venv/bin/activate"
echo "Run tests with: pytest tests/ -v"
echo "Run dashboard with: streamlit run src/dashboard/app.py"
