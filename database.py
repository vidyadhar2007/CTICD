from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)

    role = db.Column(db.String(30), default="Analyst")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ThreatLog(db.Model):
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