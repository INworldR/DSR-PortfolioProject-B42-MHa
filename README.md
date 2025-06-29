# DSR Cybersecurity RAG System

Advanced context-aware threat detection using RAG (Retrieval-Augmented Generation) + LLM for MITRE ATT&CK classification.

## 🎯 Project Goals

- **Automated Dataset Management**: Download and process cybersecurity datasets from Hugging Face Hub
- **RAG Pipeline**: Context-aware threat analysis using ChromaDB and LLM
- **MITRE ATT&CK Integration**: Precise technique classification and mapping
- **Professional Documentation**: Complete Sphinx documentation with ReadTheDocs theme
- **Modular Architecture**: Clean, maintainable codebase with type hints and error handling

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git
- Virtual environment (recommended)

### Installation

```bash
# Clone repository
git clone <repository-url>
cd DSR-PortfolioProject-B42-MHa

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp env.example .env
# Edit .env with your settings (optional - defaults work)
```

### Dataset Management

```bash
# Download all cybersecurity datasets
python src/01_get_datasets.py

# Preview downloaded datasets
python src/02_preview_datasets.py
```

### Documentation

```bash
# Build documentation
cd docs
make html

# View documentation (optional)
python -m http.server 8000 --directory _build/html
# Open http://localhost:8000 in browser
```

## 📊 Supported Datasets

The system automatically downloads and manages 4 key cybersecurity datasets:

1. **Heimdall** - Cybersecurity conversation dataset (~26MB)
2. **TTP Mapping** - MITRE ATT&CK technique relationships (~2MB)
3. **Security Attacks** - Attack pattern examples (~150KB)
4. **Cyber Rules** - Detection rules and signatures (~4MB)

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │───▶│   RAG Engine    │───▶│  ChromaDB +     │
│                 │    │                 │    │  LLM     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Configuration  │    │  Dataset Mgmt   │    │  Vector Store   │
│  Management     │    │  & Processing   │    │  & Embeddings   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
DSR-PortfolioProject-B42-MHa/
├── src/
│   ├── 01_get_datasets.py      # Dataset download functionality
│   ├── 02_preview_datasets.py  # Dataset preview functionality
│   ├── utils/                  # Utilities and config
│   │   ├── config.py          # Configuration management
│   │   ├── logger.py          # Logging utility
│   │   ├── chromadb_client.py
│   │   └── ollama_client.py
│   ├── models/                 # ML models
│   ├── rag/                    # RAG pipeline
│   └── web_ui/                 # Streamlit interface
├── data/
│   ├── raw/                    # Downloaded datasets
│   └── processed/              # Processed data
├── docs/                       # Sphinx documentation
├── requirements.txt            # Dependencies
└── CHANGELOG.md               # Version history
```

## 🔧 Configuration

The system uses centralized configuration with Pydantic:

```python
from src.utils.config import get_config, get_raw_path

# Get configuration
config = get_config()
print(config.OLLAMA_DEFAULT_MODEL)  # llama3.1:8b

# Get data paths
raw_path = get_raw_path()  # data/raw
```

### Default Settings
- **ChromaDB**: localhost:8000
- **Ollama**: localhost:11434 (llama3.1:8b model)
- **Streamlit**: localhost:8501
- **Data Paths**: data/, data/raw/, data/processed/

## 📚 Documentation

Complete documentation is available in the `docs/` directory:

- **Installation Guide**: Setup and configuration
- **Quickstart Guide**: Get up and running quickly
- **Dataset Documentation**: Detailed dataset information
- **API Reference**: Complete function documentation
- **Configuration Guide**: All configuration options

Build and view documentation:
```bash
cd docs
make html
# Open _build/html/index.html in browser
```

## 🛠️ Development

### Code Quality
- **Type Hints**: Full type annotation for better IDE support
- **Error Handling**: Comprehensive try-catch blocks with logging
- **Logging**: Professional syslog-style logging with timestamps
- **Documentation**: Google-style docstrings for all functions

### Adding New Datasets
```python
from src.data.get_datasets import download_dataset

download_dataset(
    name='new_dataset',
    dataset_id='username/dataset-name',
    folder_name='new_dataset'
)
```

### Configuration Management
```python
from src.utils.config import get_config

# Add new configuration options in src/utils/config.py
# They will be automatically available via environment variables
```

## 🤝 Team

- **Marc Haenle** - Project Lead
- **Krzysztof Buzar** - Technical Mentor
- **DSR Portfolio Project B42-MHa**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📈 Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history and changes.

---

*Advanced RAG + LLM + Streamlit for Cybersecurity Classification with Professional Documentation*
