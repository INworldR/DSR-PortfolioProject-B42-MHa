"""
Core log classification logic using ChromaDB and pattern matching.
Clean, focused implementation without defensive error handling.
"""

from typing import List, Dict, Any
from .chromadb_client import ChromaDBClient
from .mitre_mapper import map_content_to_mitre_techniques, expand_technique_mapping


def classify_single_log(log: Dict, chromadb_client: ChromaDBClient) -> Dict:
    """
    Classify a single log entry using ChromaDB similarity search.

    Args:
        log: Log entry with content, timestamp, labels
        chromadb_client: ChromaDB client instance

    Returns:
        Classification result with techniques, confidence, method
    """
    content = log["content"]

    # Try ChromaDB similarity search first
    try:
        similar_results = search_chromadb_for_patterns(content, chromadb_client)
        if similar_results and len(similar_results.get("documents", [[]])[0]) > 0:
            techniques = extract_techniques_from_similarity(similar_results)
            confidence = calculate_similarity_confidence(similar_results)

            return {
                "original_log": log,
                "suggested_techniques": techniques,
                "confidence": confidence,
                "method": "chromadb_similarity",
                "similar_count": len(similar_results.get("documents", [[]])[0]),
            }
    except Exception:
        pass  # Fall through to pattern matching

    # Fallback to pattern matching
    techniques, confidence = map_content_to_mitre_techniques(content)
    expanded_techniques = expand_technique_mapping(content, techniques)

    return {
        "original_log": log,
        "suggested_techniques": expanded_techniques,
        "confidence": confidence,
        "method": "pattern_matching",
        "pattern_matches": len(expanded_techniques),
    }


def classify_log_batch(logs: List[Dict], chromadb_client: ChromaDBClient) -> List[Dict]:
    """
    Classify a batch of logs.

    Args:
        logs: List of log entries
        chromadb_client: ChromaDB client instance

    Returns:
        List of classification results
    """
    return [classify_single_log(log, chromadb_client) for log in logs]


def search_chromadb_for_patterns(
    content: str,
    chromadb_client: ChromaDBClient,
    collection_name: str = "mitre_techniques",
) -> Dict:
    """
    Search ChromaDB for similar cybersecurity patterns.

    Args:
        content: Log content to search for
        chromadb_client: ChromaDB client instance
        collection_name: ChromaDB collection to search

    Returns:
        ChromaDB query results
    """
    # Query ChromaDB for similar content
    results = chromadb_client.query(
        collection_name=collection_name, query_texts=[content], n_results=5
    )

    return results or {}


def extract_techniques_from_similarity(similarity_results: Dict) -> List[str]:
    """
    Extract MITRE techniques from ChromaDB similarity results.

    Args:
        similarity_results: ChromaDB query results

    Returns:
        List of MITRE technique IDs and names
    """
    techniques = []

    # Extract techniques from metadata
    metadatas = similarity_results.get("metadatas", [[]])[0]
    for metadata in metadatas:
        if isinstance(metadata, dict):
            technique = metadata.get("technique") or metadata.get("mitre_technique")
            if technique:
                techniques.append(technique)

    # Extract techniques from document content
    documents = similarity_results.get("documents", [[]])[0]
    for doc in documents:
        if isinstance(doc, str):
            # Look for technique patterns in the document
            content_techniques, _ = map_content_to_mitre_techniques(doc)
            techniques.extend(content_techniques)

    # Remove duplicates and return
    return list(set(techniques))


def calculate_similarity_confidence(similarity_results: Dict) -> float:
    """
    Calculate confidence based on ChromaDB similarity distances.

    Args:
        similarity_results: ChromaDB query results with distances

    Returns:
        Confidence score between 0.0 and 1.0
    """
    distances = similarity_results.get("distances", [[]])[0]

    if not distances:
        return 0.5

    # Convert distances to confidence (lower distance = higher confidence)
    avg_distance = sum(distances) / len(distances)
    confidence = max(0.0, min(1.0, 1.0 - avg_distance))

    # Boost confidence for very similar results
    if avg_distance < 0.3:
        confidence = min(0.95, confidence + 0.2)
    elif avg_distance < 0.5:
        confidence = min(0.85, confidence + 0.1)

    return round(confidence, 2)


def get_classification_summary(results: List[Dict]) -> Dict:
    """
    Generate summary statistics for classification results.

    Args:
        results: List of classification results

    Returns:
        Summary statistics
    """
    if not results:
        return {}

    total_logs = len(results)
    total_techniques = sum(len(r["suggested_techniques"]) for r in results)
    avg_confidence = sum(r["confidence"] for r in results) / total_logs

    methods = {}
    for result in results:
        method = result.get("method", "unknown")
        methods[method] = methods.get(method, 0) + 1

    chromadb_used = methods.get("chromadb_similarity", 0) > 0

    return {
        "logs_processed": total_logs,
        "total_techniques_suggested": total_techniques,
        "average_confidence": round(avg_confidence, 2),
        "methods_used": methods,
        "chromadb_integration": "SUCCESS" if chromadb_used else "PATTERN_MATCHING_ONLY",
    }


def print_classification_results(results: List[Dict]):
    """
    Print classification results in a clean, professional format.

    Args:
        results: List of classification results to display
    """
    print("\nLOG CLASSIFICATION RESULTS")
    print("=" * 80)

    for i, result in enumerate(results, 1):
        log = result["original_log"]
        techniques = result["suggested_techniques"]
        confidence = result["confidence"]
        method = result.get("method", "unknown")

        # Extract log info
        content = log["content"]
        job = log["labels"].get("job", "unknown")
        hostname = log["labels"].get("hostname", log["labels"].get("host", "unknown"))
        source = log.get("source", "unknown")

        print(f"\n[{i}] {job}@{hostname} ({source})")
        print(f"    Content: {content[:100]}...")
        print(f"    Method: {method}")
        print(f"    Confidence: {confidence}")

        if method == "chromadb_similarity":
            similar_count = result.get("similar_count", 0)
            print(f"    Similar patterns found: {similar_count}")

        print(f"    MITRE Techniques:")
        for technique in techniques:
            print(f"      - {technique}")
        print("-" * 80)

    # Print summary
    summary = get_classification_summary(results)
    print(f"\nSUMMARY:")
    print(f"   Logs processed: {summary.get('logs_processed', 0)}")
    print(
        f"   Total techniques suggested: {summary.get('total_techniques_suggested', 0)}"
    )
    print(f"   Average confidence: {summary.get('average_confidence', 0.0):.2f}")
    print(f"   ChromaDB integration: {summary.get('chromadb_integration', 'UNKNOWN')}")
