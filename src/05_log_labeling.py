# \!/usr/bin/env python3
"""
05_log_labeling.py - Clean Log Classification Implementation

Unified, refactored implementation using modular utilities.
No defensive error handling - ChromaDB is always available locally.

Author: DSR Portfolio Project
Version: 2.0.0 (Refactored)
"""

import sys
import os
from pathlib import Path

# Add project paths
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / "src"))

from utils.chromadb_client import ChromaDBClient
from utils.loki_client import get_logs_with_fallback
from utils.log_classifier import classify_log_batch, print_classification_results


def main():
    """Main execution function - clean and simple."""
    print("DSR Log Classification - Refactored Implementation")
    print("=" * 60)

    # Initialize ChromaDB (no try/catch - it should work)
    print("Initializing local ChromaDB...")
    chromadb_client = ChromaDBClient()
    chromadb_client.connect()
    print("ChromaDB initialized successfully")

    # Fetch logs (with fallback to mock if Loki unavailable)
    print("\nFetching logs from cluster Loki service...")
    logs = get_logs_with_fallback(limit=5)

    if not logs:
        print("No logs available, exiting")
        return

    # Classify logs using ChromaDB + pattern matching
    print("\nClassifying logs with ChromaDB similarity search...")
    results = classify_log_batch(logs, chromadb_client)

    # Display results
    print_classification_results(results)

    print("\nLog classification completed successfully\!")


if __name__ == "__main__":
    main()
