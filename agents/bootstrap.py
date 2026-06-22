from agents.agent_registry import registry
from agents.candido.agent import agent as candido_agent
from agents.hello_agent import agent as hello_agent
from agents.dario.agent import agent as dario_agent

class AgentRegistrar:
    def __init__(self, registry_instance):
        self.registry = registry_instance
        # Mantém a lista de agentes centralizada na classe
        self._agents_to_register = [
            hello_agent,
            dario_agent,
            candido_agent
        ]

    def register_all(self) -> None:
        for agent in self._agents_to_register:
            self.registry.register(agent["name"], agent)


def register_agents():
    regist = AgentRegistrar(registry)
    regist.register_all()