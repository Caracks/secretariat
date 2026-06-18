from core.pattern_loader import load_task_prefixes
from tools.task_tool import (
    create_task_from_text,
    normalize_task_text,
    get_open_tasks_text
)

def is_list_request(text):
    prefixes = load_task_prefixes()
    clean_text = (text or "").lower()

    return any(keyword in clean_text for keyword in prefixes)


def run(message):
    raw_text = message["text"]

    if is_list_request(raw_text):
        return {"should_reply": True, "text": get_open_tasks_text()}

    normalized_text = normalize_task_text(raw_text)
    task_id = create_task_from_text(text=raw_text, sender_name=message["sender_name"])
    
    return {"should_reply": True, "text": f"Task criada #{task_id}: {normalized_text}"}


agent = {
    "name": "dario",
    "display_name": "Dário",
    "description": "Task agent responsible for detecting and managing pending tasks.",
    "instruction_file": "agents/dario/instructions.md",
    "skills_file": "agents/dario/skills.md",
    "run": run,
}
