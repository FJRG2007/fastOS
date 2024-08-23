import src.lib.colors as cl
from src.utils.basics import terminal, fileManager
import os, json, winreg, shutil, requests, subprocess

def is_program_installed(program_name, paths=None):
    if paths:
        # Check if the executable exists in any of the specified paths.
        for path in paths:
            if os.path.exists(path): return True
    # Check if program is installed via PATH (for executables).
    if shutil.which(program_name): return True
    # Check via Windows registry.
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall") as key:
            i = 0
            while True:
                try:
                    with winreg.OpenKey(key, winreg.EnumKey(key, i)) as subkey:
                        if program_name.lower() in winreg.QueryValueEx(subkey, "DisplayName")[0].lower(): return True
                    i += 1
                except OSError: break
    except OSError as e: terminal("e", f"Error accessing the registry: {e}")
    return False

def download_file(url, local_path):
    # Downloads a file from a URL and saves it locally
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(local_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk: f.write(chunk)
    else: terminal("e", f"Error downloading the file. Status code: {response.status_code}")

def install_executable(url, local_filename, name, paths=None):
    if is_program_installed(local_filename, paths): return terminal("s", f"{cl.BOLD}{name}{cl.ENDC} is already installed.", newline=False)
    print(f"Downloading the installer from {url}...")
    local_path = fileManager("executables", local_filename)
    # Download the executable.
    download_file(url, local_path)
    # Install the executable.
    try:
        if local_filename.endswith(".msi"):
            # Install MSI files using msiexec.
            print("📥 Installing the MSI installer...", os.path.abspath(local_path))
            subprocess.run(["msiexec", "/i", os.path.abspath(local_path), "/quiet"], check=True)
        else:
            # For other executables, just run them directly.
            print("📥 Installing the executable...")
            subprocess.run([local_path], check=True)
        terminal("s", f"{cl.BOLD}{name}{cl.ENDC} installation complete.", newline=False)
    except subprocess.CalledProcessError as e: terminal("e", f"Error during installation: {e}", newline=False)
    except OSError as e:
        if e.winerror == 216: terminal("e", f"{name} is not compatible with your version of Windows.", newline=False)
        if e.winerror == 1392: terminal("e", f"{local_filename} is corrupted and unreadable.", newline=False)
    finally:
        print(f"🗑️ Deleting the {cl.BOLD}{name}{cl.ENDC} installer...", newline=False)
        try:
            os.remove(local_path)
            terminal("s", f"{local_filename} ({name}) has been deleted.", newline=False)
        except FileNotFoundError: terminal("e", f"{local_filename} ({name}) not found for deletion.", newline=False)
        except PermissionError: terminal("e", f"Error: Permission denied while trying to delete {local_filename} ({name}).", newline=False)
        except OSError as e: terminal("e", f"Error running {local_filename} ({name}): {e}", newline=False)
        finally: 
            if os.path.exists(local_path): os.remove(local_path)

def main():
    print("Installing security programs and basic utilities...")
    with open("src/services/windows/modules/configurator/modules/installer/programs.json", "r") as file:
        data = json.load(file)
    for program in data["basic"]:
        install_executable(program["url"], program["filename"], program["name"], program.get("paths", []))
    terminal("s", "All downloads complete.")