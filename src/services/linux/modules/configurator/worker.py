from src.utils.basics import terminal

from .modules.installer.worker import main as mainInstaller

def main():
    # Install security programs and basic utilities.
    mainInstaller()