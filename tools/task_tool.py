from core.database import create_task
from core.pattern_loader import load_task_prefixes


def normalize_task_text(text):
    clean_text = (text or "").strip()
    lower_text = clean_text.lower()

    task_prefixes = load_task_prefixes()

    for prefix in task_prefixes:
        if lower_text.startswith(prefix):
            return clean_text[len(prefix) :].strip()

    return clean_text


def create_task_from_text(text, sender_name=None):
    normalized_text = normalize_task_text(text)

    task_id = create_task(
        title=normalized_text,
        created_by=sender_name,
        raw_text=text,
        normalized_text=normalized_text,
    )

    return task_id
