import json, datetime, gc, os, ctypes, subprocess, re
from llama_cpp import Llama, llama_log_set, llama_log_callback
from core.tools.web import search_web
from core.utils.cmd_ui import get_project, print_error, print_info, print_markdown
from core.utils.config import get_setting, update_setting, MEMORY_DIR
from core.utils.logger import get_logger
from core.ai.prompts import get_system_prompt
from core.tools.pc_control import execute_system_command

_llm_instance = None
logger = get_logger(__name__)

def get_system_prompt():
    import platform
    import datetime
    from core.utils.cmd_ui import get_project
    
    os_info = f"{platform.system()} {platform.release()}"
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    path = get_project() or "Not selected"
    
    prompt = (
        f"Your name is Markus. You are an elite, local AI daemon running directly on the user's machine ({os_info}).\n"
        f"[SYSTEM DATA]\n"
        f"- Current Time: {current_time}\n"
        f"- Current Workspace: {path}\n"
        f"-----------------\n"
        "Your primary role is expert software engineering, specifically focusing on Python architecture and complex C++ data structures. "
        "Communication style: direct, structurally precise, highly reliable, and subtly elegant. "
        "Rules: No emojis. No robotic clichés (never say 'As an AI'). Answer directly without introductory fluff. "
        "When writing code, prioritize optimal performance, memory safety, and clean architecture."
    )
    return prompt

_chat_history = []

'''
LLAMA MANAGER
'''

@llama_log_callback
def suppress_llama_logs(level, message, user_data):
    pass
llama_log_set(suppress_llama_logs, ctypes.c_void_p())

def load_llm():
    global _llm_instance
    model_path = current_model()
    
    logger.info(f"Attempting to load model from path: {model_path}")
    
    if not model_path or not os.path.exists(model_path):
        logger.error(f"Model file not found: {model_path}")
        return False
        
    try:
        print_info(f"Loading model... (Context: {current_ctx_size()})", title="System")
        _llm_instance = Llama(
            model_path=model_path,
            n_ctx=current_ctx_size(),   # Size of the context window
            n_gpu_layers=-1,            # 1.0.0: Максимальне вивантаження у відеокарту
            verbose=False               # Turn off verbose logging
        )
        logger.info("Model successfully loaded into memory.")
        return True
    except Exception as e:
        logger.exception(f"[CRITICAL ERROR] occurred while loading the model: {e}")
        print_error(f"Engine Error: {e}")
        return False

def load_ai():    
    if _llm_instance is not None:
        return "AI is already loaded and running."
    
    success = load_llm()
    
    if success:
        return "AI Engine started successfully!"
    else:
        return "Failed to start AI Engine. Check logs for details."

def unload_ai():
    global _llm_instance
    if _llm_instance is None:
        return "AI is not loaded anyway."
    
    try:
        del _llm_instance
        _llm_instance = None
        
        gc.collect()
        
        logger.info("Model unloaded from memory.")
        return "AI Engine stopped. Memory cleared."
    except Exception as e:
        logger.error(f"Error while unloading model: {e}")
        return f"Error: {e}"

def load_status():
    if _llm_instance is not None:
        return "Model Loaded (Active)"
    
    path = current_model()
    if not path:
        return "No Model Set"
    if not os.path.exists(path):
        return "Model file missing"
        
    return "Ready to load"

'''
MODEL MANAGER 
     &
COMMUNICATION WITH AI
'''

def get_or_set_model():
    model = current_model()
    if model:
        return model
    
    model = ""
    while not model:
        model = input("Enter model: ").strip()
        if not model:
            print("ERROR: Model name cannot be empty.")
            
    change_model(model)
    return model

def change_model(new_model):
    new_model = new_model.strip()
    update_setting("model", new_model)
    logger.info(f"Loading model from: {new_model}")
    if load_llm():
        return f"Successful: Model loaded."
    else:
        return "[ERROR] Path saved, but failed to load model."

def current_model(): 
    return get_setting("model")

def ask_ai(prompt, silent=False):
    global _llm_instance, _chat_history
    model_path = current_model()
    
    if not model_path:
        return "ERROR: Model is not set."

    if _llm_instance is None:
        if not load_llm(): return "[ERROR] Failed to load model."

    if len(_chat_history) > 15:
        _chat_history = [_chat_history[0]] + _chat_history[-10:]

    if not _chat_history or _chat_history[0].get("role") != "system":
        _chat_history.insert(0, {"role": "system", "content": get_system_prompt()})

    user_content = prompt
    if "WEB SEARCH RESULTS" not in prompt:
        user_content += "\n\n[SYSTEM: If you need real-time data, use EXACTLY: [CMD: SEARCH | query].]"

    _chat_history.append({"role": "user", "content": user_content})

    try: 
        if not silent: logger.info(f"Sending request to AI...")

        response = _llm_instance.create_chat_completion(
            messages=_chat_history, 
            max_tokens=2048,
            stream=False 
        )

        full_response = response["choices"][0]["message"]["content"]
        commands = re.findall(r'\[CMD:\s*(.*?)\s*\|\s*(.*?)\s*\]', full_response)
        
        for action, target in commands:
            action = action.upper().strip()

            if action == "SEARCH":  
                search_results = search_web(target)
                _chat_history.append({"role": "system", "content": f"Search results:\n{search_results}\n\nIf you see a specific URL that likely contains the answer, use [CMD: BROWSE | url]. Otherwise, answer now."})
                return ask_ai(f"I found some links for '{target}'. Look at them. If one looks perfect, browse it. If you have enough info, just answer the user.", silent=silent)

            elif action == "BROWSE":
                if not silent:
                    from core.utils.cmd_ui import print_info
                    print_info(f"Reading page: {target}...", title="Web Agent")
                
                from core.tools.web import fetch_page_content
                page_text = fetch_page_content(target)
                
                _chat_history.append({"role": "system", "content": f"Content of {target}:\n{page_text}"})
                return ask_ai(
    f"I just read {target}. If it contains weather data (temp/humidity), tell the user. "
    "IF THE DATA IS MISSING OR IRRELEVANT, DO NOT APOLOGIZE. "
    "Instead, look at the previous search results and BROWSE a different URL, or just use the snippets. "
    "Answer in Ukrainian.", 
    silent=silent
)
            
        display_response = re.sub(r'\[CMD:\s*.*?\s*\|\s*.*?\s*\]', '', full_response).strip()
        
        if not silent and display_response:
            print() 
            from core.utils.cmd_ui import print_markdown
            print_markdown(display_response)
            print() 
        
        _chat_history.append({"role": "assistant", "content": full_response})
        save_to_memory(prompt, full_response)
        
        return full_response if silent else None
        
    except Exception as e:
        logger.exception("AI Error")
        _chat_history.pop()
        return f"[ERROR]: {e}"
    
'''
RAM SIZE MANAGER
'''

def change_ctx_size(new_size):
    try:
        size_int = int(new_size.strip())
        if size_int < 512:
            return "ERROR: Size is too small (minimum 512)."
        
        update_setting("ctx_size", size_int)
        logger.info(f"Context size changed to {size_int}")
        
        global _llm_instance
        if _llm_instance is not None:
            print(f"\nReloading model with new memory size ({size_int})...")
            if load_llm():
                return f"Successful: Context size updated to {size_int} and model reloaded."
            else:
                return "ERROR: Size changed, but failed to reload model."
        return f"Successful: Context size updated to {size_int}."
    except ValueError:
        return "ERROR: Please enter a number (e.g., -ctx 2048)"

def current_ctx_size():
    return get_setting("ctx_size", default=2048)

'''
HISTORY MANAGER
'''

def set_memory_recording(state: bool):
    update_setting("record_history", state)
    status = "ON" if state else "OFF"
    return f"Memory recording {status}"

def get_memory_status():
    return "ON" if get_setting("record_history") else "OFF"

'''
SESSION MANAGER
'''

def save_to_memory(prompt, response):
    if not get_setting("record_history"):
        return

    if not os.path.exists(MEMORY_DIR):
        os.makedirs(MEMORY_DIR)
    
    history_file = os.path.join(MEMORY_DIR, "history.txt")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(history_file, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}]\nPrompt:\n{prompt}\n\n")
        file.write(f"AI Response:\n{response}\n")
        file.write("=" * 60 + "\n\n")

def save_session(session_name):
    if not os.path.exists(MEMORY_DIR):
        os.makedirs(MEMORY_DIR)
    
    file_path = os.path.join(MEMORY_DIR, f"{session_name}.json")
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(_chat_history, f, indent=4, ensure_ascii=False)
        return f"Session successfully saved to {session_name}.json"
    except Exception as e:
        logger.error(f"Error saving session: {e}")
        return f"ERROR saving session: {e}"

def load_session(session_name):
    global _chat_history
    file_path = os.path.join(MEMORY_DIR, f"{session_name}.json")
    
    if not os.path.exists(file_path):
        return f"ERROR: Session '{session_name}' not found in memory."
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            loaded_history = json.load(f)
            
        _chat_history = loaded_history
        logger.info(f"Session {session_name} loaded. Messages: {len(_chat_history)}")
        return f"Session '{session_name}' loaded! (Memory contains {len(_chat_history)} messages)"
    except Exception as e:
        logger.error(f"Error loading session: {e}")
        return f"ERROR loading session: {e}"

def analyze_project():
    project_path = get_project()
    if not project_path or not os.path.exists(project_path):
        return "[ERROR] Project path invalid or not set. Use: -p <path>"

    from core.dispatcher import ALLOWED_EXTENSIONS
    
    files_to_read = []
    ignore_set = {'.git', '__pycache__', 'node_modules', 'venv', 'env', 'build', 'dist', '.idea', '.vscode'}

    ignore_file = os.path.join(project_path, '.belowignore')
    if os.path.exists(ignore_file):
        try:
            with open(ignore_file, 'r', encoding='utf-8') as f:
                custom_ignores = {line.strip() for line in f if line.strip() and not line.startswith('#')}
                ignore_set.update(custom_ignores)
        except Exception:
            pass 

    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in ignore_set]
        for file in files:
            if os.path.splitext(file)[1].lower() in ALLOWED_EXTENSIONS:
                files_to_read.append(os.path.join(root, file))

    if not files_to_read: 
        return "No supported code files found."

    print_info(f"Found {len(files_to_read)} files. Starting analysis...", title="Project Scanner")

    full_context = "This is a local project analysis. Below is the source code of the project:\n\n"
    
    for file_path in files_to_read:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            rel_path = os.path.relpath(file_path, project_path)
            _, extension = os.path.splitext(file_path)
            lang = extension.replace(".", "")
            
            # Додаємо файл до загального контексту
            full_context += f"File: {rel_path}\n```{lang}\n{content}\n```\n\n"
            
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")

    full_context += "Please provide a brief overview of this project architecture and main functionality."

    return ask_ai(full_context)