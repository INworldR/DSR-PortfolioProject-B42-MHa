# \!/usr/bin/env python3
"""
ChromaDB Vector Database Builder for Cybersecurity RAG System.

This module creates and populates ChromaDB collections with cybersecurity datasets.
Each dataset gets its own collection with appropriate embedding models and metadata.
Designed for efficient similarity search and retrieval in RAG pipeline.

Author: DSR Portfolio Project Team
"""

import sys
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional

sys.path.append(".")
from utils.logger import setup_logger
from utils.config import get_config
import chromadb
from chromadb.config import Settings

logger = setup_logger()

# Import load_all_datasets function
import importlib.util

spec = importlib.util.spec_from_file_location(
    "load_datasets", "src/03_load_datasets.py"
)
load_datasets_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(load_datasets_module)
load_all_datasets = load_datasets_module.load_all_datasets


class ChromaDBBuilder:
    """Builder class for creating and populating ChromaDB collections."""

    def __init__(self, config=None):
        """Initialize ChromaDB builder with configuration."""
        self.config = config or get_config()
        self.client = None
        self.collections = {}

        # Collection configurations for different dataset types
        self.collection_configs = {
            "heimdall": {
                "name": "cybersec_conversations",
                "metadata": {"hnsw:space": "cosine"},
                "description": "Cybersecurity conversation dataset for RAG",
                "text_field": "assistant",  # Main content field
                "batch_size": 500,
            },
            "ttp_mapping": {
                "name": "mitre_techniques",
                "metadata": {"hnsw:space": "cosine"},
                "description": "MITRE ATT&CK technique mappings",
                "text_field": "text1",
                "batch_size": 500,
            },
            "security_attacks": {
                "name": "attack_patterns",
                "metadata": {"hnsw:space": "cosine"},
                "description": "Security attack pattern examples",
                "text_field": "text",
                "batch_size": 100,
            },
            "cyber_rules": {
                "name": "detection_rules",
                "metadata": {"hnsw:space": "cosine"},
                "description": "Cybersecurity detection rules",
                "text_field": "instruction",
                "batch_size": 200,
            },
        }

    def connect_to_chromadb(self) -> bool:
        """Connect to ChromaDB server."""
        try:
            # Use local persistent ChromaDB for development
            logger.info("Connecting to local ChromaDB...")

            # Ensure data/chromadb directory exists
            chromadb_path = Path("data/chromadb")
            chromadb_path.mkdir(parents=True, exist_ok=True)

            self.client = chromadb.PersistentClient(
                path=str(chromadb_path), settings=Settings(allow_reset=True)
            )

            logger.info("Connected to local ChromaDB successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to connect to ChromaDB: {e}")
            return False

    def create_collection(self, dataset_name: str) -> Optional[Any]:
        """Create a ChromaDB collection for a dataset."""
        try:
            config = self.collection_configs[dataset_name]
            collection_name = config["name"]

            # Delete existing collection if it exists
            try:
                existing = self.client.get_collection(collection_name)
                self.client.delete_collection(collection_name)
                logger.info(f"Deleted existing collection: {collection_name}")
            except:
                pass  # Collection doesn't exist, which is fine

            # Create new collection
            collection = self.client.create_collection(
                name=collection_name, metadata=config["metadata"]
            )

            logger.info(f"Created collection: {collection_name} for {dataset_name}")
            self.collections[dataset_name] = collection
            return collection

        except Exception as e:
            logger.error(f"Failed to create collection for {dataset_name}: {e}")
            return None

    def add_documents_to_collection(self, dataset_name: str, df: pd.DataFrame) -> bool:
        """Add documents from DataFrame to ChromaDB collection."""
        try:
            config = self.collection_configs[dataset_name]
            collection = self.collections[dataset_name]
            text_field = config["text_field"]
            batch_size = config["batch_size"]

            # Prepare documents
            documents = []
            metadatas = []
            ids = []

            for idx, row in df.iterrows():
                # Main text content
                if text_field in row and pd.notna(row[text_field]):
                    text = str(row[text_field]).strip()
                    if len(text) > 10:  # Only add meaningful texts
                        documents.append(text)

                        # Metadata (all other fields)
                        metadata = {}
                        for col in df.columns:
                            if col != text_field and pd.notna(row[col]):
                                metadata[col] = str(row[col])[
                                    :200
                                ]  # Limit metadata length

                        metadata["dataset"] = dataset_name
                        metadata["original_index"] = int(idx)
                        metadatas.append(metadata)

                        # Unique ID
                        ids.append(f"{dataset_name}_{idx}")

            # Add documents in batches
            total_docs = len(documents)
            logger.info(f"Adding {total_docs} documents to {config['name']} collection")

            for i in range(0, total_docs, batch_size):
                end_idx = min(i + batch_size, total_docs)
                batch_docs = documents[i:end_idx]
                batch_metadata = metadatas[i:end_idx]
                batch_ids = ids[i:end_idx]

                collection.add(
                    documents=batch_docs, metadatas=batch_metadata, ids=batch_ids
                )

                batch_num = i // batch_size + 1
                logger.info(
                    f"Processed batch {batch_num}: {len(batch_docs)} documents added"
                )

            logger.info(
                f"Successfully added {total_docs} documents to {config['name']} collection"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to add documents for {dataset_name}: {e}")
            return False

    def build_vector_database(self) -> Dict[str, Any]:
        """Build complete ChromaDB vector database from all datasets."""
        logger.info("Starting ChromaDB vector database build process")

        # Connect to ChromaDB
        if not self.connect_to_chromadb():
            return {"success": False, "error": "ChromaDB connection failed"}

        # Load datasets
        logger.info("Loading cybersecurity datasets for vector database")
        datasets = load_all_datasets()

        if not datasets:
            return {"success": False, "error": "No datasets available"}

        # Build collections
        results = {}
        total_documents = 0

        for dataset_name, df in datasets.items():
            logger.info(f"Processing {dataset_name} dataset for vector indexing")

            # Create collection
            collection = self.create_collection(dataset_name)
            if not collection:
                results[dataset_name] = {
                    "success": False,
                    "error": "Collection creation failed",
                }
                continue

            # Add documents
            success = self.add_documents_to_collection(dataset_name, df)
            if success:
                doc_count = collection.count()
                results[dataset_name] = {
                    "success": True,
                    "collection_name": self.collection_configs[dataset_name]["name"],
                    "documents": doc_count,
                }
                total_documents += doc_count
                logger.info(f"Completed {dataset_name}: {doc_count} documents indexed")
            else:
                results[dataset_name] = {
                    "success": False,
                    "error": "Document insertion failed",
                }

        # Summary
        successful = sum(1 for r in results.values() if r["success"])
        results["summary"] = {
            "total_collections": len(results) - 1,  # Exclude summary itself
            "successful_collections": successful,
            "total_documents": total_documents,
            "chromadb_path": "data/chromadb",
        }

        logger.info(
            f"Vector database build completed: {successful}/{len(results)-1} collections, {total_documents} total documents"
        )
        return results

    def test_search(self) -> None:
        """Test vector search functionality."""
        try:
            logger.info("Testing vector search functionality")

            # Test search on Heimdall collection
            heimdall_collection = self.client.get_collection("cybersec_conversations")

            # Sample query
            query = "How to detect malware in network traffic?"
            logger.info(f"Executing test query: '{query}'")

            results = heimdall_collection.query(query_texts=[query], n_results=3)

            # Log results
            for i, (doc, distance) in enumerate(
                zip(results["documents"][0], results["distances"][0])
            ):
                similarity = 1 - distance
                preview = doc[:100] + "..." if len(doc) > 100 else doc
                logger.info(
                    f"Search result {i+1}: similarity={similarity:.3f}, text='{preview}'"
                )

            logger.info("Vector search test completed successfully")

        except Exception as e:
            logger.error(f"Vector search test failed: {e}")


def main():
    """Main function to build ChromaDB vector database."""
    logger.info("ChromaDB vector database builder started")

    builder = ChromaDBBuilder()

    # Build the vector database
    results = builder.build_vector_database()

    # Log results summary
    if "summary" in results:
        summary = results["summary"]
        logger.info(
            f"Build summary: {summary['successful_collections']}/{summary['total_collections']} collections successful"
        )
        logger.info(f"Total documents indexed: {summary['total_documents']:,}")
        logger.info(f"ChromaDB location: {summary['chromadb_path']}")

    # Log detailed results
    for dataset, result in results.items():
        if dataset != "summary":
            if result["success"]:
                logger.info(
                    f"Collection {result['collection_name']}: {result['documents']} documents from {dataset}"
                )
            else:
                logger.error(f"Failed to process {dataset}: {result['error']}")

    # Test search if successful
    if results.get("summary", {}).get("successful_collections", 0) > 0:
        builder.test_search()

    logger.info("ChromaDB vector database build process completed")


if __name__ == "__main__":
    main()
