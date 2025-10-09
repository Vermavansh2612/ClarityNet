"""
ClarityNet - Configuration File
Loads API keys and model configs from environment variables.
"""

import os
from dotenv import load_dotenv

# Load from .env file (for local development only)
load_dotenv()

# === 🔐 Gemini API Key (loaded from env or Streamlit Secrets) ===
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY is None:
    raise ValueError("❌ GEMINI_API_KEY not found. Set it in your .env or Streamlit Secrets.")

# === 🤖 Model Settings ===
MODELS = {
    "rapid": "gemini-2.0-flash",       # Fast/cheap
    "advanced": "gemini-2.5-pro",      # Smart/expensive
}

MODEL_NAMES = {
    "rapid": "Rapid Response Engine",
    "advanced": "Advanced Reasoning Engine"
}

# === 📊 Thresholds ===
COMPLEXITY_THRESHOLD = 0.6
WORD_COUNT_THRESHOLD = 50

# === 🧠 Keywords for analysis ===
TECHNICAL_KEYWORDS = [
    "explain", "analyze", "how", "why", "what", "describe",
    "compare", "evaluate", "define", "code", "optimize",
    "architecture", "algorithm", "debug", "refactor", "develop"
]

# === ✍️ Generation Configuration ===
GENERATION_CONFIG = {
    "temperature": 0.7,
    "max_output_tokens": 8192,
    "top_p": 0.95,
    "top_k": 40
}

# === 🌐 UI Branding ===
APP_TITLE = "ClarityNet"
APP_ICON = "🔮"
APP_SUBTITLE = "Explainable AI with Transparent Decision Making"

# === 📁 File Uploads ===
ALLOWED_IMAGE_TYPES = ['png', 'jpg', 'jpeg']
MAX_FILE_SIZE_MB = 10
