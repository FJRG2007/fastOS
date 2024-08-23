import importlib
import src.lib.colors as cl
from src.utils.basics import cls, terminal, get_os_info, quest

def get_function(module_name, function_name="main"):
    return getattr(importlib.import_module(f"src.services.{module_name}.worker"), function_name)

options = [
    ("1", "all", f"All {cl.y}(Default){cl.w}"),
    ("2", "cleaner", f"Cleaner {cl.y}(Removes cache, uninstalled program files, etc.){cl.w}"),
    ("3", "configurator", f"Configurator {cl.y}(Improved performance and safety){cl.w}"),
    ("4", "troubleshooter", f"Troubleshooter {cl.y}(Improve performance and troubleshoot problems){cl.w}"),
    ("5", "uninstaller", f"Uninstaller {cl.y}(Removes bloatware and unnecessary apps){cl.w}")
]

def display_menu():
    # Display the menu options.
    terminal("info", f"Select an option below to continue.")
    for i, (number, key, name) in enumerate(options, 1):
        print(f"{cl.b}[{cl.w}{number}{cl.b}]{cl.w} {name}")
        # Add separator for visual clarity every 3 items.
        if i % 3 == 0 and i != len(options): print(f" {cl.w}|")

def main():
    os_info = get_os_info()
    while True:
        display_menu()
        selector = quest("Select a number")
        # Validate and parse the selector.
        try:
            index = int(selector) - 1
            if 0 <= index < len(options):
                cls()
                if os_info["slug"] and os_info["slug"] != "error": get_function(os_info["slug"])(os_info["distribution_slug"], options[index][1]) if os_info["slug"] == "linux" else get_function(os_info["slug"])(options[index][1])
                break  # Exit the loop if a valid option was processed.
            else: raise ValueError("Invalid selection")
        except ValueError as e: terminal("e", f"Invalid input: {e}")