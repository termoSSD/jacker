import os
import time
import sys
import subprocess
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
Cosmetics:
- Smooth printing
- Clear console
'''

def show_menu():
    clear()
    print("""
============================================================
                AI DEVELOPMENT ASSISTANT
============================================================
    """)

def show_help_menu():
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
  -h, --help                Show this help message
  -c, --clear               Clear the terminal screen
  -m, --model [name]        View current model or set a new one
  -p, --project <path>      Set the project workspace directory
  --memory [on|off|s]       Enable, disable, or check history status
  -r, --restart             Restart the program
  -e, --exit                Exit the program

AI COMMANDS:
  ai "<prompt>"             Ask a general question
  ai file <name> ["prompt"] Analyze a file (optional custom prompt)
  ai project                Run full project analysis

====================================================================
    """)

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