# \!/usr/bin/env python3
"""
Dataset Loading Module for Cybersecurity RAG System.

Simple utility to load previously downloaded datasets into memory for processing.
This module provides a unified interface to access all cybersecurity datasets
and prepare them for RAG pipeline ingestion.

Author: DSR Portfolio Project Team
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Optional
from utils.logger import setup_logger
from utils.config import get_raw_path

logger = setup_logger()


def load_dataset(dataset_name: str) -> Optional[pd.DataFrame]:
    """
    Load a single dataset from the raw data directory.

    Args:
        dataset_name: Name of the dataset folder (heimdall, ttp_mapping, etc.)

    Returns:
        DataFrame containing the dataset or None if not found
    """
    try:
        raw_path = get_raw_path()
        dataset_dir = Path(raw_path) / dataset_name

        if not dataset_dir.exists():
            logger.error(f"Dataset directory not found: {dataset_dir}")
            return None

        # Find parquet files in the dataset directory
        parquet_files = list(dataset_dir.glob("*.parquet"))

        if not parquet_files:
            logger.error(f"No parquet files found in {dataset_dir}")
            return None

        # Load the first parquet file (assuming single file per dataset)
        parquet_file = parquet_files[0]
        logger.info(f"Loading dataset: {dataset_name} from {parquet_file.name}")

        df = pd.read_parquet(parquet_file)
        logger.info(f"Loaded {len(df)} records with {len(df.columns)} columns")

        return df

    except Exception as e:
        logger.error(f"Error loading dataset {dataset_name}: {e}")
        return None


def load_all_datasets() -> Dict[str, pd.DataFrame]:
    """
    Load all available cybersecurity datasets.

    Returns:
        Dictionary mapping dataset names to DataFrames
    """
    datasets = {}
    available_datasets = ["heimdall", "ttp_mapping", "security_attacks", "cyber_rules"]

    logger.info("Loading all cybersecurity datasets...")

    for dataset_name in available_datasets:
        df = load_dataset(dataset_name)
        if df is not None:
            datasets[dataset_name] = df
            memory_mb = df.memory_usage(deep=True).sum() / 1024**2
            logger.info(
                f"Successfully loaded {dataset_name}: {len(df)} records, {memory_mb:.1f} MB"
            )
        else:
            logger.warning(f"Failed to load dataset: {dataset_name}")

    total_records = sum(len(df) for df in datasets.values())
    total_memory = (
        sum(df.memory_usage(deep=True).sum() for df in datasets.values()) / 1024**2
    )

    logger.info(
        f"Dataset loading complete: {len(datasets)}/4 datasets successfully loaded"
    )
    logger.info(
        f"Total records: {total_records:,}, Total memory: {total_memory:.1f} MB"
    )

    return datasets


def get_dataset_summary(datasets: Dict[str, pd.DataFrame]) -> None:
    """
    Log summary information for all loaded datasets.

    Args:
        datasets: Dictionary of dataset name to DataFrame mappings
    """
    if not datasets:
        logger.warning("No datasets available for summary")
        return

    logger.info("Dataset summary report:")

    total_records = 0
    total_memory = 0

    for name, df in datasets.items():
        memory_mb = df.memory_usage(deep=True).sum() / 1024**2
        cols_preview = ", ".join(list(df.columns)[:3])
        if len(df.columns) > 3:
            cols_preview += f" (+{len(df.columns)-3} more)"

        logger.info(
            f"  {name}: {len(df):,} records, {len(df.columns)} columns, {memory_mb:.1f} MB"
        )
        logger.info(f"    Columns: {cols_preview}")

        total_records += len(df)
        total_memory += memory_mb

    logger.info(
        f"Summary totals: {total_records:,} records, {total_memory:.1f} MB across {len(datasets)} datasets"
    )


if __name__ == "__main__":
    # Load all datasets
    datasets = load_all_datasets()

    if datasets:
        # Show detailed summary
        get_dataset_summary(datasets)

        # Example: Show sample from Heimdall if available
        if "heimdall" in datasets:
            heimdall_df = datasets["heimdall"]
            sample_record = heimdall_df.iloc[0].to_dict()
            logger.info(f"Heimdall sample record preview: {len(sample_record)} fields")

            # Log first few characters of each field for preview
            for key, value in list(sample_record.items())[:3]:
                preview = (
                    str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                )
                logger.info(f"  {key}: {preview}")

    else:
        logger.error("No datasets could be loaded. Run 01_get_datasets.py first.")
