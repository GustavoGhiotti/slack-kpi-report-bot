import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root when running outside the IDE.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(PROJECT_ROOT / ".env")

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

EMAIL_USER = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_SENHA")
EMAIL_SMTP_HOST = os.getenv("EMAIL_SMTP_HOST", "smtp.gmail.com")
EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", "465"))

DB_CONFIG = {
    "server": os.getenv("DB_SERVER"),
    "database": "DB_PLANEJAMENTO",
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}
