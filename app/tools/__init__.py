import importlib
import inspect
import pkgutil
from pathlib import Path


def load_tools() -> list:
    tools = []
    package_path = str(Path(__file__).parent)
    for module_info in pkgutil.iter_modules([package_path]):
        module = importlib.import_module(f"app.tools.{module_info.name}")
        exports = getattr(module, "__all__", None)
        for name, obj in inspect.getmembers(module, inspect.isfunction):
            if obj.__module__ != module.__name__:
                continue
            if exports is not None and name not in exports:
                continue
            if name.startswith("_"):
                continue
            tools.append(obj)
    return tools
