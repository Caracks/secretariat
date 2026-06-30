from core.pattern_loader import (
    TASK_PATTERNS_PATH,
    load_patterns_as_namespace,
)

def route_message(message):
    text = (message.get("text") or "").lower()
    task_patterns = load_patterns_as_namespace(TASK_PATTERNS_PATH)

    if any(
        k in text
        for k in task_patterns.confirm_keywords + task_patterns.reject_keywords
    ):
        return {
            "agent": "candido",
            "confidence": 0.99,
            "reason": "candidate_resolution",
        }

    if any(k in text for k in task_patterns.candidate_keywords):
        return {"agent": "candido", "confidence": 0.85, "reason": "candidate_detected"}

    if any(k in text for k in task_patterns.main_keywords + task_patterns.done_keywords):
        return {"agent": "josefa", "confidence": 0.95, "reason": "task_detected"}

    return {"agent": "hello_agent", "confidence": 1.0, "reason": "default"}

