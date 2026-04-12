# BELOW
**Advanced Local Development Intelligence**
**Version:** 0.9.5
**Type:** Command Line Interface (CLI)
**Status:** Beta

---

## 1. SYSTEM DESCRIPTION
**BELOW** is an autonomous console-based AI assistant for local code analysis and project management. All data processing is executed exclusively on local hardware utilizing the `llama.cpp` engine. No code fragments are transmitted to external servers. 

The system is designed for seamless integration into a developer's workflow, supporting contextual directory analysis, Git commit generation, and memory session persistence.

---

## 2. SYSTEM REQUIREMENTS
Ensure the following conditions are met prior to operation:
* **Model:** A local LLM in `.gguf` format is required (e.g., qwen2.5-coder).
* **Hardware:** RAM or VRAM capacity must accommodate the selected model size and the specified context window.
* **OS:** Windows 10/11 (for the compiled `.exe`) or a Python 3.9+ environment for source code execution.

---

## 3. INSTALLATION AND EXECUTION

### Option A: Compiled Binary (Recommended)
1. Download `Below.exe`.
2. Place the executable into a dedicated directory (e.g., `C:\Tools\Below`).
3. Execute the file. The program will automatically generate the required configuration files and directories (`settings.json`, `LOG/`, `memory/`).

### Option B: Source Code Execution
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install llama-cpp-python
3. Run the initializer:
   ```bash
   python main.py
## 4. COMMAND SPECIFICATION
Commands must be entered following the >> prompt. Syntax rules are strictly enforced.

BASE COMMANDS (SYSTEM CORE)

    -m, --model <path> : Set the absolute path to the .gguf model file. Mandatory on first launch.

    -p, --project <path> : Specify the root directory of the current project for file analysis.

    -ctx, --context <size> : Set the context window size (minimum 512). Requires a model reload.

    --memory [on|off|s] : Control global query history recording.

    -r, --restart : Force process restart.

    -e, --exit : Terminate operation.

AI OPERATIONS

    ai "<prompt>" : Direct query to the model. Prompt text must be enclosed in quotation marks.

    ai file <filename> ["prompt"] : Analyze a specific file within the defined project (-p).

    ai project : Execute a full recursive analysis of all supported files within the project directory.

    ai commit : Automatically generate a git commit message based on staged changes.

    ai save <session_name> : Export the current dialogue context to a JSON file.

    ai load <session_name> : Import a dialogue context from a JSON file.

COSMETIC AND SERVICE COMMANDS

    -h, --help : Display the general help menu.

    -s, --settings : Output current system parameters.

    -c, --clear : Clear the terminal screen.

    --autoclear [on|off] : Toggle automatic screen clearing prior to menu display.

    -v, --version : Display the current version.

    -v up : Manually check for updates on GitHub.

    --autoupdate [on|off] : Toggle automatic update checking on system boot.

## 5. DATA ARCHITECTURE

The program creates and maintains the following structure in its root directory:

    settings.json — Configuration file. Manual editing is permitted, but JSON syntax violations will trigger a factory reset.

    LOG/assistant.log — Event and error log. Inspect this file in the event of critical failures.

    memory/ — Directory for storing sessions (.json) and global history (history.txt).

## 6. WARNINGS AND LIMITATIONS

    File Paths: Avoid using non-Latin characters (e.g., Cyrillic) in model and project paths. This may induce fatal errors at the C++ library level.

    Memory Overflow: Setting an excessively large -ctx parameter may result in a program crash (Out of Memory). Monitor your system resources.

    Autonomy: The system does not require an Internet connection for AI tasks. Network access is utilized exclusively by the update function (check_for_updates).
