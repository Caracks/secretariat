from pathlib import Path
import yaml


BASE_DIR = Path(__file__).resolve().parent.parent
TASK_PATTERNS_PATH = BASE_DIR / "config" / "task_patterns.yaml"


def load_task_patterns():
    with TASK_PATTERNS_PATH.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    return {
        "keywords": data.get("keywords", []),
        "prefixes": data.get("prefixes", []),
    }


def load_task_keywords():
    return load_task_patterns()["keywords"]

def load_task_prefixes():
    return load_task_patterns()["prefixes"]
