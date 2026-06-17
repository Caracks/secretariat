# Rute - Routing Agent

## Purpose

Rute is responsible for deciding which agent should process a message.

Rute does not execute business logic.

Rute only selects the appropriate agent.

---

# Current Behaviour

Current implementation:

```text
If message contains:
    pendente

Then:
    Dário
```

Otherwise:

```text
hello_agent
```

---

# Future Behaviour

Rute will become an LLM-powered routing layer.

Expected flow:

```text
Message
    |
    v
Rute
    |
    v
Decision JSON
```

Example:

```json
{
  "agent": "dario",
  "confidence": 0.92,
  "reason": "task_detection"
}
```

---

# Responsibilities

* Intent detection
* Agent selection
* Confidence scoring
* Context awareness

---

# Non Responsibilities

Rute must not:

* Send WhatsApp messages
* Query Gmail
* Create Calendar events
* Execute tasks

Those responsibilities belong to specialized agents.

```
```
