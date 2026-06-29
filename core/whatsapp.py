import requests

from core.config import Settings
from core.database import save_outbound_message
from core.logger import log


def send_whatsapp_message(group_id: str, text: str, related_message_id: str = None):
    url = f"{Settings.evolution_api_url}/message/sendText/{Settings.evolution_instance}"

    headers = {
        "Content-Type": "application/json"
    }

    if Settings.evolution_api_url:
        headers["apikey"] = Settings.evolution_api_key

    payload = {
        "number": group_id,
        "text": text
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)

        log("SEND STATUS:", response.status_code)

        response_text = response.text

        save_outbound_message(
            related_message_id=related_message_id,
            group_id=group_id,
            text=text,
            status_code=response.status_code,
            response_body=response_text
        )

        if response.status_code not in (200, 201):
            log("SEND ERROR:", response_text)
            return None

        return response.json()

    except Exception as e:
        log("SEND EXCEPTION:", str(e))

        save_outbound_message(
            related_message_id=related_message_id,
            group_id=group_id,
            text=text,
            status_code=None,
            response_body=str(e)
        )

        return None
