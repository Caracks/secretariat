import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DEFAULT_DB_PATH = str(BASE_DIR / "storage" / "bot.db")
DEFAULT_TASK_PATTERNS = str(BASE_DIR / "config" / "task_patterns.yaml")
DEFAULT_CALENDAR_PATTERNS = str(BASE_DIR / "config" / "calendar_patterns.yaml")


@dataclass(frozen=True)
class Settings:
    """Encapsula as configurações da aplicação de forma imutável (SOLID/PEP8)."""

    # Evolution API
    evolution_api_url: str = os.getenv("EVOLUTION_API_URL", "http://192.168.1.68:8080")
    evolution_instance: str = os.getenv("EVOLUTION_INSTANCE", "secretariat-bot")
    evolution_api_key: str = os.getenv("EVOLUTION_API_KEY", "")

    # Application Config
    app_host: str = os.getenv("APP_HOST", "0.0.0.0")
    app_port: int = int(os.getenv("APP_PORT", "5000"))
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # Database
    db_path: str = os.getenv("DB_PATH", DEFAULT_DB_PATH)


    # YAML Pattern Files
    task_patterns_path: Path = Path(os.getenv("TASK_PATTERNS_PATH", DEFAULT_TASK_PATTERNS))
    calendar_patterns_path: Path = Path(os.getenv("CALENDAR_PATTERNS_PATH", DEFAULT_CALENDAR_PATTERNS))


# Instância única para o projeto (Singleton)
settings = Settings()