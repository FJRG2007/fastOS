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
    chrome_cache = Path.home() / ".config/google-chrome/Default/Cache"
    if chrome_cache.exists(): delete_folder_contents(chrome_cache)
    
    # Cache path for Firefox.
    for profile in Path.home() / ".mozilla/firefox".glob("*"):
        cache_folder = profile / "cache2"
        if cache_folder.exists(): delete_folder_contents(cache_folder)

def remove_uninstalled_program_files():
    # Deletes files from programs that are no longer installed.
    # This is a common place where some programs leave remnants.
    # Be cautious with deletion.
    remove_paths = [
        Path.home() / ".local/share"
        # ...
    ]
    for path in remove_paths:
        delete_folder_contents(path)

def empty_trash():
    # Empties the trash can.
    trash_path = Path.home() / ".local/share/Trash"
    if trash_path.exists():
        delete_folder_contents(trash_path / "files")
        delete_folder_contents(trash_path / "info")

def main():
    print("Starting cleanup...")
    clear_temp_files()
    clear_cache()
    empty_trash()
    remove_uninstalled_program_files()
    terminal("s", "Cleanup completed.")