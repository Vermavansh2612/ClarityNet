"""
ClarityNet - Configuration File (INCREASED TOKEN LIMIT)
Contains all API keys and configuration settings
"""

# API Configuration
GEMINI_API_KEY = "AIzaSyCOvC3GEZnXWrcb6gSbGUORI2FP0vpYyjc"  # Replace with your actual API key

# Model Configuration - UPDATED WITH CORRECT MODEL NAMES
MODELS = {
    "rapid": "gemini-2.0-flash",      # Fast experimental model for simple queries
    "advanced": "gemini-2.5-pro"          # Powerful model for complex queries (stable version)
}

# Alternative model configurations you can try:
# Option 1: Stable versions
# MODELS = {
#     "rapid": "gemini-2.0-flash",
#     "advanced": "gemini-2.5-pro"
# }

# Option 2: Latest flash models
# MODELS = {
#     "rapid": "gemini-2.5-flash",
#     "advanced": "gemini-2.5-pro"
# }

# Option 3: Preview versions for cutting-edge features
# MODELS = {
#     "rapid": "gemini-2.0-flash-exp",
#     "advanced": "gemini-2.5-pro-preview-05-06"
# }

# Model Names (User-facing)
MODEL_NAMES = {
    "rapid": "Rapid Response Engine",
    "advanced": "Advanced Reasoning Engine"
}

# Analysis Thresholds
COMPLEXITY_THRESHOLD = 0.6
WORD_COUNT_THRESHOLD = 50

# Technical Keywords for Detection
TECHNICAL_KEYWORDS = [
    "explain", "analyze", "how", "why", "what", "describe",
    "detail", "compare", "evaluate", "calculate", "define",
    "code", "algorithm", "implement", "debug", "develop",
    "architecture", "design", "optimize", "refactor"
]

# Generation Configuration - MASSIVELY INCREASED TOKEN LIMIT
GENERATION_CONFIG = {
    "temperature": 0.7,
    "max_output_tokens": 8192,  # Increased from 2048 to 8192 for complete answers
    "top_p": 0.95,
    "top_k": 40
}

# UI Configuration
APP_TITLE = "ClarityNet"
APP_ICON = "🔮"
APP_SUBTITLE = "Explainable AI with Transparent Decision Making"

# File Upload Settings
ALLOWED_IMAGE_TYPES = ['png', 'jpg', 'jpeg']
MAX_FILE_SIZE_MB = 10