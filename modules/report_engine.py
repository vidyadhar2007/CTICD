import random
from datetime import datetime


def generate_report_data():
    return {
        "generated_at": datetime.now().strftime("%d %b %Y %I:%M:%S %p"),
        "report_id": f"CTICD-RPT-{random.randint(10000, 99999)}",
        "overall_risk": random.choice(["High", "Critical", "Medium"]),
        "risk_score": random.randint(65, 96),
        "total_alerts": random.randint(1200, 2500),
        "malicious_ips": random.randint(8000, 11000),
        "ioc_detected": random.randint(20000, 28000),
        "critical_cves": random.randint(5, 18),
        "malware_samples": random.randint(40, 120),
        "top_actor": random.choice(["APT29", "Lazarus Group", "Volt Typhoon", "FIN7", "LockBit"]),
        "top_malware": random.choice(["Emotet", "RedLine Stealer", "AgentTesla", "Mirai", "LockBit"]),
        "top_cve": random.choice(["CVE-2024-3094", "CVE-2023-34362", "CVE-2021-44228"]),
        "summary": "CTICD correlated multiple indicators across threat feeds, malware intelligence, CVE intelligence and MITRE ATT&CK mapping. Immediate review is recommended for high severity indicators.",
        "recommendations": [
            "Block confirmed malicious IPs and domains at firewall/proxy level.",
            "Prioritize Critical and High CVEs for patching.",
            "Quarantine suspicious malware samples from affected endpoints.",
            "Review authentication logs for brute force or credential stuffing patterns.",
            "Correlate threat actor activity with endpoint and network telemetry."
        ],
        "events": [
            {
                "time": datetime.now().strftime("%I:%M:%S %p"),
                "type": "Malware Detected",
                "severity": "High",
                "source": "United States",
                "target": "Germany"
            },
            {
                "time": datetime.now().strftime("%I:%M:%S %p"),
                "type": "Brute Force Attack",
                "severity": "Critical",
                "source": "Russia",
                "target": "India"
            },
            {
                "time": datetime.now().strftime("%I:%M:%S %p"),
                "type": "CVE Exploitation",
                "severity": "Critical",
                "source": "China",
                "target": "United States"
            },
            {
                "time": datetime.now().strftime("%I:%M:%S %p"),
                "type": "Phishing Campaign",
                "severity": "Medium",
                "source": "Singapore",
                "target": "Australia"
            }
        ]
    }