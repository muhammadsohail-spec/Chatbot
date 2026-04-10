import logging
import os
from datetime import datetime
import json

def get_logger(name="AutomationFramework"):
    """
    Singleton Logger instance that outputs to a dedicated /logs folder with unique timestamps
    and avoids adding exponential duplicate handlers if called multiple times globally.
    """
    logger = logging.getLogger(name)
    
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    # Automatically generate the professional 'logs' directory at project root
    log_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)

    # Generate a unique timestamped file for tracing exactly when execution happened
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_path = os.path.join(log_dir, f"automation_run_{current_time}.log")

    # Physical File Output
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    # Console / Standard Output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Standardized Enterprise Formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s", 
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def load_guidelines():
    with open("testdata/guidelines.json") as f:
        return json.load(f)