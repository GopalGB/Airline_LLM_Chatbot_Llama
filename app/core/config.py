import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API settings
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# LLaMa-2-7B model settings
MODEL_NAME = "deepseek/deepseek-chat-v3-0324:free"

# Conversation settings
MAX_HISTORY_LENGTH = 10  # Maximum number of conversation turns to keep
TEMPERATURE = 0.7  # Controls randomness: lower is more deterministic
MAX_TOKENS = 1024  # Maximum number of tokens in response

# Define airline domain knowledge topics
AIRLINE_TOPICS = [
    "flight booking",
    "check-in procedures",
    "baggage policies", 
    "flight status",
    "frequent flyer programs",
    "in-flight services",
    "special assistance",
    "cancellation policies",
    "airport information"
]