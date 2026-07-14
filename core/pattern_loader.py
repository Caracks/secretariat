from enum import Enum
from functools import lru_cache
from pathlib import Path
from types import SimpleNamespace

import yaml

from core.config import Settings

TASK_PATTERNS_PATH = Path(Settings.task_patterns_path)
CALENDAR_PATTERNS_PATH = Path(Settings.calendar_patterns_path)


class TaskField(str, Enum):
    keywords = "keywords"
    prefixes = "prefixes"
    done_keywords = "done_keywords"
    list_keywords = "list_keywords"
    confirm_keywords = "confirm_keywords"
    reject_keywords = "reject_keywords"
    candidate_keywords = "candidate_keywords"
    main_keywords = "main_keywords"


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


@lru_cache(maxsize=1)
def _load_yaml_file() -> dict:
    if not TASK_PATTERNS_PATH.exists():
        return {}
    with TASK_PATTERNS_PATH.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def get_task_field(field: TaskField) -> list:
    data = _load_yaml_file()
    raw_list = data.get(field.value, [])

    if not isinstance(raw_list, list):
        return []

    clean_list = []
    for item in raw_list:
        if item is False:
            clean_list.append("no")
        elif item is True:
            clean_list.append("yes")
        elif item is not None:
            clean_list.append(str(item))

    return clean_list


def clear_patterns_cache():
    _load_yaml_file.cache_clear()
