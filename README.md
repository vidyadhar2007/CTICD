# Cyber Threat Intelligence Correlation Dashboard (CTICD)
### Enterprise Security Operations Center (SOC) & Threat Hunting Platform

![Version](https://img.shields.io/badge/version-2.5_Enterprise-0ea5e9.svg)
![Security Posture](https://img.shields.io/badge/DEFCON-2_Elevated-ef4444.svg)
![Framework](https://img.shields.io/badge/Framework-Flask_3.1-22c55e.svg)
![Classification](https://img.shields.io/badge/TLP-AMBER%2BSTRICT-f59e0b.svg)

---

## 🛡️ Overview

The **Cyber Threat Intelligence Correlation Dashboard (CTICD)** is an enterprise-grade CTI and SOC platform designed to ingest, enrich, correlate, and operationalize cyber threat intelligence across the entire intrusion lifecycle.

Built for Threat Hunters, SOC Tier 2/3 Analysts, and CISOs, CTICD links disparate indicators of compromise (IOCs) to adversary threat groups, weaponized CVE vulnerabilities, MITRE ATT&CK tactics & techniques, malware families, and targeted industry sectors.

---

## ⚡ Key Capabilities

### 1. 🌐 Real-Time Global Threat Map & Tactical Intercept Terminal
- **Live Ballistic Trajectory Engine**: Visualizes cyber attacks across 32 sovereign global hubs with MapLibre GL.
- **Accurate Real-Time Telemetry**: Millisecond UTC timestamps (`YYYY-MM-DD HH:MM:SS.mmm UTC`), exact source & target geographic coordinates (lat, lng), autonomous systems (ASNs), and named critical target infrastructure (e.g. JPMorgan SWIFT Node, Mayo Clinic EHR, PJM Power Grid).
- **Tactical Intercept Stream**: Auto-streaming terminal logging incoming events with interactive click-to-inspect dossiers.
- **Forensic Tactical Dossier Modal**: Click ANY stream event to inspect origin ASN, target sector, MITRE ATT&CK codes, weaponized CVE, raw packet hex dump, and 1-click perimeter firewall drop rules.
- **Tactical Audio Synthesizer**: Optional discrete Web Audio radar blip oscillator (muted by default, toggleable on the HUD).
- **Controls**: Pause/resume stream and category filters (C2 Beaconing, Ransomware, DDoS, Exploits).

### 2. 🕸️ Multi-Entity Intelligence Correlation Engine
- **Graph Link Analysis**: Interactive Vis.js topology linking Adversaries ➔ Capabilities ➔ Infrastructure ➔ Victims.
- **Diamond Model of Intrusion**: Adversary, Capability, Infrastructure, and Victim decomposition.
- **Cyber Kill Chain Progression**: Tracks stages from Reconnaissance to Actions on Objectives.
- **Automated Detection Engineering**: Generates production-ready **YARA rules**, **Snort / Suricata IDS signatures**, and **Sigma SIEM detection queries** with 1-click clipboard copy.
- **STIX 2.1 JSON Export**: Industry-standard threat intelligence export.

### 3. 🔍 OSINT IOC Search & Multi-Feed Enrichment
- **Automated Typing**: Detects IPv4, IPv6, Domains, URLs, CIDR blocks, MD5, SHA1, and SHA256 hashes.
- **Multi-Sensor Reputation Scoring**: Combines signals from VirusTotal, AbuseIPDB, Shodan, and AlienVault OTX.
- **Geolocation & ASN Telemetry**: Autonomous System numbers, ISPs, hosting profiles (Bulletproof, Tor Exit, VPS), and coordinates.
- **Perimeter Firewall Syntax**: Generates instant drop rules for Linux `iptables`, Cisco IOS ACLs, Palo Alto PAN-OS, and Windows Defender Firewall.

### 4. ⚠️ CVE Vulnerability & Exploit Intelligence
- **CVSS v3.1 Calculator**: Vector string decomposition (AV, AC, PR, UI, S, C, I, A).
- **CISA KEV Catalog Tracking**: Flags Known Exploited Vulnerabilities with mandatory federal remediation deadlines.
- **EPSS Scoring**: Exploit Prediction Scoring System probability and percentile rankings.
- **Remediation Advisories**: Actionable patch guidance, workarounds, and perimeter Snort detection signatures.

### 5. 🔬 Malware Static & Dynamic Sandbox Analysis
- **PE Section Dissection**: Computes section entropy (.text, .rdata, .data, .rsrc); detects packing and UPX obfuscation.
- **Dynamic Behavioral Profile**: Identifies suspicious Win32 APIs, dropped files, registry persistence keys, and mutexes.
- **Simulated Process Execution Tree**: Visualizes parent-child process execution flow.
- **12-Vendor Antivirus Matrix**: Detailed detections from CrowdStrike, Microsoft Defender, SentinelOne, Kaspersky, Bitdefender, and Sophos.

### 6. 🚨 SOC Alert Center & Incident Workflow
- **Active Incident Triage**: Queue management for Critical, High, Medium, and Low security incidents.
- **Lifecycle Status Updates**: Move incidents seamlessly between `New` ➔ `Investigating` ➔ `Contained` ➔ `Resolved` ➔ `False Positive`.
- **Analyst Audit Logs**: Attach timestamped investigation findings and lead analyst assignment.

### 7. 📄 Executive CTI Briefings & Reporting
- **CISO Strategic Summaries**: Executive risk matrix, posture trends, and key threat landscape highlights.
- **TLP 2.0 Classifications**: Standardized TLP:AMBER, TLP:CLEAR, and TLP:RED tags.
- **Multi-Format Exports**: 1-click **Print / PDF export**, **STIX 2.1 JSON**, and **CSV reports**.

### 8. 🔎 Unified Global Threat Search
- Universal search bar in the top navigation header automatically parses and dispatches queries (e.g. `185.220.101.45`, `CVE-2024-3094`, `Volt Typhoon`, `LockBit`) to the appropriate intelligence engine.

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- Modern Web Browser (Chrome, Firefox, Edge, Safari)

### Installation

1. **Navigate to the Project Directory**:
   ```bash
   cd "d:\CyberThreat Intelligence Correlation Dashboard (CTICD)"
   ```

2. **Activate the Virtual Environment**:
   - Windows PowerShell:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - Windows CMD:
     ```cmd
     .\venv\Scripts\activate.bat
     ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the CTICD Application**:
   ```bash
   python app.py
   ```

5. **Access the Web Dashboard**:
   Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## 🔑 Default Analyst Credentials

| Role | Email | Password | Clearance |
| :--- | :--- | :--- | :--- |
| **Lead Threat Hunter** | `analyst@cticd.soc` | `Analyst@2026` | SECRET // TLP:AMBER |

*(New analyst accounts can also be self-provisioned via the **Register Analyst** portal).*

---

## 📂 Project Architecture

```
CTICD/
├── app.py                      # Flask Application Controller & Route Endpoints
├── config.py                   # Enterprise SOC Configuration & API Settings
├── database.py                 # SQLAlchemy Data Models (User, SecurityAlert, ThreatLog, etc.)
├── report_generator.py         # Executive Briefing & Export Engine
├── threat_engine.py            # Central Query Dispatcher & Classifier
├── requirements.txt            # Python Dependencies
├── Procfile                    # Production Deployment Profile
├── data/
│   └── threat_data.csv         # Curated Threat Intelligence Benchmark Dataset
├── modules/
│   ├── correlation_engine.py   # Multi-Entity Graph Correlation & Diamond Model Engine
│   ├── cve_engine.py           # CVE, CVSS v3.1, EPSS, & CISA KEV Intelligence
│   ├── ioc_engine.py           # OSINT Enrichment & Firewall Rule Generator
│   ├── malware_engine.py       # PE Entropy, Sandbox Behavior, & YARA Engine
│   ├── report_engine.py        # Executive Summary & Metrics Provider
│   └── threat_feed.py          # Real-Time STIX/TAXII Feed Aggregator
├── services/
│   └── geoip_service.py        # Live Cyber Threat Map Geospatial Simulation
├── static/
│   ├── style.css               # Modern High-Contrast Cyber SOC Stylesheet
│   └── script.js               # Client-Side Telemetry, Clocks, MapLibre & Charts
└── templates/
    ├── base.html               # Master Layout (Sidebar, Topbar, Global Search, Clocks)
    ├── dashboard.html          # Operations Command Center Dashboard
    ├── threat_map.html         # Live Global Cyber Threat Telemetry Map
    ├── threat_feed.html        # Real-Time Threat Feed (STIX/TAXII)
    ├── correlation_engine.html # Interactive Vis.js Threat Relationship Graph
    ├── ioc_search.html         # OSINT IOC Scanner & Enrichment
    ├── cve_explorer.html       # CVE Vulnerability & Exploit Explorer
    ├── malware_analysis.html   # Malware Static & Dynamic Sandbox Analysis
    ├── alerts.html             # SOC Alert Center & Incident Triage
    ├── reports.html            # Executive Threat Intelligence Briefings
    ├── profile.html            # Analyst Identity & Security Profile
    ├── edit_profile.html       # Profile Editor
    ├── change_password.html    # Password Management
    ├── login.html              # Secure Analyst Authentication Portal
    └── signup.html             # Analyst Clearance Registration
```

---

## 🛡️ Security & Privacy Notice
- This platform operates in alignment with the **Traffic Light Protocol (TLP 2.0)**.
- Sensitive indicators marked `TLP:AMBER+STRICT` should not be disseminated outside authorized security operations groups.
