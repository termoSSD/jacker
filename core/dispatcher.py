import os
import re
from core.ai import (
    ask_ai, change_ctx_size, change_model, current_ctx_size, current_model, load_ai, load_llm, 
    load_session, load_status, save_session, set_memory_recording, get_memory_status, unload_ai
)
from core.cmd import (
    get_app_version, set_auto_clear, set_auto_update, set_project, get_project, 
    clear, show_ai_help_menu, show_base_help_menu, show_full_help_menu, 
    show_cosmetic_menu, read_file, restart_program, exit_program, show_menu, show_settings, check_for_updates
)
from core.config import (
    get_auto_load_status, set_auto_load
)


ALLOWED_EXTENSIONS = {
    '.py', '.js', '.ts', '.html', '.css', '.cpp', 
    '.c', '.h', '.java', '.txt', '.md', '.json', '.go', '.rs'
}


def handle_help(args):
    if args == "base": return show_base_help_menu()
    if args == "ai": return show_ai_help_menu()
    if args == "csmt": return show_cosmetic_menu()
    if args == "-": return show_menu()
    show_full_help_menu()
    return None

def handle_clear(args):
    clear()
    return None

def handle_settings(args):
    show_settings()
    return None

def handle_version(args):
    if args == "up":
        check_for_updates(manual_check=True)
        return None
    return get_app_version()

def handle_model(args):
    if args: return change_model(args)
    return f"Current model: {current_model()}"

def handle_project(args):
    if args: return set_project(args.strip('"\''))
    current = get_project()
    return current if current else "Path empty. Use: -p <path>"

def handle_context(args):
    if args: return change_ctx_size(args)
    return f"Current context: {current_ctx_size()}"

def handle_exit(args):
    exit_program()

def handle_autoclear(args):
    if args == "off": return set_auto_clear(False)
    if args == "on": return set_auto_clear(True)
    return "Usage: --autoclear [on|off]"

def handle_autoupdate(args):
    if args == "off": return set_auto_update(False)
    if args == "on": return set_auto_update(True)
    return "Usage: --autoupdate [on|off]"

def handle_memory(args):
    if args == "off": return set_memory_recording(False)
    if args == "on": return set_memory_recording(True)
    if args == "s": return f"Memory recording: {get_memory_status()}"
    return "Usage: --memory [on|off|s]"

def handle_autoload(args):
    if args == "on": return set_auto_load(True)
    if args == "off": return set_auto_load(False)
    status = "ON" if get_auto_load_status() else "OFF"
    return f"Auto-load is {status}. Use: --autoload on/off"

# --- DISPATCH TABLE ---

COMMANDS = {
    "-h": handle_help, "--help": handle_help,
    "-c": handle_clear, "--clear": handle_clear,
    "-s": handle_settings, "--settings": handle_settings,
    "-v": handle_version, "--version": handle_version,
    "-m": handle_model, "--model": handle_model,
    "-p": handle_project, "--path": handle_project,
    "-ctx": handle_context, "--context": handle_context,
    "-astr": handle_autoload,
    "--load": lambda x: load_ai(),
    "--stop": lambda x: unload_ai(),
    "--status": lambda x: load_status(),
    "--autoclear": handle_autoclear,    
    "--autoupdate": handle_autoupdate,  
    "--memory": handle_memory,          
    "-e": handle_exit, "exit": handle_exit,
    "-r": lambda x: restart_program()
}

def handle_command(command_text):
    text = command_text.strip()
    if not text: return None

    # Розбиваємо введення на базову команду та аргументи
    parts = text.split(" ", 1)
    base_cmd = parts[0].lower()
    args = parts[1].strip() if len(parts) > 1 else ""

    # 1. Перевіряємо, чи є це системна команда зі словника
    if base_cmd in COMMANDS:
        return COMMANDS[base_cmd](args)

    # 2. Обробка складних команд AI
    
    # Збереження / Завантаження сесій
    if text.startswith("ai save "):
        return save_session(text[len("ai save "):].strip())
    if text.startswith("ai load "):
        return load_session(text[len("ai load "):].strip())

    # Прямий запит
    if text.startswith('ai "'):
        clean_prompt = text[3:].strip().strip('"\'')
        return ask_ai(clean_prompt)

    # Аналіз файлу (Тут обірвався твій код)
    if text.startswith("ai file "):
        match = re.match(r'ai file\s+([^\s"]+)\s+"([^"]+)"', text)
        file_name = match.group(1).strip() if match else text[len("ai file "):].strip()
        user_prompt = match.group(2).strip() if match else "Analyze this file"
        
        code = read_file(file_name)
        if not code: 
            return f"Could not read file: {file_name} (Set project path first)"
        
        # Отримуємо розширення файлу (наприклад, '.py') і забираємо крапку
        _, ext = os.path.splitext(file_name)
        ext_clean = ext.replace(".", "")
        
        # Формуємо красивий запит з Markdown
        final_prompt = f"{user_prompt}:\n\n```{ext_clean}\n{code}\n```"
        
        return ask_ai(final_prompt)