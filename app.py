import os
import json
from io import BytesIO
from datetime import datetime, timedelta, timezone

# India Standard Time (IST)
IST = timezone(timedelta(hours=5, minutes=30), name="IST")

from flask import (
    Flask, render_template, request, redirect, url_for, flash,
    jsonify, send_file, session
)
from flask_login import (
    LoginManager, login_user, logout_user, login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from database import db, User, ThreatLog, SecurityAlert, ThreatIndicator, InvestigationCase

from services.geoip_service import generate_live_attack, get_live_threat_telemetry_batch
from modules.ioc_engine import analyze_ioc
from modules.threat_feed import generate_threat_feed, get_feed_stats
from modules.cve_engine import analyze_cve
from modules.malware_engine import analyze_malware_hash
from modules.correlation_engine import correlate_indicator
from modules.report_engine import generate_report_data
from report_generator import ReportGenerator
from threat_engine import ThreatEngine

app = Flask(__name__)
app.config.from_object(Config)

try:
    if not os.getenv("VERCEL"):
        os.makedirs(os.path.join(app.root_path, "instance"), exist_ok=True)
except Exception:
    pass
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message_category = "warning"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def seed_database_defaults():
    """Seeds default analyst and initial active security alerts if empty."""
    # Seed default user if no users exist
    if not User.query.first():
        default_analyst = User(
            name="Alex Mercer",
            email="analyst@cticd.soc",
            password=generate_password_hash("Analyst@2026"),
            role="Lead Threat Hunter",
            department="Cyber Threat Intelligence Operations",
            mobile="+1 (555) 019-2831",
            badge_id="CTICD-ALPHA-01"
        )
        db.session.add(default_analyst)
        db.session.commit()

    # Seed default alerts if empty
    if not SecurityAlert.query.first():
        now = datetime.utcnow()
        default_alerts = [
            SecurityAlert(
                alert_id="ALR-2026-9041",
                title="Cobalt Strike C2 Beaconing to Suspicious Foreign IP",
                severity="critical",
                category="Command and Control",
                source_ip="185.220.101.45",
                target_ip="10.0.12.84",
                source_country="Russia",
                target_country="United States",
                mitre_id="T1071.001",
                mitre_name="Application Layer Protocol: Web Protocols",
                mitre_tactic="Command and Control",
                status="Investigating",
                assigned_to="Alex Mercer",
                analyst_notes="Host exhibiting regular 60s jitter beacons matching Cobalt Strike malleable C2 profile.",
                created_at=now - timedelta(minutes=14)
            ),
            SecurityAlert(
                alert_id="ALR-2026-9042",
                title="Exploitation Attempt of Edge VPN (CVE-2024-21887)",
                severity="critical",
                category="Vulnerability Exploit",
                source_ip="45.144.227.55",
                target_ip="192.168.1.1",
                source_country="China",
                target_country="Germany",
                mitre_id="T1190",
                mitre_name="Exploit Public-Facing Application",
                mitre_tactic="Initial Access",
                status="New",
                assigned_to="Unassigned",
                analyst_notes="POST probe detected against Ivanti ICS REST API endpoint from untrusted ASN.",
                created_at=now - timedelta(minutes=28)
            ),
            SecurityAlert(
                alert_id="ALR-2026-9043",
                title="Distributed SSH & RDP Credential Stuffing Campaign",
                severity="high",
                category="Brute Force",
                source_ip="103.21.244.12",
                target_ip="10.0.4.15",
                source_country="India",
                target_country="United Kingdom",
                mitre_id="T1110.001",
                mitre_name="Password Guessing",
                mitre_tactic="Credential Access",
                status="New",
                assigned_to="Unassigned",
                analyst_notes="Over 400 failed authentication attempts within 3 minutes; threshold alert triggered.",
                created_at=now - timedelta(minutes=45)
            ),
            SecurityAlert(
                alert_id="ALR-2026-9044",
                title="Suspicious Data Exfiltration Pattern - Double Extension Archive",
                severity="high",
                category="Data Exfiltration",
                source_ip="10.0.8.22",
                target_ip="89.248.172.12",
                source_country="United States",
                target_country="Netherlands",
                mitre_id="T1048",
                mitre_name="Exfiltration Over Alternative Protocol",
                mitre_tactic="Exfiltration",
                status="Contained",
                assigned_to="Alex Mercer",
                analyst_notes="4.2 GB archive upload outbound to Tor exit node blocked by perimeter firewall.",
                created_at=now - timedelta(hours=2)
            ),
            SecurityAlert(
                alert_id="ALR-2026-9045",
                title="Web Application SQL Injection Probe on Authentication Endpoint",
                severity="medium",
                category="Web Attack",
                source_ip="177.105.12.8",
                target_ip="10.0.2.100",
                source_country="Brazil",
                target_country="Singapore",
                mitre_id="T1190",
                mitre_name="Exploit Public-Facing Application",
                mitre_tactic="Initial Access",
                status="Resolved",
                assigned_to="Alex Mercer",
                analyst_notes="Classic UNION SELECT probe sanitized by WAF; client IP throttled.",
                created_at=now - timedelta(hours=4)
            )
        ]
        for a in default_alerts:
            db.session.add(a)
        db.session.commit()


# ================= ROOT & AUTH =================

@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid analyst email or password. Access denied.", "danger")
            return redirect(url_for("login"))

        user.last_login = datetime.utcnow()
        db.session.commit()

        login_user(user)
        flash(f"Welcome back, {user.name}. CTICD Operations online.", "success")
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()
        role = request.form.get("role", "Security Analyst").strip()

        if not name or not email or not password:
            flash("All required analyst registration fields must be completed.", "danger")
            return redirect(url_for("signup"))

        if len(password) < 6:
            flash("Password must be at least 6 characters long for operational security.", "danger")
            return redirect(url_for("signup"))

        if User.query.filter_by(email=email).first():
            flash("Email already registered in CTICD identity directory. Please login.", "danger")
            return redirect(url_for("login"))

        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            role=role,
            department="Cyber Threat Intelligence Operations"
        )

        db.session.add(user)
        db.session.commit()

        flash("Analyst credential registered successfully. Please authenticate.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Session securely terminated. Operator logged out.", "success")
    return redirect(url_for("login"))


# ================= DASHBOARD & OPERATIONS =================

@app.route("/dashboard")
@login_required
def dashboard():
    stats = {
        "threat_level": "CRITICAL",
        "defcon": "DEFCON 2",
        "risk_score": 88,
        "live_attacks": 4210,
        "malicious_ips": 9461,
        "ioc_detected": 25040,
        "countries_attacked": 128,
        "active_feeds": 8,
        "total_feeds": 8
    }

    # Fetch alerts from database or fallback
    db_alerts = SecurityAlert.query.order_by(SecurityAlert.created_at.desc()).limit(5).all()
    recent_alerts = []
    for a in db_alerts:
        recent_alerts.append({
            "level": a.severity,
            "type": a.title,
            "from": a.source_country or "Unknown",
            "to": a.target_country or "Unknown",
            "time": a.created_at.strftime("%I:%M:%S %p"),
            "status": a.status
        })

    malicious_ips = [
        {"ip": "185.220.101.45", "country": "Russia", "asn": "AS205540", "hits": 842, "actor": "APT29"},
        {"ip": "45.144.227.55", "country": "China", "asn": "AS4134", "hits": 619, "actor": "Volt Typhoon"},
        {"ip": "103.21.244.12", "country": "India", "asn": "AS13335", "hits": 458, "actor": "Lazarus"},
        {"ip": "89.248.172.12", "country": "Germany", "asn": "AS3320", "hits": 391, "actor": "Sandworm"},
        {"ip": "194.26.29.112", "country": "Netherlands", "asn": "AS60729", "hits": 310, "actor": "LockBit"}
    ]

    initial_attacks = get_live_threat_telemetry_batch(6)

    return render_template(
        "dashboard.html",
        MAP_KEY=app.config.get("MAPTILER_API_KEY", ""),
        stats=stats,
        recent_alerts=recent_alerts,
        malicious_ips=malicious_ips,
        initial_attacks=initial_attacks
    )


@app.route("/threat-map")
@login_required
def threat_map():
    initial_attacks = get_live_threat_telemetry_batch(10)
    return render_template(
        "threat_map.html",
        MAP_KEY=app.config.get("MAPTILER_API_KEY", ""),
        initial_attacks=initial_attacks
    )


@app.route("/threat-feed", methods=["GET"])
@login_required
def threat_feed():
    feed = generate_threat_feed()
    stats = get_feed_stats(feed)

    return render_template(
        "threat_feed.html",
        title="Live Threat Feed",
        feed=feed,
        stats=stats,
        current_time=datetime.now(IST).strftime("%d %b %Y %H:%M:%S IST")
    )


@app.route("/api/live-attack")
@login_required
def api_live_attack():
    return jsonify(generate_live_attack())


@app.route("/api/live-attacks-batch")
@login_required
def api_live_attacks_batch():
    count = min(request.args.get("count", 8, type=int), 25)
    return jsonify(get_live_threat_telemetry_batch(count))


# ================= INTELLIGENCE ENGINES =================

@app.route("/ioc-search", methods=["GET", "POST"])
@login_required
def ioc_search():
    result = None
    query_ioc = request.args.get("ioc", "").strip()

    if request.method == "POST":
        query_ioc = request.form.get("ioc", "").strip()

    if query_ioc:
        result = analyze_ioc(query_ioc)
        if result:
            # Persist search to ThreatLog
            try:
                log_entry = ThreatLog(
                    ioc_value=result["ioc"],
                    ioc_type=result["ioc_type"],
                    threat_level=result["severity"],
                    threat_score=result["threat_score"],
                    country=result["geo"].get("country", "Unknown"),
                    malware_family=result.get("actor", "Unknown"),
                    attack_type=result["mitre"].get("name", "Unknown"),
                    recommendation=result.get("recommendation", "")
                )
                db.session.add(log_entry)
                db.session.commit()
            except Exception as e:
                db.session.rollback()

    return render_template("ioc_search.html", result=result, query_ioc=query_ioc)


@app.route("/correlation-engine", methods=["GET", "POST"])
@login_required
def correlation_engine():
    result = None
    indicator = request.args.get("indicator", "").strip()

    if request.method == "POST":
        indicator = request.form.get("indicator", "").strip()

    if indicator:
        result = correlate_indicator(indicator)

    return render_template("correlation_engine.html", result=result, indicator=indicator)


@app.route("/cve-explorer", methods=["GET", "POST"])
@login_required
def cve_explorer():
    result = None
    error = None
    cve = request.args.get("cve", "").strip()

    if request.method == "POST":
        cve = request.form.get("cve", "").strip()

    if cve:
        result = analyze_cve(cve)
        if not result.get("valid"):
            error = result.get("error")
            result = None

    return render_template(
        "cve_explorer.html",
        result=result,
        error=error,
        query_cve=cve,
        current_time=datetime.now(IST).strftime("%d %b %Y %H:%M:%S IST")
    )


@app.route("/malware-analysis", methods=["GET", "POST"])
@login_required
def malware_analysis():
    result = None
    file_hash = request.args.get("file_hash", "").strip()

    if request.method == "POST":
        file_hash = request.form.get("file_hash", "").strip()

    if file_hash:
        result = analyze_malware_hash(file_hash)

    return render_template(
        "malware_analysis.html",
        result=result,
        query_hash=file_hash
    )


# ================= GLOBAL SEARCH =================

@app.route("/global-search")
@login_required
def global_search():
    query = request.args.get("q", "").strip()
    if not query:
        return redirect(url_for("dashboard"))

    classified = ThreatEngine.classify_and_analyze(query)
    if classified:
        target_route = classified["target_route"]
        param_name = classified["param_name"]
        return redirect(url_for(target_route, **{param_name: query}))

    return redirect(url_for("correlation_engine", indicator=query))


# ================= ALERTS & INCIDENTS =================

@app.route("/alerts")
@login_required
def alerts():
    all_alerts = SecurityAlert.query.order_by(SecurityAlert.created_at.desc()).all()

    critical_count = sum(1 for a in all_alerts if a.severity.lower() == "critical")
    high_count = sum(1 for a in all_alerts if a.severity.lower() == "high")
    medium_count = sum(1 for a in all_alerts if a.severity.lower() == "medium")
    low_count = sum(1 for a in all_alerts if a.severity.lower() == "low")

    # Serialize alerts for template
    formatted_alerts = []
    for a in all_alerts:
        formatted_alerts.append({
            "id": a.id,
            "alert_id": a.alert_id,
            "title": a.title,
            "level": a.severity.lower(),
            "type": a.category,
            "source": a.source_country or "Unknown",
            "source_ip": a.source_ip or "N/A",
            "target": a.target_country or "Unknown",
            "target_ip": a.target_ip or "N/A",
            "mitre": f"{a.mitre_id} - {a.mitre_name}" if a.mitre_id else "N/A",
            "description": a.analyst_notes or "Suspicious anomaly detected by perimeter sensors.",
            "status": a.status,
            "assigned_to": a.assigned_to,
            "time": a.created_at.strftime("%I:%M:%S %p")
        })

    return render_template(
        "alerts.html",
        alerts=formatted_alerts,
        critical_count=critical_count,
        high_count=high_count,
        medium_count=medium_count,
        low_count=low_count
    )


@app.route("/api/alerts/<int:alert_id>/status", methods=["POST"])
@login_required
def update_alert_status(alert_id):
    alert = db.session.get(SecurityAlert, alert_id)
    if not alert:
        return jsonify({"success": False, "error": "Alert not found"}), 404

    data = request.get_json() or {}
    new_status = data.get("status")
    notes = data.get("notes")

    if new_status:
        alert.status = new_status
    if notes:
        alert.analyst_notes = (alert.analyst_notes or "") + f"\n[{datetime.utcnow().strftime('%Y-%m-%d %H:%M')}] {current_user.name}: {notes}"
    alert.assigned_to = current_user.name

    db.session.commit()
    return jsonify({"success": True, "status": alert.status, "assigned_to": alert.assigned_to})


# ================= REPORTS & EXPORTS =================

@app.route("/reports")
@login_required
def reports():
    report = generate_report_data()
    return render_template("reports.html", report=report)


@app.route("/export/report/json")
@login_required
def export_report_json():
    report = generate_report_data()
    file_data = json.dumps(report, indent=4)
    buffer = BytesIO(file_data.encode("utf-8"))
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{report['report_id']}.json",
        mimetype="application/json"
    )


@app.route("/export/report/csv")
@login_required
def export_report_csv():
    report = generate_report_data()
    csv_data = ReportGenerator.export_csv_report(report)
    buffer = BytesIO(csv_data.encode("utf-8"))
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{report['report_id']}.csv",
        mimetype="text/csv"
    )


@app.route("/api/export/stix", methods=["POST"])
@login_required
def export_stix():
    data = request.get_json() or {}
    indicator = data.get("indicator", "185.220.101.45")
    analysis = analyze_ioc(indicator)
    stix_bundle = analysis.get("stix_bundle", {})
    buffer = BytesIO(json.dumps(stix_bundle, indent=4).encode("utf-8"))
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"stix_bundle_{indicator.replace('.', '_')}.json",
        mimetype="application/json"
    )


# ================= PROFILE & PREFERENCES =================

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@app.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        mobile = request.form.get("mobile", "").strip()
        role = request.form.get("role", "").strip()
        department = request.form.get("department", "").strip()

        if not name:
            flash("Full name is required.", "danger")
            return redirect(url_for("edit_profile"))

        current_user.name = name
        current_user.mobile = mobile
        if role:
            current_user.role = role
        if department:
            current_user.department = department

        db.session.commit()
        flash("Analyst profile updated successfully.", "success")
        return redirect(url_for("profile"))

    return render_template("edit_profile.html")


@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        current_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not check_password_hash(current_user.password, current_password):
            flash("Current password verification failed.", "danger")
            return redirect(url_for("change_password"))

        if new_password != confirm_password:
            flash("New passwords do not match.", "danger")
            return redirect(url_for("change_password"))

        if len(new_password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return redirect(url_for("change_password"))

        current_user.password = generate_password_hash(new_password)
        db.session.commit()

        flash("Credential successfully updated.", "success")
        return redirect(url_for("profile"))

    return render_template("change_password.html")


@app.route("/export-profile")
@login_required
def export_profile():
    data = {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "department": getattr(current_user, "department", "Cyber Threat Intelligence"),
        "mobile": getattr(current_user, "mobile", ""),
        "badge_id": getattr(current_user, "badge_id", "SOC-8421"),
        "last_login": current_user.last_login.isoformat() if current_user.last_login else None,
        "status": "Authenticated Operator"
    }

    file_data = json.dumps(data, indent=4)
    buffer = BytesIO(file_data.encode("utf-8"))
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="analyst_profile_export.json",
        mimetype="application/json"
    )


@app.route("/init-db")
def init_db():
    with app.app_context():
        db.create_all()
        seed_database_defaults()
    return "Database schema synchronized and seeded successfully."


# Initialize database automatically on startup
with app.app_context():
    db.create_all()
    seed_database_defaults()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
