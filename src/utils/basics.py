import os, re, platform
import src.lib.colors as cl
from rich.panel import Panel
from rich import print as rprint
from rich.console import Console
from urllib.parse import urlparse
from rich.markdown import Markdown
import os, re, sys, time, ctypes, subprocess

try: import distro
except ImportError: distro = None

def get_os_info():
    osName = platform.system()
    response = { "os": osName, "slug": osName.lower(), "version": platform.release() }
    if response["slug"] == "windows":
        try: is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        except: is_admin = False
        if not is_admin: ctypes.windll.shell32.ShellExecuteW(None, "runas", "powershell.exe", f'powershell -Command "python "{sys.argv[0]}" {" ".join(sys.argv[1:])}"', None, 1)
        if distro: response["distribution"] = distro.linux_distribution(full_distribution_name=False)[0]
        else:
            try:
                with open('/etc/os-release') as f:
                    for line in f:
                        if line.startswith('NAME='):
                            response["distribution"] = line.split("=")[1].strip().replace('"', "")
                            break
            except Exception as e: response["distribution"] = "Unknown"
        response["distribution_slug"] = response["distribution"].lower()
    # Enabling root permissions in Unix/Linux distributions.
    elif response["slug"] == "linux" and os.geteuid() != 0: 
        try: subprocess.check_call(["sudo", sys.executable] + sys.argv)
        except subprocess.CalledProcessError as e: terminal("e", f"Failed to elevate privileges: {e}")
    return response

console = Console()

def cls() -> None:
    print(f"{cl.b}{cl.ENDC}", end="")
    if sys.platform == "win32": os.system("cls")
    else: os.system("clear")

def coloredText(word, hex_color) -> str:
    try:
        if not word.startswith("#"): word = f"#{str(word)}"
        rgb = tuple(int(hex_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        return f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m{str(word)}\033[0m"
    except: return word

def quest(prompt, newline=False, lowercase=False, tab=False, format_type=str):
    prefix = f"\n" if newline else ''
    prefix += f"\t" if tab else ''
    while True:
        try:
            response = input(f"{prefix}{cl.b}[{cl.w}?{cl.b}]{cl.w} {prompt}: ")
            if format_type == int: return int(response)
            elif format_type == str and lowercase: return response.lower()
            return response
        except ValueError: terminal("e", "Enter a valid value.", timer=True)

def getPositive(q, default=True) -> bool:
    positive_responses = ["y", "yes", "yeah", "continue", "s", "si", "sí", "oui", "wa", "ja"]
    if default: positive_responses.append("")
    return q.lower() in positive_responses

def noToken(name) -> str: 
    return f"{cl.y}Set up your {name} token.{cl.w}"

def validURL(url) -> bool:
    try:
        r = urlparse(url)
        return all([r.scheme, r.netloc])
    except ValueError: return False
    
def getTypeString(v) -> str:
    if re.match(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$', v): return "email"
    elif re.match(r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$', v): return "tel"
    else: return "unknown"
    
def setColor(v):
    return f"{cl.g}True{cl.w}" if v == "True" or v == True else \
           f"{cl.r}False{cl.w}" if v == "False" or v == False else \
           f"{cl.r}{v}{cl.w}" if any(term in str(v).lower() for term in ["not", "error"]) else \
           f"{cl.y}{v}{cl.w}" if any(term in str(v).lower() for term in ["coming soon"]) else \
           f"{v}"

def validTarget(target) -> bool:
    # Validate IP address (IPv4).
    if re.compile(r"^(\d{1,3}\.){3}\d{1,3}$").match(target):
        if all(0 <= int(part) <= 255 for part in target.split(".")): return True
    # Validate domain.
    return re.compile(r"^(?=.{1,253}$)(?:(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,10}$").match(target)

def terminal(typeMessage, string="", exitScript=False, clear="n", newline=True, timer=False) -> None:
    if (clear == "b" or typeMessage == "iom"): cls()
    if isinstance(typeMessage, str):
        if typeMessage == "e": print(f"\n{cl.R} ERROR {cl.w} {string}") # X or ❌
        if typeMessage == "s": print(f"\n{cl.g}✅ {string}{cl.w}") # ✓ or ✅
        if typeMessage == "i": rprint(f"{'\n' if newline else ''}[cyan]{string}[/cyan]")
        if typeMessage == "w": rprint(f"\n[bold yellow]Warning:[/bold yellow] [yellow]{string}[/yellow]")
        if typeMessage == "h": print(f"\n{cl.B}💡 TIP {cl.w} {string}") # X or ❌
        if typeMessage == "nmi": print(f"\n{cl.R} ERROR {cl.w} Could not install {string}. Please install it manually.")
        if typeMessage == "nei": print(f"\n{cl.R} ERROR {cl.w} {string} is not installed or not found in PATH. Please install it manually.")
        if typeMessage == "l": print("\nThis may take a few seconds...")
        if typeMessage == "ai": 
            console.print(Panel(Markdown(string), title="Model's Response", title_align="left", expand=False, style="bold white"))
        if typeMessage == "info": console.print(Panel(Markdown(string), title="FastOS", title_align="left", expand=False, style="bold white"))
        if typeMessage == "iom": 
            print(f"\n{cl.R} ERROR {cl.w} Please enter a valid option.")
            time.sleep(2)
    elif isinstance(typeMessage, type) and issubclass(typeMessage, BaseException):
        if typeMessage == KeyboardInterrupt: print(f"\n{cl.R} ERROR {cl.w} Exiting Program: Canceled by user.")
        sys.exit(1)
    else: print(f"\nUnhandled typeMessage: {typeMessage}")
    if exitScript: sys.exit(1 if typeMessage == "e" else 0)
    if clear == "a" or typeMessage == "iom": cls()
    if timer: time.sleep(2)

def fileManager(path, filename, create=True):
    directory = f"disposable/{path}/{filename}"
    filename = re.sub(r'[^A-Za-z0-9._@-]', "", filename)
    if create: os.makedirs(os.path.dirname(directory), exist_ok=True)
    return directory