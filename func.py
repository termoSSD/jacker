from core import *

def handle_command(cmd):

    # set project path 
    if cmd.startswith(("--path ", "-p ")):
        path = cmd.split(" ", 1)[1].strip()
        path = path.strip('"\'') 
        return set_project(path)

    # show project path
    if cmd.startswith(("--path", "-p")):
        current_path = get_project()
        if current_path: #  if no path
            return f"{current_path}"
        else: # if path empty
            return "Path empty USE: -p <шлях>" 
        
    # clear console
    if cmd.startswith(("--clear", "-c")):
        clear()
        return None

    # AI chat
    if cmd.startswith('ai "'):
        prompt = cmd[4:-1]
        return ask_ai(prompt)

    # AI file 
    if cmd.startswith("ai file "):
        file_name = cmd[len("ai file "):]
        code = read_file(file_name)

        if not code:
            return "❌ File not found"

        return ask_ai(f"Explain this code:\n{code}")

    # project analyze
    if cmd == "ai project":
        if not get_project():
            return "Set project first"

        result = ""

        for root, _, files in os.walk(get_project()):
            for f in files:
                path = os.path.join(root, f)

                with open(path, "r", encoding="utf-8", errors="ignore") as file:
                    code = file.read()

                result += f"\n\nFILE: {f}\n"
                result += ask_ai(f"Analyze this file:\n{code}")

        return result

    # help menu
    if cmd.strip() in ("--help", "-h"):
        show_help_menu()
    
    # change model
    if cmd.startswith(("--model ", "-m ")):
        new_model = cmd.split(" ", 1)[1].strip()
        return change_model(new_model)
        
    # showing current model
    if cmd.strip() in ("--model", "-m"):
        current = current_model()
        return f"{current}"
        
    # restart program
    if cmd.strip() in ("restart", "-r"):
        restart_program()

    if cmd.strip() in ("exit", "-e"):
        exit()
        
    return None
