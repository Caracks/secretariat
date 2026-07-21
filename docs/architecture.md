# Secretariat Bot - Architecture

## Purpose

Secretariat Bot is an agentic assistant operating through WhatsApp.

The architecture is designed to:

* Receive WhatsApp messages
* Route messages to specialized agents
* Execute actions through tools
* Persist conversation history
* Remain modular and extensible

---

# Current Architecture

```text
WhatsApp Group
        |
        v
Evolution API
        |
        v
AI Orchestrator
        |
        v
Rute
        |
        v
Agent Registry
        |
        +--> hello_agent
        |
        +--> josefa
```

---

# Current Runtime Components

## Evolution API

Role:

* WhatsApp gateway
* Receives and sends WhatsApp messages
* Emits webhook events

Container:

* openwa

IP:

* 192.168.1.68

---

## AI Orchestrator

Role:

* Central application
* Receives webhooks
* Persists messages
* Invokes Rute
* Executes agents

Container:

* secretariat

IP:

* 192.168.1.76

Runtime:

* Python
* Flask
* Gunicorn
* Systemd

---

# Message Flow

```text
WhatsApp
    |
    v
Evolution API
    |
    v
Webhook
    |
    v
app.py
    |
    v
Rute
    |
    v
Agent Registry
    |
    v
Selected Agent
    |
    v
WhatsApp Response
```

---

# Current Persistence Layer

Database:

* SQLite

Location:

```text
storage/bot.db
```

Current tables:

* messages
* outbound_messages
* webhook_events

---

# Design Principles

* Modular agents
* Single orchestrator
* Explicit routing
* Agent registry pattern
* Local-first execution
* SQLite-first persistence
* Future LLM routing through Rute
* WhatsApp remains an interface, not the intelligence layer

```
```
