from flask import Flask, request, jsonify
import time

from core.config import APP_HOST, APP_PORT
from core.database import (
    init_db,
    is_duplicate,
    save_inbound_message,
    save_webhook_event
)
from core.logger import log
from core.normalizer import normalize_whatsapp_data, get_data_list
from core.whatsapp import send_whatsapp_message
from agents.hello_agent import run as hello_agent_run


app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.get_json(silent=True) or {}

    event = payload.get("event")

    if event != "messages.upsert":
        save_webhook_event(event, True, "not_messages_upsert", payload)
        return jsonify({"ignored": True, "reason": "not_messages_upsert"})

    data_list = get_data_list(payload)

    if data_list is None:
        save_webhook_event(event, True, "invalid_data_shape", payload)
        return jsonify({"ignored": True, "reason": "invalid_data_shape"})

    processed_count = 0
    duplicate_count = 0

    for data in data_list:
        message = normalize_whatsapp_data(data)

        if message["from_me"]:
            continue

        if not message["message_id"]:
            continue

        if is_duplicate(message["message_id"]):
            duplicate_count += 1
            log("SKIP DUPLICATE:", message["message_id"])
            continue

        log("PROCESS:", message["message_id"], message["text"])

        save_inbound_message(
            message_id=message["message_id"],
            group_id=message["group_id"],
            sender_id=message["sender_id"],
            sender_name=message["sender_name"],
            text=message["text"],
            raw_payload=message["raw"]
        )

        if not message["group_id"] or not message["text"]:
            continue

        agent_result = hello_agent_run(message)

        if agent_result.get("should_reply"):
            time.sleep(0.2)

            send_whatsapp_message(
                group_id=message["group_id"],
                text=agent_result["text"],
                related_message_id=message["message_id"]
            )

        processed_count += 1

    return jsonify({
        "status": "ok",
        "processed": processed_count,
        "duplicates": duplicate_count
    })


init_db()

if __name__ == "__main__":
    app.run(host=APP_HOST, port=APP_PORT)
