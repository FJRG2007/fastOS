from pathlib import Path
import os, shutil, tempfile
from src.utils.basics import terminal

def delete_folder_contents(folder_path):
    # Deletes the contents of a folder.
    if os.path.exists(folder_path):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            try:
                if os.path.isdir(item_path): shutil.rmtree(item_path)
                else: os.remove(item_path)
            except Exception as e: terminal("e", f"Error deleting {item_path}: {e}")

def clear_temp_files():
    # Deletes temporary files from the system.
    delete_folder_contents(tempfile.gettempdir())

def clear_cache():
    # Deletes browser cache (Chrome and Firefox).
    # Cache path for Google Chrome.
    chrome_cache = Path("~/Library/Caches/Google/Chrome/Default/Cache").expanduser()
    if chrome_cache.exists(): delete_folder_contents(chrome_cache)
    
    # Cache path for Firefox.
    firefox_cache = Path("~/Library/Application Support/Firefox/Profiles").expanduser()
    for profile in firefox_cache.glob("*"):
        cache_folder = profile / "cache2"
        if cache_folder.exists(): delete_folder_contents(cache_folder)
    
    # Cache path for Epic Games Launcher
    epic_cache_path = Path("~/Library/Caches/com.epicgames.EpicGamesLauncher/webcache").expanduser()
    if epic_cache_path.exists():
        try:
            shutil.rmtree(epic_cache_path)
            terminal("s", "Removed Epic Games cache: webcache")
        except Exception as e: terminal("e", f"Error deleting {epic_cache_path}: {e}")
    else: terminal("i", "Epic Games webcache not found.")

def empty_trash():
    # Empties the trash on macOS.
    try:
        os.system("rm -rf ~/.Trash/*")
        terminal("s", "Trash emptied successfully.")
    except Exception as e:
        terminal("e", f"Error emptying Trash: {e}")

def main():
    print("Starting cleanup...")
    clear_temp_files()
    clear_cache()
    empty_trash()
    terminal("s", "Cleanup completed.")