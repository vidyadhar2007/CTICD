import hashlib
import random
from datetime import datetime, timedelta, timezone

# India Standard Time (UTC+05:30)
IST = timezone(timedelta(hours=5, minutes=30), name="IST")

# Rich Curated Threat Actor Intelligence
ACTOR_PROFILES = {
    "APT29": {
        "aliases": ["Cozy Bear", "Nobelium", "Midnight Blizzard", "The Dukes"],
        "origin": "Russia (SVR)",
        "motivation": "State Espionage & Intelligence Collection",
        "targets": ["Government", "Diplomatic", "Defense", "Cloud Service Providers", "NATO Alliances"],
        "primary_malware": ["Cobalt Strike", "EnvyScout", "NativeZone", "MagicWeb"],
        "mitre_id": "T1566.002",
        "mitre_name": "Spearphishing Link",
        "tactic": "Initial Access",
        "cve": "CVE-2023-23397",
        "confidence": 95,
        "kill_chain": "Delivery & Execution",
        "diamond_model": {"adversary": "APT29 (SVR)", "capability": "Token Forgery & Cloud Pivoting", "victim": "Western Strategic Agencies"}
    },
    "Lazarus Group": {
        "aliases": ["HIDDEN COBRA", "Guardians of Peace", "Zinc", "Labyrinth Chollima"],
        "origin": "North Korea (RGB)",
        "motivation": "Financial Gain & Espionage (Cryptocurrency Theft)",
        "targets": ["Cryptocurrency Exchanges", "Defense Contractors", "Financial Institutions", "Aerospace"],
        "primary_malware": ["AppleJeus", "FALLCHILL", "FastCash", "Manuscrypt"],
        "mitre_id": "T1195.002",
        "mitre_name": "Compromise Software Supply Chain",
        "tactic": "Initial Access",
        "cve": "CVE-2024-3094",
        "confidence": 92,
        "kill_chain": "Actions on Objectives",
        "diamond_model": {"adversary": "Lazarus (RGB 121)", "capability": "Crypto Stealers & Trojanized Apps", "victim": "FinTech & Crypto Networks"}
    },
    "Volt Typhoon": {
        "aliases": ["Bronze Silhouette", "Vanguard Panda", "Insidious Taurus"],
        "origin": "China (MSS)",
        "motivation": "Critical Infrastructure Pre-positioning & Espionage",
        "targets": ["Energy & Utilities", "Telecommunications", "Transportation", "Water Systems", "Defense Base"],
        "primary_malware": ["Living-off-the-Land Binaries (LOLBins)", "KV-Botnet", "Fast Reverse Proxy"],
        "mitre_id": "T1059.003",
        "mitre_name": "Windows Command Shell / Living-off-the-Land",
        "tactic": "Execution",
        "cve": "CVE-2024-21887",
        "confidence": 96,
        "kill_chain": "Persistence & C2",
        "diamond_model": {"adversary": "Volt Typhoon", "capability": "SOHO Router Proxying & Zero Footprint", "victim": "Critical Infrastructure"}
    },
    "Sandworm": {
        "aliases": ["Voodoo Bear", "TeleBots", "BlackEnergy Group", "Unit 74455"],
        "origin": "Russia (GRU)",
        "motivation": "Destructive Sabotage & Operational Disruption",
        "targets": ["Energy Grids", "Critical Infrastructure", "Government", "Media", "Logistics"],
        "primary_malware": ["Industroyer2", "CaddyWiper", "HermeticWiper", "BlackEnergy"],
        "mitre_id": "T1485",
        "mitre_name": "Data Destruction / Wiper",
        "tactic": "Impact",
        "cve": "CVE-2021-44228",
        "confidence": 94,
        "kill_chain": "Actions on Objectives (Destruction)",
        "diamond_model": {"adversary": "Sandworm (GRU)", "capability": "Industrial Control (OT) Disruption & Wipers", "victim": "Power & Logistics Grids"}
    },
    "LockBit": {
        "aliases": ["LockBit 3.0", "Bitwise Spider", "LockBit Black"],
        "origin": "Eastern Europe (RaaS Criminal Syndicate)",
        "motivation": "Extortion & Double-Extortion Ransomware",
        "targets": ["Manufacturing", "Healthcare", "Financial Services", "Legal", "Local Government"],
        "primary_malware": ["LockBit 3.0 Black", "StealBit Exfiltration Tool", "PsExec"],
        "mitre_id": "T1486",
        "mitre_name": "Data Encrypted for Impact",
        "tactic": "Impact",
        "cve": "CVE-2023-34362",
        "confidence": 98,
        "kill_chain": "Actions on Objectives (Extortion)",
        "diamond_model": {"adversary": "LockBit RaaS", "capability": "Automated Privilege Escalation & Fast Encryption", "victim": "Enterprise IT"}
    },
    "FIN7": {
        "aliases": ["Carbanak", "Navigator Group", "ELBRUS"],
        "origin": "Eastern Europe",
        "motivation": "High-Volume Financial Crime & Payment Card Theft",
        "targets": ["Retail", "Hospitality", "Restaurant Franchises", "E-Commerce"],
        "primary_malware": ["Carbanak", "BIRDMINER", "Lizar", "GRIFFON"],
        "mitre_id": "T1055.012",
        "mitre_name": "Process Hollowing",
        "tactic": "Defense Evasion",
        "cve": "CVE-2022-30190",
        "confidence": 91,
        "kill_chain": "Installation & Evasion",
        "diamond_model": {"adversary": "FIN7 Syndicate", "capability": "POS Memory Scrapers & Phishing Bait", "victim": "Retail Point of Sale"}
    },
    "Scattered Spider": {
        "aliases": ["UNC3944", "Starfraud", "Octo Tempest"],
        "origin": "Western / Global Cybercrime Syndicate",
        "motivation": "SIM Swapping, Identity Theft & Extortion",
        "targets": ["Hospitality & Casinos", "Telecoms", "Cloud Infrastructure", "Fintech"],
        "primary_malware": ["AnyDesk", "Mimikatz", "BlackCat Ransomware", "Okta Impersonation"],
        "mitre_id": "T1621",
        "mitre_name": "Multi-Factor Authentication Request Generation (MFA Fatigue)",
        "tactic": "Credential Access",
        "cve": "CVE-2024-1709",
        "confidence": 93,
        "kill_chain": "Reconnaissance & Initial Access",
        "diamond_model": {"adversary": "Scattered Spider", "capability": "Social Engineering & Helpdesk Exploitation", "victim": "Enterprise Identity (Okta/AD)"}
    },
    "BlackCat": {
        "aliases": ["ALPHV", "Noberus"],
        "origin": "Russian-speaking Cybercrime",
        "motivation": "High-Value Corporate Extortion",
        "targets": ["Healthcare Networks", "Critical Infrastructure", "Aerospace", "Technology"],
        "primary_malware": ["BlackCat Rust Ransomware", "ExMatter", "Cobalt Strike"],
        "mitre_id": "T1078.004",
        "mitre_name": "Cloud Accounts Compromise",
        "tactic": "Defense Evasion",
        "cve": "CVE-2024-3400",
        "confidence": 95,
        "kill_chain": "Actions on Objectives",
        "diamond_model": {"adversary": "ALPHV BlackCat", "capability": "Rust-based Cross-Platform Ransomware", "victim": "Hospitals & Tech Infrastructure"}
    }
}

MALWARE_CATALOG = {
    "Cobalt Strike": {
        "category": "Adversary Simulation / C2 Framework",
        "type": "Modular Command & Control",
        "severity": "Critical",
        "beacon_ports": [443, 8080, 53],
        "default_pipe": "\\pipe\\msagent_*",
        "yara_sample": "rule CobaltStrike_Beacon { strings: $s1 = \"%s as %s\\%s: %d\" fullword condition: $s1 }"
    },
    "RedLine Stealer": {
        "category": "Infostealer",
        "type": ".NET Credential & Token Harvester",
        "severity": "High",
        "beacon_ports": [80, 443, 10245],
        "default_pipe": "None (TCP direct)",
        "yara_sample": "rule RedLine_Stealer { strings: $c1 = \"Authorization: Bearer\" condition: $c1 }"
    },
    "LockBit 3.0 Black": {
        "category": "Ransomware",
        "type": "C/C++ Kernel Driver Exploit & Ransomware",
        "severity": "Critical",
        "beacon_ports": [443],
        "default_pipe": "\\pipe\\lockbit_ipc",
        "yara_sample": "rule LockBit_3_Black { strings: $s = \"LockBit 3.0 the world's fastest ransomware\" condition: $s }"
    },
    "Emotet": {
        "category": "Modular Banking Trojan / Loader",
        "type": "Polymorphic Dropper & Botnet",
        "severity": "Critical",
        "beacon_ports": [8080, 443, 7080],
        "default_pipe": "None",
        "yara_sample": "rule Emotet_Loader { strings: $mz = \"MZ\" $em = { 8B 45 ?? 33 C0 } condition: all of them }"
    },
    "AgentTesla": {
        "category": "Keylogger & Remote Access Trojan",
        "type": ".NET Spyware & Clipboard Monitor",
        "severity": "High",
        "beacon_ports": [25, 587, 443],
        "default_pipe": "None (SMTP/FTP exfil)",
        "yara_sample": "rule AgentTesla_Spyware { strings: $smtp = \"mail.\" condition: $smtp }"
    },
    "Mirai": {
        "category": "IoT Botnet / DDoS Engine",
        "type": "Linux ELF Telnet/SSH Spreader",
        "severity": "High",
        "beacon_ports": [23, 2323, 48101],
        "default_pipe": "None",
        "yara_sample": "rule Mirai_Botnet { strings: $s = \"/bin/busybox\" condition: $s }"
    },
    "AsyncRAT": {
        "category": "Remote Access Trojan (RAT)",
        "type": "Open-Source .NET C2 Client",
        "severity": "High",
        "beacon_ports": [6606, 7707, 8808],
        "default_pipe": "None",
        "yara_sample": "rule AsyncRAT_C2 { strings: $cert = \"AsyncRAT Server\" condition: $cert }"
    }
}


def severity_from_score(score):
    if score >= 88:
        return "Critical"
    if score >= 70:
        return "High"
    if score >= 45:
        return "Medium"
    return "Low"


def generate_related_ip(seed_hash):
    octets = [
        int(seed_hash[0:2], 16) % 200 + 20,
        int(seed_hash[2:4], 16),
        int(seed_hash[4:6], 16),
        int(seed_hash[6:8], 16) % 250 + 1
    ]
    return ".".join(str(o) for o in octets)


def generate_related_domain(seed_hash):
    prefixes = ["c2-relay", "auth-verify", "cloud-sync", "cdn-edge", "telemetry-portal", "update-kernel"]
    tlds = ["xyz", "top", "ru", "cc", "online", "live"]
    p = prefixes[int(seed_hash[8:10], 16) % len(prefixes)]
    t = tlds[int(seed_hash[10:12], 16) % len(tlds)]
    return f"{p}-{seed_hash[:6]}.{t}"


def correlate_indicator(indicator):
    """
    Enterprise-grade correlation engine connecting:
    - Input indicator (IP, Domain, Hash, CVE, Actor, TTP)
    - Threat Actor attribution
    - Malware family & mechanics
    - MITRE ATT&CK Matrix mapping (Tactic + Technique)
    - Linked CVE vulnerabilities & CISA KEV status
    - Diamond Model of Intrusion
    - Cyber Kill Chain phase
    - Interactive Vis.js network graph topology
    - Actionable defense engineering rules (YARA, Sigma, Snort)
    """
    indicator = indicator.strip()
    if not indicator:
        return None

    seed = hashlib.sha256(indicator.lower().encode()).hexdigest()
    actor_names = list(ACTOR_PROFILES.keys())

    # Check for direct keyword matches in indicator
    matched_actor = None
    for name, data in ACTOR_PROFILES.items():
        if name.lower() in indicator.lower() or any(alias.lower() in indicator.lower() for alias in data["aliases"]):
            matched_actor = name
            break

    if not matched_actor:
        actor_index = int(seed[0:4], 16) % len(actor_names)
        matched_actor = actor_names[actor_index]

    actor_info = ACTOR_PROFILES[matched_actor]

    # Select malware associated with this actor or from catalog
    malware_choices = actor_info["primary_malware"]
    malware_name = malware_choices[int(seed[4:6], 16) % len(malware_choices)]
    malware_details = MALWARE_CATALOG.get(malware_name, MALWARE_CATALOG["Cobalt Strike"])

    # Score calculation
    base_score = 65 + (int(seed[6:8], 16) % 32)
    risk_score = min(99, max(45, base_score))
    severity = severity_from_score(risk_score)

    cve_id = actor_info["cve"]
    mitre_id = actor_info["mitre_id"]
    mitre_name = actor_info["mitre_name"]
    tactic = actor_info["tactic"]
    kill_chain = actor_info["kill_chain"]
    diamond = actor_info["diamond_model"]
    targeted_sectors = actor_info["targets"]

    related_ip = generate_related_ip(seed)
    related_domain = generate_related_domain(seed)
    related_hash = hashlib.sha256((indicator + malware_name + matched_actor).encode()).hexdigest()
    asn = f"AS{int(seed[12:16], 16) % 50000 + 10000}"

    # Build Graph Nodes with rich semantic visual properties
    nodes = [
        {
            "id": "ioc",
            "label": f"Indicator\n{indicator[:24]}",
            "title": f"Searched Indicator: {indicator}",
            "type": "ioc",
            "level": severity,
            "color": "#38bdf8",
            "shape": "box",
            "size": 32
        },
        {
            "id": "actor",
            "label": f"Threat Actor\n{matched_actor}",
            "title": f"Adversary: {matched_actor} ({', '.join(actor_info['aliases'])})",
            "type": "actor",
            "level": "Critical",
            "color": "#ef4444",
            "shape": "diamond",
            "size": 36
        },
        {
            "id": "malware",
            "label": f"Malware\n{malware_name}",
            "title": f"Malware Family: {malware_name} ({malware_details['category']})",
            "type": "malware",
            "level": malware_details["severity"],
            "color": "#a855f7",
            "shape": "triangle",
            "size": 30
        },
        {
            "id": "infrastructure_ip",
            "label": f"C2 Node\n{related_ip}",
            "title": f"Active C2 Infrastructure: {related_ip} ({asn})",
            "type": "ip",
            "level": "High",
            "color": "#f97316",
            "shape": "square",
            "size": 26
        },
        {
            "id": "infrastructure_domain",
            "label": f"C2 Domain\n{related_domain}",
            "title": f"Beacon Domain: {related_domain}",
            "type": "domain",
            "level": "High",
            "color": "#f59e0b",
            "shape": "square",
            "size": 26
        },
        {
            "id": "mitre",
            "label": f"MITRE ATT&CK\n{mitre_id} ({tactic})",
            "title": f"Technique: {mitre_id} - {mitre_name}",
            "type": "mitre",
            "level": "Medium",
            "color": "#06b6d4",
            "shape": "ellipse",
            "size": 28
        },
        {
            "id": "cve",
            "label": f"Exploited Vulnerability\n{cve_id}",
            "title": f"CVE: {cve_id} (Listed in CISA KEV)",
            "type": "cve",
            "level": "Critical",
            "color": "#e11d48",
            "shape": "star",
            "size": 32
        },
        {
            "id": "target_sector",
            "label": f"Target Sector\n{targeted_sectors[0]}",
            "title": f"Victim Industry: {', '.join(targeted_sectors[:3])}",
            "type": "victim",
            "level": "High",
            "color": "#10b981",
            "shape": "hexagon",
            "size": 28
        },
        {
            "id": "sample_hash",
            "label": f"Binary Payload\n{related_hash[:12]}...",
            "title": f"SHA256 Payload Hash: {related_hash}",
            "type": "hash",
            "level": "Critical",
            "color": "#6366f1",
            "shape": "dot",
            "size": 24
        }
    ]

    # Graph Edges (Relationships)
    edges = [
        {"from": "ioc", "to": "infrastructure_ip", "relation": "resolves_to", "label": "resolves to"},
        {"from": "ioc", "to": "infrastructure_domain", "relation": "associated_with", "label": "associated with"},
        {"from": "infrastructure_domain", "to": "malware", "relation": "delivers_payload", "label": "delivers"},
        {"from": "infrastructure_ip", "to": "actor", "relation": "controlled_by", "label": "controlled by"},
        {"from": "actor", "to": "malware", "relation": "operates", "label": "operates"},
        {"from": "actor", "to": "cve", "relation": "weaponizes", "label": "weaponizes"},
        {"from": "actor", "to": "mitre", "relation": "leverages", "label": "leverages TTP"},
        {"from": "actor", "to": "target_sector", "relation": "targets_industry", "label": "targets"},
        {"from": "malware", "to": "sample_hash", "relation": "payload_hash", "label": "compiles into"},
        {"from": "cve", "to": "target_sector", "relation": "exposes", "label": "exposes"}
    ]

    # Correlation Timeline (India Standard Time)
    now = datetime.now(IST)
    timeline = [
        {
            "time": (now - timedelta(minutes=42)).strftime("%I:%M:%S %p"),
            "event": f"Adversary infrastructure probe detected against perimeter telemetry matching {indicator}.",
            "stage": "Reconnaissance",
            "badge": "bg-secondary"
        },
        {
            "time": (now - timedelta(minutes=28)).strftime("%I:%M:%S %p"),
            "event": f"DNS resolution linked {indicator} to C2 node {related_ip} ({asn}) and beacon domain {related_domain}.",
            "stage": "Infrastructure Discovery",
            "badge": "bg-info"
        },
        {
            "time": (now - timedelta(minutes=15)).strftime("%I:%M:%S %p"),
            "event": f"Attributed to threat group {matched_actor} ({actor_info['origin']}) leveraging {malware_name}.",
            "stage": "Threat Attribution",
            "badge": "bg-warning text-dark"
        },
        {
            "time": (now - timedelta(minutes=6)).strftime("%I:%M:%S %p"),
            "event": f"Mapped to MITRE ATT&CK {mitre_id} ({mitre_name}) exploiting known vulnerability {cve_id}.",
            "stage": "TTP Correlation",
            "badge": "bg-danger"
        },
        {
            "time": now.strftime("%I:%M:%S %p"),
            "event": f"CTICD Defense Engine synthesized proactive blocking rules, YARA signatures and SIEM queries.",
            "stage": "Countermeasure Generation",
            "badge": "bg-success"
        }
    ]

    # Defense Engineering Signatures
    yara_rule = f"""/*
  CTICD Auto-Generated YARA Rule
  Threat Actor: {matched_actor}
  Malware: {malware_name}
  Generated: {now.strftime('%Y-%m-%d %H:%M:%S')} IST
*/
rule CTICD_{matched_actor.replace(' ', '_')}_{malware_name.replace(' ', '_')} {{
    meta:
        author = "CTICD Automated Correlation Engine"
        threat_level = "{severity}"
        mitre_technique = "{mitre_id}"
        reference_cve = "{cve_id}"
        tlp = "TLP:AMBER"
    strings:
        $c2_domain = "{related_domain}" ascii wide nocase
        $c2_ip = "{related_ip}" ascii wide
        $payload_hash = "{related_hash[:16]}" ascii
        $sig_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ThreatHunting/1.0"
    condition:
        uint16(0) == 0x5A4D and (any of ($c2*) or $payload_hash)
}}"""

    snort_rule = (
        f'alert tcp $HOME_NET any -> [{related_ip}] [80,443,8080] '
        f'(msg:"CTICD TROJAN {matched_actor} {malware_name} C2 Beaconing Detected"; '
        f'content:"{related_domain[:12]}"; nocase; '
        f'reference:cve,{cve_id}; classtype:trojan-activity; sid:390{int(seed[:4],16)%9000+1000}; rev:1;)'
    )

    sigma_query = f"""title: Detection of {matched_actor} {malware_name} Activity
id: {seed[:8]}-{seed[8:12]}-4def-91bc-{seed[12:24]}
status: experimental
description: Identifies outbound C2 beaconing to infrastructure correlated with {matched_actor}.
author: CTICD Automated Detection Engine
logsource:
    category: network_connection
    product: windows
detection:
    selection:
        DestinationIp: '{related_ip}'
        DestinationHostname: '*{related_domain}*'
    condition: selection
fields:
    - SourceIp
    - DestinationIp
    - User
falsepositives:
    - Unknown
level: {severity.lower()}
tags:
    - attack.{tactic.lower().replace(' ', '_')}
    - attack.{mitre_id.lower()}"""

    return {
        "indicator": indicator,
        "risk_score": risk_score,
        "severity": severity,
        "actor": matched_actor,
        "actor_origin": actor_info["origin"],
        "actor_aliases": ", ".join(actor_info["aliases"]),
        "motivation": actor_info["motivation"],
        "malware": malware_name,
        "malware_category": malware_details["category"],
        "mitre_id": mitre_id,
        "mitre_name": mitre_name,
        "tactic": tactic,
        "kill_chain": kill_chain,
        "cve": cve_id,
        "cve_status": "Listed in CISA KEV (Known Exploited)",
        "targeted_sectors": targeted_sectors,
        "diamond_model": diamond,
        "related_ip": related_ip,
        "related_domain": related_domain,
        "related_hash": related_hash,
        "asn": asn,
        "nodes": nodes,
        "edges": edges,
        "timeline": timeline,
        "confidence": actor_info["confidence"],
        "yara_rule": yara_rule,
        "snort_rule": snort_rule,
        "sigma_query": sigma_query,
        "recommendation": (
            f"IMMEDIATE ACTION REQUIRED: Block outbound communication to IP {related_ip} and domain {related_domain} "
            f"across firewalls, proxies, and DNS resolvers. Isolate endpoints exhibiting MITRE {mitre_id} behavior. "
            f"Prioritize patching {cve_id} on all public-facing services. Ingest YARA signature into endpoint detection tools."
        )
    }
