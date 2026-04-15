import json, datetime, gc, os, ctypes, subprocess
from llama_cpp import Llama, llama_log_set, llama_log_callback
from core.cmd import get_project, print_error, print_info, print_markdown
from core.config import get_setting, update_setting, MEMORY_DIR
from core.logger import get_logger

_llm_instance = None
logger = get_logger(__name__)

_chat_history = [
    {"role": "system", "content": "You are a helpful AI development assistant. Answer concisely."}
]

'''
LLAMA MANAGER
'''

@llama_log_callback
def suppress_llama_logs(level, message, user_data):
    pass
llama_log_set(suppress_llama_logs, ctypes.c_void_p())

def load_llm():
    from core import cmd
    global _llm_instance
    model_path = current_model()
    
    logger.info(f"Спроба завантажити модель за шляхом: {model_path}")
    
    if not model_path or not os.path.exists(model_path):
        logger.error(f"Файл моделі не знайдено: {model_path}")
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
    from core import cmd
    
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
        logger.warning("Attempting to use AI without a set model.")
        return "ERROR: Model is not set. Use -m <path_to_model.gguf>"

    if _llm_instance is None:
        logger.info("Model not loaded. Initializing load...")
        if not load_llm():
            logger.error("Failed to load model.")
            return "[ERROR] Failed to load model."

    if len(_chat_history) > 15:
        _chat_history = [_chat_history[0]] + _chat_history[-10:]

    _chat_history.append({"role": "user", "content": prompt})

    try: 
        if not silent:
            logger.info(f"Sending request to AI: '{prompt[:30]}...'")

        response = _llm_instance.create_chat_completion(
            messages=_chat_history, 
            max_tokens=2048,
            stream=False 
        )
        
        full_response = response["choices"][0]["message"]["content"]
        
        if not silent:
            print() 
            print_markdown(full_response)
            print() 
        
        logger.debug(f"AI response generated (length: {len(full_response)} characters)")
        _chat_history.append({"role": "assistant", "content": full_response})
        
        save_to_memory(prompt, full_response)
        
        return full_response if silent else None
        
    except Exception as e:
        logger.exception("[CRITICAL ERROR] occurred while generating AI response")
        error_msg = f"[ERROR] Error during generation: {e}"
        if not silent: print(f"\n{error_msg}")

        _chat_history.pop()
        return error_msg   


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