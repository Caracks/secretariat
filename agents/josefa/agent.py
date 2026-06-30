from agents import registry
from core.pattern_loader import (
    load_task_patterns
)

from tools.task_tool import (
    create_task_from_text,
    normalize_task_text,
    get_open_tasks_text,
    complete_task_from_text,
)

patterns = load_task_patterns()

def is_list_request(text):
    clean_text = (text or "").lower()
    return any(keyword in clean_text for keyword in patterns.list_keywords)


def is_done_request(text):
    clean_text = (text or "").lower()
    return any(keyword in clean_text for keyword in patterns.done_keywords)


def run(message):
    raw_text = message["text"]

    if is_list_request(raw_text):
        return {"should_reply": True, "text": get_open_tasks_text()}

    if is_done_request(raw_text):
        result = complete_task_from_text(raw_text)

        return {"should_reply": True, "text": result["message"]}

    normalized_text = normalize_task_text(raw_text)

    task_id = create_task_from_text(text=raw_text, sender_name=message["sender_name"])

    return {"should_reply": True, "text": f"Task criada #{task_id}: {normalized_text}"}


agent = {
    "name": "josefa",
    "display_name": "Josafa",
    "description": "Task agent responsible for detecting and managing pending tasks.",
    "instruction_file": "agents/josefa/instructions.md",
    "skills_file": "agents/josefa/skills.md",
    "run": run,
}

registry.register(agent["name"], agent)