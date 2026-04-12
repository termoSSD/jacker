import os
import time
from core.config import get_setting
from core.ai import get_or_set_model
from core.cmd import clear, show_menu, print_smoothly, check_for_updates
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
    cmd = input(">> ").strip()
    if not cmd:
        continue

    result = handle_command(cmd)
    
    if result is not None and str(result).strip():
        if not cmd.startswith("ai"):
            print("\n== ", end="") 
            print_smoothly(str(result), delay=0.01)
            print()

