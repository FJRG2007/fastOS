import src.lib.colors as cl
import os, json, subprocess
from src.utils.basics import terminal

def execute_commands(commands):
    # Execute a list of shell commands.
    for cmd in commands:
        print(f"Executing command: {cmd}")
        subprocess.run(cmd, shell=True, check=True)

def install_program(program):
    name = program["name"]
    # Detect the distribution.
    distro_slug = os.popen("lsb_release -cs").read().strip()
    for distro in program["distros"]:
        if distro_slug in distro["compatibility"]:
            print(f"Installing {name} on {distro_slug}...")
            execute_commands(distro["cmd"])
            terminal("s", f"{cl.BOLD}{name}{cl.ENDC} installation complete.", newline=False)
            break
    else: terminal("e", f"No compatible distribution found for {name}.", newline=False)

def main():
    print("Installing security programs and basic utilities...")
    with open("src/services/linux/modules/configurator/modules/installer/programs.json", "r") as file:
        data = json.load(file)
    for program in data["basic"]:
        install_program(program)
    terminal("s", "All installations complete.")