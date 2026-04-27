import os
from dotenv import load_dotenv

# 1. Load the safe
load_dotenv()

# 2. Extract the contents
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY", "")
USER_NAME = os.getenv("USER_NAME", "Guest")

# 3. App Settings
SERVER_PORT = 8000
GROQ_MODEL = "llama-3.1-70b-versatile"
