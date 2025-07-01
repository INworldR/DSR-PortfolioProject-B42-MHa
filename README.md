# DSR Cybersecurity RAG System

Advanced context-aware threat detection using RAG (Retrieval-Augmented Generation) + LLM for MITRE ATT&CK classification with ATP log generation and portfolio demonstration capabilities.

## 🎯 Project Goals

- **ATP Log Generation**: Simulate APT group activities with realistic MITRE ATT&CK techniques
- **RAG Pipeline**: Context-aware threat analysis using local ChromaDB and LLM
- **Portfolio Demonstration**: Complete web interface for cybersecurity portfolio presentation
- **MITRE ATT&CK Integration**: Precise technique classification and attack simulation
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
```

### ATP Demo Interface

The project includes a Streamlit web interface for demonstrating ATP log generation capabilities:

```bash
# Start Streamlit demo
streamlit run src/streamlit_atp_demo.py --server.port 8501 --server.address 0.0.0.0

# Access demo interface
# Local: http://localhost:8501
# Cluster: http://10.5.3.10:8501 (via LoadBalancer)
```

## 🏗️ Project Structure

```
DSR-PortfolioProject-B42-MHa/
├── src/
│   ├── atp_log_generator.py      # ATP log generation with APT groups
│   ├── streamlit_atp_demo.py     # Web interface for demonstrations
│   ├── 01_get_datasets.py        # Dataset management
│   ├── 04_build_chromadb.py      # Vector database setup
│   └── utils/                    # Utility modules
├── data/
│   ├── chromadb/                 # Vector database (884MB)
│   ├── generated_logs/           # ATP log outputs
│   └── raw/                      # Source datasets
├── docs/                         # Sphinx documentation
├── deployment/                   # Kubernetes configurations
└── tests/                        # Test suites
```

## 💡 Features

### ATP Log Generation
- **APT Groups**: APT29 (Cozy Bear), APT1 (Comment Crew), Lazarus Group
- **MITRE Techniques**: 16 implemented ATT&CK techniques
- **Realistic IOCs**: IP addresses, domains, file hashes, processes
- **Confidence Scoring**: 0.0-1.0 threat indicator confidence levels

### ChromaDB Integration
- **Vector Database**: 884MB with 25,000+ documents
- **Semantic Search**: Cosine similarity with configurable thresholds
- **RAG Queries**: Context-aware threat analysis
- **Performance**: <100ms average query response time

### Web Interface
- **Streamlit Demo**: Interactive ATP log generation
- **Real-time Queries**: Live ChromaDB search capabilities
- **IOC Visualization**: Threat indicator display and analysis
- **Portfolio Mode**: Professional demonstration interface

## 🔧 Usage Examples

### Command Line Interface
```bash
# Generate logs for specific APT group
python src/atp_log_generator.py --apt-group APT29 --count 10 --output logs/apt29.json

# Mixed APT activity simulation
python src/atp_log_generator.py --mixed --count 50 --format json

# Query existing logs
python src/atp_log_generator.py --query PowerShell execution suspicious activity
```

### Python API
```python
from src.atp_log_generator import ATPLogGenerator

# Initialize generator
generator = ATPLogGenerator()

# Generate ATP logs
logs = generator.generate_logs(apt_group=APT29, count=10)

# Query ChromaDB
results = generator.query_logs(lateral movement techniques)

# Extract IOCs
iocs = generator.extract_iocs(logs)
```

## 📊 Technical Specifications

### Performance Metrics
- **Log Generation**: <1s per log entry
- **ChromaDB Queries**: <100ms average response
- **Vector Dimensions**: 384 (sentence-transformers/all-MiniLM-L6-v2)
- **Scalability**: Handles 1000+ log entries efficiently

### MITRE ATT&CK Coverage
- **16 Techniques**: T1566.001, T1055.001, T1059.001, T1003.001, and more
- **3 APT Groups**: Comprehensive nation-state actor simulation
- **IOC Generation**: Realistic threat intelligence artifacts
- **Attack Chains**: Multi-stage APT campaign simulation

## 🚀 Deployment

### Kubernetes Deployment
The project includes Kubernetes configurations for container deployment:

```bash
# Deploy to development environment
kubectl apply -f deployment/

# Access via LoadBalancer
curl http://10.5.3.10:8501
```

### Service Configuration
- **Streamlit Service**: LoadBalancer on port 8501
- **Namespace**: dev-environment
- **Node Selector**: cn5 (x86_64 Alpine VM)

## 📚 Documentation

Complete documentation is available in the `docs/` directory:

```bash
# Build documentation
cd docs/
make html

# View documentation
open _build/html/index.html
```

## 🧪 Testing

```bash
# Run test suite
python -m pytest tests/

# Test ChromaDB integration
python src/test_chromadb_injection.py

# Validate ATP log generation
python src/atp_log_generator.py --test
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 🎓 Portfolio Highlights

This project demonstrates:

- **Advanced Threat Simulation**: Nation-state actor behavior modeling
- **Vector Database Implementation**: ChromaDB with semantic search
- **Full-stack Development**: CLI, API, and web interface components
- **Cybersecurity Expertise**: MITRE ATT&CK framework implementation
- **Software Engineering**: Clean architecture and comprehensive testing
- **Container Orchestration**: Kubernetes deployment and service configuration

---

**Version**: 2.0.0
**Status**: Portfolio Ready
**Demo**: http://10.5.3.10:8501
