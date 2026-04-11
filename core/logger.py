import os
import logging
from core.config import BASE_DIR

# 1. Directory for logs
LOG_DIR = os.path.join(BASE_DIR, "LOG")

# Create LOG directory if it doesn't exist
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 2. Path to log file
LOG_FILE = os.path.join(LOG_DIR, "assistant.log")

# 3. Baseic logging configuration
logging.basicConfig(
    level=logging.INFO, # Minimum level for recording (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s [%(levelname)s] %(message)s", # Format: Time [Level] Message
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        # Write logs to file with UTF-8 encoding
        logging.FileHandler(LOG_FILE, encoding="utf-8")
    ]
)

def get_logger(name):
    """Function to get a named logger in any file"""
    return logging.getLogger(name)