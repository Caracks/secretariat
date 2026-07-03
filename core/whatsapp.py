import requests
from core.database import save_outbound_message
from core.logger import log

class EvolutionAPI:
    def __init__(self, api_url, instance, api_key):
        self.api_url = api_url.rstrip("/")
        self.instance = instance
        self.api_key = api_key

    def call(self, endpoint: str, action: str, payload: dict, related_message_id=None, **kwargs):
        """
        endpoint: 'message', 'settings', 'group', etc.
        action: 'sendText', 'rejectCall', etc.
        kwargs: payload dinâmico
        """
        
        url = f"{self.api_url}/{endpoint}/{action}/{self.instance}"

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["apikey"] = self.api_key

        payload = {**payload, **kwargs}
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)

            log("SEND STATUS:", response.status_code)

            save_outbound_message(
                related_message_id=related_message_id,
                group_id=payload.get("number"),
                text=payload.get("text"),
                status_code=response.status_code,
                response_body=response.text,
            )

            if response.status_code not in (200, 201):
                log("SEND ERROR:", response.text)
                return None

            return response.json()

        except Exception as e:
            log("SEND EXCEPTION:", str(e))

            save_outbound_message(
                related_message_id=related_message_id,
                group_id=payload.get("number"),
                text=payload.get("text"),
                status_code=None,
                response_body=str(e),
            )

            return None
