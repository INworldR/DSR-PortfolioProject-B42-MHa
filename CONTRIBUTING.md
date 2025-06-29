# Contributing to DSR Cybersecurity RAG System

We welcome contributions to the DSR Cybersecurity RAG System\! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

### Our Pledge

We are committed to making participation in this project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes:**
- Use of sexualized language or imagery and unwelcome sexual attention
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate in a professional setting

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git for version control
- Virtual environment management (venv or conda)
- Basic understanding of machine learning and cybersecurity concepts

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/DSR-PortfolioProject-B42-MHa.git
   cd DSR-PortfolioProject-B42-MHa
   ```

2. **Environment Setup**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configuration**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Verify Installation**
   ```bash
   python src/01_get_datasets.py
   python src/02_preview_datasets.py
   ```

## Development Process

### Branching Strategy

- **main**: Production-ready code
- **develop**: Integration branch for features
- **feature/**: New features (`feature/log-classification`)
- **bugfix/**: Bug fixes (`bugfix/chromadb-connection`)
- **hotfix/**: Critical production fixes

### Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Follow coding standards
   - Add tests for new functionality
   - Update documentation

3. **Commit Changes**
   ```bash
   git add .
   git commit -m feat: add MITRE technique mapping enhancement
   ```

4. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   # Create PR through GitHub interface
   ```

### Commit Message Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

**Examples:**
```
feat: add ChromaDB vector similarity search
fix: resolve Loki API connection timeout
docs: update installation guide for new dependencies
refactor: extract MITRE mapping logic to separate module
```

## Coding Standards

### Python Style Guide

- **PEP 8**: Follow Python Enhancement Proposal 8
- **Type Hints**: Use type hints for all function parameters and return values
- **Docstrings**: Google-style docstrings for all functions and classes
- **Line Length**: Maximum 88 characters (Black formatter default)

### Code Quality Tools

```bash
# Install development dependencies
pip install black isort flake8 mypy pytest

# Format code
black src/
isort src/

# Lint code
flake8 src/
mypy src/

# Run tests
pytest tests/
```

### Function Documentation

```python
def classify_log_batch(logs: List[Dict], chromadb_client: ChromaDBClient) -> List[Dict]:
    """
    Classify a batch of security logs using ChromaDB similarity search.

    Args:
        logs: List of log entries with content, timestamp, and labels
        chromadb_client: Configured ChromaDB client instance

    Returns:
        List of classification results with MITRE techniques and confidence scores

    Raises:
        ValueError: If logs list is empty or malformed
        ConnectionError: If ChromaDB client is not connected

    Example:
        >>> client = ChromaDBClient()
        >>> client.connect()
        >>> logs = [{'content': 'Failed login attempt', 'timestamp': '...'}]
        >>> results = classify_log_batch(logs, client)
        >>> print(results[0]['suggested_techniques'])
        ['T1078 - Valid Accounts', 'T1110 - Brute Force']
    """
```

### Error Handling

- **Strategic Error Handling**: Only catch exceptions you can meaningfully handle
- **Logging**: Use structured logging instead of print statements
- **User-Friendly Messages**: Provide clear, actionable error messages

```python
import logging
from utils.logger import get_logger

logger = get_logger(__name__)

def process_logs(logs: List[Dict]) -> List[Dict]:
    """Process security logs with proper error handling."""
    if not logs:
        raise ValueError("Logs list cannot be empty")

    try:
        results = []
        for log in logs:
            result = classify_single_log(log)
            results.append(result)

        logger.info(f"Successfully processed {len(results)} logs")
        return results

    except Exception as e:
        logger.error(f"Failed to process logs: {e}")
        raise
```

## Testing Guidelines

### Test Structure

```
tests/
├── unit/                   # Unit tests for individual functions
│   ├── test_loki_client.py
│   ├── test_mitre_mapper.py
│   └── test_log_classifier.py
├── integration/            # Integration tests for module interactions
│   ├── test_chromadb_integration.py
│   └── test_log_classification_pipeline.py
├── fixtures/               # Test data and fixtures
│   ├── sample_logs.json
│   └── mock_chromadb_data.json
└── conftest.py            # Pytest configuration
```

### Writing Tests

```python
import pytest
from unittest.mock import Mock, patch
from src.utils.log_classifier import classify_single_log

def test_classify_single_log_success():
    """Test successful log classification."""
    # Arrange
    mock_log = {
        'content': 'Failed login attempt from 192.168.1.100',
        'timestamp': '2025-06-29T10:00:00Z',
        'labels': {'job': 'security', 'host': 'server1'}
    }
    mock_chromadb_client = Mock()

    # Act
    result = classify_single_log(mock_log, mock_chromadb_client)

    # Assert
    assert 'suggested_techniques' in result
    assert 'confidence' in result
    assert result['confidence'] > 0.0
    assert 'T1078' in str(result['suggested_techniques'])

def test_classify_single_log_empty_content():
    """Test log classification with empty content."""
    mock_log = {'content': '', 'timestamp': '...', 'labels': {}}
    mock_chromadb_client = Mock()

    result = classify_single_log(mock_log, mock_chromadb_client)

    assert result['confidence'] == 0.5  # Default confidence
```

### Test Coverage

- **Minimum Coverage**: 80% code coverage for new modules
- **Critical Paths**: 100% coverage for security-related functions
- **Edge Cases**: Test empty inputs, malformed data, network failures

```bash
# Run tests with coverage
pytest --cov=src tests/
pytest --cov=src --cov-report=html tests/
```

## Documentation

### Documentation Types

1. **Code Documentation**: Docstrings and inline comments
2. **API Documentation**: Sphinx-generated API reference
3. **User Documentation**: Installation, quickstart, and user guides
4. **Developer Documentation**: Architecture, contributing guidelines

### Updating Documentation

```bash
# Update API documentation after code changes
cd docs
sphinx-apidoc -f -o api ../src
make clean
make html

# View documentation
open _build/html/index.html
```

### Documentation Standards

- **Clear Examples**: Provide working code examples
- **Up-to-Date**: Keep documentation synchronized with code changes
- **User-Focused**: Write for the intended audience (users vs. developers)
- **Visual Aids**: Use diagrams and flowcharts where helpful

## Submitting Changes

### Pull Request Process

1. **Pre-submission Checklist**
   - [ ] Code follows style guidelines
   - [ ] Tests pass locally
   - [ ] Documentation updated
   - [ ] CHANGELOG.md updated
   - [ ] No sensitive data in commits

2. **Pull Request Template**
   ```markdown
   ## Description
   Brief description of changes and motivation.

   ## Type of Change
   - [ ] Bug fix (non-breaking change that fixes an issue)
   - [ ] New feature (non-breaking change that adds functionality)
   - [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
   - [ ] Documentation update

   ## Testing
   - [ ] Unit tests added/updated
   - [ ] Integration tests added/updated
   - [ ] Manual testing completed

   ## Checklist
   - [ ] Code follows project style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] CHANGELOG.md updated
   ```

3. **Review Process**
   - Automated checks must pass
   - At least one code review required
   - Documentation review for significant changes
   - Testing verification

### Code Review Guidelines

**For Authors:**
- Keep PRs focused and reasonably sized
- Provide clear description and context
- Respond promptly to feedback
- Test changes thoroughly

**For Reviewers:**
- Focus on code quality, security, and maintainability
- Provide constructive feedback
- Ask questions for clarification
- Approve when ready, request changes if needed

## Development Environment

### Recommended Tools

- **IDE**: VS Code, PyCharm, or similar with Python support
- **Extensions**: Python, Black Formatter, GitLens
- **Database Browser**: DB Browser for SQLite (for ChromaDB inspection)
- **API Testing**: Postman or curl for API endpoint testing

### Environment Variables

```bash
# .env file template
DATA_DIR=data
CHROMADB_HOST=localhost
CHROMADB_PORT=8000
LLM_HOST=localhost
LLM_PORT=11434
LOG_LEVEL=INFO
DEBUG_MODE=false
```

## Getting Help

### Communication Channels

- **Issues**: GitHub Issues for bug reports and feature requests
- **Discussions**: GitHub Discussions for questions and ideas
- **Documentation**: Check existing documentation first
- **Code Review**: Use PR comments for code-specific questions

### Issue Templates

**Bug Report:**
```markdown
**Describe the Bug**
Clear description of the issue.

**To Reproduce**
Steps to reproduce the behavior.

**Expected Behavior**
What you expected to happen.

**Environment**
- OS: [e.g., macOS, Ubuntu]
- Python version: [e.g., 3.9.7]
- Project version: [e.g., 2.0.0]

**Additional Context**
Any other context about the problem.
```

**Feature Request:**
```markdown
**Feature Description**
Clear description of the proposed feature.

**Use Case**
Why is this feature needed?

**Proposed Solution**
How should this feature work?

**Alternatives Considered**
Other approaches you've considered.
```

## Security Considerations

### Reporting Security Issues

- **Do NOT** open public issues for security vulnerabilities
- Email security concerns directly to project maintainers
- Provide detailed information about the vulnerability
- Allow reasonable time for fix before disclosure

### Security Guidelines

- Never commit sensitive data (API keys, passwords, personal information)
- Validate all user inputs
- Use secure dependencies and keep them updated
- Follow principle of least privilege
- Encrypt sensitive data in transit and at rest

---

## Recognition

Contributors are recognized in:
- CHANGELOG.md for significant contributions
- README.md contributors section
- Project documentation acknowledgments

Thank you for contributing to the DSR Cybersecurity RAG System\!
