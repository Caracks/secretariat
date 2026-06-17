from dotenv import load_dotenv
import os

load_dotenv()

EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL", "http://192.168.1.68:8080")
EVOLUTION_INSTANCE = os.getenv("EVOLUTION_INSTANCE", "secretariat-bot")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY", "")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
DB_PATH = os.getenv("DB_PATH", "/app/ai-orchestrator/storage/bot.db")
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "5000"))
