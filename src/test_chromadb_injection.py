# \!/usr/bin/env python3
"""
ChromaDB Integration Test for ATP Log Generator.

Tests ATP log injection and retrieval from ChromaDB for RAG system validation.

Author: DSR Portfolio Project Team
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Any

sys.path.append(".")
from utils.logger import setup_logger
from utils.chromadb_client import ChromaDBClient
from atp_log_generator import ATPLogGenerator

logger = setup_logger()


class ATPChromaDBTester:
    """Test ATP logs with ChromaDB integration."""

    def __init__(self):
        """Initialize ChromaDB tester."""
        logger.info("Initializing ATP ChromaDB Tester")
        self.generator = ATPLogGenerator()
        self.chroma_client = ChromaDBClient()
        self.collection_name = "atp_simulation_logs"

    def test_injection(self, apt_group: str, num_logs: int = 5) -> bool:
        """Test ATP log injection into ChromaDB."""
        logger.info(f"Testing ChromaDB injection for {apt_group}")

        # Generate ATP logs
        logs = self.generator.generate_attack_sequence(apt_group, num_logs)

        # Prepare documents for ChromaDB
        documents = []
        metadatas = []
        ids = []

        for i, log in enumerate(logs):
            # Create document text for RAG queries
            doc_text = self._create_document_text(log)
            documents.append(doc_text)

            # Create metadata for filtering
            metadata = {
                "apt_group": log["apt_group"],
                "mitre_technique": log["mitre_technique"],
                "technique_name": log["technique_name"],
                "tactic": log["tactic"],
                "severity": log["severity"],
                "timestamp": log["timestamp"],
            }
            metadatas.append(metadata)
            ids.append(f"{apt_group}_{i+1:03d}")

        # Inject into ChromaDB
        collection = self.chroma_client.get_or_create_collection(
            self.collection_name, metadata={"description": "ATP simulation logs"}
        )
        if collection is None:
            logger.error("Failed to create or get ChromaDB collection")
            return False
        collection.add(documents=documents, metadatas=metadatas, ids=ids)

        logger.info(f"Injected {len(documents)} ATP logs into ChromaDB")
        return True

    def _create_document_text(self, log: Dict[str, Any]) -> str:
        """Create searchable document text from log entry."""
        return f"""ATP Simulation Log
APT Group: {log['apt_group']}
MITRE Technique: {log['mitre_technique']} - {log['technique_name']}
Tactic: {log['tactic']}
Severity: {log['severity']}
Process: {log['process_name']}
Command: {log['command_line']}
Indicators: {', '.join(log['indicators'])}
Target: {log['target_host']}
Success: {log['success']}
Threat Score: {log['threat_score']}/10
"""

    def test_query(self, query_text: str, n_results: int = 3) -> Dict[str, Any]:
        """Test RAG queries against ATP logs."""
        logger.info(f"Testing query: {query_text}")

        collection = self.chroma_client.get_or_create_collection(
            self.collection_name, metadata={"description": "ATP simulation logs"}
        )
        if collection is None:
            logger.error("Failed to create or get ChromaDB collection")
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results,
            include=["documents", "metadatas", "distances"],
        )

        logger.info(f"Found {len(results['documents'][0])} results")
        return results

    def run_demo_tests(self) -> None:
        """Run comprehensive demo tests."""
        logger.info("Starting ATP ChromaDB demo tests")

        # Test injection for all APT groups
        for apt_group in ["apt29_cozy_bear", "apt1_comment_crew", "lazarus_group"]:
            self.test_injection(apt_group, 5)

        # Test various queries
        test_queries = [
            "PowerShell execution techniques",
            "Credential dumping attacks",
            "Lateral movement methods",
            "Data exfiltration patterns",
            "Registry persistence techniques",
        ]

        for query in test_queries:
            results = self.test_query(query)
            print(f"\nQuery: {query}")
            for i, doc in enumerate(results["documents"][0]):
                metadata = results["metadatas"][0][i]
                distance = results["distances"][0][i]
                print(
                    f"  Result {i+1}: {metadata['mitre_technique']} - {metadata['technique_name']} (distance: {distance:.3f})"
                )

        logger.info("ATP ChromaDB demo tests completed")


def main():
    """Main function for standalone execution."""
    tester = ATPChromaDBTester()
    tester.run_demo_tests()


if __name__ == "__main__":
    main()
