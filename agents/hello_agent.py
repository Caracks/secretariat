from agents import registry

def run(message):
    return {
        "should_reply": True,
        "text": "olá 👋"
    }


agent = {
    "name": "hello_agent",
    "description": "Simple MVP hello agent",
    "run": run
}

registry.register(agent["name"], agent)