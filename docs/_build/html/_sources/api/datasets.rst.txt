Datasets API
============

This section documents the dataset management API for downloading and processing cybersecurity datasets.

Dataset Download Functions
--------------------------

.. automodule:: src.data.get_datasets
   :members:
   :undoc-members:
   :show-inheritance:

Dataset Preview Functions
-------------------------

.. automodule:: src.data.preview_datasets
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
--------------

**Download a Single Dataset**:

.. code-block:: python

   from src.data.get_datasets import download_dataset

   # Download Heimdall dataset
   download_dataset(
       name='heimdall',
       dataset_id='AlicanKiraz0/Cybersecurity-Dataset-Heimdall-v1.1',
       folder_name='heimdall'
   )

**Download All Datasets**:

.. code-block:: python

   # Run the main script
   python src/01_get_datasets.py

**Preview Datasets**:

.. code-block:: python

   # Run the preview script
   python src/02_preview_datasets.py

**Programmatic Preview**:

.. code-block:: python

   import pandas as pd
   from src.utils.config import get_raw_path

   # Load and preview a specific dataset
   raw_path = get_raw_path()
   df = pd.read_parquet(raw_path / 'heimdall' / 'heimdall_train.parquet')
   print(f"Shape: {df.shape}")
   print(df.head())

Dataset Information
-------------------

**Supported Datasets**:

1. **Heimdall** (`heimdall`)
   * Source: `AlicanKiraz0/Cybersecurity-Dataset-Heimdall-v1.1`
   * Type: Conversation dataset
   * Size: ~26MB

2. **TTP Mapping** (`ttp_mapping`)
   * Source: `tumeteor/Security-TTP-Mapping`
   * Type: Technique mapping
   * Size: ~2MB

3. **Security Attacks** (`security_attacks`)
   * Source: `dattaraj/security-attacks-MITRE`
   * Type: Attack patterns
   * Size: ~150KB

4. **Cyber Rules** (`cyber_rules`)
   * Source: `jcordon5/cybersecurity-rules`
   * Type: Detection rules
   * Size: ~4MB

**File Structure**:

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

Error Handling
--------------

The dataset functions include comprehensive error handling:

* **Network Errors**: Automatic retry and clear error messages
* **Disk Space**: Validation before download
* **Corrupted Files**: Detection and re-download capability
* **Permission Issues**: Clear error messages for file system problems

**Example Error Handling**:

.. code-block:: python

   try:
       download_dataset('heimdall', 'invalid/dataset', 'heimdall')
   except Exception as e:
       print(f"Download failed: {e}")
       # Handle error appropriately

Configuration
-------------

Dataset paths are configured through the central configuration system:

.. code-block:: python

   from src.utils.config import get_raw_path, get_data_path

   raw_path = get_raw_path()  # data/raw
   data_path = get_data_path()  # data

Performance Considerations
-------------------------

* **Caching**: Datasets are cached locally after first download
* **Format**: Parquet format for fast reading and writing
* **Compression**: Automatic compression for disk space efficiency
* **Validation**: Automatic format validation on download

**Performance Tips**:

1. **SSD Storage**: Use SSD for faster dataset access
2. **Sufficient RAM**: Ensure enough memory for large datasets
3. **Network**: Stable internet connection for initial downloads
4. **Disk Space**: ~35MB total space required

Troubleshooting
---------------

**Common Issues and Solutions**:

1. **Download Timeout**:
   * Check internet connection
   * Increase timeout in configuration
   * Use VPN if needed

2. **Disk Space Errors**:
   * Free up space in data directory
   * Check available disk space
   * Clean up old datasets

3. **Permission Errors**:
   * Check write permissions for data directory
   * Run with appropriate user privileges
   * Verify directory ownership

4. **Corrupted Downloads**:
   * Delete corrupted files
   * Re-run download script
   * Check file integrity

**Debug Mode**:

Enable debug logging for detailed information:

.. code-block:: python

   import logging
   logging.basicConfig(level=logging.DEBUG)

   # Run download with debug output
   download_dataset('heimdall', '...', 'heimdall')
