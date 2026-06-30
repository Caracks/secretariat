import importlib
import pkgutil
import sys
from pathlib import Path
from agents.agent_registry import registry

__all__ = ["registry"]

package_dir = str(Path(__file__).resolve().parent)

for _, module_name, is_pkg in pkgutil.iter_modules([package_dir]):
    if module_name in ("agent_registry") or module_name.startswith("_"):
        continue

    try:
        full_module_name = f"{__name__}.{module_name}"
        module = importlib.import_module(full_module_name)

        if is_pkg:
            try:
                sub_module = importlib.import_module(f"{full_module_name}.agent")
                if hasattr(sub_module, "agent"):
                    agent_obj = getattr(sub_module, "agent")
                    var_name = f"{module_name}_agent"
                    globals()[var_name] = agent_obj
                    __all__.append(var_name)
            except ImportError:
                continue
        else:
            if hasattr(module, "agent"):
                agent_obj = getattr(module, "agent")
                var_name = (
                    f"{module_name}"
                    if "agent" in module_name
                    else f"{module_name}_agent"
                )
                globals()[var_name] = agent_obj
                __all__.append(var_name)

    except Exception as e:
        print(
            f"[Warning] Erro ao carregar o agente {module_name}: {e}", file=sys.stderr
        )
