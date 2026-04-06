from core import *

print("🤖 Loading AI Assistant...")
for i in range(101):
    print("Loading " + str(i) + "%")

print("📁 Initializing project system...")
print("✅ Ready!\n")

clear()
show_menu()

def handle_command(cmd):

    # 📁 project
    if cmd.startswith("project "):
        return set_project(cmd[len("project "):])

    if cmd.startswith("clear"):
        clear()
        show_menu1()

    # 💬 AI chat
    if cmd.startswith('ai "'):
        prompt = cmd[4:-1]
        return ask_ai(prompt)

    # 📄 file
    if cmd.startswith("ai file "):
        file_name = cmd[len("ai file "):]
        code = read_file(file_name)

        if not code:
            return "❌ File not found"

        return ask_ai(f"Explain this code:\n{code}")

    # 📦 project analyze
    if cmd == "ai project":
        if not get_project():
            return "❌ Set project first"

        result = ""

        for root, _, files in os.walk(get_project()):
            for f in files:
                path = os.path.join(root, f)

                with open(path, "r", encoding="utf-8", errors="ignore") as file:
                    code = file.read()

                result += f"\n\nFILE: {f}\n"
                result += ask_ai(f"Analyze this file:\n{code}")

        return result

    if cmd.strip() == "help":
        clear()
        return """
============================================================
                    AI DEVELOPMENT ASSISTANT
============================================================

Commands:
  - help
  - clear
  - project <path>
  - ai "text"
       file <name>
       ai project

============================================================
"""
    
    
    return None


while True:
    cmd = input(">> ").strip()

    if cmd == "exit":
        break

    result = handle_command(cmd)

    if result is not None:
        print("\n=== ", result, "\n")