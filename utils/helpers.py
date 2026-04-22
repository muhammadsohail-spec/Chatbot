import random
import string

def generate_unique_email(base_email="testsadaf2@gmail.com"):
    """
    Generates a unique email by adding random string after '+'.
    Example: testsadaf2+abc123@gmail.com
    """
    local_part, domain = base_email.split("@")
    # Generate random 5 character string
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    unique_email = f"{local_part}+{random_str}@{domain}"
    return unique_email

import random

def generate_dynamic_chat_message():
    greetings = ["Hi", "Hello", "Hey", "Good morning", "Good evening"]

    verbs = [
        "help", "assist", "support", "guide", "check", "explain"
    ]

    objects = [
        "this issue", "my account", "the system", "the feature",
        "my request", "this problem"
    ]

    questions = [
        "how it works?",
        "what should I do?",
        "can you help me?",
        "what is the status?",
        "how does it work?"
    ]

    # Fully dynamic sentence structure
    sentence_types = [
        lambda: f"{random.choice(greetings)}, {random.choice(questions)}",
        lambda: f"Can you {random.choice(verbs)} {random.choice(objects)}?",
        lambda: f"{random.choice(greetings)}! I need help with {random.choice(objects)}.",
        lambda: f"Please {random.choice(verbs)} {random.choice(objects)} for me."
    ]

    return random.choice(sentence_types)()


import re

def extract_link(text):
    url_pattern = r'(https?://[^\s]+)'
    match = re.search(url_pattern, text)
    return match.group(0) if match else None
