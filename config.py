import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(admin_id) for admin_id in os.getenv("ADMIN_IDS", "").split(",") if admin_id.strip()]

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables")

LANGFLOW_API = os.getenv("LANGFLOW_API")
LANGFLOW_WEBHOOK = os.getenv("LANGFLOW_WEBHOOK")

# Database configuration
DB_PATH = os.getenv("DB_PATH", "bot.db")
