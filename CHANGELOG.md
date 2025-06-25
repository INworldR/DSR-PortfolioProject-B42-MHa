# Changelog

All notable changes to the DSR Cybersecurity RAG System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-06-25

### Added
- **Dataset Management System**
  - Automated download of cybersecurity datasets from Hugging Face Hub
  - Support for 4 key datasets: Heimdall, TTP Mapping, Security Attacks, Cyber Rules
  - Automatic caching and format conversion to Parquet
  - Dataset preview functionality with shape and sample data display

- **Configuration Management**
  - Centralized configuration using Pydantic Settings
  - Environment variable support with `.env` file integration
  - Configurable paths for data directories
  - Service configuration for ChromaDB, Ollama, and Streamlit

- **Logging System**
  - Professional syslog-style logging with timestamps
  - Centralized logger utility with configurable levels
  - Structured error handling and success messages

- **Documentation System**
  - Complete Sphinx documentation with ReadTheDocs theme
  - User guides: Installation, Quickstart, Datasets
  - API documentation with automatic docstring generation
  - Configuration and troubleshooting guides

- **Project Structure**
  - Modular architecture with clear separation of concerns
  - DRY (Don't Repeat Yourself) code principles
  - Type hints for better IDE support and code quality
  - Professional docstrings following Google style

### Technical Features
- **Data Processing**
  - Parquet format for efficient data storage and access
  - Automatic directory creation and path management
  - Dataset validation and error handling
  - Support for both single-split and multi-split datasets

- **Code Quality**
  - Comprehensive error handling with try-catch blocks
  - Input validation and type checking
  - Professional logging with different severity levels
  - Clean code practices with meaningful variable names

- **Dependencies**
  - Core RAG stack: ChromaDB, Streamlit, Requests
  - Data processing: Pandas, NumPy, Datasets, PyArrow
  - ML components: Transformers, Scikit-learn
  - Documentation: Sphinx, ReadTheDocs theme, MyST parser
  - Code quality: Black, Pre-commit, Pydantic

### Files Added
- `src/01_get_datasets.py` - Dataset download functionality
- `src/02_preview_datasets.py` - Dataset preview and inspection
- `src/utils/config.py` - Configuration management
- `src/utils/logger.py` - Logging utility
- `docs/` - Complete documentation structure
- `requirements.txt` - Project dependencies
- `CHANGELOG.md` - This changelog file

### Configuration
- Default ChromaDB: localhost:8000
- Default Ollama: localhost:11434 (llama3.1:8b)
- Default Streamlit: localhost:8501
- Data paths: data/, data/raw/, data/processed/

### Documentation
- Installation guide with prerequisites and troubleshooting
- Quickstart guide with step-by-step instructions
- Comprehensive dataset documentation
- API reference with examples
- Configuration guide with environment variables

### Security & Privacy
- No PII in datasets
- Local data storage only
- Public datasets from Hugging Face Hub
- No external API calls after initial download

---

## [Unreleased]

### Planned
- RAG pipeline implementation
- ChromaDB integration
- Ollama LLM integration
- Streamlit web interface
- MITRE ATT&CK classification
- Vector embedding generation
- Query processing and response generation

### Technical Debt
- Add unit tests for all modules
- Implement CI/CD pipeline
- Add code coverage reporting
- Performance optimization for large datasets
- Add data validation schemas

---

## Version History

- **1.0.0** - Initial release with dataset management and documentation
- **Unreleased** - Future RAG implementation and features

---

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
