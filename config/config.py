# config/config.py

URL = "https://evergreenbeta.guidelinebuddy.com/auth/login"
URLBeta = "https://beta.guidelinebuddy.com/chat"
URLFSB = "https://fsbbeta.guidelinebuddy.com/auth/login"

# FSB credentials
USERNAME_FSB = "testsadaf2+fsbbeta@gmail.com"
PASSWORD_FSB = "DefaultPassword123&"

# Primary test credentials
USERNAME = "testsadaf2+testing1@gmail.com"
PASSWORD = "DefaultPassword123*"
NEW_PASSWORD = "DefaultPassword123."

# Negative-test credentials (intentionally invalid)
WRONG_USERNAME = "wronguser@gmail.com"
WRONG_PASSWORD = "wrongpass"

# OTP used across test flows (move to a secrets vault for production)
TEST_OTP = "712312"

EMAIL = "testsadaf2+12344@gmail.com"
EMAIL_PASSWORD = "testsadaf123."

INPUT_DATA_GUIDELINE_MESSAFGE = "HI,How are you?"