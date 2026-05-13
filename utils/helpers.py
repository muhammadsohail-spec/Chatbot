"""
utils/helpers.py
================
Shared utility functions used across the test suite.

Functions:
    generate_unique_email      – Produce a unique email address for signup tests.
    generate_dynamic_chat_message – Build a random human-like chat message.
    extract_link               – Pull the first URL out of a text string.
    take_screenshot            – Save a PNG locally and attach it to Allure.
"""

import os
import random
import re
import string
from datetime import datetime
from pathlib import Path

import allure

# Default directory for failure / debug screenshots.
SCREENSHOT_DIR = Path("failed_testcases_screenshoot")


# ---------------------------------------------------------------------------
# Email helpers
# ---------------------------------------------------------------------------

def generate_unique_email(base_email: str = "testsadaf2@gmail.com") -> str:
    """
    Generate a unique email address by injecting a random suffix before the
    ``@`` symbol using Gmail's ``+`` alias feature.

    Args:
        base_email: The template email address to extend.

    Returns:
        A unique email such as ``testsadaf2+ab3x7@gmail.com``.

    Example:
        >>> generate_unique_email()
        'testsadaf2+k9m2z@gmail.com'
    """
    local_part, domain = base_email.split("@", 1)
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=5))
    return f"{local_part}+{suffix}@{domain}"


# ---------------------------------------------------------------------------
# Chat message generator
# ---------------------------------------------------------------------------

def generate_dynamic_chat_message() -> str:
    """
    Compose a random, human-like chat message from predefined word banks.

    The function randomly selects one of four sentence templates and fills
    it with words drawn from greetings, verbs, objects, and questions lists.

    Returns:
        A plausible one-line chat message string.

    Example:
        >>> generate_dynamic_chat_message()
        'Hi! I need help with my account.'
    """
    greetings = ["Hi", "Hello", "Hey", "Good morning", "Good evening"]
    verbs     = ["help", "assist", "support", "guide", "check", "explain"]
    objects   = ["this issue", "my account", "the system", "the feature",
                 "my request", "this problem"]
    questions = [
        "how it works?", "what should I do?", "can you help me?",
        "what is the status?", "how does it work?"
    ]

    templates = [
        lambda: f"{random.choice(greetings)}, {random.choice(questions)}",
        lambda: f"Can you {random.choice(verbs)} {random.choice(objects)}?",
        lambda: f"{random.choice(greetings)}! I need help with {random.choice(objects)}.",
        lambda: f"Please {random.choice(verbs)} {random.choice(objects)} for me.",
    ]

    return random.choice(templates)()


# ---------------------------------------------------------------------------
# Text / URL helpers
# ---------------------------------------------------------------------------

_URL_PATTERN = re.compile(r"https?://\S+")


def extract_link(text: str) -> str | None:
    """
    Return the first HTTP/HTTPS URL found in ``text``, or ``None``.

    Args:
        text: Any string that may contain a URL.

    Returns:
        The matched URL string, or ``None`` if no URL is present.

    Example:
        >>> extract_link("Visit https://example.com for details.")
        'https://example.com'
    """
    match = _URL_PATTERN.search(text)
    return match.group(0) if match else None


# ---------------------------------------------------------------------------
# Screenshot helpers
# ---------------------------------------------------------------------------

def take_screenshot(driver, name: str = "screenshot") -> None:
    """
    Save a PNG screenshot to disk and attach it to the current Allure report.

    The file is written to ``SCREENSHOT_DIR/<name>_<timestamp>.png``.
    If the directory does not exist it is created automatically.

    Args:
        driver: Active Selenium WebDriver instance.
        name:   Base name for the screenshot file and Allure attachment label.
    """
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = SCREENSHOT_DIR / f"{name}_{timestamp}.png"

    driver.save_screenshot(str(file_path))

    allure.attach.file(
        str(file_path),
        name=name,
        attachment_type=allure.attachment_type.PNG,
    )
