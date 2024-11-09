import os, sys, ctypes, subprocess
from src.utils.basics import terminal

def win_run_command(command):
    # Executes a command and prints its output and errors.
    try:
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"Command: {" ".join(command).strip()}")
        if result.stdout.strip(): print("STDOUT:\n", result.stdout.strip())
        if result.stderr.strip(): print("STDERR:\n", result.stderr.strip())
    except subprocess.CalledProcessError as e:
        if e.returncode == 740:
            terminal("e", f"Error executing {" ".join(command)}: Elevated permissions are required.")
            terminal("e", f"Error Code: {e.returncode}")
            terminal("e", f"Command Output: {e.output}")
            terminal("e", f"Command Error Output: {e.stderr}")
            # Attempt to re-run the script with elevated privileges.
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
                    sys.exit()
                except Exception as e:
                    terminal("e", f"Failed to elevate privileges: {e}")
                    sys.exit(1)
        else:
            terminal("e", f"Error executing {" ".join(command)}: {e}")
            print("STDOUT:\n", e.stdout)
            print("STDERR:\n", e.stderr)