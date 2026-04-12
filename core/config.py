import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
MEMORY_DIR = os.path.join(BASE_DIR, "memory")

VERSION = "0.9.6"
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
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        # If there's an error loading settings, reset to default
        return DEFAULT_SETTINGS

def save_settings(settings_dict):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings_dict, file, indent=4, ensure_ascii=False)

def get_setting(key):
    settings = load_settings()
    return settings.get(key, DEFAULT_SETTINGS.get(key))

def update_setting(key, value):
    settings = load_settings()
    settings[key] = value
    save_settings(settings)