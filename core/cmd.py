import os, time, sys, subprocess, urllib.request
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from core.logger import get_logger
from core import ai
from core.config import VERSION, GITHUB_VERSION_URL, update_setting, get_setting

logger = get_logger(__name__)
console = Console()

'''
HELPS MENUS
'''

def show_menu():
    if get_setting("clear_before_menu"): clear()

    logo = (
        " ____  ______  _               \n"
        "|  _ \\|  ____ | |              \n"
        "| |_) | |__   | | _____      __\n"
        "|  _ <|  __|  | |/ _ \\ \\ /\\ / /\n"
        "| |_) | |____ | | (_) \\ V  V / \n"
        "|____/|______ |_|\\___/ \\_/\\_/  \n"
    )

    v_text = f"v {VERSION} (Beta)".center(31)
    full_text = f"{logo}\n{v_text}"

    console.print(Panel(full_text, style="bold cyan", border_style="blue", padding=(1, 2), expand=False))

def print_markdown(text):
    console.print(Markdown(text))

def print_info(text, title="BELOW"):
    console.print(Panel(text, title=title, border_style="green", expand=False))

def print_error(text):
    console.print(f"[bold red] [ERROR]:[/bold red] {text}")

def clear():
    if os.name == 'nt':
        os.system('cls')
    else: 
        os.system('clear')

def get_app_version(): 
    return f"BELOW version {VERSION}"

def show_cosmetic_menu():
    if get_setting("clear_before_menu"):
        clear()
    print("""
=======================================================================================
                          COSMETIC COMMANDS HELP MENU
=======================================================================================

COSMETIC COMMANDS:
    -h, --help [base|ai|csmt] Show this help message
    -s, --settings            Show all current program settings
    -c, --clear               Clear the terminal screen
          
    --autoclear [on|off]      Toggle auto-clearing the screen before showing the menu
    --autoupdate [on|off]     Toggle automatic update check on startup     

=======================================================================================
""")

def show_base_help_menu():
    if get_setting("clear_before_menu"):
        clear()
    print("""
====================================================================
                       BASE COMMANDS HELP MENU
====================================================================

BASE COMMANDS:
    -v, --version [up]        Checking for updates
    -m, --model [path]        View current model or set a new one
    -p, --project <path>      Set the project workspace directory
    -ctx, --context <size>    Set the context size for the AI model (e.g., -ctx 2048)
    --memory [on|off|s]       Enable, disable, or check history status
          
    -r, --restart             Restart the program
    -e, --exit                Exit the program
          
====================================================================
    """)

def show_ai_help_menu():
    if get_setting("clear_before_menu"):
        clear()
    print("""
====================================================================
                       AI COMMANDS HELP MENU
====================================================================

USAGE:
  <command> [arguments]

AI COMMANDS:
    ai "<prompt>"               Ask a general question
    ai file <name> ["prompt"]   Analyze a file (optional custom prompt)
    ai project                  Run full project analysis

    ai save <name>              Save current session to a file
    ai load <name>              Load a session from a file
          
====================================================================
    """)

def show_full_help_menu():
    if get_setting("clear_before_menu"):
        clear()
    print("""
====================================================================
                  ____  _____ __     _____  __    __
                  ||=)  ||==  ||    ((   )) \\ /\ //
                  ||_)) ||___ ||__|  \\_//   \V/\V/  
====================================================================
Code analysis & AI helper for local projects.
--------------------------------------------------------------------

USAGE:
  <command> [arguments]

BASE COMMANDS:
    -m, --model [path]        View current model or set a new one
    -p, --project <path>      Set the project workspace directory
    -astr [on|off]            Toggle auto start AI
    -ctx, --context <size>    Set the context size for the AI model
    --memory [on|off|s]       Enable, disable, or check history status
  
    -r, --restart             Restart the program
    -e, --exit                Exit the program

AI COMMANDS:
    ai "<prompt>"             Ask a general question
    ai file <name> ["prompt"] Analyze a file (optional custom prompt)
    ai project                Run full project analysis
    ai save <session_name>    Save current session to a file
    ai load <session_name>    Load a session from a file          

COSMETIC COMMANDS:
    -h, --help [base|ai|csmt] Show this help message
    -s, --settings            Show all current program settings      
    -c, --clear               Clear the terminal screen
          
    --autoclear [on|off]      Toggle auto-clearing the screen 
    --autoupdate [on|off]     Toggle automatic update check on startup
          
====================================================================
    """)

def show_settings():
    
    if get_setting("clear_before_menu"):
        clear()

    print("\n" + "="*40)
    print(f"       SYSTEM SETTINGS (v{VERSION})")
    print("="*40)
    
    # Take all relevant settings and format them for display
    settings = {
        "Model Path": get_setting("model") or "Not set",
        "Context Size": get_setting("ctx_size"),
        "Memory (History)": "ON" if get_setting("record_history") else "OFF",
        "Auto-clear Menu": "ON" if get_setting("clear_before_menu") else "OFF",
        "Auto-update Check": "ON" if get_setting("auto_update_check") else "OFF", # <--- НОВИЙ РЯДОК
        "Project Path": get_setting("project_path") or "Not set"
    }
    
    for key, value in settings.items():
        # Format the output to align values
        print(f"{key:<20}: {value}")
        
    print("="*40 + "\n")

'''
UTILITY FUNCTIONS
'''

def clear():
    if os.name == 'nt':
        os.system('cls')
        sys.stdout.write('\033[3J\033[H')
    else:
        os.system('clear')
    sys.stdout.flush()

def print_smoothly(text, delay=0.03):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def set_auto_clear(state: bool):
    update_setting("clear_before_menu", state)
    status = "ON" if state else "OFF"
    return f"Auto-clear before menu is now {status}"

'''
APP MANAGER
'''
def get_app_version():
    return f"Current Version: {VERSION}v"

def check_for_updates(manual_check=False):
    """Checks for updates on GitHub. If available, prompts to download and apply."""
    try:
        if manual_check:
            print("Checking for updates on GitHub...")
            
        with urllib.request.urlopen(GITHUB_VERSION_URL, timeout=5) as response:
            remote_version = response.read().decode('utf-8').strip()
            
        if not remote_version:
            return "Error: Empty version received." if manual_check else None

        no_cache_url = f"{GITHUB_VERSION_URL}?t={int(time.time())}"
        
        with urllib.request.urlopen(no_cache_url, timeout=5) as response:
            remote_version = response.read().decode('utf-8').strip()

        def parse_version(v):
            return tuple(map(int, v.split('.')))

        # Check if remote version is strictly greater than the local version
        if parse_version(remote_version) > parse_version(VERSION):
            print(f"\n[UPDATE AVAILABLE] v{VERSION} -> v{remote_version}")
            
            # Ask the user for confirmation
            ans = input("Do you want to download and apply the update now? [y/n]: ").strip().lower()
            
            if ans in ('y', 'yes'):
                print("Pulling updates from GitHub...")
                try:
                    # Execute 'git pull' command in the terminal
                    subprocess.run(["git", "pull"], check=True)
                    print("\nUpdate successful!")
                    
                    # Offer to restart the program immediately to apply changes
                    ans_restart = input("Restart program to apply changes? [y/n]: ").strip().lower()
                    if ans_restart in ('y', 'yes'):
                        restart_program() 
                        
                except subprocess.CalledProcessError as e:
                    print(f"\n[ERROR] Failed to pull updates. (You might have uncommitted local changes)")
                    print("Try running 'git commit' first, or 'git pull' manually.")
            else:
                print("Update skipped. You can update later using '-v up'.")
                
            return None # Output is already printed, no need to return a string
            
        else:
            # If no updates are available
            if manual_check:
                print(f"You are using the latest version (v{VERSION}).")
            return None 

    except urllib.error.URLError:
        return "Error: No internet connection." if manual_check else None
    except Exception as e:
        logger.exception(f"Update error: {e}")
        return f"Error checking updates: {e}" if manual_check else None

def set_auto_update(state: bool):
    update_setting("auto_update_check", state)
    status = "ON" if state else "OFF"
    return f"Auto-update check on startup is now {status}"

'''
PROJECT MANAGER
'''

def read_file(name):
    p_path = get_project()
    if not p_path:
        return None

    for root, _, files in os.walk(p_path):
        for f in files:
            if f == name:
                with open(os.path.join(root, f), "r", encoding="utf-8") as file:
                    return file.read()
    return None

def get_project():
    return get_setting("project_path")

def set_project(path):
    if not os.path.exists(path):
        return "Invalid path"
    update_setting("project_path", path)
    return f"Project set: {path}"

def restart_program():
    print("\nRestarting...")
    sys.stdout.flush()
    time.sleep(0.5)
    cmd = f'start python "{sys.argv[0]}"'
    subprocess.Popen(cmd, shell=True)
    os._exit(0)
 
def exit_program():
    os._exit(0)