.. DSR Cybersecurity RAG System documentation master file, created by
   sphinx-quickstart on Wed Jun 25 05:21:48 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

DSR Cybersecurity RAG System
============================

A comprehensive RAG (Retrieval-Augmented Generation) system for cybersecurity classification using MITRE ATT&CK framework.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   user_guide/installation
   user_guide/quickstart
   user_guide/datasets
   api/modules
   api/config
   api/datasets

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Features
--------

* **Dataset Management**: Automated download and processing of cybersecurity datasets
* **RAG Pipeline**: ChromaDB vector database with LLM LLM integration
* **MITRE ATT&CK**: Specialized for cybersecurity threat classification
* **Web Interface**: Streamlit-based user interface
* **Modular Architecture**: Clean, maintainable codebase

Quick Start
-----------

1. Install dependencies: ``pip install -r requirements.txt``
2. Download datasets: ``python src/01_get_datasets.py``
3. Preview data: ``python src/02_preview_datasets.py``
4. Start web interface: ``streamlit run src/web_ui/app.py``

Project Structure
-----------------

.. code-block:: text

   DSR-PortfolioProject-B42-MHa/
   ├── src/
   │   ├── data/           # Dataset management
   │   ├── models/         # ML models
   │   ├── rag/           # RAG pipeline
   │   ├── utils/         # Utilities and config
   │   └── web_ui/        # Streamlit interface
   ├── data/
   │   ├── raw/           # Downloaded datasets
   │   └── processed/     # Processed data
   ├── docs/              # This documentation
   └── requirements.txt   # Dependencies
