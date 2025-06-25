"""
Dataset Preview Module for Cybersecurity RAG System.

This module provides functionality to preview and inspect downloaded cybersecurity
datasets. It displays key information including dataset shape, column names,
and sample data in a formatted table view.

The module automatically discovers all Parquet files in the raw data directory
and provides a comprehensive overview of each dataset's structure and content.

Features:
- Automatic dataset discovery
- Tabular data preview with pandas formatting
- Shape and column information
- Sample data display (first 3 rows)

Author: DSR Portfolio Project Team
"""

import pandas as pd
from pathlib import Path
from utils.config import get_raw_path

# Configure pandas for better display
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", 50)

raw_dir = get_raw_path()
for folder in raw_dir.iterdir():
    for file in folder.glob("*.parquet"):
        df = pd.read_parquet(file)
        print(f"\n{'='*50}")
        print(f"FILE: {file}")
        print(f"SHAPE: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"COLUMNS: {list(df.columns)}")
        print(f"SAMPLE DATA:")
        print(df.head(3).to_string(index=False, max_colwidth=50))
        print(f"{'='*50}")
