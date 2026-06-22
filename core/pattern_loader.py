from enum import Enum
from functools import lru_cache
from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
TASK_PATTERNS_PATH = BASE_DIR / "config" / "task_patterns.yaml"


class TaskField(str, Enum):
    keywords = "keywords"
    prefixes = "prefixes"
    done_keywords = "done_keywords"
    list_keywords = "list_keywords"
    confirm_keywords = "confirm_keywords"
    reject_keywords = "reject_keywords"
    candidate_keywords = "candidate_keywords"

@lru_cache(maxsize=1)
def _load_yaml_file() -> dict:
    if not TASK_PATTERNS_PATH.exists():
        return {}
    with TASK_PATTERNS_PATH.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}

def get_task_field(field: TaskField) -> list:
    data = _load_yaml_file()
    raw_list = data.get(field.value, []) # Usa .value explicitamente para garantir a string da chave
    
    if not isinstance(raw_list, list):
        return []
        
    # SEGREDO DA SEGURANÇA: Converte itens como False (que era "no") de volta para string "no"
    # Se o item extraído for o booleano False, nós traduzimos explicitamente para "no"
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