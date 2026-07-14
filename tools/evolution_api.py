import requests

from core.database import save_outbound_message
from core.logger import log


class EvolutionAPI:
    def __init__(self, api_url, instance, api_key):
        self.api_url = api_url.rstrip("/")
        self.instance = instance
        self.api_key = api_key

    def call(
        self,
        endpoint: str,
        action: str,
        payload: dict | None = None,
        related_message_id=None,
        persist=True,
        **kwargs,
    ):
        url = f"{self.api_url}/{endpoint}/{action}/{self.instance}"

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["apikey"] = self.api_key

        request_payload = {**(payload or {}), **kwargs}

        try:
            response = requests.post(
                url,
                json=request_payload,
                headers=headers,
                timeout=10,
            )

            log("EVOLUTION STATUS:", response.status_code)

            if persist:
                save_outbound_message(
                    related_message_id=related_message_id,
                    group_id=request_payload.get("number"),
                    text=request_payload.get("text"),
                    status_code=response.status_code,
                    response_body=response.text,
                )

            if response.status_code not in (200, 201):
                log("EVOLUTION ERROR:", response.text)
                return None

            return response.json()

        except Exception as exc:
            log("EVOLUTION EXCEPTION:", str(exc))

            if persist:
                save_outbound_message(
                    related_message_id=related_message_id,
                    group_id=request_payload.get("number"),
                    text=request_payload.get("text"),
                    status_code=None,
                    response_body=str(exc),
                )

            return None