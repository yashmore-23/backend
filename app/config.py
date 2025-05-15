import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Email configuration
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Optional: Warnings for missing critical values
if not EMAIL_USERNAME or not EMAIL_PASSWORD:
    print("⚠️ Warning: Email credentials are missing. Email sending may fail.")
if not SECRET_KEY:
    print("⚠️ Warning: JWT SECRET_KEY is missing. Authentication may be insecure.")

# OpenRouter AI API configuration
OPENROUTER__API_KEY = os.getenv("OPENROUTER_API_KEY", "your-openrouter-ai-api-key")  # Default value can be empty or a fallback message
