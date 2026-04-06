# 🚀 Jacker - AI Development Assistant

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/Python-3.x-yellow.svg)](https://www.python.org/)

> **Jacker** is a purely local, CLI-based AI development assistant. Powered by [Ollama](https://ollama.ai/) and the `qwen2.5-coder` model, it helps you analyze code, explain specific files, or review entire projects directly from your terminal—without sending a single line of your code to the cloud.

## 📑 Table of Contents
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage (Commands)](#-usage-commands)
- [Project Structure](#-project-structure)
- [License](#-license)

---

## ✨ Features
* 🔒 **100% Privacy:** All AI generation happens locally on your machine via Ollama. No data leaks.
* 📂 **Full Project Analysis:** Automatically iterates through all files in a specified directory and generates an AI review for each.
* 📄 **File-Specific Explanations:** Quickly ask the AI to break down a specific module or script.
* 💬 **Built-in Chat:** Ask general programming questions directly from your terminal.

## ⚙️ Prerequisites
Since this project relies on local AI generation, you must have the following installed before running it:
1. **Python 3.x**
2. [**Ollama**](https://ollama.ai/) installed and running.
3. The `qwen2.5-coder` model ar another downloaded. To do this, open your terminal and run:

   ```bash
   ollama pull qwen2.5-coder

🛠 Installation

    Clone the repository:
    Bash

    git clone [https://github.com/termoSSD/Jacker.git](https://github.com/termoSSD/Jacker.git)
    cd Jacker

    Install the required dependencies (requests library):
    Bash

    pip install requests

    Ensure Ollama is running in the background (defaulting to http://localhost:11434), then start the assistant:
    Bash

    python main.py

🚀 Usage (Commands)

Once you run main.py, you will enter an interactive CLI menu. The following commands are available:
Command	Description
project <path>	Sets the path to the local project directory you want to analyze.
ai "<text>"	Sends a custom prompt to the AI. Example: ai "How do I write a for loop in Python?" (Make sure to include the quotation marks).
ai file <name>	Reads the specified file from the active project directory and asks the AI to explain the code.
ai project	Iterates through all files in the active project directory and generates an AI analysis for each one.
clear	Clears the terminal screen.
help	Displays the list of available commands.
exit	Exits the application.

Example Workflow:
Bash

>> project C:/my_projects/calculator
✅ Project set: C:/my_projects/calculator

>> ai file math_logic.py
=== [Detailed AI explanation of the code will appear here] ===

📁 Project Structure

    main.py — The entry point of the app, containing the CLI interface and command routing.

    core.py — The core logic: handles file system operations and interacts with the Ollama API (http://localhost:11434/api/generate).

    config.py — Contains configuration variables like the workspace path and the selected AI model.

📄 License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). For more details, see the LICENSE file.
