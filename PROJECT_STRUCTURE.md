# Project Structure Overview

This document provides a detailed explanation of the RAG-Enhanced Cybersecurity Classification System project structure.

## 📁 Root Directory

```
DSR-PortfolioProject-B42-MHa/
├── .venv/                  # Python virtual environment (not in git)
├── data/                   # All data storage and processing directories
├── deployment/             # Deployment configurations and scripts
├── docs/                   # Project documentation
├── env.example             # Environment variables template
├── LICENSE                 # Project license
├── logs/                   # Application and service logs
├── notebooks/              # Jupyter notebooks for development and analysis
├── outputs/                # Generated outputs, reports, and results
├── PROJECT_STRUCTURE.md    # This file - detailed structure explanation
├── README.md               # Main project documentation
├── requirements-minimal.txt # Minimal Python dependencies
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
├── processed/              # Cleaned and processed log data
└── raw/                    # Original firewall and Apache log files
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
Project documentation and technical specifications.
```
docs/
├── api/                    # API documentation
├── architecture/           # System architecture diagrams
├── user-guide/             # User documentation
└── technical/              # Technical specifications
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
├── data/                   # Data processing and ingestion modules
├── models/                 # Machine learning models and utilities
├── rag/                    # RAG (Retrieval-Augmented Generation) engine
├── utils/                  # Utility functions and helpers
└── web_ui/                 # Streamlit web interface
```

#### `src/data/`
Data processing, ingestion, and transformation modules.
```
src/data/
├── ingestion/              # Log ingestion from various sources
├── preprocessing/          # Data cleaning and preprocessing
├── validation/             # Data validation and quality checks
└── storage/                # Data storage and retrieval utilities
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
├── config.py               # Configuration management (loads from .env)
├── ollama_client.py        # Ollama LLM client
└── logging.py              # Logging configuration
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
- `env.example`: Template for environment variables (ChromaDB, Ollama, etc.)
- `requirements-minimal.txt`: Minimal Python dependencies for RAG demo
- `.env`: Environment variables with real settings (not in git)

### Main Application Files
- `src/rag/engine.py`: Core RAG engine
- `src/web_ui/app.py`: Streamlit web interface
- `src/utils/config.py`: Configuration management (loads from .env)
- `src/utils/ollama_client.py`: Ollama LLM client
- `src/utils/chromadb_client.py`: ChromaDB client

### Documentation
- `README.md`: Main project overview and quick start
- `PROJECT_STRUCTURE.md`: This file - detailed structure explanation
- `docs/`: Additional documentation

## 🚀 Development Workflow

1. **Setup**: `env.example` → `.env` → `source .venv/bin/activate`
2. **Data Processing**: Raw logs → `data/raw/` → `src/data/` → `data/processed/`
3. **Model Development**: `notebooks/` → `src/models/` → `tests/`
4. **RAG Engine**: `src/rag/` → `src/utils/` → `outputs/`
5. **Web Interface**: `src/web_ui/` → Streamlit application
6. **Deployment**: `deployment/` → Production environment

## 📝 Notes

- **Virtual Environment**: `.venv/` contains the Python virtual environment and should not be committed
- **Configuration**: All settings are managed via `.env` file (copy from `env.example`)
- **Dependencies**: Only minimal requirements in `requirements-minimal.txt` (no PyTorch/CUDA)
- **Logs**: Application logs are stored in `logs/` directory by component (not committed to git)
- **Outputs**: All generated outputs go to the `outputs/` directory
- **Testing**: Test data and fixtures are stored in `tests/data/`
- **Documentation**: Organized in the `docs/` directory with subdirectories for different types
- **Security**: No real IPs or model names in committed files - only placeholders in examples
