from agents.agent_registry import registry
from agents.hello_agent import agent as hello_agent
from agents.josefa.agent import agent as josefa_agent


def register_agents():
    registry.register(
        hello_agent["name"],
        hello_agent
    )

    registry.register(
        josefa_agent["name"],
        josefa_agent
    )
