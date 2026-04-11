import json
import datetime
import os
import ctypes
from urllib import response
from llama_cpp import Llama, llama_log_set, llama_log_callback
from core.config import get_setting, update_setting, MEMORY_DIR
from core.logger import get_logger

_llm_instance = None
logger = get_logger(__name__)

_chat_history = [
    {"role": "system", "content": "You are a helpful AI development assistant. Answer concisely."}
]

@llama_log_callback
def suppress_llama_logs(level, message, user_data):
    pass

llama_log_set(suppress_llama_logs, ctypes.c_void_p())

def load_llm():
    global _llm_instance
    model_path = current_model()
    
    logger.info(f"Спроба завантажити модель за шляхом: {model_path}")
    
    if not model_path or not os.path.exists(model_path):
        logger.error(f"Файл моделі не знайдено: {model_path}")
        return False
        
    try:
        _llm_instance = Llama(
            model_path=model_path,
            n_ctx=current_ctx_size(),   # Size of the context window
            verbose=False # Turn off verbose logging from the Llama library itself to avoid cluttering our logs
        )
        logger.info("Model successfully loaded into memory.")
        return True
    except Exception as e:
        logger.exception(f"[CRITICAL ERROR] occurred while loading the model: {e}")
        return False

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

def change_ctx_size(new_size):
    try:
        size_int = int(new_size.strip())
        if size_int < 512:
            return "ERROR: Size is too small (minimum 512)."
        
        update_setting("ctx_size", size_int)
        logger.info(f"Context size changed to {size_int}")
        
        # If the model is already loaded, reload it with the new memory size
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
    return get_setting("ctx_size")

def ask_ai(prompt):
    global _llm_instance, _chat_history
    model_path = current_model()
    
    if not model_path:
        logger.warning("Attempting to use AI without a set model.")
        return "ERROR: Model is not set. Use -m <path_to_model.gguf>"

    # if model is not loaded yet, try to load it before generating a response
    if _llm_instance is None:
        logger.info("Model not loaded. Initializing load...")
        if not load_llm():
            logger.error("Failed to load model.")
            return "[ERROR] Failed to load model."

    _chat_history.append({"role": "user", "content": prompt})

    try: 
        logger.info(f"Sending request to AI: '{prompt[:30]}...'")

        # Streaming enabled (stream=True) for smooth console output
        stream = _llm_instance.create_chat_completion(
            messages=_chat_history, 
            max_tokens=2048,
            stream=True
        )
        
        full_response = ""
        for output in stream:
            delta = output["choices"][0]["delta"]
            if "content" in delta:
                chunk = delta["content"]
                print(chunk, end="", flush=True) 
                full_response += chunk
                
        print() 
        
        logger.debug(f"AI response generated (length: {len(full_response)} characters)")
        _chat_history.append({"role": "assistant", "content": full_response})
        
        save_to_memory(prompt, full_response)
        
        return full_response 
        
    except Exception as e:
        logger.exception("[CRITICAL ERROR] occurred while generating AI response")
        error_msg = f"[ERROR] Error during generation: {e}"
        print(f"\n{error_msg}")

        _chat_history.pop()
        
        return error_msg   

def set_memory_recording(state: bool):
    update_setting("record_history", state)
    status = "ON" if state else "OFF"
    return f"Memory recording {status}"

def get_memory_status():
    return "ON" if get_setting("record_history") else "OFF"

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
    # Create memory directory if it doesn't exist
    if not os.path.exists(MEMORY_DIR):
        os.makedirs(MEMORY_DIR)
    
    file_path = os.path.join(MEMORY_DIR, f"{session_name}.json")
    try:
        # Save the entire chat history in JSON format
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
        # Load the JSON back into memory
        with open(file_path, "r", encoding="utf-8") as f:
            loaded_history = json.load(f)
            
        _chat_history = loaded_history
        logger.info(f"Session {session_name} loaded. Messages: {len(_chat_history)}")
        return f"Session '{session_name}' loaded! (Memory contains {len(_chat_history)} messages)"
    except Exception as e:
        logger.error(f"Error loading session: {e}")
        return f"ERROR loading session: {e}"