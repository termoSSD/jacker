import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, "config")
SETTINGS_PATH = os.path.join(CONFIG_DIR, "settings.json")

SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
MEMORY_DIR = os.path.join(BASE_DIR, "memory")

VERSION = "0.9.5"
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/termoSSD/below/main/VERSION"

DEFAULT_SETTINGS = {
    "model": "",
    "project_path": "",
    "record_history": False,
    "ctx_size": 4096,
    "clear_before_menu": True,
    "auto_update_check": True
}

'''
COMPILE SCRIPT
'''

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

'''
FUNCTIONS
'''

def load_settings():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    if not os.path.exists(SETTINGS_PATH):
        return {}

    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_settings(settings_dict):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings_dict, file, indent=4, ensure_ascii=False)

def get_setting(key, default=None):
    settings = load_settings()
    return settings.get(key, default)

def update_setting(key, value):
    settings = load_settings()
    settings[key] = value

    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
        
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)

def set_auto_load(state: bool):
    update_setting("auto_load", state)
    return f"Auto-load model on start: {'ON' if state else 'OFF'}"

def get_auto_load_status():
    return get_setting("auto_load", default=True)