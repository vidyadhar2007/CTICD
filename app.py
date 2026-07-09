from datetime import datetime
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from database import db, User, ThreatLog

from flask import jsonify
from services.geoip_service import generate_live_attack
from modules.ioc_engine import analyze_ioc
from modules.threat_feed import generate_threat_feed, get_feed_stats
from modules.cve_engine import analyze_cve
from modules.malware_engine import analyze_malware_hash
from modules.correlation_engine import correlate_indicator
from modules.report_engine import generate_report_data
from flask import request, render_template, redirect, url_for, flash
from flask import send_file
from werkzeug.security import check_password_hash, generate_password_hash
import json
from io import BytesIO

app = Flask(__name__)
app.config.from_object(Config)

os.makedirs("instance", exist_ok=True)

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message_category = "warning"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for("signup"))

        if User.query.filter_by(email=email).first():
            flash("Email already registered. Please login.", "danger")
            return redirect(url_for("login"))

        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            role="Security Analyst"
        )

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully. Please login.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid email or password.", "danger")
            return redirect(url_for("login"))

        login_user(user)
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    stats = {
        "threat_level": "CRITICAL",
        "risk_score": 92,
        "live_attacks": 3203,
        "malicious_ips": 9461,
        "ioc_detected": 25040,
        "countries_attacked": 123
    }

    recent_alerts = [
        {"level": "critical", "type": "Brute Force Attack", "from": "Russia", "to": "India", "time": "10:24:32 AM"},
        {"level": "high", "type": "Malware Detected", "from": "United States", "to": "Germany", "time": "10:23:11 AM"},
        {"level": "critical", "type": "DDoS Attack", "from": "China", "to": "United States", "time": "10:22:45 AM"},
        {"level": "medium", "type": "SQL Injection Attempt", "from": "Brazil", "to": "Portugal", "time": "10:21:02 AM"}
    ]

    malicious_ips = [
        {"ip": "185.220.101.45", "country": "Russia", "hits": 398},
        {"ip": "103.21.244.12", "country": "India", "hits": 312},
        {"ip": "45.144.227.55", "country": "China", "hits": 276},
        {"ip": "89.248.172.12", "country": "Netherlands", "hits": 198}
    ]

    return render_template(
        "dashboard.html",
        MAP_KEY=app.config.get("MAPTILER_API_KEY", ""),
        stats=stats,
        recent_alerts=recent_alerts,
        malicious_ips=malicious_ips
    )


@app.route("/threat-feed", methods=["GET"])
@login_required
def threat_feed():
    feed = generate_threat_feed()
    stats = get_feed_stats(feed)

    return render_template(
        "threat_feed.html",
        title="Threat Feed",
        feed=feed,
        stats=stats,
        current_time=datetime.now().strftime("%d %b %Y  %H:%M:%S")
    )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("login"))


@app.route("/init-db")
def init_db():
    db.create_all()
    return "Database created successfully."

@app.route("/api/live-attack")
@login_required
def api_live_attack():
    return jsonify(generate_live_attack())

@app.route("/ioc-search", methods=["GET", "POST"])
@login_required
def ioc_search():
    result = None

    if request.method == "POST":
        ioc = request.form.get("ioc", "").strip()

        if ioc:
            result = analyze_ioc(ioc)
        else:
            flash("Please enter a valid IOC.", "danger")

    return render_template("ioc_search.html", result=result)


@app.route("/cve-explorer", methods=["GET", "POST"])
@login_required
def cve_explorer():

    result = None
    error = None

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
        current_time=datetime.now().strftime("%d %b %Y %I:%M:%S %p")
    )

@app.route("/malware-analysis", methods=["GET", "POST"])
@login_required
def malware_analysis():

    result = None

    if request.method == "POST":

        file_hash = request.form.get("file_hash", "").strip()

        if file_hash:
            result = analyze_malware_hash(file_hash)

    return render_template(
        "malware_analysis.html",
        result=result
    )

@app.route("/correlation-engine", methods=["GET", "POST"])
@login_required
def correlation_engine():
    result = None

    if request.method == "POST":
        indicator = request.form.get("indicator", "").strip()

        if indicator:
            result = correlate_indicator(indicator)

    return render_template(
        "correlation_engine.html",
        result=result
    )

@app.route("/reports")
@login_required
def reports():

    report = generate_report_data()

    return render_template(
        "reports.html",
        report=report
    )

@app.route("/threat-map")
@login_required
def threat_map():
    return render_template(
        "threat_map.html",
        MAP_KEY=app.config.get("MAPTILER_API_KEY", "")
    )

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

        if not name:
            flash("Name is required.", "danger")
            return redirect(url_for("edit_profile"))

        current_user.name = name

        if hasattr(current_user, "mobile"):
            current_user.mobile = mobile

        db.session.commit()

        flash("Profile updated successfully.", "success")
        return redirect(url_for("profile"))

    return render_template("edit_profile.html")

@app.route("/alerts")
@login_required
def alerts():
    alerts = [
        {
            "level": "critical",
            "type": "Brute Force Attack",
            "source": "Russia",
            "target": "India",
            "description": "Multiple failed login attempts detected from suspicious IP range.",
            "mitre": "T1110 - Brute Force",
            "time": "10:24:32 AM"
        },
        {
            "level": "high",
            "type": "Malware Detected",
            "source": "United States",
            "target": "Germany",
            "description": "Malware beaconing activity detected from endpoint telemetry.",
            "mitre": "T1059 - Command and Scripting Interpreter",
            "time": "10:22:11 AM"
        },
        {
            "level": "critical",
            "type": "DDoS Attack",
            "source": "China",
            "target": "United States",
            "description": "High volume traffic spike detected against public service.",
            "mitre": "T1499 - Endpoint Denial of Service",
            "time": "10:20:45 AM"
        },
        {
            "level": "medium",
            "type": "SQL Injection Attempt",
            "source": "Brazil",
            "target": "Portugal",
            "description": "Suspicious SQL payload detected in web request logs.",
            "mitre": "T1190 - Exploit Public-Facing Application",
            "time": "10:19:18 AM"
        },
        {
            "level": "low",
            "type": "Phishing Campaign",
            "source": "Singapore",
            "target": "Australia",
            "description": "Suspicious email campaign identified by threat feed correlation.",
            "mitre": "T1566 - Phishing",
            "time": "10:17:02 AM"
        }
    ]

    critical_count = sum(1 for alert in alerts if alert["level"] == "critical")
    high_count = sum(1 for alert in alerts if alert["level"] == "high")
    medium_count = sum(1 for alert in alerts if alert["level"] == "medium")
    low_count = sum(1 for alert in alerts if alert["level"] == "low")

    return render_template(
        "alerts.html",
        alerts=alerts,
        critical_count=critical_count,
        high_count=high_count,
        medium_count=medium_count,
        low_count=low_count
    )

@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        current_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not check_password_hash(current_user.password, current_password):
            flash("Current password is incorrect.", "danger")
            return redirect(url_for("change_password"))

        if new_password != confirm_password:
            flash("New passwords do not match.", "danger")
            return redirect(url_for("change_password"))

        if len(new_password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return redirect(url_for("change_password"))

        current_user.password = generate_password_hash(new_password)
        db.session.commit()

        flash("Password changed successfully.", "success")
        return redirect(url_for("profile"))

    return render_template("change_password.html")


@app.route("/export-profile")
@login_required
def export_profile():
    data = {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "mobile": getattr(current_user, "mobile", ""),
        "role": "Security Analyst",
        "status": "Active"
    }

    file_data = json.dumps(data, indent=4)
    buffer = BytesIO()
    buffer.write(file_data.encode("utf-8"))
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="profile_export.json",
        mimetype="application/json"
    )

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)