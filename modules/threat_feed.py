import random
from datetime import datetime, timedelta, timezone

# India Standard Time (UTC+05:30)
IST = timezone(timedelta(hours=5, minutes=30), name="IST")

FEED_SOURCES = [
    "CISA Automated Indicator Sharing (AIS)",
    "AbuseIPDB Global Blacklist",
    "URLhaus Malware Distribution",
    "ThreatFox Abuse.ch Tracker",
    "AlienVault OTX Community Pulses",
    "Feodo Botnet C2 Intelligence",
    "Palo Alto Unit 42 Telemetry",
    "Shadowserver Special Reports"
]

THREAT_ACTORS = [
    "APT29 (Cozy Bear)",
    "Lazarus Group",
    "Volt Typhoon",
    "LockBit 3.0 Syndicate",
    "BlackCat (ALPHV)",
    "Sandworm (GRU)",
    "FIN7 (Carbanak)",
    "Scattered Spider (UNC3944)",
    "MuddyWater",
    "TA505"
]

TARGET_SECTORS = [
    "Financial Services & Banking",
    "Critical Infrastructure & Energy",
    "Government & Diplomatic Missions",
    "Healthcare & Pharmaceuticals",
    "Aerospace & Defense Contractors",
    "Cloud & Telecommunications",
    "Manufacturing & Supply Chain"
]

SEVERITIES = [
    ("Critical", "#ef4444"),
    ("High", "#f97316"),
    ("Medium", "#eab308"),
    ("Low", "#22c55e")
]

COUNTRIES = [
    {"name": "United States", "code": "US", "flag": "🇺🇸"},
    {"name": "Germany", "code": "DE", "flag": "🇩🇪"},
    {"name": "India", "code": "IN", "flag": "🇮🇳"},
    {"name": "United Kingdom", "code": "GB", "flag": "🇬🇧"},
    {"name": "Japan", "code": "JP", "flag": "🇯🇵"},
    {"name": "Russia", "code": "RU", "flag": "🇷🇺"},
    {"name": "China", "code": "CN", "flag": "🇨🇳"},
    {"name": "Singapore", "code": "SG", "flag": "🇸🇬"},
    {"name": "Australia", "code": "AU", "flag": "🇦🇺"},
    {"name": "Brazil", "code": "BR", "flag": "🇧🇷"}
]

MITRE_TECHNIQUES = [
    ("T1110.001", "Password Guessing / Brute Force", "Credential Access"),
    ("T1566.002", "Spearphishing Link", "Initial Access"),
    ("T1071.001", "Web Protocols (C2 Beaconing)", "Command and Control"),
    ("T1498.001", "Direct Network Flood (DDoS)", "Impact"),
    ("T1190", "Exploit Public-Facing Application", "Initial Access"),
    ("T1059.001", "PowerShell Execution", "Execution"),
    ("T1027", "Obfuscated Files or Information", "Defense Evasion"),
    ("T1486", "Data Encrypted for Impact (Ransomware)", "Impact"),
    ("T1055.012", "Process Hollowing", "Defense Evasion")
]

CURATED_INDICATORS = [
    {"indicator": "185.220.101.45", "type": "IP Address", "event": "Cobalt Strike C2 Beacon Active", "actor": "APT29 (Cozy Bear)", "source": "Palo Alto Unit 42 Telemetry", "sev": ("Critical", "#ef4444"), "target": "United States", "sector": "Government & Diplomatic Missions"},
    {"indicator": "45.144.227.55", "type": "IP Address", "event": "SOHO Router Proxy Tunnel Established", "actor": "Volt Typhoon", "source": "CISA Automated Indicator Sharing (AIS)", "sev": ("Critical", "#ef4444"), "target": "United States", "sector": "Critical Infrastructure & Energy"},
    {"indicator": "auth-secure-update.xyz", "type": "Domain", "event": "Phishing Gateway for Banking Stealer", "actor": "FIN7 (Carbanak)", "source": "ThreatFox Abuse.ch Tracker", "sev": ("High", "#f97316"), "target": "United Kingdom", "sector": "Financial Services & Banking"},
    {"indicator": "103.21.244.12", "type": "IP Address", "event": "SSH / RDP Distributed Brute Force", "actor": "Lazarus Group", "source": "AbuseIPDB Global Blacklist", "sev": ("High", "#f97316"), "target": "India", "sector": "Financial Services & Banking"},
    {"indicator": "https://cdn-firmware.top/payload.bin", "type": "URL", "event": "Second-Stage Dropper for Stealer", "actor": "Scattered Spider (UNC3944)", "source": "URLhaus Malware Distribution", "sev": ("Critical", "#ef4444"), "target": "Germany", "sector": "Cloud & Telecommunications"},
    {"indicator": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "type": "SHA256 Hash", "event": "LockBit 3.0 Kernel Driver Dropped", "actor": "LockBit 3.0 Syndicate", "source": "AlienVault OTX Community Pulses", "sev": ("Critical", "#ef4444"), "target": "Japan", "sector": "Healthcare & Pharmaceuticals"},
    {"indicator": "89.248.172.12", "type": "IP Address", "event": "SYN-Flood DDoS Amplification Node", "actor": "Sandworm (GRU)", "source": "Shadowserver Special Reports", "sev": ("High", "#f97316"), "target": "Australia", "sector": "Critical Infrastructure & Energy"},
    {"indicator": "portal-support-login.online", "type": "Domain", "event": "Credential Harvesting Reverse Proxy", "actor": "BlackCat (ALPHV)", "source": "URLhaus Malware Distribution", "sev": ("High", "#f97316"), "target": "Singapore", "sector": "Manufacturing & Supply Chain"},
    {"indicator": "194.26.29.112", "type": "IP Address", "event": "Mirai Botnet Telnet Scanner", "actor": "Opportunistic Botnet Operator", "source": "Feodo Botnet C2 Intelligence", "sev": ("Medium", "#eab308"), "target": "Brazil", "sector": "Cloud & Telecommunications"},
    {"indicator": "https://payment-invoicing.su/invoice.pdf.exe", "type": "URL", "event": "Malicious PDF Double Extension Payload", "actor": "TA505", "source": "ThreatFox Abuse.ch Tracker", "sev": ("Critical", "#ef4444"), "target": "United States", "sector": "Financial Services & Banking"},
    {"indicator": "91.215.85.17", "type": "IP Address", "event": "Fast Reverse Proxy Listener", "actor": "MuddyWater", "source": "CISA Automated Indicator Sharing (AIS)", "sev": ("High", "#f97316"), "target": "Germany", "sector": "Aerospace & Defense Contractors"},
    {"indicator": "c2-sync-cloudservice.cc", "type": "Domain", "event": "Dynamic DNS Command & Control", "actor": "Lazarus Group", "source": "Palo Alto Unit 42 Telemetry", "sev": ("High", "#f97316"), "target": "Japan", "sector": "Financial Services & Banking"}
]


def generate_threat_feed(limit=18):
    feed = []
    now = datetime.now(IST)

    # Mix curated and dynamic entries
    base_pool = CURATED_INDICATORS.copy()
    random.shuffle(base_pool)

    for idx, item in enumerate(base_pool[:limit]):
        event_time = now - timedelta(minutes=idx * random.randint(3, 8), seconds=random.randint(5, 50))
        source_country = random.choice([c for c in COUNTRIES if c["name"] != item["target"]])
        target_country = next((c for c in COUNTRIES if c["name"] == item["target"]), COUNTRIES[0])
        mitre_id, mitre_name, mitre_tactic = random.choice(MITRE_TECHNIQUES)

        confidence = random.randint(82, 99) if item["sev"][0] in ["Critical", "High"] else random.randint(65, 84)

        feed.append({
            "id": f"CTI-FEED-{idx+1:04d}",
            "time": event_time.strftime("%I:%M:%S %p"),
            "date": event_time.strftime("%d %b %Y"),
            "timestamp": event_time.isoformat(),
            "indicator": item["indicator"],
            "type": item["type"],
            "event_type": item["event"],
            "actor": item["actor"],
            "feed_source": item["source"],
            "severity": item["sev"][0],
            "color": item["sev"][1],
            "tlp": "TLP:AMBER",
            "source_country": source_country["name"],
            "source_flag": source_country["flag"],
            "target_country": target_country["name"],
            "target_flag": target_country["flag"],
            "target_sector": item["sector"],
            "mitre_id": mitre_id,
            "mitre_name": mitre_name,
            "mitre_tactic": mitre_tactic,
            "confidence": confidence,
            "status": random.choice(["Active Threat", "Correlated", "Investigating", "Blocked at Edge"]),
            "summary": f"{item['source']} verified malicious telemetry linked with {item['actor']} targeting {item['sector']}."
        })

    return feed


def get_feed_stats(feed):
    if not feed:
        return {"total": 0, "critical": 0, "high": 0, "medium": 0, "low": 0, "active_actors": 0, "avg_confidence": 0}

    critical = sum(1 for item in feed if item["severity"] == "Critical")
    high = sum(1 for item in feed if item["severity"] == "High")
    medium = sum(1 for item in feed if item["severity"] == "Medium")
    low = sum(1 for item in feed if item["severity"] == "Low")
    actors = len(set(item["actor"] for item in feed))
    avg_conf = round(sum(item["confidence"] for item in feed) / len(feed), 1)

    return {
        "total": len(feed),
        "critical": critical,
        "high": high,
        "medium": medium,
        "low": low,
        "active_actors": actors,
        "avg_confidence": avg_conf,
        "critical_percentage": round((critical / len(feed)) * 100, 1)
    }
