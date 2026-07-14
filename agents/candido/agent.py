<<<<<<< HEAD
from core.pattern_loader import load_task_patterns
=======
from core.pattern_loader import TaskField, get_task_field
>>>>>>> origin/main
from tools.candidate_tool import (
    create_candidate_from_message,
    confirm_candidate_from_text,
    reject_candidate_from_text,
)


def is_confirm_request(text):
    clean_text = (text or "").lower()
<<<<<<< HEAD
    confirm_keywords = load_task_patterns().confirm_keywords
=======
    confirm_keywords = get_task_field(TaskField.confirm_keywords)
>>>>>>> origin/main
    return any(keyword in clean_text for keyword in confirm_keywords)


def is_reject_request(text):
    clean_text = (text or "").lower()
<<<<<<< HEAD
    reject_keywords = load_task_patterns().reject_keywords
=======
    reject_keywords = get_task_field(TaskField.reject_keywords)
>>>>>>> origin/main
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
<<<<<<< HEAD
            f'Responde "sim #{result["candidate_id"]}" para confirmar '
            f'ou "não #{result["candidate_id"]}" para rejeitar.'
=======
            f'Responde "sim" para confirmar '
            f'ou "não" para rejeitar.'
>>>>>>> origin/main
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
