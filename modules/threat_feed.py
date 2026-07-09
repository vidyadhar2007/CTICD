import random
from datetime import datetime, timedelta


THREAT_ACTORS = [
    "APT29",
    "Lazarus Group",
    "Volt Typhoon",
    "BlackCat",
    "LockBit",
    "FIN7",
    "Sandworm",
    "Scattered Spider"
]

EVENT_TYPES = [
    "New malicious IP observed",
    "Ransomware infrastructure detected",
    "Phishing domain registered",
    "Botnet command-and-control detected",
    "Credential stuffing campaign observed",
    "DDoS activity spike detected",
    "Suspicious malware beaconing detected",
    "Exploit activity linked to known CVE"
]

SEVERITIES = [
    ("Critical", "#ef4444"),
    ("High", "#f97316"),
    ("Medium", "#eab308"),
    ("Low", "#22c55e")
]

COUNTRIES = [
    "Russia",
    "China",
    "United States",
    "India",
    "Germany",
    "Netherlands",
    "Singapore",
    "Brazil",
    "Japan",
    "United Kingdom"
]

MITRE_TECHNIQUES = [
    ("T1110", "Brute Force"),
    ("T1566", "Phishing"),
    ("T1071", "Application Layer Protocol"),
    ("T1498", "Network Denial of Service"),
    ("T1190", "Exploit Public-Facing Application"),
    ("T1059", "Command and Scripting Interpreter"),
    ("T1027", "Obfuscated Files or Information")
]


def random_ip():
    return f"{random.randint(11, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


def random_domain():
    names = ["secure-login", "update-panel", "cloud-auth", "cdn-check", "mail-verify", "gateway-sync"]
    tlds = ["com", "net", "org", "xyz", "top", "ru"]
    return f"{random.choice(names)}-{random.randint(100,999)}.{random.choice(tlds)}"


def generate_threat_feed(limit=12):
    feed = []

    now = datetime.now()

    for index in range(limit):
        severity, color = random.choice(SEVERITIES)
        mitre_id, mitre_name = random.choice(MITRE_TECHNIQUES)

        event_time = now - timedelta(minutes=index * random.randint(2, 7))

        feed.append({
            "time": event_time.strftime("%I:%M:%S %p"),
            "date": event_time.strftime("%d %b %Y"),
            "event_type": random.choice(EVENT_TYPES),
            "actor": random.choice(THREAT_ACTORS),
            "severity": severity,
            "color": color,
            "source_country": random.choice(COUNTRIES),
            "target_country": random.choice(COUNTRIES),
            "source_ip": random_ip(),
            "indicator": random.choice([random_ip(), random_domain()]),
            "mitre_id": mitre_id,
            "mitre_name": mitre_name,
            "confidence": random.randint(62, 99),
            "status": random.choice(["New", "Investigating", "Correlated", "Escalated"]),
            "summary": "Threat intelligence correlation identified suspicious infrastructure linked with active cyber activity."
        })

    return feed


def get_feed_stats(feed):
    critical = len([item for item in feed if item["severity"] == "Critical"])
    high = len([item for item in feed if item["severity"] == "High"])
    medium = len([item for item in feed if item["severity"] == "Medium"])
    low = len([item for item in feed if item["severity"] == "Low"])

    return {
        "total": len(feed),
        "critical": critical,
        "high": high,
        "medium": medium,
        "low": low,
        "active_actors": len(set(item["actor"] for item in feed)),
        "avg_confidence": round(sum(item["confidence"] for item in feed) / len(feed), 2) if feed else 0
    }