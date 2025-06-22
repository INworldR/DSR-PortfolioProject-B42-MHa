# RAG-Enhanced Cybersecurity Classification System

Advanced context-aware threat detection using RAG + Ollama LLM for MITRE ATT&CK classification.

## 🎯 Goals

- Reduce false positives through RAG-based context analysis
- Precise MITRE ATT&CK technique classification
- Confidence scoring for threat assessments
- Streamlit UI for analysis

## 🚀 Quick Start

```bash
# Setup
git clone <repository-url>
cd DSR-PortfolioProject-B42-MHa
python -m venv rag-env
source rag-env/bin/activate
pip install -r requirements.txt

# Configure
cp env.example .env
# Edit .env with your settings

# Test
python -m src.utils.config
python -m src.utils.ollama_client
python -m src.utils.chromadb_client
```

## 🏗️ Architecture

```
Streamlit UI → FastAPI → RAG Engine → ChromaDB + Ollama LLM
```

## 📁 Structure

```
src/
├── data/          # Data processing
├── models/        # ML models
├── rag/           # RAG engine
├── utils/         # Utilities
└── web_ui/        # Streamlit UI
```

## 🔧 Configuration

Edit `.env`:
```bash
OLLAMA_HOST=<your-server>
CHROMADB_HOST=<your-chromadb>
LOKI_HOST=<your-loki>
```

## 📊 Usage

```bash
# Start services
streamlit run src/web_ui/main.py
uvicorn src.api.main:app --reload
```

## 🤝 Team

- **Marc Haenle** - Project Lead
- **Krzysztof Buzar** - Technical Mentor
- **DSR Portfolio Project B42-MHa**

---

*RAG + Ollama + Streamlit for Cybersecurity Classification*
