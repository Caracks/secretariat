from core.pattern_loader import load_task_keywords, load_task_done

def route_message(message):
    text = (message.get("text") or "").lower()
    task_keywords = load_task_keywords()
    done_keywords = load_task_done()

    if any(keyword in text for keyword in task_keywords + done_keywords):
        return {
            "agent": "dario",
            "confidence": 0.95,
            "reason": "task_keyword_detected"
        }

    return {
        "agent": "hello_agent",
        "confidence": 1.0,
        "reason": "mvp_default_route"
    }