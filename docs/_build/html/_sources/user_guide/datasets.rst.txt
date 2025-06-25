Datasets Documentation
======================

This document describes the cybersecurity datasets used in the DSR RAG System.

Overview
--------

The system uses four primary datasets from Hugging Face Hub, each providing different aspects of cybersecurity knowledge:

* **Heimdall**: Conversation dataset for training
* **TTP Mapping**: MITRE ATT&CK technique relationships
* **Security Attacks**: Attack pattern examples
* **Cyber Rules**: Detection and response rules

Heimdall Dataset
----------------

**Source**: `AlicanKiraz0/Cybersecurity-Dataset-Heimdall-v1.1`

**Description**: A comprehensive dataset of cybersecurity conversations and Q&A pairs, designed for training AI models on security-related topics.

**Structure**:
* **conversations**: List of conversation turns
* **id**: Unique identifier
* **metadata**: Source and category information

**Use Case**: Training the RAG system to understand security queries and provide contextual responses.

**Size**: ~26MB (21,257 examples)

TTP Mapping Dataset
-------------------

**Source**: `tumeteor/Security-TTP-Mapping`

**Description**: Maps MITRE ATT&CK techniques to their relationships, helping understand technique similarities and associations.

**Structure**:
* **train/validation/test** splits
* Technique identifiers and descriptions
* Similarity scores and relationships

**Use Case**: Understanding technique relationships and improving threat classification accuracy.

**Size**: ~2MB (20,736 examples across splits)

Security Attacks Dataset
------------------------

**Source**: `dattaraj/security-attacks-MITRE`

**Description**: Collection of security attack patterns mapped to MITRE ATT&CK framework, providing real-world attack examples.

**Structure**:
* **train/validation** splits
* Attack descriptions and techniques
* MITRE ATT&CK mappings

**Use Case**: Providing concrete examples of attacks and their associated techniques.

**Size**: ~150KB (271 examples across splits)

Cyber Rules Dataset
-------------------

**Source**: `jcordon5/cybersecurity-rules`

**Description**: Detection rules and signatures for identifying security threats and incidents.

**Structure**:
* **train** split
* Rule definitions and conditions
* Detection logic and thresholds

**Use Case**: Enhancing detection capabilities and providing rule-based insights.

**Size**: ~4MB (949 examples)

Data Processing
---------------

All datasets are automatically:

1. **Downloaded** from Hugging Face Hub
2. **Converted** to Parquet format for efficiency
3. **Organized** in `data/raw/` subdirectories
4. **Cached** to avoid re-downloading

File Structure
--------------

.. code-block:: text

   data/raw/
   ├── heimdall/
   │   └── heimdall_train.parquet
   ├── ttp_mapping/
   │   ├── ttp_mapping_train.parquet
   │   ├── ttp_mapping_validation.parquet
   │   └── ttp_mapping_test.parquet
   ├── security_attacks/
   │   ├── security_attacks_train.parquet
   │   └── security_attacks_validation.parquet
   └── cyber_rules/
       └── cyber_rules_train.parquet

Usage Examples
--------------

**Download Datasets**:
.. code-block:: python

   from src.data.get_datasets import download_dataset

   download_dataset('heimdall', 'AlicanKiraz0/Cybersecurity-Dataset-Heimdall-v1.1', 'heimdall')

**Preview Data**:
.. code-block:: python

   import pandas as pd
   df = pd.read_parquet('data/raw/heimdall/heimdall_train.parquet')
   print(df.head())

**Check Dataset Info**:
.. code-block:: bash

   python src/02_preview_datasets.py

Data Quality
------------

* **Source**: All datasets are from reputable sources on Hugging Face Hub
* **Format**: Standardized Parquet format for fast access
* **Validation**: Automatic format checking and error handling
* **Updates**: Datasets can be re-downloaded to get latest versions

Privacy and Security
--------------------

* **No PII**: Datasets contain no personally identifiable information
* **Public Data**: All data is publicly available on Hugging Face Hub
* **Local Storage**: Data is stored locally in `data/raw/` directory
* **No External Calls**: Once downloaded, no internet connection required

Troubleshooting
---------------

**Common Issues**:

1. **Download Failures**: Check internet connection and Hugging Face access
2. **Disk Space**: Ensure sufficient space for ~35MB total dataset size
3. **Permission Errors**: Check write permissions for `data/` directory
4. **Corrupted Files**: Delete and re-download using `python src/01_get_datasets.py`
