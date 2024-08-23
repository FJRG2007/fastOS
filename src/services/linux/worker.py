import importlib
import src.lib.colors as cl
from src.utils.basics import cls, terminal, quest

def get_function(module_name, function_name="main"):
    return getattr(importlib.import_module(f"src.services.linux.modules.{module_name}.worker"), function_name)

def main(distro, action="all"):
    if (action == "all"):
        for module in ["cleaner", "configurator", "troubleshooter", "uninstaller"]:
            get_function(module)(distro)
    else: get_function(action)(distro)