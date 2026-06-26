from core.pattern_loader import TaskField, get_task_field

def route_message(message):
    text = (message.get("text") or "").lower()
    task_keywords = get_task_field(TaskField.keywords)
    done_keywords = get_task_field(TaskField.done_keywords)
    candidate_keywords = get_task_field(TaskField.candidate_keywords)
    candidate_confirm_keywords = get_task_field(TaskField.confirm_keywords)
    candidate_reject_keywords = get_task_field(TaskField.reject_keywords)

    if any(keyword in text for keyword in candidate_confirm_keywords + candidate_reject_keywords):
        return {
            "agent": "candido",
            "confidence": 0.99,
            "reason": "candidate_resolution_detected"
        }

    if any(keyword in text for keyword in candidate_keywords):
        return {
            "agent": "candido",
            "confidence": 0.85,
            "reason": "candidate_task_detected"
        }

    if any(keyword in text for keyword in task_keywords + done_keywords):
        return {
            "agent": "josefa",
            "confidence": 0.95,
            "reason": "task_keyword_detected"
        }

    return {
        "agent": "hello_agent",
        "confidence": 1.0,
        "reason": "mvp_default_route"
    }