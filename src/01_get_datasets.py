"""
Dataset Download Module for Cybersecurity RAG System.

This module provides functionality to download and manage cybersecurity datasets
from Hugging Face Hub. It automatically handles dataset caching, directory creation,
and supports both single-split and multi-split datasets.

Supported datasets:
- Heimdall: Cybersecurity conversation dataset
- TTP Mapping: MITRE ATT&CK technique mapping
- Security Attacks: MITRE attack patterns
- Cyber Rules: Detection rules and signatures

Author: DSR Portfolio Project Team
"""

import os
import pandas as pd

from pathlib import Path
from datasets import load_dataset
from utils.logger import setup_logger
from utils.config import get_data_path, get_raw_path

logger = setup_logger()


def download_dataset(name: str, dataset_id: str, folder_name: str) -> None:
    """
    Download and save a single dataset from Hugging Face Hub.

    This function downloads a dataset, checks for existing files to avoid re-downloading,
    and saves it in Parquet format. It automatically handles both single-split datasets
    (with 'train' attribute) and multi-split datasets (dictionary format).

    Args:
        name (str): Short name identifier for the dataset (e.g., 'heimdall')
        dataset_id (str): Hugging Face Hub dataset identifier (e.g., 'AlicanKiraz0/Cybersecurity-Dataset-Heimdall-v1.1')
        folder_name (str): Local folder name where the dataset will be stored

    Returns:
        None

    Raises:
        Exception: If dataset download or processing fails

    Example:
        >>> download_dataset('heimdall', 'AlicanKiraz0/Cybersecurity-Dataset-Heimdall-v1.1', 'heimdall')
        [2025-06-24 20:40:15] INFO: Downloading dataset 'heimdall'...
        [2025-06-24 20:40:18] INFO: Dataset 'heimdall' saved to data/raw/heimdall
    """
    try:
        logger.info(f"Downloading dataset '{name}'...")

        # Create specific subfolder if not exists (recursive)
        dataset_dir = get_raw_path() / folder_name
        dataset_dir.mkdir(parents=True, exist_ok=True)

        # Check if dataset already exists
        if (dataset_dir / f"{name}.parquet").exists():
            logger.info(f"Dataset '{name}' already exists, skipping download")
            return

        # Load dataset if not exists
        dataset = load_dataset(dataset_id)

        # Auto-save based on format
        if hasattr(dataset, "train"):
            df = dataset["train"].to_pandas()
            df.to_parquet(dataset_dir / f"{name}.parquet", index=False)
        else:
            # Handle dict format
            for split, data in dataset.items():
                df = data.to_pandas()
                df.to_parquet(dataset_dir / f"{name}_{split}.parquet", index=False)

        logger.info(f"Dataset '{name}' saved to {dataset_dir}")

    except Exception as e:
        logger.error(f"Failed to download dataset '{name}': {str(e)}")


if __name__ == "__main__":
    # Check if data directory exists
    data_dir = get_data_path()
    if not data_dir.exists():
        logger.error("'data' directory not found. Please create it first.")
        exit(1)

    # Create raw directory if not exists
    raw_dir = get_raw_path()
    if not raw_dir.exists():
        logger.info("Creating data/raw directory...")
        raw_dir.mkdir(parents=True, exist_ok=True)
        logger.info("data/raw directory created")

    # Dataset configuration with specific folders
    datasets = {
        "heimdall": ("AlicanKiraz0/Cybersecurity-Dataset-Heimdall-v1.1", "heimdall"),
        "ttp_mapping": ("tumeteor/Security-TTP-Mapping", "ttp_mapping"),
        "security_attacks": ("dattaraj/security-attacks-MITRE", "security_attacks"),
        "cyber_rules": ("jcordon5/cybersecurity-rules", "cyber_rules"),
    }

    for name, (dataset_id, folder_name) in datasets.items():
        download_dataset(name, dataset_id, folder_name)
