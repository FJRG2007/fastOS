import json, subprocess
from src.utils.basics import terminal

# Function to run PowerShell commands from Python.
def run_powershell_command(command):
    try:
        subprocess.run(["powershell", "-Command", command], check=True)
        print(f"Command executed successfully: {command}")
    except subprocess.CalledProcessError as e: print(f"Error executing command: {command}\n{e}")

# Function to uninstall bloatware applications.
def uninstall_bloatware(bloatware_apps):
    for app in bloatware_apps:
        run_powershell_command(f"Get-AppxPackage {app} | Remove-AppxPackage")

def main():
    print("Starting the uninstallation of bloatware applications...")
    # Load the bloatware apps list from bloatware.json.
    try:
        with open("src/services/windows/modules/uninstaller/bloatware.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            basic_apps = data.get("basic", [])
            web_apps = data.get("web_apps", [])
            if basic_apps:
                print("Uninstalling basic applications...")
                uninstall_bloatware(basic_apps)
            if web_apps:
                print("Uninstalling web applications...")
                uninstall_bloatware(web_apps)
            if not basic_apps and not web_apps: terminal("e", "No bloatware apps found in 'basic' or 'web_apps' sections.")
    except FileNotFoundError: terminal("e", "bloatware.json file not found.")
    except json.JSONDecodeError: terminal("e", "Failed to parse bloatware.json.")
    terminal("s", "Bloatware uninstallation process completed.")