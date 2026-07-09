import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "CTICD@2026_Internship_Project")
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "instance", "cticd.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DASHBOARD_NAME = "Cyber Threat Intelligence Correlation Dashboard"
    COMPANY = "CTICD Security Operations Center"
    VERSION = "1.0"

    MAPTILER_API_KEY = os.getenv("MAPTILER_API_KEY", "W1PfRLWxoIp2KSumhRV8")
    MAP_KEY = MAPTILER_API_KEY

    VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY", "")
    ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY", "")
    SHODAN_API_KEY = os.getenv("SHODAN_API_KEY", "")
    URLSCAN_API_KEY = os.getenv("URLSCAN_API_KEY", "")
    CENSYS_API_KEY = os.getenv("CENSYS_API_KEY", "")
    ALIENVAULT_API_KEY = os.getenv("ALIENVAULT_API_KEY", "")
    GREYNOISE_API_KEY = os.getenv("GREYNOISE_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_HTTPONLY = True

    LOW_SCORE = 25
    MEDIUM_SCORE = 50
    HIGH_SCORE = 75
    CRITICAL_SCORE = 90

    DEFAULT_COUNTRY = "India"
    DEFAULT_CITY = "Mohali"
    DEFAULT_TIMEZONE = "Asia/Kolkata"

    REFRESH_INTERVAL = 30000
    AUTO_REFRESH = True
    FEED_UPDATE_SECONDS = 30
    MAX_RESULTS = 100

    LOG_FOLDER = "logs"
    LOG_FILE = "cticd.log"
    REPORT_FOLDER = "reports"
    EXPORT_FOLDER = "exports"

    PRIMARY_COLOR = "#0EA5E9"
    SECONDARY_COLOR = "#2563EB"
    SUCCESS_COLOR = "#22C55E"
    WARNING_COLOR = "#F59E0B"
    DANGER_COLOR = "#EF4444"
    DARK_BACKGROUND = "#020617"
    CARD_BACKGROUND = "#0F172A"