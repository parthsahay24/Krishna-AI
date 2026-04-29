import os
from dotenv import load_dotenv

# 1. Load the .env file
load_dotenv()

# 2. Extract API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY", "")

# 3. AI Brain Settings
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# 4. SAFER Server Port
_raw_port = os.getenv("SERVER_PORT", "8000")
try:
    # We try to turn it into a number
    SERVER_PORT = int(_raw_port.strip())
except (ValueError, AttributeError):
    # If someone typed "abc" or left it blank, we fall back to 8000
    SERVER_PORT = 8000

# 5. User Data Fallback
USER_NAME = os.getenv("USER_NAME", "Guest")
