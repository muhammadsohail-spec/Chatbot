import re


class ResponseValidator:
    """Reusable validation logic"""

    INVALID_PATTERNS = [
        r"Error fetching response"
    ]

    @staticmethod
    def is_valid(response: str) -> bool:
        if not response:
            return False

        response = response.lower()
        return not any(
            re.search(pattern, response)
            for pattern in ResponseValidator.INVALID_PATTERNS
        )