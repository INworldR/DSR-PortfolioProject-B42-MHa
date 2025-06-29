"""
MITRE ATT&CK technique mapping utilities.
Pattern-based classification of log content to MITRE techniques.
"""

from typing import List, Tuple


def map_content_to_mitre_techniques(content: str) -> Tuple[List[str], float]:
    """
    Map log content to MITRE ATT&CK techniques using pattern matching.

    Args:
        content: Log content to analyze

    Returns:
        Tuple of (techniques list, confidence score)
    """
    content_lower = content.lower()
    techniques = []
    confidence = 0.5  # Default confidence

    # Authentication and access patterns
    if any(
        word in content_lower for word in ["login", "ssh", "authentication", "password"]
    ):
        techniques.extend(["T1078 - Valid Accounts", "T1110 - Brute Force"])
        confidence = 0.8

    # File system access patterns
    elif any(
        word in content_lower for word in ["file", "passwd", "access", "read", "write"]
    ):
        techniques.extend(
            ["T1005 - Data from Local System", "T1083 - File and Directory Discovery"]
        )
        confidence = 0.7

    # Network scanning patterns
    elif any(word in content_lower for word in ["scan", "port", "network", "probe"]):
        techniques.extend(
            ["T1046 - Network Service Discovery", "T1595 - Active Scanning"]
        )
        confidence = 0.9

    # Privilege escalation patterns
    elif any(
        word in content_lower for word in ["privilege", "escalation", "sudo", "root"]
    ):
        techniques.append("T1548 - Abuse Elevation Control Mechanism")
        confidence = 0.8

    # Process execution patterns
    elif any(
        word in content_lower for word in ["process", "execution", "command", "script"]
    ):
        techniques.append("T1059 - Command and Scripting Interpreter")
        confidence = 0.6

    # Network blocking/filtering patterns
    elif any(
        word in content_lower for word in ["firewall", "blocked", "denied", "rejected"]
    ):
        techniques.append("T1095 - Non-Application Layer Protocol")
        confidence = 0.7

    # DNS and domain patterns
    elif any(word in content_lower for word in ["dns", "domain", "resolve", "query"]):
        techniques.append("T1071 - Application Layer Protocol")
        confidence = 0.6

    # Default fallback
    else:
        techniques.append("T1059 - Command and Scripting Interpreter")
        confidence = 0.5

    return list(set(techniques)), confidence


def get_technique_confidence(techniques: List[str], content: str) -> float:
    """
    Calculate confidence score based on technique specificity and content analysis.

    Args:
        techniques: List of MITRE techniques
        content: Original log content

    Returns:
        Confidence score between 0.0 and 1.0
    """
    content_lower = content.lower()

    # High confidence indicators
    high_confidence_words = ["scan", "attack", "intrusion", "malware", "exploit"]
    if any(word in content_lower for word in high_confidence_words):
        return 0.9

    # Medium confidence indicators
    medium_confidence_words = [
        "suspicious",
        "failed",
        "denied",
        "blocked",
        "unauthorized",
    ]
    if any(word in content_lower for word in medium_confidence_words):
        return 0.7

    # Default confidence based on technique count
    if len(techniques) > 1:
        return 0.6

    return 0.5


def expand_technique_mapping(content: str, existing_techniques: List[str]) -> List[str]:
    """
    Expand technique mapping with additional context-aware techniques.

    Args:
        content: Log content
        existing_techniques: Already identified techniques

    Returns:
        Expanded list of techniques
    """
    content_lower = content.lower()
    additional_techniques = []

    # If we detected authentication issues, add related techniques
    if any("T1078" in tech or "T1110" in tech for tech in existing_techniques):
        if "remote" in content_lower or "ssh" in content_lower:
            additional_techniques.append("T1021 - Remote Services")

    # If we detected file access, add related techniques
    if any("T1005" in tech or "T1083" in tech for tech in existing_techniques):
        if "config" in content_lower or "system" in content_lower:
            additional_techniques.append("T1082 - System Information Discovery")

    # If we detected network activity, add related techniques
    if any("T1046" in tech or "T1595" in tech for tech in existing_techniques):
        if "external" in content_lower or "internet" in content_lower:
            additional_techniques.append("T1090 - Proxy")

    return existing_techniques + additional_techniques


# Technique database for reference
MITRE_TECHNIQUES = {
    "T1078": "Valid Accounts",
    "T1110": "Brute Force",
    "T1005": "Data from Local System",
    "T1083": "File and Directory Discovery",
    "T1046": "Network Service Discovery",
    "T1595": "Active Scanning",
    "T1548": "Abuse Elevation Control Mechanism",
    "T1059": "Command and Scripting Interpreter",
    "T1095": "Non-Application Layer Protocol",
    "T1071": "Application Layer Protocol",
    "T1021": "Remote Services",
    "T1082": "System Information Discovery",
    "T1090": "Proxy",
}


def get_technique_description(technique_id: str) -> str:
    """
    Get description for a MITRE technique ID.

    Args:
        technique_id: MITRE technique ID (e.g., 'T1078')

    Returns:
        Technique description
    """
    return MITRE_TECHNIQUES.get(technique_id, "Unknown Technique")


def format_technique_with_description(technique_id: str) -> str:
    """
    Format technique ID with description.

    Args:
        technique_id: MITRE technique ID

    Returns:
        Formatted string like 'T1078 - Valid Accounts'
    """
    description = get_technique_description(technique_id)
    return f"{technique_id} - {description}"
