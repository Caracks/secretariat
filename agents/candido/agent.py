from core.pattern_loader import TaskField, get_task_field
from tools.candidate_tool import (
    create_candidate_from_message,
    confirm_candidate_from_text,
    reject_candidate_from_text,
)


def is_confirm_request(text):
    clean_text = (text or "").lower()
    confirm_keywords = get_task_field(TaskField.confirm_keywords)
    return any(keyword in clean_text for keyword in confirm_keywords)


def is_reject_request(text):
    clean_text = (text or "").lower()
    reject_keywords = get_task_field(TaskField.reject_keywords)
    return any(keyword in clean_text for keyword in reject_keywords)


def run(message):
    raw_text = message["text"]

    if is_confirm_request(raw_text):
        result = confirm_candidate_from_text(
            raw_text, resolved_by=message["sender_name"]
        )

        return {"should_reply": True, "text": result["message"]}

    if is_reject_request(raw_text):
        result = reject_candidate_from_text(
            raw_text, resolved_by=message["sender_name"]
        )

        return {"should_reply": True, "text": result["message"]}

    result = create_candidate_from_message(message)

    return {
        "should_reply": True,
        "text": (
            f"Possível pendente #{result['candidate_id']}: "
            f"{result['normalized_text']}\n"
            f'Responde "sim" para confirmar '
            f'ou "não" para rejeitar.'
        ),
    }


agent = {
    "name": "candido",
    "display_name": "Cândido",
    "description": "Candidate agent responsible for managing possible tasks before confirmation.",
    "instruction_file": "agents/candido/instructions.md",
    "skills_file": "agents/candido/skills.md",
    "run": run,
}
