from tools.calendar_tool import parse_event_candidate


def run(message):
    result = parse_event_candidate(message.get("text"))

    if not result["is_event"]:
        return {
            "should_reply": False,
            "text": None,
        }

    return {
        "should_reply": True,
        "text": (
            "Possível evento detetado:\n"
            f"- Tipo: {result['title']}\n"
            f"- Data: {result['date_text']}\n"
            f"- Hora: {result['time_text'] or 'por confirmar'}\n\n"
            "Ainda não criei nada no calendário. "
        ),
    }


agent = {
    "name": "dario",
    "display_name": "Dário",
    "description": "Calendar agent responsible for detecting possible calendar events.",
    "instruction_file": "agents/dario/instructions.md",
    "skills_file": "agents/dario/skills.md",
    "run": run,
}
