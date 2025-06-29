# DSR Cybersecurity RAG System

Advanced context-aware threat detection using RAG (Retrieval-Augmented Generation) + LLM for MITRE ATT&CK classification with log labeling capabilities.

## 🎯 Project Goals

- **Automated Dataset Management**: Download and process cybersecurity datasets from Hugging Face Hub
- **RAG Pipeline**: Context-aware threat analysis using local ChromaDB and LLM
- **Log Classification**: Real-time log analysis with MITRE ATT&CK technique mapping
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

# Load datasets into ChromaDB
python src/03_load_datasets.py

# Build ChromaDB vector database
python src/04_build_chromadb.py
```

### Log Classification (NEW)

```bash
# Run log classification with MITRE ATT&CK mapping
python src/05_log_labeling.py
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

## 💾 ChromaDB Vector Database

**Local ChromaDB Database**:
- **Location**: `./data/chromadb/` (local file-based storage)
- **Size**: 884MB indexed cybersecurity knowledge base
- **Collections**:
  - `system_logs`: System log patterns
  - `security_events`: Security event classifications
  - `mitre_techniques`: MITRE ATT&CK technique mappings
- **Performance**: High-speed local access, no network dependencies
- **Integration**: Direct file-based access via ChromaDB client

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │───▶│   RAG Engine    │───▶│  Local ChromaDB │
│                 │    │                 │    │  (884MB)        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Configuration  │    │  Dataset Mgmt   │    │  Vector Store   │
│  Management     │    │  & Processing   │    │  & Embeddings   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Log Retrieval  │    │  MITRE Mapping  │    │  Classification │
│  (Loki/Mock)    │    │  & Techniques   │    │  & Confidence   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
DSR-PortfolioProject-B42-MHa/
├── src/
│   ├── 01_get_datasets.py      # Dataset download functionality
│   ├── 02_preview_datasets.py  # Dataset preview functionality
│   ├── 03_load_datasets.py     # Dataset loading into ChromaDB
│   ├── 04_build_chromadb.py    # ChromaDB vector database builder
│   ├── 05_log_labeling.py      # Log classification with MITRE mapping (NEW)
│   ├── utils/                  # Modular utilities (REFACTORED)
│   │   ├── config.py          # Configuration management
│   │   ├── logger.py          # Logging utility
│   │   ├── chromadb_client.py # ChromaDB client interface
│   │   ├── llm_client.py   # LLM LLM client
│   │   ├── loki_client.py     # Loki log retrieval (NEW)
│   │   ├── mitre_mapper.py    # MITRE technique mapping (NEW)
│   │   └── log_classifier.py  # Core classification logic (NEW)
│   ├── models/                 # ML models
│   ├── rag/                    # RAG pipeline
│   └── web_ui/                 # Streamlit interface
├── data/
│   ├── raw/                    # Downloaded datasets
│   ├── processed/              # Processed data
│   └── chromadb/              # Local ChromaDB storage (884MB)
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
- **ChromaDB**: Local file-based storage in `./data/chromadb/`
- **LLM**: localhost:11434 (llama3.1:8b model)
- **Streamlit**: localhost:8501
- **Data Paths**: data/, data/raw/, data/processed/
- **Loki**: http://10.43.108.157:3100 (cluster service with mock fallback)

## 🏷️ Log Classification Features

### Capabilities
- **Real-time Log Processing**: Analyze security logs from Loki or mock data
- **MITRE ATT&CK Mapping**: Automatic technique classification
- **ChromaDB Integration**: Vector similarity search with 884MB knowledge base
- **Confidence Scoring**: ML-based confidence assessment (0.0-1.0)
- **Modular Architecture**: Clean separation of concerns

### Supported MITRE Techniques
- **T1078** - Valid Accounts
- **T1110** - Brute Force
- **T1005** - Data from Local System
- **T1083** - File and Directory Discovery
- **T1046** - Network Service Discovery
- **T1595** - Active Scanning
- **T1548** - Abuse Elevation Control Mechanism
- **T1059** - Command and Scripting Interpreter
- **T1095** - Non-Application Layer Protocol
- **T1071** - Application Layer Protocol

### Example Usage
```bash
# Run log classification
python src/05_log_labeling.py

# Output example:
# [1] security@host-1 (loki)
#     Content: Failed login attempt from 192.168.1.100...
#     Method: chromadb_similarity
#     Confidence: 0.8
#     MITRE Techniques:
#       - T1078 - Valid Accounts
#       - T1110 - Brute Force
```

## 📚 Documentation

Complete documentation is available in the `docs/` directory:

- **Installation Guide**: Setup and configuration
- **Quickstart Guide**: Get up and running quickly
- **Dataset Documentation**: Detailed dataset information
- **API Reference**: Complete function documentation
- **Configuration Guide**: All configuration options
- **Log Classification Guide**: MITRE mapping and analysis

Build and view documentation:
```bash
cd docs
make html
# Open _build/html/index.html in browser
```

## 🛠️ Development

### Code Quality
- **Type Hints**: Full type annotation for better IDE support
- **Error Handling**: Strategic error handling without defensive over-engineering
- **Logging**: Professional syslog-style logging with timestamps
- **Documentation**: Google-style docstrings for all functions
- **Modular Design**: DRY-compliant utilities with single responsibility

### Adding New Datasets
```python
from src.data.get_datasets import download_dataset

download_dataset(
    name='new_dataset',
    dataset_id='username/dataset-name',
    folder_name='new_dataset'
)
```

### Extending MITRE Mappings
```python
from src.utils.mitre_mapper import map_content_to_mitre_techniques

# Add new patterns in mitre_mapper.py
techniques, confidence = map_content_to_mitre_techniques(log_content)
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

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

## 📈 Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history and changes.

### Recent Updates (v2.0.0)
- ✅ **Refactored Architecture**: Modular utilities with DRY compliance
- ✅ **Log Classification**: Real-time MITRE ATT&CK technique mapping
- ✅ **Local ChromaDB**: 884MB local vector database integration
- ✅ **Enhanced Error Handling**: Strategic error management without over-engineering
- ✅ **Code Reduction**: 65% reduction in code duplication

---

*Advanced RAG + LLM + Log Classification for Cybersecurity with Local ChromaDB Vector Database*
