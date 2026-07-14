import time
<<<<<<< HEAD
from agents import registry
from agents.rute.agent import route_message

from core.logger import log
from core.normalizer import normalize_whatsapp_data, get_data_list
from tools.evolution_api import EvolutionAPI
from core.config import Settings, WRONG_CONTACT_AUTO_REPLY, AUTHORIZED_GROUP_ID
=======
from flask import Flask, request, jsonify

from core.logger import log

from core.normalizer import normalize_whatsapp_data, get_data_list
from core.whatsapp import send_whatsapp_message
from agents.rute.agent import route_message
from agents.bootstrap import register_agents
from agents.agent_registry import registry

from core.config import (
    APP_HOST,
    APP_PORT,
    AUTHORIZED_GROUP_ID,
    WRONG_CONTACT_AUTO_REPLY,

)
>>>>>>> origin/main
from core.database import (
    init_db,
    is_duplicate,
    save_inbound_message,
    save_webhook_event,
    is_chat_blocked,
    block_chat,
<<<<<<< HEAD
)


evolution_api = EvolutionAPI(
    api_url=Settings.evolution_api_url,
    instance=Settings.evolution_instance,
    api_key=Settings.evolution_api_key,
=======
>>>>>>> origin/main
)

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
        chat_id = message["group_id"]

        if not chat_id:
            continue

        if AUTHORIZED_GROUP_ID and chat_id != AUTHORIZED_GROUP_ID:
            if is_chat_blocked(chat_id):
                log("SKIP BLOCKED CHAT:", chat_id)
                continue
<<<<<<< HEAD
            log("SKIP UNAUTHORIZED CHAT:", chat_id)

            evolution_api.call(
                endpoint="message",
                action="sendText",
                payload={"number": chat_id, "text": WRONG_CONTACT_AUTO_REPLY},
=======

            log("WRONG CHAT AUTO REPLY:", chat_id)

            send_whatsapp_message(
                group_id=chat_id,
                text=WRONG_CONTACT_AUTO_REPLY,
>>>>>>> origin/main
                related_message_id=message["message_id"],
            )

            block_chat(chat_id)
            continue

        if message["from_me"]:
            continue

        if not message["message_id"]:
            continue

        if is_duplicate(message["message_id"]):
            duplicate_count += 1
            log("SKIP DUPLICATE:", message["message_id"])
            continue

        log(
            "PROCESS:",
            message["message_id"],
            message["group_id"],
            message["sender_id"],
            message["text"],
        )

        save_inbound_message(
            message_id=message["message_id"],
            group_id=message["group_id"],
            sender_id=message["sender_id"],
            sender_name=message["sender_name"],
            text=message["text"],
            raw_payload=message["raw"],
        )

        if not message["group_id"] or not message["text"]:
            continue

        route = route_message(message)
        agent = registry.get(route["agent"])

        if agent is None:
            log("No Agent found:", route["agent"])
            continue

        agent_result = agent["run"](message)

        if agent_result.get("should_reply"):
            time.sleep(0.2)

<<<<<<< HEAD
            evolution_api.call(
                endpoint="message",
                action="sendText",
                payload={"number": message["group_id"], "text": agent_result["text"]},
=======
            send_whatsapp_message(
                group_id=message["group_id"],
                text=agent_result["text"],
>>>>>>> origin/main
                related_message_id=message["message_id"],
            )

        processed_count += 1

    return jsonify(
        {"status": "ok", "processed": processed_count, "duplicates": duplicate_count}
    )


init_db()

if __name__ == "__main__":
    app.run(host=Settings.app_host, port=Settings.app_port)
