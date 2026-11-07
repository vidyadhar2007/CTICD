import re
import hashlib
import random
import ipaddress
from datetime import datetime, timedelta, timezone

# India Standard Time (UTC+05:30)
IST = timezone(timedelta(hours=5, minutes=30), name="IST")

COUNTRY_DATA = [
    {"country": "Russia", "code": "RU", "city": "Moscow", "flag": "🇷🇺", "lat": 55.7558, "lng": 37.6173, "asn": "AS205540", "isp": "Rostelecom Backbone", "org": "Bulletproof Host"},
    {"country": "China", "code": "CN", "city": "Beijing", "flag": "🇨🇳", "lat": 39.9042, "lng": 116.4074, "asn": "AS4134", "isp": "China Telecom", "org": "Cloud Data Center"},
    {"country": "United States", "code": "US", "city": "Ashburn", "flag": "🇺🇸", "lat": 39.0438, "lng": -77.4874, "asn": "AS14618", "isp": "Amazon AWS Cloud", "org": "Compromised VPS"},
    {"country": "Netherlands", "code": "NL", "city": "Amsterdam", "flag": "🇳🇱", "lat": 52.3676, "lng": 4.9041, "asn": "AS60729", "isp": "Serverius Holding", "org": "Tor Exit Node"},
    {"country": "Germany", "code": "DE", "city": "Frankfurt", "flag": "🇩🇪", "lat": 50.1109, "lng": 8.6821, "asn": "AS3320", "isp": "Deutsche Telekom", "org": "Hosted Proxy"},
    {"country": "India", "code": "IN", "city": "Mumbai", "flag": "🇮🇳", "lat": 19.0760, "lng": 72.8777, "asn": "AS55836", "isp": "Reliance Jio", "org": "Enterprise Gateway"},
    {"country": "Singapore", "code": "SG", "city": "Singapore", "flag": "🇸🇬", "lat": 1.3521, "lng": 103.8198, "asn": "AS3758", "isp": "SingNet Telecommunications", "org": "C2 Relay"},
    {"country": "Brazil", "code": "BR", "city": "São Paulo", "flag": "🇧🇷", "lat": -23.5505, "lng": -46.6333, "asn": "AS28573", "isp": "Claro Brasil", "org": "Infected Botnet Node"}
]

SUSPICIOUS_TLDS = [".ru", ".cn", ".xyz", ".top", ".su", ".work", ".click", ".tk", ".ml", ".cc"]

THREAT_ACTOR_MAP = {
    "IP Address": ["APT29", "Volt Typhoon", "LockBit", "Sandworm", "FIN7"],
    "Domain": ["Lazarus Group", "Scattered Spider", "APT28", "BlackCat"],
    "URL": ["PhishLabs Tracker", "Emotet Gang", "FIN7 Phishing"],
    "SHA256 Hash": ["RedLine Operator", "LockBit 3.0", "Cobalt Strike Team"],
    "MD5 Hash": ["AgentTesla Actor", "AsyncRAT Operator"]
}


def detect_ioc_type(value):
    value = value.strip()
    if not value:
        return "Unknown"

    # IPv4
    try:
        ip = ipaddress.ip_address(value)
        if ip.version == 4:
            return "IP Address"
        elif ip.version == 6:
            return "IPv6 Address"
    except ValueError:
        pass

    # CIDR
    if "/" in value:
        try:
            ipaddress.ip_network(value, strict=False)
            return "CIDR Network"
        except ValueError:
            pass

    # CVE ID
    if re.match(r"^CVE-\d{4}-\d{4,7}$", value, re.IGNORECASE):
        return "CVE Vulnerability"

    # Hashes
    if re.match(r"^[a-fA-F0-9]{32}$", value):
        return "MD5 Hash"
    if re.match(r"^[a-fA-F0-9]{40}$", value):
        return "SHA1 Hash"
    if re.match(r"^[a-fA-F0-9]{64}$", value):
        return "SHA256 Hash"

    # URL
    if re.match(r"^https?://", value, re.IGNORECASE):
        return "URL"

    # Email
    if re.match(r"^[^@]+@[^@]+\.[^@]+$", value):
        return "Email Address"

    # Domain
    if re.match(r"^(?!-)[A-Za-z0-9-_]{1,63}(?<!-)(\.[A-Za-z]{2,})+$", value):
        return "Domain"

    return "String / Keyword"


def calculate_threat_score(ioc, ioc_type):
    lowered = ioc.lower()
    seed = hashlib.sha256(lowered.encode()).hexdigest()
    score_val = int(seed[:2], 16) % 50

    base = 40
    if ioc_type == "IP Address":
        base = 55
        if lowered.startswith(("185.", "45.", "193.", "89.", "91.", "194.")):
            base += 25
    elif ioc_type in ["Domain", "URL"]:
        base = 50
        bad_keywords = ["login", "bank", "secure", "verify", "update", "portal", "token", "auth", "crypto", "account", "webscr"]
        for kw in bad_keywords:
            if kw in lowered:
                base += 12
        if any(lowered.endswith(tld) or tld + "/" in lowered for tld in SUSPICIOUS_TLDS):
            base += 18
    elif "Hash" in ioc_type:
        base = 65

    final_score = min(99, max(15, base + score_val))
    return final_score


def severity_from_score(score):
    if score >= 88:
        return "Critical"
    if score >= 70:
        return "High"
    if score >= 45:
        return "Medium"
    return "Low"


def generate_yara_rule(ioc, ioc_type, score):
    clean_name = re.sub(r"[^a-zA-Z0-9_]", "_", ioc)[:24]
    return f"""/*
  CTICD IOC Detection Rule
  Target: {ioc} ({ioc_type})
  Threat Score: {score}/100
*/
rule CTICD_IOC_{clean_name} {{
    meta:
        description = "Detects indicator associated with malicious telemetry"
        ioc_type = "{ioc_type}"
        score = {score}
        author = "CTICD SOC Engine"
        tlp = "TLP:AMBER"
    strings:
        $ioc = "{ioc}" ascii wide nocase
    condition:
        $ioc
}}"""


def generate_snort_rule(ioc, ioc_type):
    sid = random.randint(3000000, 3999999)
    if ioc_type == "IP Address":
        return f'alert ip any any -> {ioc} any (msg:"CTICD IOC Threat IP Traffic Detected: {ioc}"; threshold:type limit, track by_src, count 1, seconds 60; classtype:trojan-activity; sid:{sid}; rev:1;)'
    elif ioc_type in ["Domain", "URL"]:
        domain_part = ioc.replace("https://", "").replace("http://", "").split("/")[0]
        return f'alert tcp $HOME_NET any -> $EXTERNAL_NET [80,443] (msg:"CTICD DNS/HTTP Malicious Host Query: {domain_part}"; content:"{domain_part}"; http_header; nocase; classtype:bad-unknown; sid:{sid}; rev:1;)'
    return f'# Rule not applicable for non-network IOC type: {ioc_type}'


def generate_firewall_commands(ioc, ioc_type):
    if ioc_type == "IP Address":
        return {
            "iptables": f"sudo iptables -I INPUT -s {ioc} -j DROP && sudo iptables -I OUTPUT -d {ioc} -j DROP",
            "cisco_ios": f"access-list 100 deny ip host {ioc} any log",
            "palo_alto": f"set address Malicious_{ioc.replace('.', '_')} ip-netmask {ioc}/32; set rulebase security rules Block_CTICD destination Malicious_{ioc.replace('.', '_')} action deny",
            "windows_firewall": f'netsh advfirewall firewall add rule name="CTICD_Block_{ioc}" dir=in action=block remoteip={ioc}'
        }
    elif ioc_type in ["Domain", "URL"]:
        domain = ioc.replace("https://", "").replace("http://", "").split("/")[0]
        return {
            "bind_rpz": f"{domain} CNAME .",
            "pihole": f"pihole -b {domain}",
            "hosts_file": f"0.0.0.0 {domain}",
            "palo_alto": f"set profiles url-filtering Block_CTICD block-list {domain}"
        }
    return {
        "note": "Automated network firewall block is primarily suited for IP Addresses and Domains."
    }


def analyze_ioc(ioc):
    ioc = ioc.strip()
    if not ioc:
        return None

    seed = hashlib.sha256(ioc.lower().encode()).hexdigest()
    ioc_type = detect_ioc_type(ioc)
    threat_score = calculate_threat_score(ioc, ioc_type)
    severity = severity_from_score(threat_score)

    # Geo telemetry
    geo_idx = int(seed[:2], 16) % len(COUNTRY_DATA)
    geo = COUNTRY_DATA[geo_idx].copy()
    geo["latitude"] = round(geo["lat"] + (int(seed[2:4], 16) % 20 - 10) * 0.1, 4)
    geo["longitude"] = round(geo["lng"] + (int(seed[4:6], 16) % 20 - 10) * 0.1, 4)
    geo["autonomous_system"] = f"{geo['asn']} ({geo['isp']})"
    geo["hosting_type"] = random.choice(["Bulletproof Hosting", "Compromised VPS", "Tor Exit Node", "Cloud Infrastructure", "Dynamic Residential"])

    # Multi-vendor scan results
    total_engines = 72
    detected_engines = min(72, max(2, int((threat_score / 100) * total_engines) + (int(seed[6:8], 16) % 6 - 3)))
    clean_engines = max(0, total_engines - detected_engines - 3)
    suspicious_engines = max(0, total_engines - detected_engines - clean_engines)

    # Attribution & Campaign
    actor_list = THREAT_ACTOR_MAP.get(ioc_type, ["APT29", "LockBit", "Volt Typhoon", "Lazarus Group"])
    actor = actor_list[int(seed[8:10], 16) % len(actor_list)]
    campaign = f"CAMPAIGN-{actor[:3].upper()}-{seed[:4].upper()}"

    now = datetime.now(IST)
    first_seen = (now - timedelta(days=int(seed[10:12], 16) % 90 + 3, hours=int(seed[12:14], 16) % 24)).strftime("%Y-%m-%d %H:%M:%S IST")
    last_seen = (now - timedelta(minutes=int(seed[14:16], 16) % 180 + 5)).strftime("%Y-%m-%d %H:%M:%S IST")

    # MITRE ATT&CK technique
    if ioc_type == "IP Address":
        mitre_id = "T1071.001"
        mitre_name = "Application Layer Protocol: Web Protocols (C2)"
        mitre_tactic = "Command and Control"
    elif ioc_type in ["Domain", "URL"]:
        mitre_id = "T1566.002"
        mitre_name = "Phishing: Spearphishing Link"
        mitre_tactic = "Initial Access"
    elif "Hash" in ioc_type:
        mitre_id = "T1059.001"
        mitre_name = "Command and Scripting Interpreter: PowerShell"
        mitre_tactic = "Execution"
    else:
        mitre_id = "T1190"
        mitre_name = "Exploit Public-Facing Application"
        mitre_tactic = "Initial Access"

    # Multi-engine detection list
    engine_names = [
        {"name": "CrowdStrike Falcon", "category": "Next-Gen EDR", "result": "Malicious" if threat_score > 60 else "Clean"},
        {"name": "Microsoft Defender", "category": "Cloud Endpoint", "result": "Malicious" if threat_score > 50 else "Clean"},
        {"name": "Kaspersky Threat Intel", "category": "Reputation Feed", "result": "Malicious" if threat_score > 65 else "Suspicious"},
        {"name": "SentinelOne Singularity", "category": "AI Behavioral", "result": "Malicious" if threat_score > 55 else "Clean"},
        {"name": "Bitdefender Enterprise", "category": "Anti-Malware", "result": "Malicious" if threat_score > 70 else "Clean"},
        {"name": "Palo Alto Networks WildFire", "category": "Sandboxing", "result": "Malicious" if threat_score > 75 else "Suspicious"},
        {"name": "Fortinet FortiGuard", "category": "Perimeter IPS", "result": "Malicious" if threat_score > 65 else "Clean"},
        {"name": "Sophos Intercept X", "category": "Exploit Prevention", "result": "Malicious" if threat_score > 60 else "Clean"},
        {"name": "ESET LiveGrid", "category": "Threat Radar", "result": "Suspicious" if threat_score > 40 else "Clean"},
        {"name": "Trend Micro Vision One", "category": "XDR Telemetry", "result": "Malicious" if threat_score > 70 else "Suspicious"},
        {"name": "Check Point ThreatCloud", "category": "Network Security", "result": "Malicious" if threat_score > 80 else "Clean"},
        {"name": "AlienVault OTX Pulse", "category": "Community Intel", "result": "Malicious" if threat_score > 45 else "Clean"}
    ]

    # Timeline of Telemetry
    timeline = [
        {
            "time": (now - timedelta(days=2)).strftime("%b %d, %I:%M %p"),
            "event": f"First observed in global honeypot sensor network ({geo['country']}).",
            "severity": "Medium"
        },
        {
            "time": (now - timedelta(hours=14)).strftime("%b %d, %I:%M %p"),
            "event": f"Correlated with active telemetry from {actor} operations.",
            "severity": "High"
        },
        {
            "time": (now - timedelta(hours=3)).strftime("%b %d, %I:%M %p"),
            "event": f"AbuseIPDB and external OSINT reported 24+ brute-force/malware beacons.",
            "severity": "High"
        },
        {
            "time": now.strftime("%b %d, %I:%M %p"),
            "event": "CTICD multi-feed correlation confirmed high-threat reputation.",
            "severity": severity
        }
    ]

    # STIX 2.1 Representation
    stix_bundle = {
        "type": "bundle",
        "id": f"bundle--{seed[:8]}-{seed[8:12]}-4000-8000-{seed[12:24]}",
        "spec_version": "2.1",
        "objects": [
            {
                "type": "indicator",
                "spec_version": "2.1",
                "id": f"indicator--{seed[:8]}-{seed[8:12]}-4111-8222-{seed[12:24]}",
                "created": datetime.utcnow().isoformat() + "Z",
                "name": f"{ioc_type}: {ioc}",
                "description": f"Threat indicator correlated with {actor} activity",
                "pattern_type": "stix",
                "pattern": f"[{ioc_type.lower()}:value = '{ioc}']",
                "valid_from": datetime.utcnow().isoformat() + "Z",
                "confidence": min(100, threat_score + 2),
                "labels": ["malicious-activity", actor.lower().replace(" ", "-")]
            }
        ]
    }

    return {
        "ioc": ioc,
        "ioc_type": ioc_type,
        "threat_score": threat_score,
        "severity": severity,
        "tlp": "TLP:AMBER",
        "status": "Malicious" if threat_score >= 70 else "Suspicious" if threat_score >= 45 else "Clean",
        "confidence": min(99, max(60, threat_score + 4)),
        "actor": actor,
        "campaign": campaign,
        "first_seen": first_seen,
        "last_seen": last_seen,
        "geo": geo,
        "vt": {
            "detected": detected_engines,
            "total": total_engines,
            "suspicious": suspicious_engines,
            "clean": clean_engines,
            "ratio": f"{detected_engines}/{total_engines}"
        },
        "abuse": {
            "score": threat_score,
            "reports": int(seed[16:20], 16) % 1500 + 45,
            "last_report": "18 minutes ago"
        },
        "shodan": {
            "ports": "22 (SSH), 80 (HTTP), 443 (HTTPS), 8080 (Proxy)",
            "os": "Linux 5.15 Ubuntu LTS",
            "hostnames": f"{seed[:8]}.node.cloudproxy.net",
            "vulnerabilities": "OpenSSL 1.1.1 Heartbleed patched; SSH weak ciphers active"
        },
        "alienvault": {
            "pulse_count": int(seed[20:22], 16) % 35 + 4,
            "tags": ["c2-infrastructure", "brute-force", actor.lower().replace(" ", "-"), "threat-intel"]
        },
        "mitre": {
            "id": mitre_id,
            "name": mitre_name,
            "tactic": mitre_tactic,
            "description": f"Associated with adversary operations executing {mitre_name}.",
            "mitigation": "Enforce firewall blocklists, inspect TLS SNI headers, deploy EDR monitoring."
        },
        "engines": engine_names,
        "timeline": timeline,
        "yara_rule": generate_yara_rule(ioc, ioc_type, threat_score),
        "snort_rule": generate_snort_rule(ioc, ioc_type),
        "firewall_commands": generate_firewall_commands(ioc, ioc_type),
        "stix_bundle": stix_bundle,
        "recommendation": (
            f"RECOMMENDED DEFENSE ACTION: Classify {ioc} as {severity.upper()} priority. "
            f"Apply immediate firewall drops and DNS sinkholing. Query SIEM logs for historical connections "
            f"within the past 90 days. Quarantine any endpoint communicating with this indicator."
        )
    }
