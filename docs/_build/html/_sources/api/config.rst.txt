Configuration
=============

The configuration system provides centralized settings management for the DSR RAG System.

Configuration Class
-------------------

.. automodule:: src.utils.config
   :members:
   :undoc-members:
   :show-inheritance:

Environment Variables
--------------------

The system can be configured using environment variables or a `.env` file:

.. code-block:: bash

   # ChromaDB Configuration
   CHROMADB_HOST=localhost
   CHROMADB_PORT=8000
   CHROMADB_URL=http://localhost:8000

   # Ollama Configuration
   OLLAMA_HOST=localhost
   OLLAMA_PORT=11434
   OLLAMA_DEFAULT_MODEL=llama3.1:8b
   OLLAMA_FALLBACK_MODEL=llama3.1:70b
   OLLAMA_TIMEOUT=30
   OLLAMA_MAX_TOKENS=2048
   OLLAMA_TEMPERATURE=0.1

   # Streamlit Configuration
   STREAMLIT_HOST=0.0.0.0
   STREAMLIT_PORT=8501

   # Data Paths
   DATA_DIR=data
   RAW_DIR=data/raw
   PROCESSED_DIR=data/processed

   # Application Settings
   LOG_LEVEL=INFO
   DEBUG_MODE=false
   ENVIRONMENT=development

Default Values
--------------

The system provides sensible defaults for all settings:

* **ChromaDB**: localhost:8000
* **Ollama**: localhost:11434 with llama3.1:8b model
* **Streamlit**: 0.0.0.0:8501
* **Data Paths**: data/, data/raw/, data/processed/
* **Logging**: INFO level, development environment

Configuration Methods
---------------------

.. code-block:: python

   from src.utils.config import get_config, get_raw_path, get_ollama_url

   # Get full configuration
   config = get_config()
   print(config.OLLAMA_DEFAULT_MODEL)

   # Get specific paths
   raw_path = get_raw_path()
   print(raw_path)

   # Get service URLs
   ollama_url = get_ollama_url()
   print(ollama_url)

Configuration Validation
-----------------------

The configuration uses Pydantic for automatic validation:

* **Type Checking**: All values are validated against expected types
* **Default Values**: Sensible defaults for all settings
* **Environment Loading**: Automatic loading from `.env` files
* **Error Handling**: Clear error messages for invalid configurations

Example Configuration File
--------------------------

Create a `.env` file in the project root:

.. code-block:: text

   # Development Configuration
   ENVIRONMENT=development
   DEBUG_MODE=true
   LOG_LEVEL=DEBUG

   # Custom Ollama Model
   OLLAMA_DEFAULT_MODEL=llama3.1:70b
   OLLAMA_TEMPERATURE=0.2

   # Custom Data Paths
   DATA_DIR=/custom/data/path
   RAW_DIR=/custom/data/raw

Troubleshooting
--------------

**Common Configuration Issues**:

1. **Invalid Port Numbers**: Ensure ports are integers between 1-65535
2. **Invalid URLs**: Check URL format and accessibility
3. **Missing Environment Variables**: Use `.env` file or set variables directly
4. **Permission Issues**: Ensure write access to data directories

**Configuration Validation**:

.. code-block:: python

   from src.utils.config import get_config

   try:
       config = get_config()
       print("Configuration valid!")
   except Exception as e:
       print(f"Configuration error: {e}")
