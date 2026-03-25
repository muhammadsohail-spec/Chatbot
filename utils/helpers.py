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