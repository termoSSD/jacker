import requests
import json
import os
import time
import sys
import subprocess

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_CONFIG_FILE = "model_config.txt"
project_path = ""

# retrieving or querying a model
def get_or_set_model():
    # Якщо файл існує, читаємо з нього
    if os.path.exists(MODEL_CONFIG_FILE):
        with open(MODEL_CONFIG_FILE, "r", encoding="utf-8") as file:
            saved_model = file.read().strip()
            if saved_model:
                return saved_model
    # Якщо файлу немає або він порожній, питаємо користувача
    selected_model = input("Enter model: ").strip()
    
    # Зберігаємо вибір у файл для наступних запусків
    with open(MODEL_CONFIG_FILE, "w", encoding="utf-8") as file:
        file.write(selected_model)
        
    print(f"Model '{selected_model}' saved!\n")
    return selected_model

# initialize the model when the module loads
MODEL = get_or_set_model()

# changing model
def change_model(new_model):
    global MODEL
        
    with open(MODEL_CONFIG_FILE, "w", encoding="utf-8") as file:
        file.write(new_model)
    
    # updating the model in the program's memory
    MODEL = new_model
    return f"Successful: {new_model}"

# returning current ai model
def current_model():
    return MODEL
    
# clear console
def clear():
    if os.name == 'nt':
        os.system('cls')
        sys.stdout.write('\033[3J\033[H')
    else:
        os.system('clear')
    sys.stdout.flush()

# show menu
def show_menu():
    clear()
    print("""
============================================================
                AI DEVELOPMENT ASSISTANT
============================================================

    """)

# show help
def show_help_menu():
    clear()
    print("""
============================================================
                AI DEVELOPMENT ASSISTANT
============================================================
Code analysis & AI helper for local projects.
------------------------------------------------------------

USAGE:
  <command> [arguments]

BASE COMMANDS:
  -h, --help             Show this help message
  -c, --clear            Clear the terminal screen
  -m, --model            View current model or set a new one
  -p, --project <path>   Set the project workspace directory
  -r, restart            Full restarting of program
  -e, exit               Exit
AI   COMMANDS:
  ai "<prompt>"          Ask a general question
  ai file <name>         Analyze a specific file
  ai project             Run full project analysis

============================================================
    """)

# ai requests
def ask_ai(prompt):
    try: # Trying to connect ollama
        r = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": True # Turn on stream
        }, stream=True)
        
        full_response = ""
        # Reading response character by character
        for line in r.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                data = json.loads(decoded_line)
                chunk = data.get("response", "")
                
                # Display the text directly on the screen without moving to a new line
                print(chunk, end="", flush=True) 
                
                full_response += chunk
                
        print() # Add an empty line at the end
        return full_response # Restore all text
        
    # if ollama isnt open
    except requests.exceptions.ConnectionError:
        return "ERROR: Run Ollama"

# smooth print
def print_smoothly(text, delay=0.03):
    for char in text:
        # Display the character without starting a new line and immediately refresh the screen
        print(char, end="", flush=True)
        time.sleep(delay) # Pause before the next letter
    print()
    
# project
def set_project(path):
    global project_path

    if not os.path.exists(path):
        return "Invalid path"

    project_path = path
    return f"Project set: {project_path}"

# show project path
def get_project():
    return project_path

# file reader
def read_file(name):
    if not project_path:
        return None

    for root, _, files in os.walk(project_path):
        for f in files:
            if f == name:
                with open(os.path.join(root, f), "r", encoding="utf-8") as file:
                    return file.read()
    return None

# restart program
def restart_program():
    print("\nRestarting...")
    sys.stdout.flush()
    time.sleep(0.5)
    
    cmd = f'start python "{sys.argv[0]}"'
    subprocess.Popen(cmd, shell=True)
    
    os._exit(0)
 
# exit the program
def exit():
    os._exit(0)