Quick Start Guide
=================

Get up and running with the DSR Cybersecurity RAG System in minutes.

Prerequisites
-------------

Ensure you have completed the :doc:`installation` guide and have:

* Python environment activated
* Dependencies installed
* Basic understanding of cybersecurity concepts

Step 1: Download Datasets
-------------------------

Download the required cybersecurity datasets:

.. code-block:: bash

   python src/01_get_datasets.py

This will download:

* **Heimdall**: Cybersecurity conversation dataset
* **TTP Mapping**: MITRE ATT&CK technique mapping
* **Security Attacks**: MITRE attack patterns
* **Cyber Rules**: Detection rules and signatures

Step 2: Preview Data
--------------------

Inspect the downloaded datasets:

.. code-block:: bash

   python src/02_preview_datasets.py

This shows:
* Dataset shapes and column information
* Sample data for each dataset
* File locations and sizes

Step 3: Start Services
---------------------

1. **Start ChromaDB** (if not running):

   .. code-block:: bash

      chroma run --host localhost --port 8000

2. **Start Ollama** (if not running):

   .. code-block:: bash

      ollama serve

3. **Pull LLM Model**:

   .. code-block:: bash

      ollama pull llama3.1:8b

Step 4: Launch Web Interface
---------------------------

Start the Streamlit web interface:

.. code-block:: bash

   streamlit run src/web_ui/app.py

Navigate to `http://localhost:8501` in your browser.

Using the System
----------------

1. **Upload Documents**: Add cybersecurity reports or logs
2. **Ask Questions**: Query the system about threats, techniques, or incidents
3. **Get Insights**: Receive AI-powered analysis with MITRE ATT&CK context

Example Queries
--------------

* "What are the common TTPs used in ransomware attacks?"
* "How do I detect lateral movement in my network?"
* "What indicators should I look for in a phishing campaign?"

Next Steps
----------

* Read the :doc:`datasets` guide for detailed dataset information
* Explore the :doc:`../api/modules` for API documentation
* Check the configuration options in :doc:`../api/config`

Troubleshooting
--------------

**Common Issues:**

* **Dataset Download Fails**: Check internet connection and Hugging Face access
* **ChromaDB Connection Error**: Ensure ChromaDB is running on port 8000
* **Ollama Model Not Found**: Run `ollama pull llama3.1:8b`
* **Streamlit Port Conflict**: Change port in configuration or kill existing process
