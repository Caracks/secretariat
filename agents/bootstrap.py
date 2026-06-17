from agents.agent_registry import registry
from agents.hello_agent import agent as hello_agent
from agents.dario.agent import agent as dario_agent


def register_agents():
    registry.register(
        hello_agent["name"],
        hello_agent
    )

    registry.register(
        dario_agent["name"],
        dario_agent
    )
