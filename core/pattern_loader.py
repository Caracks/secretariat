from types import SimpleNamespace
from pathlib import Path
import yaml
from core.config import Settings    

TASK_PATTERNS_PATH = Path(Settings.task_patterns_path)
CALENDAR_PATTERNS_PATH = Path(Settings.calendar_patterns_path)
print(TASK_PATTERNS_PATH)
print(CALENDAR_PATTERNS_PATH)


def load_yaml(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Arquivo de padrões não encontrado em: {path}")

    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def load_patterns_as_namespace(path: Path) -> SimpleNamespace:
    data = load_yaml(path)
    return SimpleNamespace(**data)


def load_task_patterns() -> SimpleNamespace:
    return load_patterns_as_namespace(TASK_PATTERNS_PATH)


def load_calendar_patterns() -> SimpleNamespace:
    return load_patterns_as_namespace(CALENDAR_PATTERNS_PATH)
