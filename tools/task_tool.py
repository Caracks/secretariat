import re
from core.database import create_task, list_open_tasks, complete_task
from core.pattern_loader import get_task_field, TaskField


def normalize_task_text(text):
    clean_text = (text or "").strip()
    lower_text = clean_text.lower()

    task_prefixes = get_task_field(TaskField.prefixes)

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


def get_open_tasks_text():
    tasks = list_open_tasks()

    if not tasks:
        return "Não tens pendentes em aberto."

    lines = ["Pendentes:"]

    for task_id, title in tasks:
        lines.append(f"#{task_id} {title}")

    return "\n".join(lines)


def extract_task_id(text):
    match = re.search(r"#?(\d+)", text or "")

    if not match:
        return None

    return int(match.group(1))


def complete_task_from_text(text):
    task_id = extract_task_id(text)

    if task_id is None:
        return {
            "success": False,
            "message": "Não percebi qual é o pendente a concluir.",
        }

    success = complete_task(task_id)

    if not success:
        return {
            "success": False,
            "message": f"Não encontrei o pendente #{task_id} em aberto.",
        }

    return {"success": True, "message": f"Task #{task_id} concluída."}
