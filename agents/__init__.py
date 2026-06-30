import importlib
import pkgutil
from pathlib import Path

from agents.agent_registry import registry

__all__ = ["registry"]

_EXCLUDED_MODULES = {"agent_registry"}


def _register_agent(agent_obj, module_name):
    registry.register(agent_obj["name"], agent_obj)

    var_name = f"{module_name}_agent"
    globals()[var_name] = agent_obj
    __all__.append(var_name)


def _load_package_agent(package_name):
    module = importlib.import_module(f"{__name__}.{package_name}.agent")

    if not hasattr(module, "agent"):
        return

    _register_agent(module.agent, package_name)


def _load_module_agent(module_name):
    module = importlib.import_module(f"{__name__}.{module_name}")

    if not hasattr(module, "agent"):
        return

    _register_agent(module.agent, module_name)


def discover_agents():
    package_dir = Path(__file__).resolve().parent

    for _, module_name, is_package in pkgutil.iter_modules([str(package_dir)]):
        if module_name in _EXCLUDED_MODULES or module_name.startswith("_"):
            continue

        if is_package:
            _load_package_agent(module_name)
        else:
            _load_module_agent(module_name)


discover_agents()
