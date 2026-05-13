"""
utils/logger.py
===============
Singleton logger factory for the automation framework.

Usage:
    from utils.logger import get_logger

    logger = get_logger("MyModule")
    logger.info("Test started.")

Design:
    - ``get_logger`` returns a named ``logging.Logger`` instance.
    - The first call for a given name creates the logger, attaches a
      rotating file handler and a console handler, then returns it.
    - Subsequent calls for the same name return the already-configured
      logger without adding duplicate handlers.
    - All log files are written to ``<project_root>/logs/`` with an
      ISO-style timestamp in the filename so every test run produces its
      own log file.
"""

import json
import logging
import os
from datetime import datetime

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

LOG_DIR = os.path.join(os.getcwd(), "logs")
LOG_FORMAT = "%(asctime)s [%(levelname)-8s] %(name)s: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_logger(name: str = "AutomationFramework") -> logging.Logger:
    """
    Return a named logger configured with file + console output.

    The logger is created only once per ``name``; calling this function
    multiple times with the same ``name`` returns the identical instance,
    preventing duplicate log entries.

    Args:
        name: Logical name for the logger (e.g. module or class name).

    Returns:
        A fully configured ``logging.Logger`` instance.
    """
    logger = logging.getLogger(name)

    # Guard: already configured — return as-is to avoid duplicate handlers.
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.DEBUG)

    # Ensure the logs directory exists.
    os.makedirs(LOG_DIR, exist_ok=True)

    # Build a timestamped log file for this execution run.
    run_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(LOG_DIR, f"automation_run_{run_timestamp}.log")

    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

    # File handler — captures everything at DEBUG and above.
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console handler — surfaces INFO and above to the terminal.
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# ---------------------------------------------------------------------------
# Test-data helpers
# ---------------------------------------------------------------------------

def load_guidelines(path: str = "testdata/guidelines.json") -> dict:
    """
    Load and return the contents of the guidelines JSON file.

    Args:
        path: Relative or absolute path to the JSON file.

    Returns:
        Parsed JSON content as a Python ``dict``.

    Raises:
        FileNotFoundError: If the file does not exist at ``path``.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    with open(path, encoding="utf-8") as f:
        return json.load(f)