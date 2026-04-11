import os
import time
import sys
import subprocess
from turtle import clear
from core.ai import current_model, change_model
from core.config import update_setting, get_setting


def get_or_set_model():
    model = current_model()
    if model:
        return model
    
    # If no model is set, ask the user to input one
    model = ""
    while not model:
        model = input("Enter model: ").strip()
        if not model:
            print("ERROR: Model name cannot be empty.")
            
    # Save the model to the config file and update the global variable
    change_model(model)
    return model

'''
HELP MENUS
'''

def show_menu():
    clear()
    print("""
============================================================
                AI DEVELOPMENT ASSISTANT
============================================================
    """)

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
                      AI DEVELOPMENT ASSISTANT
====================================================================
Code analysis & AI helper for local projects.
--------------------------------------------------------------------

USAGE:
  <command> [arguments]

BASE COMMANDS:
    -m, --model [path]        View current model or set a new one
    -p, --project <path>      Set the project workspace directory
    -ctx, --context <size>    Set the context size for the AI model (e.g., -ctx 2048)
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
          
====================================================================
    """)

def show_settings():
    
    if get_setting("clear_before_menu"):
        clear()

    print("\n" + "="*40)
    print("       CURRENT SYSTEM SETTINGS")
    print("="*40)
    
    # Take all relevant settings and format them for display
    settings = {
        "Model Path": get_setting("model") or "Not set",
        "Context Size": get_setting("ctx_size"),
        "Memory (History)": "ON" if get_setting("record_history") else "OFF",
        "Auto-clear Menu": "ON" if get_setting("clear_before_menu") else "OFF",
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
Project management
'''

def read_file(name):
    if not project_path:
        return None

    for root, _, files in os.walk(project_path):
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