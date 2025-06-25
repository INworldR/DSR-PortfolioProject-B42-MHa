Installation Guide
==================

This guide will help you install and set up the DSR Cybersecurity RAG System.

Prerequisites
-------------

* Python 3.8 or higher
* Git
* Virtual environment (recommended)

Installation Steps
------------------

1. **Clone the Repository**

   .. code-block:: bash

      git clone <repository-url>
      cd DSR-PortfolioProject-B42-MHa

2. **Create Virtual Environment**

   .. code-block:: bash

      python -m venv .venv
      source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. **Install Dependencies**

   .. code-block:: bash

      pip install -r requirements.txt

4. **Verify Installation**

   .. code-block:: bash

      python -c "import chromadb, streamlit, datasets; print('Installation successful!')"

Configuration
-------------

The system uses environment variables for configuration. Copy the example file:

.. code-block:: bash

   cp env.example .env

Edit `.env` to configure:

* **ChromaDB**: Database connection settings
* **Ollama**: LLM model and connection settings
* **Streamlit**: Web interface settings

Default Configuration
---------------------

The system works with default settings:

* ChromaDB: localhost:8000
* Ollama: localhost:11434 (llama3.1:8b model)
* Streamlit: localhost:8501

Troubleshooting
--------------

**Common Issues:**

1. **Port Conflicts**: Change ports in `.env` file
2. **Memory Issues**: Use smaller Ollama models
3. **Dataset Download Failures**: Check internet connection and Hugging Face access

**Getting Help:**

* Check the logs in `logs/` directory
* Review the configuration in `src/utils/config.py`
* Ensure all services are running (ChromaDB, Ollama)
