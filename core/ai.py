import requests
import json
import datetime
import os
from core.config import get_setting, update_setting, OLLAMA_URL, MEMORY_DIR

def change_model(new_model):
    new_model = new_model.strip()
    update_setting("model", new_model)
    return f"Successful: {new_model}"

def current_model(): 
    return get_setting("model")

def ask_ai(prompt):
    model = current_model()
    if not model:
        return "ERROR: Model is not set. Use -m <model_name>"

    save_to_memory(prompt)

    try: 
        r = requests.post(OLLAMA_URL, json={
            "model": model,
            "prompt": prompt,
            "stream": True
        }, stream=True)
        
        full_response = ""
        for line in r.iter_lines():
            if line:
                try:
                    decoded_line = line.decode('utf-8')
                    data = json.loads(decoded_line)
                    chunk = data.get("response", "")
                    print(chunk, end="", flush=True) 
                    full_response += chunk
                except json.JSONDecodeError:
                    continue
                
        print() 
        return full_response 
        
    except requests.exceptions.ConnectionError:
        return "ERROR: Run Ollama"

def set_memory_recording(state: bool):
    update_setting("record_history", state)
    status = "ON" if state else "OFF"
    return f"Memory recording {status}"

def get_memory_status():
    return "ON" if get_setting("record_history") else "OFF"

def save_to_memory(prompt):
    # Беремо статус запису прямо з файлу налаштувань
    if not get_setting("record_history"):
        return

    if not os.path.exists(MEMORY_DIR):
        os.makedirs(MEMORY_DIR)
    
    history_file = os.path.join(MEMORY_DIR, "history.txt")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(history_file, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}]\nPrompt:\n{prompt}\n")
        file.write("=" * 60 + "\n\n")