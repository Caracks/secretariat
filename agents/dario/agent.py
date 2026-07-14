<<<<<<< HEAD
from tools.calendar_tool import parse_event_candidate
=======
from core.pattern_loader import TaskField, get_task_field
from tools.task_tool import (
    create_task_from_text,
    normalize_task_text,
    get_open_tasks_text,
    complete_task_from_text,
)

def is_list_request(text):
    list_keywords = get_task_field(TaskField.list_keywords)
    clean_text = (text or "").lower()
    return any(keyword in clean_text for keyword in list_keywords)


def is_done_request(text):
    done_keywords = get_task_field(TaskField.done_keywords)
    clean_text = (text or "").lower()
    return any(keyword in clean_text for keyword in done_keywords)
>>>>>>> origin/main


def run(message):
    result = parse_event_candidate(message.get("text"))

    if not result["is_event"]:
        return {
            "should_reply": False,
            "text": None,
        }

<<<<<<< HEAD
    return {
        "should_reply": True,
        "text": (
            "Possível evento detetado:\n"
            f"- Tipo: {result['title']}\n"
            f"- Data: {result['date_text']}\n"
            f"- Hora: {result['time_text'] or 'por confirmar'}\n\n"
            "Ainda não criei nada no calendário. "
        ),
    }
=======
    if is_done_request(raw_text):
        result = complete_task_from_text(raw_text)
        return {"should_reply": True, "text": result["message"]}

    normalized_text = normalize_task_text(raw_text)
    task_id = create_task_from_text(text=raw_text, sender_name=message["sender_name"])

    return {"should_reply": True, "text": f"Task criada #{task_id}: {normalized_text}"}
>>>>>>> origin/main


agent = {
    "name": "dario",
    "display_name": "Dário",
    "description": "Calendar agent responsible for detecting possible calendar events.",
    "instruction_file": "agents/dario/instructions.md",
    "skills_file": "agents/dario/skills.md",
    "run": run,
}
