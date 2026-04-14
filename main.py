import os, sys, time
from core.config import get_setting
from core.ai import get_or_set_model
from core.cmd import clear, exit_program, print_error, print_info, show_menu, print_smoothly, check_for_updates
from func import handle_command

if os.name == 'nt':
    os.system('cls && mode con: cols=120 lines=30')
    
time.sleep(0.1)
clear()

print("Loading AI Assistant...")
for i in range(101):
    print(f"\rLoading {i}%", end="", flush=True)
    time.sleep(0.005)
print("\n     - Ready!\n")

get_or_set_model()
show_menu()

if get_setting("auto_update_check"):
    check_for_updates()

while True:
    try:
        command_input = input(">> ").strip()
        
        if not command_input:
            continue

        is_ai_command = command_input.startswith("ai")
        
        result = handle_command(command_input)
        
        if result is not None and str(result).strip():
            if not is_ai_command:
                print_info(str(result), title="System Response")
            
    except KeyboardInterrupt:
        print("\n[System] Shutting down BELOW. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected crash: {e}")
