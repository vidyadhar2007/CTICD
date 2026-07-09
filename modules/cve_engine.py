import re
import random
from datetime import datetime


CVE_DATABASE = {
    "CVE-2024-3094": {
        "title": "XZ Utils Backdoor",
        "product": "XZ Utils",
        "vendor": "Tukaani",
        "cvss": 10.0,
        "severity": "Critical",
        "exploit_status": "Exploited in the wild",
        "cwe": "CWE-506",
        "mitre_id": "T1195",
        "mitre_name": "Supply Chain Compromise",
        "summary": "Backdoor discovered in XZ Utils affecting Linux distributions.",
        "patch": "Update XZ Utils immediately and verify package integrity."
    },
    "CVE-2023-34362": {
        "title": "MOVEit Transfer SQL Injection",
        "product": "MOVEit Transfer",
        "vendor": "Progress",
        "cvss": 9.8,
        "severity": "Critical",
        "exploit_status": "Exploited in the wild",
        "cwe": "CWE-89",
        "mitre_id": "T1190",
        "mitre_name": "Exploit Public-Facing Application",
        "summary": "SQL injection vulnerability exploited for data theft.",
        "patch": "Apply vendor patches and review suspicious file transfer activity."
    },
    "CVE-2021-44228": {
        "title": "Apache Log4Shell",
        "product": "Apache Log4j",
        "vendor": "Apache",
        "cvss": 10.0,
        "severity": "Critical",
        "exploit_status": "Widely exploited",
        "cwe": "CWE-502",
        "mitre_id": "T1203",
        "mitre_name": "Exploitation for Client Execution",
        "summary": "Remote code execution vulnerability in Apache Log4j.",
        "patch": "Upgrade Log4j to a fixed version and scan applications for vulnerable libraries."
    }
}


def normalize_cve(cve_id):
    cve_id = cve_id.strip().upper()
    pattern = r"^CVE-\d{4}-\d{4,7}$"

    if re.match(pattern, cve_id):
        return cve_id

    return None


def severity_from_cvss(score):
    if score >= 9.0:
        return "Critical"
    if score >= 7.0:
        return "High"
    if score >= 4.0:
        return "Medium"
    return "Low"


def generate_unknown_cve(cve_id):
    cvss = round(random.uniform(4.0, 9.8), 1)
    sev = severity_from_cvss(cvss)

    return {
        "cve_id": cve_id,
        "title": "Unverified Vulnerability Intelligence",
        "product": random.choice(["Apache Server", "OpenSSL", "Windows Server", "Linux Kernel", "WordPress Plugin"]),
        "vendor": random.choice(["Apache", "Microsoft", "OpenSSL", "Linux", "Unknown Vendor"]),
        "cvss": cvss,
        "severity": sev,
        "exploit_status": random.choice(["No known exploit", "Proof of concept available", "Exploitation suspected"]),
        "cwe": random.choice(["CWE-79", "CWE-89", "CWE-787", "CWE-22", "CWE-287"]),
        "mitre_id": random.choice(["T1190", "T1059", "T1203", "T1068"]),
        "mitre_name": random.choice(["Exploit Public-Facing Application", "Command and Scripting Interpreter", "Exploitation for Client Execution"]),
        "summary": "This CVE was not found in the local sample database. CTICD generated a simulated vulnerability intelligence profile.",
        "patch": "Verify this CVE using official advisories, apply vendor patches, and monitor exploit activity."
    }


def analyze_cve(cve_input):
    normalized = normalize_cve(cve_input)

    if not normalized:
        return {
            "valid": False,
            "error": "Invalid CVE format. Use format like CVE-2024-3094."
        }

    if normalized in CVE_DATABASE:
        data = CVE_DATABASE[normalized].copy()
    else:
        data = generate_unknown_cve(normalized)

    data["valid"] = True
    data["cve_id"] = normalized
    data["last_checked"] = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

    data["timeline"] = [
        {"time": datetime.now().strftime("%I:%M:%S %p"), "event": "CVE submitted for analysis."},
        {"time": datetime.now().strftime("%I:%M:%S %p"), "event": "CVSS severity calculated."},
        {"time": datetime.now().strftime("%I:%M:%S %p"), "event": "MITRE mapping completed."},
        {"time": datetime.now().strftime("%I:%M:%S %p"), "event": "Patch recommendation generated."}
    ]

    return data