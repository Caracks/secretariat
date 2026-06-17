from flask import Flask, request, jsonify
import requests
import os
import time

app = Flask(__name__)

EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL", "http://192.168.1.68:8080")
EVOLUTION_INSTANCE = os.getenv("EVOLUTION_INSTANCE", "secretariat-bot")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY", "")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

# dedupe com timestamp (muito mais robusto)
processed_messages = {}


def log(*args):
    if DEBUG:
        print(*args, flush=True)


def send_whatsapp_message(group_id: str, text: str):
    url = f"{EVOLUTION_API_URL}/message/sendText/{EVOLUTION_INSTANCE}"

    headers = {
        "Content-Type": "application/json",
        "apikey": EVOLUTION_API_KEY
    }

    payload = {
        "number": group_id,
        "text": text
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)

        log("SEND STATUS:", response.status_code)

        if response.status_code not in (200, 201):
            log("SEND ERROR:", response.text, flush=True)
            return None

        return response.json()

    except Exception as e:
        log("SEND EXCEPTION:", str(e))
        return None


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.get_json(silent=True) or {}

    event = payload.get("event")

    if event != "messages.upsert":
        return jsonify({"ignored": True})

    data_raw = payload.get("data",[])

    if isinstance(data_raw, list):
      data_list = data_raw
    elif isinstance(data_raw, dict):
      data_list = [data_raw]
    else:
        return jsonify({"ignored": True})

    now = time.time()

    # limpar mensagens antigas (> 60s)
    for k in list(processed_messages.keys()):
        if now - processed_messages[k] > 60:
            del processed_messages[k]

    for data in data_list:
        key = data.get("key", {})

        # ignora mensagens do próprio bot
        if key.get("fromMe"):
            continue

        message_id = key.get("id")
        if not message_id:
            continue

        # dedupe correto (não quebra o bot)
        if message_id in processed_messages:
            log("SKIP DUPLICATE:", message_id)
            continue

        processed_messages[message_id] = now

        group_id = key.get("remoteJid")

        message = data.get("message", {})

        text = (
            message.get("conversation")
            or message.get("extendedTextMessage", {}).get("text")
            or ""
        )

        log("PROCESS:", message_id, text)

        if not group_id or not text:
            continue

        # pequeno throttle para evitar spam API
        time.sleep(0.2)

        send_whatsapp_message(group_id, "olá 👋")

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    # 🔥 melhor para Linux containers / servidores
    app.run(host="0.0.0.0", port=5000)
