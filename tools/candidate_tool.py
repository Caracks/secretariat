import re
from tools.task_tool import normalize_task_text
from core.database import (
    create_task,
    create_task_candidate,
    get_task_candidate,
    update_task_candidate_status,
)


def extract_candidate_id(text):
    match = re.search(r"#?(\d+)", text or "")

    if not match:
        return None
    return int(match.group(1))


def create_candidate_from_message(message):
    raw_text = message["text"]
    normalized_text = normalize_task_text(raw_text)

    candidate_id = create_task_candidate(
        source_message_id=message["message_id"],
        source_chat_id=message["group_id"],
        source_sender_name=message["sender_name"],
        raw_text=raw_text,
        normalized_text=normalized_text,
    )

    return {
        "candidate_id": candidate_id,
        "normalized_text": normalized_text,
    }


def confirm_candidate_from_text(text, resolved_by=None):
    candidate_id = extract_candidate_id(text)

    if candidate_id is None:
        return {
            "success": False,
            "message": "Não percebi qual é o candidato a confirmar.",
        }

    candidate = get_task_candidate(candidate_id)

    if candidate is None:
        return {
            "success": False,
            "message": f"Não encontrei o candidato #{candidate_id}.",
        }

    candidate_id, normalized_text, status = candidate

    if status != "pending_confirmation":
        return {
            "success": False,
            "message": f"O candidato #{candidate_id} já foi tratado.",
        }

    updated = update_task_candidate_status(
        candidate_id=candidate_id,
        status="confirmed",
        resolved_by=resolved_by,
    )

    if not updated:
        return {
            "success": False,
            "message": f"Não consegui confirmar o candidato #{candidate_id}.",
        }

    task_id = create_task(
        title=normalized_text,
        created_by=resolved_by,
        raw_text=text,
        normalized_text=normalized_text,
    )

    return {
        "success": True,
        "message": f"Candidato #{candidate_id} confirmado. Task criada #{task_id}: {normalized_text}",
    }


def reject_candidate_from_text(text, resolved_by=None):
    candidate_id = extract_candidate_id(text)

    if candidate_id is None:
        return {
            "success": False,
            "message": "Não percebi qual é o candidato a rejeitar.",
        }

    candidate = get_task_candidate(candidate_id)

    if candidate is None:
        return {
            "success": False,
            "message": f"Não encontrei o candidato #{candidate_id}.",
        }

    candidate_id, normalized_text, status = candidate

    if status != "pending_confirmation":
        return {
            "success": False,
            "message": f"O candidato #{candidate_id} já foi tratado.",
        }

    updated = update_task_candidate_status(
        candidate_id=candidate_id,
        status="rejected",
        resolved_by=resolved_by,
    )

    if not updated:
        return {
            "success": False,
            "message": f"Não consegui rejeitar o candidato #{candidate_id}.",
        }

    return {"success": True, "message": f"Candidato #{candidate_id} rejeitado."}
