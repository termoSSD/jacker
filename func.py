import os
import re
from core.ai import ask_ai, change_ctx_size, change_model, current_ctx_size, current_model, load_session, save_session, set_memory_recording, get_memory_status
from core.cmd import get_app_version, set_auto_clear, set_project, get_project, clear, show_ai_help_menu, show_base_help_menu, show_full_help_menu, show_cosmetic_menu, read_file, restart_program, exit_program, show_settings

ALLOWED_EXTENSIONS = {
    '.py', '.js', '.ts', '.html', '.css', '.cpp', 
    '.c', '.h', '.java', '.txt', '.md', '.json', '.go', '.rs'
}

def handle_command(cmd):

    parts = cmd.lower().split()
    if not parts:
        return None
   
    # Cosmetic commands    
    if parts[0] in ("--help", "-h"):    
        if len(parts) > 1:
            sub = parts[1]
            if sub == "ai":
                show_ai_help_menu()
                return None
            if sub == "base":
                show_base_help_menu()
                return None
            if sub == "csmt":
                show_cosmetic_menu()
                return None
        
        show_full_help_menu()
        return None
    if cmd.strip() in ("--clear", "-c"):
        clear()
        return None
    if cmd.strip() == "--autoclear off":
        return set_auto_clear(False)
    if cmd.strip() == "--autoclear on":
        return set_auto_clear(True)
    if cmd.strip() in ("--settings", "-s"):
        show_settings()
        return None
   
    if cmd.strip() in ("--version", "-v"):
        return get_app_version()

    # Path commands
    if cmd.startswith(("--path ", "-p ")):
        path = cmd.split(" ", 1)[1].strip()
        path = path.strip('"\'')
        return set_project(path)
    if cmd.startswith(("--path", "-p")):
        current_path = get_project()
        if current_path: 
            return f"{current_path}"
        else: 
            return "Path empty USE: -p <path>" 

    # AI commands
    if cmd.startswith('ai "'):
        clean_prompt = cmd[3:].strip().strip('"\'') + " (write plain text, no markdown, no asterisks)"
        return ask_ai(clean_prompt)
    if cmd.startswith("ai file "):
        match = re.match(r'ai file\s+([^\s"]+)\s+"([^"]+)"', cmd)
        
        if match:
            file_name = match.group(1).strip()
            user_prompt = match.group(2).strip()
        else:
            file_name = cmd[len("ai file "):].strip()
            user_prompt = "Analyze this file"
            
        code = read_file(file_name)
        if not code: 
            return f"Could not read file: {file_name} (Make sure project path is set)"

        full_query = f"{user_prompt}:\n{code}\n\n(Important: Plain text only, no asterisks)"
        return ask_ai(full_query)
    if cmd == "ai project":
        if not get_project():
            return "Set project first"

        result = ""

        for root, dirs, files in os.walk(get_project()):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
           
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext not in ALLOWED_EXTENSIONS:
                    continue 

                path = os.path.join(root, f)
                try:
                    with open(path, "r", encoding="utf-8") as file:
                        code = file.read()

                    result += f"\n\n--- FILE: {f} ---\n"
                    result += ask_ai(f"Analyze this file:\n{code}") 
                except Exception as e:
                    result += f"\nError reading {f}: {e}"

        return result

    # Model commands
    if cmd.startswith(("--model ", "-m ")):
        new_model = cmd.split(" ", 1)[1].strip()
        return change_model(new_model)
    if cmd.strip() in ("--model", "-m"):
        current = current_model()
        return f"{current}"
    
    # Memory recording commands
    if cmd.strip() == "--memory off":
        return set_memory_recording(False)
    if cmd.strip() == "--memory on":
        return set_memory_recording(True)
    if cmd.strip() == "--memory s":
        return f"Memory recording is {get_memory_status()}"

    # Session commands
    if cmd.startswith("ai save "):
        session_name = cmd[len("ai save "):].strip()
        if not session_name:
            return "Provide a session name (e.g., ai save project1)"
        return save_session(session_name)
    if cmd.startswith("ai load "):
        session_name = cmd[len("ai load "):].strip()
        if not session_name:
            return "Provide a session name (e.g., ai load project1)"
        return load_session(session_name)
    
    # Context size commands
    if cmd.startswith(("--context ", "-ctx ")):
        new_size = cmd.split(" ", 1)[1].strip()
        return change_ctx_size(new_size)
    if cmd.strip() in ("--context", "-ctx"):
        current = current_ctx_size()
        return f"Current context size: {current}"

    # Restart and exit commands
    if cmd.strip() in ("restart", "-r"):
        restart_program()
    if cmd.strip() in ("exit", "-e"):
        exit_program()
        
    return None