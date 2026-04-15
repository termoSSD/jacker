import os
import subprocess
import webbrowser
from core.utils.logger import get_logger

logger = get_logger(__name__)

def execute_system_command(action, target):
    """Виконує системні дії на ПК."""
    action = action.upper().strip()
    target = target.strip()
    
    try:
        if action == "BROWSER":
            if not target.startswith("http"):
                target = f"https://www.google.com/search?q={target}"
            webbrowser.open(target)
            return True
            
        elif action == "VSCODE":
            path = target if target else "."
            subprocess.Popen(["code", path], shell=True)
            return True
            
        elif action == "EXPLORER":
            path = target if target else "."
            subprocess.Popen(f'explorer "{path}"')
            return True
            
        else:
            logger.warning(f"Unknown system action requested: {action}")
            return False
            
    except Exception as e:
        logger.error(f"Failed to execute {action} on {target}: {e}")
        return False