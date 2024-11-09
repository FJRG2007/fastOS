from src.utils.terminal import win_run_command
import os, tempfile, subprocess, src.lib.colors as cl
from src.utils.basics import quest, terminal, getPositive

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
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ps1") as temp_script:
            temp_script_path = temp_script.name
        
            # Write the PowerShell script to run the .bat file as admin
            script_content = f"""
            Start-Process cmd.exe -ArgumentList '/c \"{script_path}\"' -Verb RunAs
            """
            temp_script.write(script_content.encode())
        result = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", temp_script_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("PowerShell script executed successfully.")
        print("STDOUT:\n", result.stdout)
        print("STDERR:\n", result.stderr)
    except subprocess.CalledProcessError as e: 
        terminal("e", f"Error executing PowerShell script: {e}")
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
            (["DISM", "/Online", "/Cleanup-Image", "/ScanHealth"], "complete"),
            (["DISM", "/Online", "/Cleanup-Image", "/RestoreHealth"], "complete"),
            (["DISM", "/Online", "/Cleanup-Image", "/StartComponentCleanup"], "complete"),
            # Disable Recall feature.
            (["Dism", "/Online", "/Disable-Feature", "/Featurename:Recall", "2>nul"], "complete"),
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
        ] if level == "complete" or cmd_level == level]: win_run_command(command)
        if (level == "complete"):
            for filename in os.listdir("src/services/windows/modules/troubleshooter/scripts"):
                if filename.endswith(".bat"):
                    print(f"Executing {filename} as administrator...")
                    run_bat_as_admin(os.path.abspath(os.path.join("src/services/windows/modules/troubleshooter/scripts", filename)))
        if getPositive(quest("Do you want to restart your computer (recommended)?")): os.system("shutdown /r /t 0")
        break