"""
CTICD Central Threat Intelligence Engine (CTIE).
Unified orchestration gateway dispatching queries to specialized engines:
- IOC Detection & Multi-Feed OSINT
- CVE & Vulnerability Intelligence
- Malware Static & Dynamic Behavioral Analysis
- Threat Actor & TTP Correlation
"""

from modules.ioc_engine import analyze_ioc, detect_ioc_type
from modules.cve_engine import analyze_cve, normalize_cve
from modules.malware_engine import analyze_malware_hash, normalize_hash
from modules.correlation_engine import correlate_indicator, ACTOR_PROFILES


class ThreatEngine:
    @staticmethod
    def classify_and_analyze(query):
        query = query.strip()
        if not query:
            return None

        # 1. Check if it's a CVE
        if normalize_cve(query):
            cve_result = analyze_cve(query)
            return {
                "type": "CVE Vulnerability",
                "target_route": "cve_explorer",
                "param_name": "cve",
                "data": cve_result,
                "summary": f"{cve_result.get('cve_id')}: {cve_result.get('title')} (CVSS {cve_result.get('cvss')} {cve_result.get('severity')})"
            }

        # 2. Check if it's a file hash
        hash_type, normalized_hash = normalize_hash(query)
        if len(query) in [32, 40, 64] and all(c in "0123456789abcdefABCDEF" for c in query):
            malware_result = analyze_malware_hash(query)
            return {
                "type": "Malware Sample Hash",
                "target_route": "malware_analysis",
                "param_name": "file_hash",
                "data": malware_result,
                "summary": f"{malware_result.get('malware_family')} - Score {malware_result.get('threat_score')}/100 ({malware_result.get('severity')})"
            }

        # 3. Check if it's a known threat actor
        for actor_name in ACTOR_PROFILES.keys():
            if actor_name.lower() in query.lower():
                corr_result = correlate_indicator(actor_name)
                return {
                    "type": "Threat Actor",
                    "target_route": "correlation_engine",
                    "param_name": "indicator",
                    "data": corr_result,
                    "summary": f"Threat Actor: {corr_result.get('actor')} ({corr_result.get('actor_origin')}) - Primary Malware: {corr_result.get('malware')}"
                }

        # 4. Standard IOC (IP, Domain, URL)
        ioc_type = detect_ioc_type(query)
        if ioc_type in ["IP Address", "Domain", "URL", "IPv6 Address", "CIDR Network"]:
            ioc_result = analyze_ioc(query)
            return {
                "type": ioc_type,
                "target_route": "ioc_search",
                "param_name": "ioc",
                "data": ioc_result,
                "summary": f"{ioc_type}: {ioc_result.get('ioc')} - Threat Score {ioc_result.get('threat_score')}/100 ({ioc_result.get('severity')})"
            }

        # Default fallback to correlation
        corr_result = correlate_indicator(query)
        return {
            "type": "Correlated Intelligence",
            "target_route": "correlation_engine",
            "param_name": "indicator",
            "data": corr_result,
            "summary": f"Correlated with {corr_result.get('actor')} / {corr_result.get('malware')} ({corr_result.get('severity')})"
        }
