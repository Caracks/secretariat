from core.pattern_loader import load_task_patterns


def route_message(message):
    text = (message.get("text") or "").lower()
    keywords =  load_task_patterns()

    if any(keyword in text for keyword in keywords.main_keywords + keywords.done_keywords):
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