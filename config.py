import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "CTICD@2026_Enterprise_SOC_Key_Secured")
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "instance", "cticd.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DASHBOARD_NAME = "Cyber Threat Intelligence Correlation Dashboard"
    DASHBOARD_ACRONYM = "CTICD"
    COMPANY = "CTICD Cyber Defense & Intelligence Operations"
    VERSION = "2.5 Enterprise"
    DEFCON_LEVEL = "DEFCON 2 - ELEVATED"

    # Geo Map API
    MAPTILER_API_KEY = os.getenv("MAPTILER_API_KEY", "W1PfRLWxoIp2KSumhRV8")
    MAP_KEY = MAPTILER_API_KEY

    # Threat Intelligence Integrations
    VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY", "")
    ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY", "")
    SHODAN_API_KEY = os.getenv("SHODAN_API_KEY", "")
    URLSCAN_API_KEY = os.getenv("URLSCAN_API_KEY", "")
    CENSYS_API_KEY = os.getenv("CENSYS_API_KEY", "")
    ALIENVAULT_API_KEY = os.getenv("ALIENVAULT_API_KEY", "")
    GREYNOISE_API_KEY = os.getenv("GREYNOISE_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    # Security & Sessions
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_HTTPONLY = True

    # Scoring Thresholds
    LOW_SCORE = 25
    MEDIUM_SCORE = 50
    HIGH_SCORE = 75
    CRITICAL_SCORE = 88

    # Localization (India Standard Time)
    DEFAULT_COUNTRY = "India"
    DEFAULT_TIMEZONE = "Asia/Kolkata"
    TIMEZONE_LABEL = "IST"

    # Refresh Intervals (ms)
    REFRESH_INTERVAL = 30000
    AUTO_REFRESH = True
    FEED_UPDATE_SECONDS = 25
    MAX_RESULTS = 150

    # Folders
    LOG_FOLDER = "logs"
    LOG_FILE = "cticd.log"
    REPORT_FOLDER = "reports"
    EXPORT_FOLDER = "exports"

    # Standard TLP classifications
    TLP_LEVELS = ["TLP:CLEAR", "TLP:GREEN", "TLP:AMBER", "TLP:AMBER+STRICT", "TLP:RED"]
    DEFAULT_TLP = "TLP:AMBER"

    # UI Theme Palette
    PRIMARY_COLOR = "#0ea5e9"
    SECONDARY_COLOR = "#2563eb"
    SUCCESS_COLOR = "#22c55e"
    WARNING_COLOR = "#f59e0b"
    DANGER_COLOR = "#ef4444"
    PURPLE_COLOR = "#a855f7"
    DARK_BACKGROUND = "#020617"
    CARD_BACKGROUND = "#0f172a"
