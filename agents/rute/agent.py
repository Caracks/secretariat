import re

from core.pattern_loader import (
    CALENDAR_PATTERNS_PATH,
    TASK_PATTERNS_PATH,
    load_patterns_as_namespace,
)


def contains_any(text, patterns):
    return any(pattern in text for pattern in patterns)


def build_candidate_response_pattern(confirm_keywords, reject_keywords):
    keywords = confirm_keywords + reject_keywords
    escaped_keywords = [re.escape(keyword) for keyword in keywords]

    return re.compile(
        rf"\b({'|'.join(escaped_keywords)})\s+#\d+\b",
        re.IGNORECASE,
    )


def has_candidate_response(text, task_patterns):
    pattern = build_candidate_response_pattern(
        task_patterns.confirm_keywords,
        task_patterns.reject_keywords,
    )
    return bool(pattern.search(text))


def route_message(message):
    text = (message.get("text") or "").lower()

    task_patterns = load_patterns_as_namespace(TASK_PATTERNS_PATH)
    calendar_patterns = load_patterns_as_namespace(CALENDAR_PATTERNS_PATH)

    if has_candidate_response(text, task_patterns):
        return {
            "agent": "candido",
            "confidence": 0.99,
            "reason": "candidate_resolution",
        }

    if contains_any(text, calendar_patterns.event_keywords):
        return {
            "agent": "dario",
            "confidence": 0.90,
            "reason": "calendar_event_detected",
        }

    if contains_any(text, task_patterns.candidate_keywords):
        return {
            "agent": "candido",
            "confidence": 0.85,
            "reason": "candidate_detected",
        }

    if contains_any(text, task_patterns.main_keywords + task_patterns.done_keywords):
        return {
            "agent": "josefa",
            "confidence": 0.95,
            "reason": "task_detected",
        }

    return {
        "agent": "hello_agent",
        "confidence": 1.0,
        "reason": "default",
    }
