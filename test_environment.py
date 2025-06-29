# \!/usr/bin/env python3
"""
Test script to verify the Python environment and installed packages.
"""

import sys
import os


def main():
    print("=== Python Environment Test ===")
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Virtual environment: {os.environ.get('VIRTUAL_ENV', 'Not activated')}")

    print("\n=== Installed Packages ===")
    try:
        import pkg_resources

        installed_packages = [d.project_name for d in pkg_resources.working_set]
        print(f"Total packages: {len(installed_packages)}")

        # Show key packages
        key_packages = [
            "chromadb",
            "llm",
            "streamlit",
            "fastapi",
            "pydantic",
            "loguru",
        ]
        for package in key_packages:
            try:
                version = pkg_resources.get_distribution(package).version
                print(f"[OK] {package}: {version}")
            except pkg_resources.DistributionNotFound:
                print(f"[MISSING] {package}: Not installed")

    except ImportError:
        print("pkg_resources not available")

    print("\n=== Environment Variables ===")
    env_vars = ["VIRTUAL_ENV", "PYTHONPATH", "PATH"]
    for var in env_vars:
        value = os.environ.get(var, "Not set")
        print(f"{var}: {value}")


if __name__ == "__main__":
    main()
