from tools.task_tool import create_task_from_text, normalize_task_text


def run(message):
    raw_text = message["text"]
    normalized_text = normalize_task_text(raw_text)

    task_id = create_task_from_text(
        text=raw_text,
        sender_name=message["sender_name"]
    )

    return {
        "should_reply": True,
        "text": f"Task criada - {task_id}: {normalized_text}"
    }


agent = {
    "name": "dario",
    "display_name": "Dário",
    "description": "Task agent responsible for detecting and managing pending tasks.",
    "instruction_file": "agents/dario/instructions.md",
    "skills_file": "agents/dario/skills.md",
    "run": run
}
