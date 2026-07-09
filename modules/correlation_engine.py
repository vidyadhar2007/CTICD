import hashlib
import random
from datetime import datetime


THREAT_ACTORS = [
    "APT29",
    "Lazarus Group",
    "Volt Typhoon",
    "FIN7",
    "Sandworm",
    "Scattered Spider",
    "BlackCat",
    "LockBit"
]

MALWARE_FAMILIES = [
    "Emotet",
    "RedLine Stealer",
    "AgentTesla",
    "Mirai",
    "AsyncRAT",
    "LockBit",
    "BlackCat",
    "FormBook"
]

MITRE_TECHNIQUES = [
    ("T1110", "Brute Force", "Credential Access"),
    ("T1566", "Phishing", "Initial Access"),
    ("T1071", "Application Layer Protocol", "Command and Control"),
    ("T1190", "Exploit Public-Facing Application", "Initial Access"),
    ("T1059", "Command and Scripting Interpreter", "Execution"),
    ("T1027", "Obfuscated Files or Information", "Defense Evasion"),
    ("T1105", "Ingress Tool Transfer", "Command and Control")
]

CVES = [
    "CVE-2024-3094",
    "CVE-2023-34362",
    "CVE-2021-44228",
    "CVE-2022-30190",
    "CVE-2023-23397"
]


def generate_ip(seed_value):
    seed = hashlib.sha256(seed_value.encode()).hexdigest()
    return f"{int(seed[0:2], 16)}.{int(seed[2:4], 16)}.{int(seed[4:6], 16)}.{int(seed[6:8], 16)}"


def generate_domain(seed_value):
    seed = hashlib.sha256(seed_value.encode()).hexdigest()
    return f"node-{seed[:8]}.xyz"


def severity_from_score(score):
    if score >= 85:
        return "Critical"
    if score >= 70:
        return "High"
    if score >= 45:
        return "Medium"
    return "Low"


def correlate_indicator(indicator):
    indicator = indicator.strip()

    if not indicator:
        return None

    seed = hashlib.sha256(indicator.encode()).hexdigest()
    score_seed = int(seed[:2], 16)
    risk_score = 45 + (score_seed % 55)

    severity = severity_from_score(risk_score)

    actor = THREAT_ACTORS[int(seed[2:4], 16) % len(THREAT_ACTORS)]
    malware = MALWARE_FAMILIES[int(seed[4:6], 16) % len(MALWARE_FAMILIES)]
    mitre_id, mitre_name, tactic = MITRE_TECHNIQUES[int(seed[6:8], 16) % len(MITRE_TECHNIQUES)]
    cve = CVES[int(seed[8:10], 16) % len(CVES)]

    related_ip = generate_ip(indicator)
    related_domain = generate_domain(indicator)
    related_hash = hashlib.sha256((indicator + malware).encode()).hexdigest()

    nodes = [
        {"id": "ioc", "label": "Input IOC", "value": indicator, "type": "ioc", "level": severity},
        {"id": "ip", "label": "Related IP", "value": related_ip, "type": "ip", "level": severity},
        {"id": "domain", "label": "Related Domain", "value": related_domain, "type": "domain", "level": severity},
        {"id": "malware", "label": "Malware Family", "value": malware, "type": "malware", "level": severity},
        {"id": "actor", "label": "Threat Actor", "value": actor, "type": "actor", "level": severity},
        {"id": "mitre", "label": "MITRE Technique", "value": f"{mitre_id} - {mitre_name}", "type": "mitre", "level": severity},
        {"id": "cve", "label": "Linked CVE", "value": cve, "type": "cve", "level": severity},
        {"id": "hash", "label": "Related Hash", "value": related_hash[:32] + "...", "type": "hash", "level": severity}
    ]

    edges = [
        {"from": "ioc", "to": "ip", "relation": "resolves_to"},
        {"from": "ioc", "to": "domain", "relation": "associated_with"},
        {"from": "domain", "to": "malware", "relation": "delivers"},
        {"from": "ip", "to": "actor", "relation": "controlled_by"},
        {"from": "malware", "to": "mitre", "relation": "uses"},
        {"from": "actor", "to": "cve", "relation": "exploits"},
        {"from": "malware", "to": "hash", "relation": "sample_hash"}
    ]

    timeline = [
        {"time": datetime.now().strftime("%I:%M:%S %p"), "event": "IOC submitted to correlation engine."},
        {"time": datetime.now().strftime("%I:%M:%S %p"), "event": "Related IP and domain discovered."},
        {"time": datetime.now().strftime("%I:%M:%S %p"), "event": "Malware family and threat actor correlated."},
        {"time": datetime.now().strftime("%I:%M:%S %p"), "event": "MITRE and CVE mapping completed."}
    ]

    return {
        "indicator": indicator,
        "risk_score": risk_score,
        "severity": severity,
        "actor": actor,
        "malware": malware,
        "mitre_id": mitre_id,
        "mitre_name": mitre_name,
        "tactic": tactic,
        "cve": cve,
        "related_ip": related_ip,
        "related_domain": related_domain,
        "related_hash": related_hash,
        "nodes": nodes,
        "edges": edges,
        "timeline": timeline,
        "confidence": min(risk_score + random.randint(1, 8), 100),
        "recommendation": "Correlate this IOC with firewall, endpoint and proxy logs. Block related infrastructure if confirmed malicious."
    }