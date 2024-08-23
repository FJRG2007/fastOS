from pathlib import Path
import os, shutil, ctypes, tempfile
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
    # Cache path for Google Chrome
    chrome_cache = Path(os.getenv("LOCALAPPDATA")) / "Google/Chrome/User Data/Default/Cache"
    if chrome_cache.exists(): delete_folder_contents(chrome_cache)
    
    # Cache path for Firefox
    firefox_cache = Path(os.getenv("APPDATA")) / "Mozilla/Firefox/Profiles"
    for profile in firefox_cache.glob("*"):
        cache_folder = profile / "cache2"
        if cache_folder.exists(): delete_folder_contents(cache_folder)

def empty_recycle_bin():
    # Empties the recycle bin.
    ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 1)

def remove_uninstalled_program_files():
    # Deletes files from programs that are no longer installed.
    # This is a common place where some programs leave remnants.
    # Be cautious with deletion.
    delete_folder_contents(Path(os.getenv("PROGRAMDATA")))

def main():
    print("Starting cleanup...")
    clear_temp_files()
    clear_cache()
    empty_recycle_bin()
    remove_uninstalled_program_files()
    print("Cleanup completed.")