ATP Log Generator Module
========================

Overview
--------

The ATP (Advanced Threat Persistence) Log Generator is a sophisticated cybersecurity tool designed to simulate realistic attack patterns from nation-state APT groups. It generates MITRE ATT&CK framework-compliant logs for security testing, threat hunting practice, and portfolio demonstrations.

Key Features
------------

* **Three APT Group Profiles**: APT29 (Cozy Bear), APT1 (Comment Crew), Lazarus Group
* **16 MITRE ATT&CK Techniques**: Covering complete attack chains from initial access to exfiltration
* **ChromaDB Integration**: Vector database storage for RAG-powered threat intelligence queries
* **Multiple Interfaces**: Command line, Python API, and Streamlit web interface
* **Realistic IOCs**: Generated indicators of compromise with confidence scoring

APT Group Coverage
------------------

APT29 (Cozy Bear)
~~~~~~~~~~~~~~~~~

Russian state-sponsored group targeting government and private organizations.

**Attack Chain:**
- T1566.001 - Spearphishing Attachment
- T1059.001 - PowerShell
- T1055 - Process Injection
- T1003.001 - LSASS Memory
- T1021.001 - Remote Desktop Protocol
- T1041 - Exfiltration Over C2

APT1 (Comment Crew)
~~~~~~~~~~~~~~~~~~~

Chinese military unit 61398 focusing on intellectual property theft.

**Attack Chain:**
- T1190 - Exploit Public-Facing Application
- T1059.003 - Windows Command Shell
- T1547.001 - Registry Run Keys
- T1083 - File and Directory Discovery
- T1005 - Data from Local System

Lazarus Group
~~~~~~~~~~~~~

North Korean state-sponsored group known for financial and espionage operations.

**Attack Chain:**
- T1566.002 - Spearphishing Link
- T1204.002 - Malicious File
- T1112 - Modify Registry
- T1016 - System Network Configuration Discovery
- T1039 - Data from Network Shared Drive

Usage Examples
--------------

Command Line Interface
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Generate logs for specific APT group
   python src/atp_log_generator.py

   # Test ChromaDB integration
   python src/test_chromadb_injection.py

Python API
~~~~~~~~~~

.. code-block:: python

   from atp_log_generator import ATPLogGenerator

   # Initialize generator
   generator = ATPLogGenerator()

   # Generate attack sequence
   logs = generator.generate_attack_sequence(apt29_cozy_bear, 10)

   # Generate complete demo dataset
   demo_data = generator.generate_demo_logs()

Streamlit Web Interface
~~~~~~~~~~~~~~~~~~~~~~~

Access the interactive demo at http://10.5.3.6:8501

Features:
- APT group selection
- Configurable log quantity
- Real-time log generation
- Copy-paste ready JSON output
- ChromaDB integration testing

Log Format
----------

Generated logs follow a standardized JSON format:

.. code-block:: json

   {
     timestamp: 2025-06-30T14:23:15.123Z,
     event_type: atp_simulation,
     apt_group: apt29_cozy_bear,
     mitre_technique: T1059.001,
     technique_name: PowerShell,
     tactic: Execution,
     severity: high,
     source_ip: 192.168.121.246,
     target_host: victim-19,
     process_name: powershell.exe,
     command_line: powershell.exe -WindowStyle Hidden -EncodedCommand...,
     success: true,
     threat_score: 9,
     indicators: [powershell.exe, base64_payload],
     detection_confidence: 0.85,
     false_positive_probability: 0.15
   }

ChromaDB Integration
--------------------

The ATP Log Generator integrates seamlessly with ChromaDB for advanced threat intelligence capabilities:

Vector Storage
~~~~~~~~~~~~~~

* **Collection**: atp_simulation_logs
* **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2
* **Vector Dimensions**: 384
* **Similarity Metric**: Cosine similarity

RAG Queries
~~~~~~~~~~~

Supports semantic search queries such as:
- PowerShell execution techniques
- Credential dumping attacks
- Lateral movement methods
- Data exfiltration patterns
- Registry persistence techniques

API Reference
-------------

.. automodule:: atp_log_generator
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: ATPLogGenerator
   :members:
   :undoc-members:

.. autoclass:: AttackTechnique
   :members:
   :undoc-members:
