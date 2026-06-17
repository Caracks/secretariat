def normalize_whatsapp_data(data):
    key = data.get("key", {})

    message = data.get("message", {})

    text = (
        message.get("conversation")
        or message.get("extendedTextMessage", {}).get("text")
        or ""
    )

    return {
        "message_id": key.get("id"),
        "group_id": key.get("remoteJid"),
        "sender_id": key.get("participant") or key.get("participantAlt"),
        "sender_name": data.get("pushName"),
        "from_me": bool(key.get("fromMe")),
        "text": text,
        "raw": data
    }


def get_data_list(payload):
    data_raw = payload.get("data", [])

    if isinstance(data_raw, list):
        return data_raw

    if isinstance(data_raw, dict):
        return [data_raw]

    return None
