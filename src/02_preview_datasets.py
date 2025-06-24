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
        print(f"📁 {file}")
        print(f"📊 Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"📋 Columns: {list(df.columns)}")
        print(f"🔍 Sample Data:")
        print(df.head(3).to_string(index=False, max_colwidth=50))
        print(f"{'='*50}")
