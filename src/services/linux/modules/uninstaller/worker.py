import json, subprocess
from src.utils.basics import terminal

# Function to run bash commands from Python.
def run_bash_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Command executed successfully: {command}")
    except subprocess.CalledProcessError as e: print(f"Error executing command: {command}\n{e}")

# Function to uninstall bloatware applications using apt, dnf, or snap (depending on the distro).
def uninstall_bloatware(bloatware_apps):
    for app in bloatware_apps:
        # Attempt to uninstall the application via apt (Debian/Ubuntu), dnf (Fedora/RHEL), or snap.
        print(f"Attempting to uninstall {app}...")
        # First, try using apt for Debian-based systems.
        run_bash_command(f"sudo apt remove --purge -y {app}")
        # If it's not an apt package, try dnf for Fedora-based systems.
        run_bash_command(f"sudo dnf remove -y {app}")
        # Finally, try to remove it via snap if it was installed as a snap package.
        run_bash_command(f"sudo snap remove {app}")

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