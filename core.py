import requests
import os

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder"

project_path = ""

def show_menu1():
    print("""
============================================================
                AI DEVELOPMENT ASSISTANT
============================================================

    """)

def show_menu():
    print("""
============================================================
                AI DEVELOPMENT ASSISTANT
============================================================

Code analysis & AI helper for local projects.

------------------------------------------------------------

Commands:
  - help
  - clear
  - project <path>
  - ai "text"
       file <name>
       ai project

============================================================
    """)

# 🤖 AI
def ask_ai(prompt):
    r = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    })
    return r.json()["response"]


# 📁 project
def set_project(path):
    global project_path

    if not os.path.exists(path):
        return "❌ Invalid path"

    project_path = path
    return f"✅ Project set: {project_path}"


def get_project():
    return project_path


# 📄 file reader
def read_file(name):
    if not project_path:
        return None

    for root, _, files in os.walk(project_path):
        for f in files:
            if f == name:
                with open(os.path.join(root, f), "r", encoding="utf-8") as file:
                    return file.read()
    return None
    

def clear():
    os.system("cls" if os.name == "nt" else "clear")


