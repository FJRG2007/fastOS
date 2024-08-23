import src.lib.colors as cl
import os, sys, ctypes, tempfile, subprocess
from src.utils.basics import quest, terminal

options = [
    ("1", f"Complete {cl.y}(+45mins approx.){cl.w}"),
    ("2", f"Quick {cl.y}(1-10mins approx.){cl.w}")
]

def display_menu():
    # Display the menu options.
    terminal("info", f"Select an option below to continue.")
    for i, (number, name) in enumerate(options, 1):
        print(f"{cl.b}[{cl.w}{number}{cl.b}]{cl.w} {name}")
        # Add separator for visual clarity every 3 items.
        if i % 3 == 0 and i != len(options): print(f" {cl.w}|")

def run_bat_as_admin(script_path):
    # Creates and runs a PowerShell script to execute a .bat file as an administrator.
    with tempfile.NamedTemporaryFile(delete=False, suffix='.ps1') as temp_script:
        # Write the PowerShell script to run the .bat file as admin
        temp_script.write(f"""
        Start-Process powershell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -Command "Start-Process cmd.exe -ArgumentList '/c {script_path}' -Verb RunAs"' -Verb RunAs
        """.encode())
    try: subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", temp_script.name], check=True)
    except subprocess.CalledProcessError as e: terminal("e", f"Error executing PowerShell script: {e}")
    finally: os.remove(temp_script.name)

def run_command(command):
    # Executes a command and prints its output and errors.
    try:
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"Command: {" ".join(command)}")
        print("STDOUT:\n", result.stdout)
        print("STDERR:\n", result.stderr)
    except subprocess.CalledProcessError as e:
        if e.returncode == 740:
            terminal("e", f"Error executing {" ".join(command)}: Elevated permissions are required.")
            print("STDOUT:\n", e.stdout)
            print("STDERR:\n", e.stderr)
            # Attempt to re-run the script with elevated privileges
            if os.name == "nt":
                try:
                    # Attempt to re-run the script with elevated privileges.
                    ctypes.windll.shell32.ShellExecuteW(
                        None,
                        "runas",
                        sys.executable,
                        f'"{os.path.abspath(sys.argv[0])}" {" ".join(sys.argv[1:])}',
                        None,
                        1
                    )
                    sys.exit()  # Exit the current instance
                except Exception as e:
                    terminal("e", f"Failed to elevate privileges: {e}")
                    sys.exit(1)
        else:
            terminal("e", f"Error executing {" ".join(command)}: {e}")
            print("STDOUT:\n", e.stdout)
            print("STDERR:\n", e.stderr)

def main():
    while True:
        display_menu()
        # Validate the user selection.
        level = quest("Select a number")
        if level not in dict(options).keys():
            terminal("e", "Invalid selection. Please choose a valid option.")
            continue
        # Determine the level based on the selection.
        level = "complete" if level == "1" else "quick"
        # Run the selected commands.
        for command in [cmd for cmd, cmd_level in [
            # Repairs Windows image.
            (["DISM", "/Online", "/Cleanup-Image", "/RestoreHealth"], "complete"),
            # Scans and fixes corrupted system files.
            (["sfc", "/scannow"], "quick"),
            # Checks disk for errors and repairs them.
            (["chkdsk", "C:", "/f", "/r"], "complete"),
            # Resets network settings (Winsock).
            (["netsh", "winsock", "reset"], "quick"),
            # Clears the DNS cache.
            (["ipconfig", "/flushdns"], "quick"),
            # Disable hibernation.
            (["powercfg", "-h", "off"], "quick")
            # Run Disk Cleanup.
            (["Cleanmgr", "/sagerun:1"], "complete"),
            # Optimize the volume.
            (["powershell.exe", "-Command", "Optimize-Volume -DriveLetter C -ReTrim -Verbose"], "complete")
        ] if level == "complete" or cmd_level == level]: run_command(command)
        if (level == "complete"):
            for filename in os.listdir("src/services/windows/modules/troubleshooter/scripts"):
                if filename.endswith('.bat'):
                    file_path = os.path.join("src/services/windows/modules/troubleshooter/scripts", filename)
                    print(f"Executing {file_path} as administrator...")
                    try: subprocess.run(f'powershell Start-Process cmd.exe -ArgumentList "/c {os.path.abspath(file_path)}" -Verb RunAs', check=True, shell=True)
                    except subprocess.CalledProcessError as e: run_bat_as_admin(os.path.abspath(file_path))
        break