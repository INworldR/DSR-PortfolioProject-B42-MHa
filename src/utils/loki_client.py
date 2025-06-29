"""
Loki API client for log retrieval.
Simple, direct access to cluster Loki service without defensive error handling.
"""

import requests
from typing import List, Dict
from datetime import datetime, timedelta


def fetch_logs(limit: int = 10, hours_back: int = 1) -> List[Dict]:
    """
    Fetch logs directly from cluster Loki service.

    Args:
        limit: Maximum number of logs to retrieve
        hours_back: How many hours back to search

    Returns:
        List of log entries with timestamp, content, and labels
    """
    loki_url = "http://10.43.108.157:3100"
    query_url = f"{loki_url}/loki/api/v1/query"

    params = {"query": '{job\!=""}', "limit": limit}

    response = requests.get(query_url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    logs = []

    if data.get("status") == "success" and "data" in data:
        for stream in data["data"]["result"]:
            for entry in stream.get("values", []):
                timestamp, log_line = entry
                logs.append(
                    {
                        "timestamp": timestamp,
                        "content": log_line,
                        "labels": stream.get("stream", {}),
                        "source": "loki",
                    }
                )

    return logs[:limit]


def get_mock_logs(limit: int = 5) -> List[Dict]:
    """
    Generate mock security logs for testing.

    Args:
        limit: Number of mock logs to generate

    Returns:
        List of mock log entries
    """
    mock_logs = [
        "Failed login attempt from 192.168.1.100 for user admin",
        "Suspicious file access detected: /etc/passwd",
        "Port scan detected from external IP 203.0.113.5",
        "Multiple failed SSH attempts from 10.0.0.15",
        "Unusual network traffic to suspicious domain malware.example.com",
        "Privilege escalation attempt detected for user guest",
        "File modification in system directory /bin/bash",
        "DNS query to known C2 server detected",
        "Abnormal process execution: /tmp/suspicious_binary",
        "Firewall blocked connection attempt to port 4444",
    ]

    logs = []
    for i, content in enumerate(mock_logs[:limit]):
        logs.append(
            {
                "timestamp": str(int(datetime.now().timestamp() * 1000000000)),
                "content": content,
                "labels": {"job": "security", "host": f"test-host-{i%3}"},
                "source": "mock",
            }
        )

    return logs


def get_logs_with_fallback(limit: int = 5) -> List[Dict]:
    """
    Get logs from Loki with mock fallback.

    Args:
        limit: Number of logs to retrieve

    Returns:
        List of log entries
    """
    try:
        logs = fetch_logs(limit)
        if logs:
            print(f"Retrieved {len(logs)} logs from Loki")
            return logs
    except Exception as e:
        print(f"Loki unavailable ({e}), using mock logs")

    logs = get_mock_logs(limit)
    print(f"Generated {len(logs)} mock logs for testing")
    return logs
