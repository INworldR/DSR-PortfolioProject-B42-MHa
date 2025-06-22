"""
ChromaDB client utilities for the RAG Cybersecurity Classification System.
Provides an interface to the ChromaDB vector database for RAG operations.
"""

import chromadb
from chromadb.api import ClientAPI
from typing import List, Dict, Any, Optional, Union
from loguru import logger

from .config import get_config


class ChromaDBClient:
    """Client for interacting with the ChromaDB vector database."""

    def __init__(self, config=None):
        """Initialize the ChromaDB client with configuration."""
        self.config = config or get_config()
        self.client: Optional[ClientAPI] = None
        self.collections: Dict[str, Any] = {}

        logger.info(
            f"ChromaDB client initialized for URL: {self.config.chromadb_url()}"
        )

    def connect(self) -> bool:
        """Connect to the ChromaDB server."""
        try:
            self.client = chromadb.HttpClient(
                host=self.config.CHROMADB_HOST, port=self.config.CHROMADB_PORT
            )
            logger.info("ChromaDB connection established")
            return True
        except Exception as e:
            logger.error(f"ChromaDB connection failed: {e}")
            return False

    def test_connection(self) -> bool:
        """Test connection to the ChromaDB server."""
        try:
            if not self.client:
                return self.connect()

            # Try to list collections
            collections = self.client.list_collections()
            logger.info(
                f"ChromaDB connection successful. Collections: {[c.name for c in collections]}"
            )
            return True
        except Exception as e:
            logger.error(f"ChromaDB connection test failed: {e}")
            return False

    def get_or_create_collection(
        self, name: str, metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[Any]:
        """Get an existing collection or create a new one."""
        try:
            if not self.client:
                if not self.connect():
                    return None

            # Try to get existing collection
            try:
                collection = self.client.get_collection(name=name)
                logger.info(f"Retrieved existing collection: {name}")
            except:
                # Create new collection
                collection = self.client.create_collection(
                    name=name, metadata=metadata or {}
                )
                logger.info(f"Created new collection: {name}")

            self.collections[name] = collection
            return collection

        except Exception as e:
            logger.error(f"Error getting/creating collection {name}: {e}")
            return None

    def add_documents(
        self,
        collection_name: str,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
    ) -> bool:
        """Add documents to a collection."""
        try:
            collection = self.get_or_create_collection(collection_name)
            if not collection:
                return False

            # Generate IDs if not provided
            if not ids:
                import uuid

                ids = [str(uuid.uuid4()) for _ in documents]

            # Prepare metadatas with proper typing
            if metadatas is None:
                metadatas = [{} for _ in documents]

            # Add documents
            collection.add(documents=documents, metadatas=metadatas, ids=ids)

            logger.info(
                f"Added {len(documents)} documents to collection {collection_name}"
            )
            return True

        except Exception as e:
            logger.error(f"Error adding documents to {collection_name}: {e}")
            return False

    def query(
        self,
        collection_name: str,
        query_texts: List[str],
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        """Query a collection for similar documents."""
        try:
            collection = self.get_or_create_collection(collection_name)
            if not collection:
                return None

            results = collection.query(
                query_texts=query_texts, n_results=n_results, where=where
            )

            # Convert QueryResult to dict
            result_dict = {
                "ids": results.get("ids", []),
                "distances": results.get("distances", []),
                "metadatas": results.get("metadatas", []),
                "documents": results.get("documents", []),
                "embeddings": results.get("embeddings", []),
            }

            logger.debug(
                f"Query returned {len(result_dict.get('documents', []))} results from {collection_name}"
            )
            return result_dict

        except Exception as e:
            logger.error(f"Error querying collection {collection_name}: {e}")
            return None

    def get_collection_info(self, collection_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a collection."""
        try:
            collection = self.get_or_create_collection(collection_name)
            if not collection:
                return None

            info = {
                "name": collection.name,
                "count": collection.count(),
                "metadata": collection.metadata,
            }

            return info

        except Exception as e:
            logger.error(f"Error getting collection info for {collection_name}: {e}")
            return None

    def list_collections(self) -> List[str]:
        """List all collections."""
        try:
            if not self.client:
                if not self.connect():
                    return []

            collections = self.client.list_collections()
            return [c.name for c in collections]

        except Exception as e:
            logger.error(f"Error listing collections: {e}")
            return []

    def delete_collection(self, collection_name: str) -> bool:
        """Delete a collection."""
        try:
            if not self.client:
                if not self.connect():
                    return False

            self.client.delete_collection(name=collection_name)
            if collection_name in self.collections:
                del self.collections[collection_name]

            logger.info(f"Deleted collection: {collection_name}")
            return True

        except Exception as e:
            logger.error(f"Error deleting collection {collection_name}: {e}")
            return False

    def health_check(self) -> Dict[str, Any]:
        """Perform a health check on the ChromaDB service."""
        health = {
            "status": "unknown",
            "collections": [],
            "connection": False,
            "url": self.config.chromadb_url(),
        }

        try:
            # Test connection
            health["connection"] = self.test_connection()

            if health["connection"]:
                health["status"] = "healthy"
                health["collections"] = self.list_collections()

                # Check collection counts
                collection_info = {}
                for collection_name in health["collections"]:
                    info = self.get_collection_info(collection_name)
                    if info:
                        collection_info[collection_name] = info["count"]

                health["collection_counts"] = collection_info
            else:
                health["status"] = "unhealthy"

        except Exception as e:
            health["status"] = "error"
            health["error"] = str(e)

        return health


def test_chromadb_connection():
    """Test ChromaDB connection and print results."""
    client = ChromaDBClient()

    print("=== ChromaDB Connection Test ===")
    print(f"ChromaDB URL: {client.config.chromadb_url()}")

    # Test connection
    if client.test_connection():
        print("✅ Connection successful")

        # List collections
        collections = client.list_collections()
        print(f"Collections: {collections}")

        # Health check
        health = client.health_check()
        print(f"Health status: {health['status']}")

        if health.get("collection_counts"):
            print("Collection counts:")
            for name, count in health["collection_counts"].items():
                print(f"  {name}: {count} documents")

    else:
        print("❌ Connection failed")


if __name__ == "__main__":
    test_chromadb_connection()
