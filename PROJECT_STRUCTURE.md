# Project Structure Overview

This document provides a detailed explanation of the DSR Cybersecurity RAG System project structure.

## 📁 Root Directory

```
DSR-PortfolioProject-B42-MHa/
├── .venv/                  # Python virtual environment (not in git)
├── CHANGELOG.md            # Version history and changes
├── data/                   # All data storage and processing directories
├── deployment/             # Deployment configurations and scripts
├── docs/                   # Sphinx documentation
├── env.example             # Environment variables template
├── LICENSE                 # Project license
├── logs/                   # Application and service logs
├── notebooks/              # Jupyter notebooks for development and analysis
├── outputs/                # Generated outputs, reports, and results
├── PROJECT_STRUCTURE.md    # This file - detailed structure explanation
├── README.md               # Main project documentation
├── requirements.txt        # Python dependencies
├── src/                    # Main source code directory
└── tests/                  # Unit tests and test data
```

## 📁 Detailed Structure

### `data/`
All data-related directories for raw, processed, and vector data.
```
data/
├── chromadb/               # ChromaDB vector database files
├── mitre/                  # MITRE ATT&CK framework data and mappings
├── processed/              # Cleaned and processed data
└── raw/                    # Downloaded cybersecurity datasets
    ├── heimdall/           # Heimdall conversation dataset
    ├── ttp_mapping/        # TTP mapping dataset
    ├── security_attacks/   # Security attacks dataset
    └── cyber_rules/        # Cyber rules dataset
```

### `logs/`
Application and service logs organized by component.
```
logs/
├── app/                    # Main application logs
├── chromadb/               # ChromaDB connection and operation logs
├── ollama/                 # Ollama LLM interaction logs
└── rag/                    # RAG engine processing logs
```

### `deployment/`
Deployment configurations for different environments.
```
deployment/
├── docker/                 # Docker configurations
├── kubernetes/             # Kubernetes manifests
└── scripts/                # Deployment and setup scripts
```

### `docs/`
Sphinx documentation with ReadTheDocs theme.
```
docs/
├── _build/                 # Generated HTML documentation
├── api/                    # API documentation
│   ├── config.rst         # Configuration API
│   ├── datasets.rst       # Dataset management API
│   └── modules.rst        # Module reference
├── user_guide/            # User documentation
│   ├── installation.rst   # Installation guide
│   ├── quickstart.rst     # Quick start guide
│   └── datasets.rst       # Dataset documentation
├── conf.py                # Sphinx configuration
├── index.rst              # Main documentation page
└── Makefile               # Documentation build commands
```

### `notebooks/`
Jupyter notebooks for development, analysis, and experimentation.
```
notebooks/
├── data-exploration/       # Data analysis and exploration
├── model-development/      # ML model development and testing
├── rag-experiments/        # RAG system experiments
└── visualization/          # Data visualization and reporting
```

### `outputs/`
Generated outputs, reports, and results from the system.
```
outputs/
├── demo/                   # Demo outputs and examples
├── figures/                # Generated charts and visualizations
└── reports/                # Analysis reports and results
```

### `src/`
Main source code directory containing all application logic.
```
src/
├── 01_get_datasets.py      # Dataset download functionality
├── 02_preview_datasets.py  # Dataset preview and inspection
├── models/                 # Machine learning models and utilities
├── rag/                    # RAG (Retrieval-Augmented Generation) engine
├── utils/                  # Utility functions and helpers
│   ├── chromadb_client.py  # ChromaDB connection and operations
│   ├── config.py           # Configuration management
│   ├── logger.py           # Logging utility
│   └── ollama_client.py    # Ollama LLM client
└── web_ui/                 # Streamlit web interface
```

#### `src/models/`
Machine learning models and related utilities.
```
src/models/
├── embeddings/             # Embedding generation and management
├── classification/         # Threat classification models
└── evaluation/             # Model evaluation and metrics
```

#### `src/rag/`
RAG (Retrieval-Augmented Generation) engine components.
```
src/rag/
├── engine.py               # Main RAG engine
├── retrieval/              # Document retrieval components
├── generation/             # LLM generation and prompting
└── context/                # Context management and processing
```

#### `src/utils/`
Utility functions and helper modules.
```
src/utils/
├── chromadb_client.py      # ChromaDB connection and operations
├── config.py               # Configuration management with Pydantic
├── logger.py               # Centralized logging utility
└── ollama_client.py        # Ollama LLM client
```

#### `src/web_ui/`
Streamlit web interface components.
```
src/web_ui/
├── app.py                  # Main Streamlit application
├── components/             # Reusable UI components
├── pages/                  # Individual application pages
└── assets/                 # Static assets (CSS, images, etc.)
```

### `tests/`
Unit tests and test data for the application.
```
tests/
├── unit/                   # Unit tests for individual modules
├── integration/            # Integration tests
├── data/                   # Test data and fixtures
└── conftest.py             # Pytest configuration
```

## 🔧 Key Files

### Configuration Files
- `env.example`: Template for environment variables
- `requirements.txt`: Python dependencies including documentation tools
- `.env`: Environment variables with real settings (not in git)
- `CHANGELOG.md`: Version history and changes

### Main Application Files
- `src/01_get_datasets.py`: Dataset download functionality
- `src/02_preview_datasets.py`: Dataset preview functionality
- `src/utils/config.py`: Configuration management with Pydantic
- `src/utils/logger.py`: Centralized logging utility
- `src/utils/ollama_client.py`: Ollama LLM client
- `src/utils/chromadb_client.py`: ChromaDB client

### Documentation
- `README.md`: Main project overview and quick start
- `PROJECT_STRUCTURE.md`: This file - detailed structure explanation
- `docs/`: Sphinx documentation with ReadTheDocs theme
- `CHANGELOG.md`: Version history and changes

## 🚀 Development Workflow

1. **Setup**: `env.example` → `.env` → `source .venv/bin/activate`
2. **Dataset Management**: `src/01_get_datasets.py` → `data/raw/`
3. **Data Inspection**: `src/02_preview_datasets.py` → Dataset analysis
4. **Model Development**: `notebooks/` → `src/models/` → `tests/`
5. **RAG Engine**: `src/rag/` → `src/utils/` → `outputs/`
6. **Web Interface**: `src/web_ui/` → Streamlit application
7. **Documentation**: `docs/` → `make html` → Generated documentation
8. **Deployment**: `deployment/` → Production environment

## 📊 Dataset Management

The system supports 4 key cybersecurity datasets:

1. **Heimdall** (`AlicanKiraz0/Cybersecurity-Dataset-Heimdall-v1.1`)
   - Conversation dataset for training
   - ~26MB, 21,257 examples

2. **TTP Mapping** (`tumeteor/Security-TTP-Mapping`)
   - MITRE ATT&CK technique relationships
   - ~2MB, 20,736 examples

3. **Security Attacks** (`dattaraj/security-attacks-MITRE`)
   - Attack pattern examples
   - ~150KB, 271 examples

4. **Cyber Rules** (`jcordon5/cybersecurity-rules`)
   - Detection rules and signatures
   - ~4MB, 949 examples

## 🔧 Configuration

The system uses centralized configuration with Pydantic:

- **Data Paths**: `data/`, `data/raw/`, `data/processed/`
- **Services**: ChromaDB (localhost:8000), Ollama (localhost:11434)
- **Web Interface**: Streamlit (localhost:8501)
- **Logging**: Configurable levels and formats

## 📝 Notes

- **Virtual Environment**: `.venv/` contains the Python virtual environment
- **Configuration**: All settings managed via `src/utils/config.py` and `.env`
- **Dependencies**: Comprehensive requirements in `requirements.txt`
- **Logs**: Application logs stored in `logs/` directory by component
- **Outputs**: All generated outputs go to the `outputs/` directory
- **Testing**: Test data and fixtures stored in `tests/data/`
- **Documentation**: Sphinx documentation in `docs/` with ReadTheDocs theme
- **Dataset Caching**: Automatic caching in Parquet format for efficiency
- **Type Hints**: Full type annotation for better IDE support
- **Error Handling**: Comprehensive error handling with logging
