import random

LOCATIONS = [
    {
        "ip": "185.220.101.45",
        "city": "Moscow",
        "country": "Russia",
        "lat": 55.7558,
        "lng": 37.6173,
        "asn": "AS205540",
        "isp": "Tor Exit Node"
    },
    {
        "ip": "103.21.244.12",
        "city": "New Delhi",
        "country": "India",
        "lat": 28.6139,
        "lng": 77.2090,
        "asn": "AS13335",
        "isp": "Cloudflare India"
    },
    {
        "ip": "45.144.227.55",
        "city": "Beijing",
        "country": "China",
        "lat": 39.9042,
        "lng": 116.4074,
        "asn": "AS4134",
        "isp": "China Telecom"
    },
    {
        "ip": "66.29.154.89",
        "city": "New York",
        "country": "United States",
        "lat": 40.7128,
        "lng": -74.0060,
        "asn": "AS15169",
        "isp": "Google LLC"
    },
    {
        "ip": "89.248.172.12",
        "city": "Berlin",
        "country": "Germany",
        "lat": 52.5200,
        "lng": 13.4050,
        "asn": "AS3320",
        "isp": "Deutsche Telekom"
    },
    {
        "ip": "203.116.15.23",
        "city": "Singapore",
        "country": "Singapore",
        "lat": 1.3521,
        "lng": 103.8198,
        "asn": "AS3758",
        "isp": "SingNet"
    },
    {
        "ip": "196.25.1.23",
        "city": "Cape Town",
        "country": "South Africa",
        "lat": -33.9249,
        "lng": 18.4241,
        "asn": "AS5713",
        "isp": "Telkom SA"
    },
    {
        "ip": "101.112.33.45",
        "city": "Tokyo",
        "country": "Japan",
        "lat": 35.6895,
        "lng": 139.6917,
        "asn": "AS4713",
        "isp": "NTT Communications"
    }
]


ATTACK_TYPES = [
    {
        "type": "Brute Force Attack",
        "level": "critical",
        "color": "#ef4444",
        "mitre_id": "T1110",
        "mitre_name": "Brute Force"
    },
    {
        "type": "DDoS Attack",
        "level": "critical",
        "color": "#ef4444",
        "mitre_id": "T1498",
        "mitre_name": "Network Denial of Service"
    },
    {
        "type": "Malware Beaconing",
        "level": "high",
        "color": "#f97316",
        "mitre_id": "T1071",
        "mitre_name": "Application Layer Protocol"
    },
    {
        "type": "SQL Injection Attempt",
        "level": "medium",
        "color": "#eab308",
        "mitre_id": "T1190",
        "mitre_name": "Exploit Public-Facing Application"
    },
    {
        "type": "Phishing Campaign",
        "level": "high",
        "color": "#f97316",
        "mitre_id": "T1566",
        "mitre_name": "Phishing"
    }
]


def generate_live_attack():
    source = random.choice(LOCATIONS)
    target = random.choice(LOCATIONS)

    while target["ip"] == source["ip"]:
        target = random.choice(LOCATIONS)

    attack = random.choice(ATTACK_TYPES)

    return {
        "source": source,
        "target": target,
        "attack": attack,
        "threat_score": random.randint(65, 99),
        "packets": random.randint(1200, 9500),
        "status": "active"
    }
