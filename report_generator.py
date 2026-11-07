import json
import csv
import io
from datetime import datetime, timedelta, timezone
import random

# India Standard Time (UTC+05:30)
IST = timezone(timedelta(hours=5, minutes=30), name="IST")


class ReportGenerator:
    """
    Enterprise Threat Intelligence & Incident Report Generator.
    Supports Executive Summaries, SOC Handover Reports, and Threat Bulletins.
    """

    @staticmethod
    def generate_executive_report():
        now = datetime.now(IST)
        report_id = f"CTICD-EXEC-{now.strftime('%Y%m')}-{random.randint(1000, 9999)}"

        return {
            "report_id": report_id,
            "title": "Executive Threat Intelligence & Cyber Posture Briefing",
            "classification": "TLP:AMBER+STRICT",
            "generated_at": now.strftime("%d %B %Y %I:%M:%S %p IST"),
            "author": "CTICD Threat Intelligence Operations Center",
            "period": "Last 24 Hours (Rolling Window)",
            "overall_posture": "ELEVATED RISK - DEFCON 2",
            "risk_score": 86,
            "posture_trend": "Increasing (+12.4% vs prior period)",
            "metrics": {
                "total_threat_events": 48320,
                "correlated_incidents": 142,
                "critical_cves_active": 14,
                "ransomware_campaigns_tracked": 6,
                "active_adversaries": 8,
                "blocked_ip_ranges": 9460,
                "ioc_matches": 25040
            },
            "executive_summary": (
                "During the observed cycle, CTICD correlation identified elevated offensive cyber campaigns "
                "primarily originating from state-sponsored entities (Volt Typhoon, APT29) and extortion syndicates (LockBit 3.0). "
                "A significant spike in exploitation attempts targeting perimeter edge appliances (CVE-2024-21887, CVE-2024-3400) "
                "was detected across critical infrastructure, financial, and healthcare assets. "
                "Automated firewall mitigation prevented 98.4% of direct intrusion attempts, with remaining anomalous beacons "
                "isolated in quarantine."
            ),
            "threat_landscape_highlights": [
                {
                    "title": "Edge Appliance Weaponization",
                    "severity": "Critical",
                    "description": "Adversaries are bypassing multi-factor authentication by weaponizing VPN and firewall edge zero-days.",
                    "mitre": "T1190 - Exploit Public-Facing Application"
                },
                {
                    "title": "Living-Off-The-Land (LOTL) Stealth C2",
                    "severity": "Critical",
                    "description": "Volt Typhoon continues leveraging compromised SOHO routers and native Windows binaries (PowerShell, WMI) without dropping files.",
                    "mitre": "T1059.003 - Command and Scripting Interpreter"
                },
                {
                    "title": "Ransomware Double-Extortion Pivot",
                    "severity": "High",
                    "description": "LockBit 3.0 affiliates are utilizing legitimate administrative utilities (ScreenConnect, AnyDesk) for initial foothold.",
                    "mitre": "T1219 - Remote Access Software"
                }
            ],
            "top_active_actors": [
                {"name": "Volt Typhoon", "origin": "China", "targets": "Critical Infrastructure, Energy", "risk": "Critical"},
                {"name": "APT29 (Cozy Bear)", "origin": "Russia", "targets": "Government, Diplomatic, Cloud", "risk": "Critical"},
                {"name": "LockBit 3.0", "origin": "Eastern Europe", "targets": "Manufacturing, Healthcare", "risk": "High"},
                {"name": "Lazarus Group", "origin": "North Korea", "targets": "Fintech, Crypto, Defense", "risk": "High"}
            ],
            "critical_vulnerabilities": [
                {"cve": "CVE-2024-3400", "product": "PAN-OS GlobalProtect", "cvss": 10.0, "cisa_kev": "YES", "patch_status": "Urgent Hotfix"},
                {"cve": "CVE-2024-21887", "product": "Ivanti Connect Secure", "cvss": 9.1, "cisa_kev": "YES", "patch_status": "Patched"},
                {"cve": "CVE-2024-3094", "product": "XZ Utils Backdoor", "cvss": 10.0, "cisa_kev": "YES", "patch_status": "Audited"},
                {"cve": "CVE-2023-34362", "product": "MOVEit Transfer SQLi", "cvss": 9.8, "cisa_kev": "YES", "patch_status": "Patched"}
            ],
            "strategic_recommendations": [
                "1. Enforce emergency patch cycle on all internet-exposed perimeter appliances within 24 hours.",
                "2. Restrict outbound egress on all critical server enclaves to authorized IP and DNS destinations only.",
                "3. Mandate FIDO2 hardware tokens for all privileged administrative accounts to thwart MFA fatigue.",
                "4. Continuously ingest CTICD automated YARA signatures and Snort IDS feeds into SIEM/EDR clusters.",
                "5. Conduct table-top exercises simulating double-extortion ransomware and compromised administrative credentials."
            ]
        }

    @staticmethod
    def export_csv_report(data):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Report ID", data.get("report_id")])
        writer.writerow(["Generated At", data.get("generated_at")])
        writer.writerow(["Classification", data.get("classification")])
        writer.writerow(["Risk Score", data.get("risk_score")])
        writer.writerow([])
        writer.writerow(["Metric", "Value"])
        for k, v in data.get("metrics", {}).items():
            writer.writerow([k, v])
        writer.writerow([])
        writer.writerow(["Active Threat Actors", "Origin", "Targeted Sectors", "Risk"])
        for actor in data.get("top_active_actors", []):
            writer.writerow([actor["name"], actor["origin"], actor["targets"], actor["risk"]])
        writer.writerow([])
        writer.writerow(["Critical CVE", "Product", "CVSS", "CISA KEV", "Patch Status"])
        for cve in data.get("critical_vulnerabilities", []):
            writer.writerow([cve["cve"], cve["product"], cve["cvss"], cve["cisa_kev"], cve["patch_status"]])
        return output.getvalue()
