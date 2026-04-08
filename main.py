import os
import requests
import time
from core import *
from func import *

if os.name == 'nt':
    os.system('cls && mode con: cols=120 lines=30')
    
time.sleep(0.1)
clear()

print("Loading AI Assistant...")
for i in range(101):
    print(f"\rLoading {i}%", end="", flush=True)
    time.sleep(0.005)

print("\n     - Ready!\n")

show_menu()

while True:
    cmd = input(">> ").strip()
   
    result = handle_command(cmd)
    
    if result is not None:
        print("\n== ", end="") 
        print_smoothly(str(result), delay=0.01)
        print()

