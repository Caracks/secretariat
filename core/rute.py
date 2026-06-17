def route_message(message):
    text = (message.get("text") or "").lower()

    TASK_KEYWORDS = [
        "pendente",
        "lembrar",
        "comprar",
        "fazer",
        "não esquecer",
        "temos de"
    ]

    if any(keyword in text for keyword in TASK_KEYWORDS):
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
