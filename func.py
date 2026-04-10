import os
import re
from core.ai import ask_ai, change_model, current_model, set_memory_recording, get_memory_status
from core.cmd import set_project, get_project, clear, show_help_menu, read_file, restart_program, exit_program

ALLOWED_EXTENSIONS = {
    '.py', '.js', '.ts', '.html', '.css', '.cpp', 
    '.c', '.h', '.java', '.txt', '.md', '.json', '.go', '.rs'
}

def handle_command(cmd):

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
        
    if cmd.startswith(("--clear", "-c")):
        clear()
        return None

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

        # ВИПРАВЛЕНО: _, замінено на dirs
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

    if cmd.strip() in ("--help", "-h"):
        show_help_menu()
    
    if cmd.startswith(("--model ", "-m ")):
        new_model = cmd.split(" ", 1)[1].strip()
        return change_model(new_model)
        
    if cmd.strip() in ("--model", "-m"):
        current = current_model()
        return f"{current}"
        
    if cmd.strip() == "--memory off":
        return set_memory_recording(False)
    if cmd.strip() == "--memory on":
        return set_memory_recording(True)
    if cmd.strip() == "--memory s":
        return f"Memory recording is {get_memory_status()}"

    if cmd.strip() in ("restart", "-r"):
        restart_program()

    if cmd.strip() in ("exit", "-e"):
        exit_program()
        
    return None