import importlib
import src.lib.colors as cl
from src.utils.basics import cls, terminal, quest

def get_function(module_name, function_name="main"):
    return getattr(importlib.import_module(f"src.services.windows.modules.{module_name}.worker"), function_name)

def main(action="all"):
    if (action == "all"):
        for module in ["cleaner", "configurator", "network", "troubleshooter", "uninstaller"]:
            get_function(module)()
    else: get_function(action)()