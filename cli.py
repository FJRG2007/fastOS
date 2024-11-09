from dotenv import load_dotenv
from src.utils.FastOS import FastOS
from textual.widgets import Markdown
from src.lib import data, colors as cl
from src.utils.basics import cls, terminal
from textual.app import App, ComposeResult
import sys, click, ctypes, pyfiglet, importlib

def get_function(module_name, function_name="main", clearTerminal=True):
    if clearTerminal: cls()
    return getattr(importlib.import_module(f"src.services.{module_name}.worker"), function_name)

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    cls()
    print(pyfiglet.figlet_format("FastOS"))
    print(f'\n{cl.des_space}{cl.b}>> {cl.w}Welcome to FastOS, remember to use it responsibly. \n{cl.des_space}{cl.b}>> {cl.w}Join to our Discord server on tpe.li/dsc\n{cl.des_space}{cl.b}>> {cl.w}Version: {data.version}\n')
    if not sys.version[0] in "3": return terminal("e", "FastOS only works properly with Pytnon 3. Please upgrade/use Python 3.", exitScript=True)
    load_dotenv(override=True)
    if ctx.invoked_subcommand is None: get_function("central", clearTerminal=False)()

@cli.command()
@click.argument("section", required=False)
def help(section):
    get_function("help")(section)

@cli.command()
def info():
    with open("README.md", "r", encoding="utf-8") as file:
        content = file.read()
        class MarkdownExampleApp(App):
            def compose(self) -> ComposeResult:
                yield Markdown(content)
        MarkdownExampleApp().run()

def is_admin():
    # Check if the script is running as an administrator.
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

def run_as_admin():
    # Restart the script with admin privileges.
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

def main():
    if not is_admin():
        print("Requesting admin privileges...")
        run_as_admin()
        sys.exit(0)
    try: cli()
    except KeyboardInterrupt as e: terminal(KeyboardInterrupt)
    except FastOS.InvalidOption as e: terminal("iom")

if __name__ == "__main__": main()