import importlib
from src.utils.basics import cls
from src.utils.basics import get_os_info

def get_function(module_name, function_name="main"):
    return getattr(importlib.import_module(f"src.services.{module_name}.worker"), function_name)

def main():
    os_info = get_os_info()
    print(os_info)
    if (os_info["slug"] and os_info["slug"] != "error"): return get_function(os_info["slug"])