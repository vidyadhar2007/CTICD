from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default="Security Analyst")
    department = db.Column(db.String(100), default="Cyber Defense & Threat Intel")
    mobile = db.Column(db.String(30), nullable=True, default="")
    badge_id = db.Column(db.String(30), nullable=True, default="SOC-8421")
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ThreatLog(db.Model):
    __tablename__ = "threat_logs"

    id = db.Column(db.Integer, primary_key=True)
    ioc_value = db.Column(db.String(255), nullable=False)
    ioc_type = db.Column(db.String(50), nullable=False)
    threat_level = db.Column(db.String(50), nullable=False)
    threat_score = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(100), nullable=True)
    malware_family = db.Column(db.String(100), nullable=True)
    attack_type = db.Column(db.String(100), nullable=True)
    recommendation = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class SecurityAlert(db.Model):
    __tablename__ = "security_alerts"

    id = db.Column(db.Integer, primary_key=True)
    alert_id = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    severity = db.Column(db.String(20), nullable=False, default="high")  # critical, high, medium, low
    category = db.Column(db.String(100), nullable=False)
    source_ip = db.Column(db.String(100), nullable=True)
    target_ip = db.Column(db.String(100), nullable=True)
    source_country = db.Column(db.String(100), nullable=True)
    target_country = db.Column(db.String(100), nullable=True)
    mitre_id = db.Column(db.String(50), nullable=True)
    mitre_name = db.Column(db.String(150), nullable=True)
    mitre_tactic = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(30), default="New")  # New, Investigating, Contained, Resolved, False Positive
    analyst_notes = db.Column(db.Text, nullable=True)
    assigned_to = db.Column(db.String(100), default="Unassigned")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ThreatIndicator(db.Model):
    __tablename__ = "threat_indicators"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255), index=True, nullable=False)
    ioc_type = db.Column(db.String(50), nullable=False)
    threat_score = db.Column(db.Integer, default=50)
    severity = db.Column(db.String(50), default="Medium")
    tlp = db.Column(db.String(20), default="AMBER")
    actor = db.Column(db.String(100), nullable=True)
    malware = db.Column(db.String(100), nullable=True)
    cve = db.Column(db.String(50), nullable=True)
    mitre_technique = db.Column(db.String(100), nullable=True)
    tags = db.Column(db.String(255), nullable=True)
    query_count = db.Column(db.Integer, default=1)
    first_seen = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)


class InvestigationCase(db.Model):
    __tablename__ = "investigation_cases"

    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(20), default="High")  # Critical, High, Medium, Low
    status = db.Column(db.String(30), default="Open")  # Open, In Progress, Closed
    lead_analyst = db.Column(db.String(100), default="Security Analyst")
    indicators = db.Column(db.Text, nullable=True)  # JSON or comma-separated list
    summary = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
