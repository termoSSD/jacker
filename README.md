# 🔽 BELOW
**Advanced Local Development Intelligence**

| | |
|---|---|
| **Version** | 1.0.1 |
| **Type** | Command Line Interface (CLI) |
| **Status** | Beta |
| **License** | GPL-3.0 |

---

## 📋 Table of Contents
1. [System Description](#system-description)
2. [System Requirements](#system-requirements)
3. [Installation](#installation--execution)
4. [Quick Start](#quick-start)
5. [Command Specification](#command-specification)
6. [Data Architecture](#data-architecture)
7. [Troubleshooting](#troubleshooting)
8. [Contributing](#contributing)

---

## 🎯 System Description

**BELOW** is an autonomous console-based AI assistant designed for local code analysis and intelligent project management. All data processing is executed exclusively on local hardware utilizing the `llama.cpp` engine, ensuring complete privacy and control over your development environment.

### Key Features

- 🔒 **100% Local Processing** — No cloud dependencies, all AI computations run locally
- 📁 **Project Analysis** — Recursive analysis of codebases with intelligent context preservation
- 🔄 **Git Integration** — Automatic commit message generation based on staged changes
- 💾 **Session Persistence** — Save and load dialogue contexts for continued analysis
- ⚡ **Flexible Context** — Adjustable context window sizes to match your hardware capabilities
- 🖥️ **Cross-Platform** — Compiled binary for Windows or Python 3.9+ for other systems

The system is designed for seamless integration into a developer's workflow, supporting contextual directory analysis, Git commit generation, and memory session persistence.

---

## 🔧 System Requirements

Before installation, ensure the following conditions are met:

| Requirement | Details |
|---|---|
| **Model** | Local LLM in `.gguf` format (e.g., `qwen2.5-coder`, `mistral`, `llama2`) |
| **RAM/VRAM** | Minimum 4GB (8GB+ recommended for optimal performance) |
| **OS** | Windows 10/11, Linux, or macOS with Python 3.9+ |
| **Disk Space** | ~2GB for model files + system files |

⚠️ **Important:** Avoid using non-Latin characters (e.g., Cyrillic, Chinese) in model and project paths. This may cause fatal errors at the C++ library level.

---

## 📥 Installation & Execution

### Option A: Compiled Binary (Recommended for Windows)

1. **Download** the latest `Below.exe` from [Releases](https://github.com/termoSSD/below/releases)
2. **Create** a dedicated directory (e.g., `C:\Tools\Below`)
3. **Place** the executable in this directory
4. **Run** `Below.exe` — the program will automatically create:
   - `settings.json` — Configuration file
   - `LOG/` — Directory for logs
   - `memory/` — Directory for sessions

```bash
# Example folder structure after first run
C:\Tools\Below\
├── Below.exe
├── settings.json
├── LOG/
│   └── assistant.log
└── memory/
    └── history.txt
```

### Option B: Source Code Execution

For Linux, macOS, or advanced Windows users:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/termoSSD/below.git
   cd below
   ```

2. **Install dependencies:**
   ```bash
   pip install llama-cpp-python
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

---

## 🚀 Quick Start

### 1. First Launch - Configure Your Model

```
>> -m "C:\Models\qwen2.5-coder-7b-q4_k_m.gguf"
```

✅ Model loaded successfully!

### 2. Set Your Project Path

```
>> -p "C:\Projects\MyProject"
```

### 3. Analyze Your First File

```
>> ai file "main.py"
```

### 4. Generate a Commit Message

```
>> ai commit
```

---

## 📖 Command Specification

Commands must be entered following the `>>` prompt. Syntax rules are strictly enforced.

### BASE COMMANDS (SYSTEM CORE)

| Command | Syntax | Description |
|---|---|---|
| **Model Setup** | `-m, --model <path>` | Set absolute path to `.gguf` model file (mandatory on first launch) |
| **Project Path** | `-p, --project <path>` | Specify root directory for file analysis |
| **Context Size** | `-ctx, --context <size>` | Set context window (min: 512). Requires model reload. Default: 2048 |
| **Memory Control** | `--memory [on\|off\|s]` | Control query history recording (`s` = summary only) |
| **Restart** | `-r, --restart` | Force process restart |
| **Exit** | `-e, --exit` | Terminate operation |

**Example:**
```bash
>> -m "C:\Models\model.gguf" -p "C:\Projects\app" -ctx 4096
>> -r
>> -e
```

### AI OPERATIONS

| Command | Syntax | Description |
|---|---|---|
| **Direct Query** | `ai "<prompt>"` | Send query to model (quotes required) |
| **File Analysis** | `ai file <filename> ["prompt"]` | Analyze specific file in project |
| **Project Scan** | `ai project` | Full recursive analysis of all project files |
| **Git Commit** | `ai commit` | Auto-generate commit message from staged changes |
| **Save Session** | `ai save <session_name>` | Export dialogue context to JSON |
| **Load Session** | `ai load <session_name>` | Import dialogue context from JSON |

**Examples:**
```bash
>> ai "How can I optimize this code?"
>> ai file "utils.js" "Find security issues"
>> ai project
>> ai commit
>> ai save "my_analysis_session"
>> ai load "my_analysis_session"
```

### COSMETIC & SERVICE COMMANDS

| Command | Syntax | Description |
|---|---|---|
| **Help** | `-h, --help` | Display help menu |
| **Settings** | `-s, --settings` | Show current system parameters |
| **Clear Screen** | `-c, --clear` | Clear terminal |
| **Auto Clear** | `--autoclear [on\|off]` | Toggle auto screen clearing before menu |
| **Version** | `-v, --version` | Display current version |
| **Check Updates** | `-v up` | Manually check for updates on GitHub |
| **Auto Update** | `--autoupdate [on\|off]` | Toggle auto-check on startup |

**Example:**
```bash
>> -s
>> --autoclear on
>> -v up
```

---

## 💾 Data Architecture

The program creates and maintains the following structure in its root directory:

```
below/
├── Below.exe                  # Main executable
├── settings.json              # Configuration file (JSON format)
├── LOG/
│   └── assistant.log          # Event and error log
└── memory/
    ├── history.txt            # Global query history
    └── *.json                 # Saved session files
```

### Configuration File (`settings.json`)

Manual editing is permitted, but JSON syntax violations will trigger a factory reset. Example structure:

```json
{
  "model_path": "C:\\Models\\qwen2.5-coder-7b.gguf",
  "project_path": "C:\\Projects\\MyApp",
  "context_size": 2048,
  "memory_enabled": true,
  "autoclear": false,
  "autoupdate": true
}
```

### Logs and History

- **`LOG/assistant.log`** — Inspect this file for critical failures and debugging
- **`memory/history.txt`** — Global query history (searchable)
- **`memory/*.json`** — Individual session contexts for restoration

---

## ⚠️ Warnings & Limitations

### File Paths
🚨 **Avoid non-Latin characters** (Cyrillic, Arabic, CJK) in model and project paths.
```bash
# ❌ WRONG
>> -m "C:\Модели\модель.gguf"
>> -p "C:\项目\App"

# ✅ CORRECT
>> -m "C:\Models\model.gguf"
>> -p "C:\Projects\App"
```

### Memory Overflow
⚠️ Setting an excessively large `-ctx` parameter may cause an **Out of Memory** crash.

**Recommended context sizes by hardware:**
- 2GB RAM → max 512-1024
- 4GB RAM → max 2048
- 8GB RAM → max 4096
- 16GB+ RAM → 8192+

### Network Requirements
✅ **No Internet required** for AI operations — all processing is local.
🌐 Network is used **only** for:
- Update checking (`-v up`)
- GitHub repository updates

---

## 🐛 Troubleshooting

### Issue: "Model failed to load"
**Solution:**
- Verify the file path contains only Latin characters and no spaces
- Ensure the `.gguf` file exists and is not corrupted
- Check available RAM matches model requirements

```bash
>> -m "C:\Models\qwen2.5-7b.gguf"
```

### Issue: "Out of Memory" crash
**Solution:**
- Reduce context size:
  ```bash
  >> -ctx 1024
  ```
- Check system resources with Task Manager
- Close other applications

### Issue: "Project path not found"
**Solution:**
```bash
>> -p "C:\Projects\YourProject"
>> -s  # Verify settings
```

### Issue: "Git commit command failed"
**Solution:**
- Ensure you're in a valid Git repository
- Stage changes before running:
  ```bash
  git add .
  >> ai commit
  ```

### Issue: "Settings corrupted"
**Solution:**
- Delete `settings.json` and restart the program
- Program will regenerate default configuration

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report Bugs** — [Open an Issue](https://github.com/termoSSD/below/issues)
2. **Suggest Features** — Discuss in [GitHub Discussions](https://github.com/termoSSD/below/discussions)
3. **Submit Code** — Fork the repo and create a [Pull Request](https://github.com/termoSSD/below/pulls)

### Development Setup
```bash
git clone https://github.com/termoSSD/below.git
cd below
pip install -r requirements.txt
python main.py
```

---

## 📝 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) file for details.

---

## 👤 Author & Support

**Project Maintainer:** [termoSSD](https://github.com/termoSSD)

For issues, questions, or feedback:
- 📧 Open an [Issue](https://github.com/termoSSD/below/issues)
- 💬 Start a [Discussion](https://github.com/termoSSD/below/discussions)
- ⭐ Consider starring the repo if you find it useful!

---

**Last Updated:** April 15, 2026 | **Version:** 1.0.1
