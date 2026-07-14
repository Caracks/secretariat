# Secretariat Bot - Agents

## Agent Architecture

Each agent must live in its own folder.

Example:

```text
agents/
|
└── josefa/
    |
    ├── agent.py
    ├── instructions.md
    └── skills.md
```

---

# Components

## agent.py

Technical implementation.

Responsibilities:

* Execute logic
* Return structured response
* Invoke tools when required

---

## instructions.md

Defines:

* Purpose
* Behaviour
* Personality
* Constraints
* Responsibilities

---

## skills.md

Defines:

* Available capabilities
* Supported actions
* Tool usage guidelines

---

# Current Agents

## hello_agent

Purpose:

* MVP validation

Current response:

```text
olá
```

---

## Dário

Purpose:

* Task detection agent

Current response:

```text
apanhei um possível pendente
```

Future responsibilities:

* Create tasks
* Track tasks
* Follow up unresolved tasks
* Suggest reminders

```
```
