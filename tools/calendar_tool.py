import re
from core.pattern_loader import load_calendar_patterns

calendar_patterns = load_calendar_patterns()

def _find_first_match(patterns, text):
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(0)

    return None


def _detect_event_keyword(text):
    clean_text = (text or "").lower()

    for keyword in calendar_patterns.event_keywords:
        if keyword in clean_text:
            return keyword

    return None


def parse_event_candidate(text):
    clean_text = (text or "").strip()

    if not clean_text:
        return {
            "is_event": False,
            "title": None,
            "date_text": None,
            "time_text": None,
            "confidence": "low",
            "reason": "empty_text",
        }

    event_keyword = _detect_event_keyword(clean_text)
    date_text = _find_first_match(calendar_patterns.date_patterns, clean_text)
    time_text = _find_first_match(calendar_patterns.time_patterns, clean_text)

    is_event = bool(event_keyword and date_text)

    if event_keyword and date_text and time_text:
        confidence = "high"
    elif event_keyword and date_text:
        confidence = "medium"
    else:
        confidence = "low"

    return {
        "is_event": is_event,
        "title": event_keyword,
        "date_text": date_text,
        "time_text": time_text,
        "confidence": confidence,
        "reason": "event_keyword_and_date"
        if is_event
        else "missing_event_keyword_or_date",
    }
