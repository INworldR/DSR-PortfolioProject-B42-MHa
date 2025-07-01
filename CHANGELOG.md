# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Streamlit ATP Demo now accessible via LoadBalancer service
- Auto-startup mechanism for development container services
- External access configuration for portfolio demonstrations

### Fixed
- LoadBalancer service configuration for Streamlit port 8501
- Container namespace routing for external service access

## [2.0.0] - 2025-06-30

### Added
- ATP Log Generator implementation with APT group simulation
- Support for APT29, APT1, and Lazarus Group attack patterns
- 16 MITRE ATT&CK techniques implementation
- Streamlit web interface for ATP demo
- ChromaDB integration for RAG queries (884MB vector database)
- JSON log generation with IOC artifacts
- Confidence scoring system for threat indicators

### Changed
- Major refactoring to modular architecture
- Updated project structure with utilities modules
- Enhanced documentation with Sphinx integration

### Fixed
- Live processing log data integration
- Documentation generation and formatting

## [1.0.0] - 2025-06-22

### Added
- Initial project setup with cybersecurity RAG system
- Dataset management and processing
- ChromaDB vector database implementation
- MITRE ATT&CK framework integration
- Professional documentation structure
- Log classification and labeling capabilities

### Infrastructure
- Development environment setup
- Virtual environment configuration
- Dependencies management
