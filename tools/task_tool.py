from core.database import create_task


TASK_PREFIXES = [
    "tenho um pendente para",
    "tenho um pendente de",
    "pendente para",
    "pendente de",
    "lembrar de",
    "lembrar para",
    "não esquecer de",
    "nao esquecer de"
]


def normalize_task_text(text):
    clean_text = (text or "").strip()
    lower_text = clean_text.lower()

    for prefix in TASK_PREFIXES:
        if lower_text.startswith(prefix):
            return clean_text[len(prefix):].strip()

    return clean_text


def create_task_from_text(text, sender_name=None):
    normalized_text = normalize_task_text(text)

    task_id = create_task(
        title=normalized_text,
        created_by=sender_name,
        raw_text=text,
        normalized_text=normalized_text
    )

    return task_id
