import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and draw total page count
    along with running header and running footer on pages > 1.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Cover page does not have running header/footer

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Running Top Header
        self.drawString(54, 11 * inch - 36, "CYBERTHREAT INTELLIGENCE CORRELATION DASHBOARD (CTICD)")
        self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "TLP:AMBER+STRICT | DEFCON 2 | IST")
        self.setStrokeColor(colors.HexColor("#0ea5e9"))
        self.setLineWidth(1)
        self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)

        # Running Bottom Footer
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 46, 8.5 * inch - 54, 46)
        self.drawString(54, 34, "CONFIDENTIAL — SOC OPERATIONS & THREAT DEFENSE CENTER")
        self.drawRightString(8.5 * inch - 54, 34, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    primary_color = colors.HexColor("#0f172a")     # Deep Slate Navy
    accent_cyan = colors.HexColor("#0ea5e9")       # Cyber Cyan
    accent_blue = colors.HexColor("#2563eb")       # Royal Blue
    danger_red = colors.HexColor("#ef4444")        # Crimson Alert
    warning_gold = colors.HexColor("#f59e0b")      # Amber
    success_green = colors.HexColor("#10b981")     # Emerald Green
    text_dark = colors.HexColor("#1e293b")         # Charcoal Body
    text_muted = colors.HexColor("#64748b")        # Slate Muted
    card_bg = colors.HexColor("#f8fafc")           # Light Gray Card
    border_color = colors.HexColor("#cbd5e1")      # Border Gray

    # Typography Styles
    title_style = ParagraphStyle(
        "CoverTitle",
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#0f172a"),
        alignment=0,
        spaceAfter=8
    )
    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0ea5e9"),
        alignment=0,
        spaceAfter=20
    )
    h1_style = ParagraphStyle(
        "Heading1_Custom",
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=primary_color,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        "Heading2_Custom",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=accent_blue,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        "Body_Custom",
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=text_dark,
        spaceAfter=6
    )
    body_bold = ParagraphStyle(
        "BodyBold_Custom",
        parent=body_style,
        fontName="Helvetica-Bold"
    )
    code_style = ParagraphStyle(
        "Code_Custom",
        fontName="Courier",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=4
    )
    table_cell = ParagraphStyle(
        "TableCell",
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=text_dark
    )
    table_header = ParagraphStyle(
        "TableHeader",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    story = []

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 20))
    # Top Classification Banner
    classification_data = [[
        Paragraph("<b>CLASSIFICATION: TLP:AMBER+STRICT</b>", ParagraphStyle("clf", fontName="Helvetica-Bold", fontSize=9, textColor=colors.white, alignment=1)),
        Paragraph("<b>DEFCON 2 (ELEVATED ALERT)</b>", ParagraphStyle("clf2", fontName="Helvetica-Bold", fontSize=9, textColor=colors.white, alignment=1)),
        Paragraph("<b>TIMEZONE: IST (UTC+05:30)</b>", ParagraphStyle("clf3", fontName="Helvetica-Bold", fontSize=9, textColor=colors.white, alignment=1))
    ]]
    clf_table = Table(classification_data, colWidths=[170, 170, 164])
    clf_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0f172a")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 0), (-1, -1), 2, accent_cyan)
    ]))
    story.append(clf_table)
    story.append(Spacer(1, 40))

    story.append(Paragraph("CYBERTHREAT INTELLIGENCE CORRELATION DASHBOARD (CTICD)", title_style))
    story.append(Paragraph("Comprehensive Technical Project & Engineering Architecture Report", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=accent_cyan, spaceAfter=20))

    # Meta Details Box
    meta_data = [
        [Paragraph("<b>Project Version:</b>", body_bold), Paragraph("v2.5 Enterprise Production", table_cell), Paragraph("<b>Target Environment:</b>", body_bold), Paragraph("Local / Cloud Serverless (Vercel)", table_cell)],
        [Paragraph("<b>Author / Lead Analyst:</b>", body_bold), Paragraph("Vidyadhar", table_cell), Paragraph("<b>Database Architecture:</b>", body_bold), Paragraph("SQLite / SQLAlchemy ORM (Writable /tmp)", table_cell)],
        [Paragraph("<b>Host Platform:</b>", body_bold), Paragraph("Python 3.13 / Flask 3.1", table_cell), Paragraph("<b>Standards Compliance:</b>", body_bold), Paragraph("STIX 2.1, TAXII, YARA, Snort, MITRE ATT&CK", table_cell)],
        [Paragraph("<b>Repository:</b>", body_bold), Paragraph("github.com/vidyadhar2007/CTICD", table_cell), Paragraph("<b>Report Generated:</b>", body_bold), Paragraph("November 2026 | Indian Standard Time", table_cell)]
    ]
    meta_table = Table(meta_data, colWidths=[130, 125, 125, 124])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), card_bg),
        ("BOX", (0, 0), (-1, -1), 1, border_color),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 25))

    # Executive Summary Card
    story.append(Paragraph("<b>EXECUTIVE SUMMARY</b>", h2_style))
    story.append(Paragraph(
        "The <b>CyberThreat Intelligence Correlation Dashboard (CTICD)</b> is an enterprise-grade, "
        "next-generation Security Operations Center (SOC) intelligence platform engineered to unify "
        "heterogeneous Open-Source Intelligence (OSINT), real-time sensor streams, and multi-entity graph "
        "correlation into a single operational interface. Modern enterprise defenders routinely face data fatigue "
        "caused by fragmented threat feeds, manual indicator extraction, and slow threat actor attribution. "
        "CTICD eliminates these bottlenecks by synthesizing <b>real-time ballistic origin-to-target attack trajectory "
        "telemetry</b>, automated <b>Diamond Model of Intrusion</b> graph correlation, <b>MITRE ATT&CK Enterprise Matrix "
        "heatmaps</b>, <b>PE binary entropy dissection</b>, and continuous <b>Snort / YARA / firewall drop rule generation</b>.",
        body_style
    ))
    story.append(Paragraph(
        "This project integrates client-side hardware-accelerated rendering (MapLibre GL, Vis.js Network, Web Audio "
        "radar synthesis) with a robust Python Flask backend, RESTful telemetry pipelines, and continuous deployment "
        "configured for both on-premise dedicated SOC servers and global Vercel serverless cloud runtimes. "
        "Every telemetry event and operational clock is synchronized to <b>Indian Standard Time (IST - UTC+05:30)</b>.",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # SECTION 1: ARCHITECTURE OVERVIEW
    # =========================================================================
    story.append(Paragraph("1. SYSTEM ARCHITECTURE & COMPONENT TOPOLOGY", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceAfter=10))

    story.append(Paragraph(
        "CTICD is structured into a modular, decoupled 4-tier architecture designed for low-latency ingestion, "
        "resilient correlation, and instantaneous threat intelligence presentation.",
        body_style
    ))

    arch_data = [
        [Paragraph("Tier / Layer", table_header), Paragraph("Core Technologies", table_header), Paragraph("Key Responsibilities & Capabilities", table_header)],
        [
            Paragraph("<b>Presentation & Tactical HUD</b>", table_cell),
            Paragraph("HTML5, Bootstrap 5.3, MapLibre GL 4.3, Vis.js, Chart.js, Web Audio API, CSS3 Glassmorphism", table_cell),
            Paragraph("Ballistic trajectory maps, Vis.js interactive correlation graph, real-time streaming attack terminal, Spotlight Command Palette (Ctrl+K), AI Copilot drawer, procedural audio radar synthesizer.", table_cell)
        ],
        [
            Paragraph("<b>Application & Intelligence</b>", table_cell),
            Paragraph("Python 3.13, Flask 3.1, Werkzeug, ThreatEngine, GeoIPService, IOCEngine, CVEEngine, MalwareEngine", table_cell),
            Paragraph("Multi-feed scoring algorithm (VT, AbuseIPDB, Shodan), Shannon entropy calculator, CVSS v3.1 vector parser, EPSS likelihood ranker, automated defense rule compiler (YARA, Snort, iptables).", table_cell)
        ],
        [
            Paragraph("<b>Data & Persistence</b>", table_cell),
            Paragraph("SQLite 3, SQLAlchemy 2.0 ORM, Flask-Login, CSV Ingestion Engine", table_cell),
            Paragraph("Relational persistence of analyst identities, security incidents, threat indicators, audit logs, and investigation case dossiers. Auto-recovering writable /tmp database for serverless environments.", table_cell)
        ],
        [
            Paragraph("<b>Deployment & Edge Cloud</b>", table_cell),
            Paragraph("Vercel Serverless Functions (@vercel/python), Gunicorn 26, GitHub CI/CD, Waitress", table_cell),
            Paragraph("Auto-build CI/CD via GitHub webhooks, Edge CDN caching for static bundles, isolated sub-second execution, zero-maintenance global availability.", table_cell)
        ]
    ]
    arch_table = Table(arch_data, colWidths=[120, 140, 244])
    arch_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), primary_color),
        ("BOX", (0, 0), (-1, -1), 1, border_color),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, card_bg])
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 2: CORE INTELLIGENCE ENGINES
    # =========================================================================
    story.append(Paragraph("2. CORE INTELLIGENCE ENGINES & TECHNICAL IMPLEMENTATION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceAfter=10))

    story.append(Paragraph("<b>2.1 Real-Time Geospatial Ballistic Threat Map</b>", h2_style))
    story.append(Paragraph(
        "Built on top of MapLibre GL vector tiles, the real-time ballistic map models origin-to-destination cyber attack "
        "trajectories connecting 32 sovereign strategic hubs across 6 continents. Trajectories are computed using great-circle "
        "quadratic Bezier curves with altitude jitter. Each attack event carries millisecond-accurate timestamps in <b>Indian Standard Time (IST)</b>, "
        "source IP, ASN, targeted critical asset (e.g. 5G Standalone UPF, SCADA breakers, SWIFT gateways), and forensic raw hex packet bytes. "
        "Analysts can filter vectors dynamically (Critical C2, RCE Exploits, DDoS Floods, Auth Bypasses).",
        body_style
    ))

    story.append(Paragraph("<b>2.2 Multi-Entity Correlation Engine (Vis.js & Diamond Model)</b>", h2_style))
    story.append(Paragraph(
        "The correlation engine maps complex, multi-stage intrusions across the <b>Diamond Model</b> (Adversary, Capability, "
        "Infrastructure, and Victim) and aligns nodes to the <b>Cyber Kill Chain</b> (Reconnaissance to Actions on Objectives). "
        "Using physics-based force-directed layouts via Vis.js Network, analysts can click and drag entities, inspect interconnected "
        "IPs, domains, hashes, and CVEs, and export automatically compiled detection signatures.",
        body_style
    ))

    story.append(Paragraph("<b>2.3 Multi-Feed IOC Search & OSINT Aggregator</b>", h2_style))
    story.append(Paragraph(
        "Accepts IPv4, IPv6, FQDNs, URLs, MD5, SHA1, and SHA256 indicators. Cross-references multi-vendor detection matrices "
        "(VirusTotal engine ratios, AbuseIPDB confidence percentiles, AlienVault OTX, Shodan open ports). Outputs exact "
        "perimeter mitigation commands across <b>Linux iptables</b>, <b>Cisco IOS</b>, <b>Palo Alto PAN-OS</b>, and <b>Windows Defender Firewall</b>, "
        "with 1-click export to <b>OASIS STIX 2.1 JSON</b> bundles.",
        body_style
    ))

    story.append(Paragraph("<b>2.4 CVE Vulnerability & Exploit Explorer</b>", h2_style))
    story.append(Paragraph(
        "Correlates CVE vulnerabilities (e.g. CVE-2024-3094 XZ Backdoor, CVE-2024-3400 PAN-OS RCE, CVE-2024-1709 ScreenConnect Bypass, "
        "CVE-2021-44228 Log4Shell) with CVSS v3.1 vector calculators, Exploit Prediction Scoring System (EPSS) percentiles, and "
        "CISA Known Exploited Vulnerability (KEV) catalog mandates. Automatically outputs Snort / Suricata network perimeter detection rules.",
        body_style
    ))

    story.append(Paragraph("<b>2.5 Malware Sandbox & PE Binary Entropy Dissector</b>", h2_style))
    story.append(Paragraph(
        "Calculates static Shannon entropy per Portable Executable (PE) section (.text, .rdata, .data, .rsrc). Sections with "
        "entropy exceeding 7.0 are flagged as packed or encrypted (UPX/Themida). Dissects dynamic behavioral telemetry including "
        "hooked Win32 APIs (VirtualAllocEx, WriteProcessMemory, CreateRemoteThread), registry run keys, mutexes, and 12-vendor antivirus detections.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 3: IMMERSIVE FEATURES & WAR ROOM DESIGN
    # =========================================================================
    story.append(Paragraph("3. IMMERSIVE SOC WAR ROOM & ANALYST PRODUCTIVITY SUITE", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceAfter=10))

    feature_data = [
        [Paragraph("Feature Module", table_header), Paragraph("Key Combination", table_header), Paragraph("Operational Functionality", table_header)],
        [
            Paragraph("<b>Spotlight Command Palette</b>", table_cell),
            Paragraph("<font face='Courier'>Ctrl + K</font> or <font face='Courier'>/</font>", table_cell),
            Paragraph("Keyboard-first overlay for instant global search across all engines, jumping to any page, detonating sample strains, and controlling dashboard modes without using the mouse.", table_cell)
        ],
        [
            Paragraph("<b>Interactive DEFCON Controller</b>", table_cell),
            Paragraph("Topbar Dropdown", table_cell),
            Paragraph("Live switcher between DEFCON 1 (Emergency alert with pulsing crimson screen vignette) down to DEFCON 5 (Normal defense). Synchronizes ambient lighting and sound sirens.", table_cell)
        ],
        [
            Paragraph("<b>Dynamic Theme Accents</b>", table_cell),
            Paragraph("Topbar Theme Menu", table_cell),
            Paragraph("Switches color themes instantly: Cyber Cyan, Crimson Bloodline, Matrix Emerald, and Cyberpunk Violet. Updates CSS variables dynamically and persists in localStorage.", table_cell)
        ],
        [
            Paragraph("<b>AI SOC Defense Copilot</b>", table_cell),
            Paragraph("<font face='Courier'>Alt + C</font> / Floating FAB", table_cell),
            Paragraph("Interactive AI analyst assistant slide-out drawer providing incident triage playbooks, threat actor profiling (APT29, Volt Typhoon), CVE briefings, and instant firewall drop rules.", table_cell)
        ],
        [
            Paragraph("<b>Enterprise MITRE ATT&CK Matrix</b>", table_cell),
            Paragraph("Dashboard Grid", table_cell),
            Paragraph("10-column interactive heatmap displaying real-time TTP density (Initial Access to Impact). Clicking any technique opens detection signatures and links to correlation graphs.", table_cell)
        ],
        [
            Paragraph("<b>Tactical Web Audio FX</b>", table_cell),
            Paragraph("<font face='Courier'>Alt + M</font>", table_cell),
            Paragraph("Procedural Web Audio API sound synthesizer producing tactile UI clicks, sonar radar chirps on missile intercepts, and two-tone sirens on DEFCON 1 alerts without external audio files.", table_cell)
        ],
        [
            Paragraph("<b>War Room HUD CRT Mode</b>", table_cell),
            Paragraph("<font face='Courier'>Alt + W</font>", table_cell),
            Paragraph("Overlays vintage CRT phosphor scanlines and tactical HUD corner brackets on cards for high-contrast war-room monitors and conference demonstrations.", table_cell)
        ],
        [
            Paragraph("<b>Keyboard Shortcut Cheat-Sheet</b>", table_cell),
            Paragraph("<font face='Courier'>?</font>", table_cell),
            Paragraph("Quick-reference modal displaying all two-key jump shortcuts (G+D for Dashboard, G+M for Map, G+F for Feed, G+I for IOC Search, G+C for Correlation).", table_cell)
        ]
    ]
    feat_table = Table(feature_data, colWidths=[130, 95, 279])
    feat_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), primary_color),
        ("BOX", (0, 0), (-1, -1), 1, border_color),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, card_bg])
    ]))
    story.append(feat_table)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 4: DATA MODELS & DATABASE SCHEMA
    # =========================================================================
    story.append(Paragraph("4. DATABASE PERSISTENCE & RELATIONAL ENTITY SCHEMA", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceAfter=10))

    db_data = [
        [Paragraph("Entity Model", table_header), Paragraph("Primary Fields & Types", table_header), Paragraph("Purpose & Business Logic", table_header)],
        [
            Paragraph("<b>User</b>", table_cell),
            Paragraph("id (PK), email, password_hash, name, role, department, badge_id, clearance_level, last_login", table_cell),
            Paragraph("SOC operator identity, role-based access control (Analyst, Threat Hunter, CISO), PBKDF2 password hashing.", table_cell)
        ],
        [
            Paragraph("<b>SecurityAlert</b>", table_cell),
            Paragraph("id (PK), title, severity, category, source_ip, target_ip, status, assigned_to, analyst_notes, created_at", table_cell),
            Paragraph("Operational SOC alert triage queue with state tracking (NEW, INVESTIGATING, CONTAINED, CLOSED).", table_cell)
        ],
        [
            Paragraph("<b>ThreatLog</b>", table_cell),
            Paragraph("id (PK), event_id, source_ip, destination_ip, protocol, threat_type, action_taken, signature, timestamp", table_cell),
            Paragraph("High-velocity telemetry event log recording perimeter drops, sensor intercepts, and traffic volume.", table_cell)
        ],
        [
            Paragraph("<b>ThreatIndicator</b>", table_cell),
            Paragraph("id (PK), indicator_value, indicator_type, threat_actor, confidence, tlp, first_seen, last_seen", table_cell),
            Paragraph("Curated indicator repository backing the STIX/TAXII feed, correlation engine, and OSINT lookup.", table_cell)
        ],
        [
            Paragraph("<b>InvestigationCase</b>", table_cell),
            Paragraph("id (PK), case_number, title, lead_investigator, status, mitre_ttp, priority, evidence_json", table_cell),
            Paragraph("Forensic case dossiers tracking incident response lifecycle and multi-indicator correlation graphs.", table_cell)
        ]
    ]
    db_table = Table(db_data, colWidths=[105, 165, 234])
    db_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), primary_color),
        ("BOX", (0, 0), (-1, -1), 1, border_color),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, card_bg])
    ]))
    story.append(db_table)
    story.append(PageBreak())

    # =========================================================================
    # SECTION 5: API CONTRACTS & TELEMETRY
    # =========================================================================
    story.append(Paragraph("5. API SPECIFICATIONS & TELEMETRY CONTRACTS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceAfter=10))

    api_data = [
        [Paragraph("Endpoint", table_header), Paragraph("HTTP Method", table_header), Paragraph("Authentication", table_header), Paragraph("Payload & Response Description", table_header)],
        [
            Paragraph("<b>/api/live-attack</b>", code_style),
            Paragraph("GET", table_cell),
            Paragraph("Session Required", table_cell),
            Paragraph("Returns real-time attack telemetry event with IST timestamp, source/target geo coordinates, MITRE codes, and hex byte preview.", table_cell)
        ],
        [
            Paragraph("<b>/api/live-attacks-batch</b>", code_style),
            Paragraph("GET", table_cell),
            Paragraph("Session Required", table_cell),
            Paragraph("Returns batch of N (default 8, max 25) real-time events for instant map and terminal initial seeding.", table_cell)
        ],
        [
            Paragraph("<b>/global-search?q=...</b>", code_style),
            Paragraph("GET", table_cell),
            Paragraph("Session Required", table_cell),
            Paragraph("Smart query classification dispatcher routing IPs/Domains to IOC Search, CVEs to CVE Explorer, and Actors to Correlation Engine.", table_cell)
        ],
        [
            Paragraph("<b>/api/alerts/&lt;id&gt;/status</b>", code_style),
            Paragraph("POST", table_cell),
            Paragraph("Session Required", table_cell),
            Paragraph("Updates security incident status, logs analyst note with timestamp, and assigns investigator.", table_cell)
        ],
        [
            Paragraph("<b>/api/export/stix</b>", code_style),
            Paragraph("POST", table_cell),
            Paragraph("Session Required", table_cell),
            Paragraph("Generates and returns an OASIS STIX 2.1 JSON bundle with attack-pattern and indicator objects.", table_cell)
        ],
        [
            Paragraph("<b>/export/report/json</b>", code_style),
            Paragraph("GET", table_cell),
            Paragraph("Session Required", table_cell),
            Paragraph("Exports full executive CISO briefing dataset in structured JSON format.", table_cell)
        ],
        [
            Paragraph("<b>/export/report/csv</b>", code_style),
            Paragraph("GET", table_cell),
            Paragraph("Session Required", table_cell),
            Paragraph("Streams raw threat feed records as downloadable comma-separated values (CSV).", table_cell)
        ]
    ]
    api_table = Table(api_data, colWidths=[130, 65, 85, 224])
    api_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), primary_color),
        ("BOX", (0, 0), (-1, -1), 1, border_color),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, card_bg])
    ]))
    story.append(api_table)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 6: VERCEL DEPLOYMENT & SERVERLESS ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("6. SERVERLESS CLOUD DEPLOYMENT & CI/CD PIPELINE", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceAfter=10))

    story.append(Paragraph(
        "Deploying Flask applications to serverless runtimes like Vercel introduces unique challenges, specifically "
        "the <b>read-only root filesystem</b> (`/var/task`) and request routing. CTICD solves this with zero external "
        "dependencies through two dedicated configuration files:",
        body_style
    ))

    story.append(Paragraph("<b>1. Serverless Routing Configuration (<font face='Courier'>vercel.json</font>):</b>", h2_style))
    story.append(Paragraph(
        "Directs Vercel to use the <font face='Courier'>@vercel/python</font> builder, serves static assets (<font face='Courier'>/static/*</font>) "
        "directly via Vercel's global Edge CDN, and routes dynamic requests through the WSGI gateway.",
        body_style
    ))

    story.append(Paragraph("<b>2. Serverless WSGI Entrypoint (<font face='Courier'>api/index.py</font>):</b>", h2_style))
    story.append(Paragraph(
        "Ensures project root directories are in the system path and exports the Flask <font face='Courier'>app</font> instance "
        "as the callable serverless handler.",
        body_style
    ))

    story.append(Paragraph("<b>3. Self-Healing SQLite /tmp Adaptation (<font face='Courier'>config.py</font>):</b>", h2_style))
    story.append(Paragraph(
        "Detects the <font face='Courier'>VERCEL=1</font> environment flag at runtime. If running on Vercel, it copies the "
        "seeded SQLite database (<font face='Courier'>instance/cticd.db</font>) into <font face='Courier'>/tmp/cticd.db</font>, "
        "the only writable filesystem location on AWS Lambda/Vercel serverless containers. This ensures user logins, session cookies, "
        "and alert status mutations function without read-only filesystem crashes.",
        body_style
    ))

    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 7: SECURITY & COMPLIANCE
    # =========================================================================
    story.append(Paragraph("7. SECURITY, GOVERNANCE & COMPLIANCE CONTROLS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceAfter=10))

    story.append(Paragraph(
        "• <b>Authentication Hardening:</b> Passwords hashed using PBKDF2 with SHA-256 and unique per-user salts. Session cookies protected with <font face='Courier'>HttpOnly</font> and <font face='Courier'>SameSite=Lax</font> flags.<br/>"
        "• <b>Injection Defense:</b> All database queries execute via SQLAlchemy parameterized ORM objects, eliminating SQL injection vectors. All user inputs are strictly sanitized and cast.<br/>"
        "• <b>Traffic Light Protocol (TLP 2.0):</b> Curated threat indicators are tagged with standardized TLP markings (TLP:CLEAR, TLP:GREEN, TLP:AMBER, TLP:AMBER+STRICT, TLP:RED).<br/>"
        "• <b>STIX 2.1 & TAXII Standards:</b> Exporter serializes indicator bundles conformant to OASIS CTI technical committee specifications.",
        body_style
    ))

    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 8: CONCLUSION
    # =========================================================================
    story.append(Paragraph("8. CONCLUSION & FUTURE ROADMAP", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceAfter=10))

    story.append(Paragraph(
        "CTICD v2.5 delivers a high-impact, production-ready cyber threat intelligence and operations command platform. "
        "By fusing millisecond-precision geospatial trajectory modeling, Diamond Model intrusion graph analysis, PE entropy binary dissection, "
        "and automated defense synthesis into a unified interface, CTICD reduces analyst Mean Time to Detect (MTTD) and Mean Time to Respond (MTTR).",
        body_style
    ))
    story.append(Paragraph(
        "<b>Future Strategic Enhancements:</b><br/>"
        "1. Distributed real-time event streaming via Apache Kafka or Redis Pub/Sub for millions of events per second.<br/>"
        "2. Bi-directional SIEM connectors for automatic alert ingestion from Splunk, Elastic Security, and Microsoft Sentinel.<br/>"
        "3. Automated SOAR containment integrations triggerable directly from the AI Defense Copilot.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully built: {filename}")


if __name__ == "__main__":
    out_pdf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CTICD_Project_Report.pdf")
    build_pdf(out_pdf)
