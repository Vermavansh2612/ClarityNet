"""
ui_styles.py - Bottom Input Layout with Enhanced Progress Indicators
FIXED: Clear visual feedback for answer generation
"""

from html import escape

MAIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  --primary: #5A189A;
  --primary-dark: #3c0d66;
  --primary-light: #7209B7;
  --bg-black: #000000;
  --bg-darker: #0a0a0f;
  --glass-bg: rgba(90, 24, 154, 0.1);
  --glass-border: rgba(90, 24, 154, 0.3);
  --text: #ffffff;
  --text-muted: #a0a0b8;
  --glow: rgba(90, 24, 154, 0.5);
  --success: #10b981;
}

/* Global */
* {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

h1, h2, h3, h4, h5, h6, .hero-title, .logo-text {
  font-family: 'Space Grotesk', sans-serif !important;
}

/* App structure */
.stApp {
  background: #000000 !important;
  position: relative;
  min-height: 100vh;
}

section[data-testid="stAppViewContainer"] {
  position: relative;
  z-index: 10 !important;
}

.main .block-container {
  position: relative;
  z-index: 10 !important;
  padding: 2rem 3rem 1rem 3rem !important;
  max-width: 1200px;
}

/* Animated Space Background */
.space-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  background: 
    radial-gradient(ellipse at 20% 30%, rgba(90, 24, 154, 0.15) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 70%, rgba(114, 9, 183, 0.15) 0%, transparent 50%),
    #000000;
}

.stars {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.star {
  position: absolute;
  width: 2px;
  height: 2px;
  background: white;
  border-radius: 50%;
  animation: twinkle 3s infinite;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}

/* Hero Section */
.hero-section {
  text-align: center;
  padding: 3rem 1rem 2rem 1rem;
  margin-bottom: 2rem;
  position: relative;
  z-index: 10;
}

.hero-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 3.5rem;
  font-weight: 800;
  margin: 0.5rem 0;
  background: linear-gradient(135deg, #ffffff, var(--primary-light));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -2px;
}

.hero-subtitle {
  color: var(--text-muted);
  margin-bottom: 2rem;
  font-size: 1.2rem;
  line-height: 1.8;
}

/* Feature Cards */
.feature-card {
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
  padding: 2rem 1.5rem;
  border-radius: 16px;
  color: var(--text);
  transition: all 0.3s ease;
  position: relative;
  z-index: 10;
  height: 100%;
}

.feature-card:hover {
  transform: translateY(-5px);
  border-color: var(--primary);
  box-shadow: 0 15px 50px var(--glow);
}

/* Chat History Container */
.chat-history-container {
  position: relative;
  z-index: 10;
  padding-bottom: 2rem;
}

/* Chat Messages */
.chat-message {
  margin-bottom: 1.5rem;
  animation: slideUp 0.4s ease-out;
  position: relative;
  z-index: 10;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.user-message {
  background: linear-gradient(135deg, rgba(90, 24, 154, 0.25), rgba(114, 9, 183, 0.15));
  backdrop-filter: blur(20px);
  padding: 1.25rem 1.5rem;
  border-radius: 18px 18px 4px 18px;
  margin-left: auto;
  max-width: 75%;
  border: 1px solid var(--glass-border);
  box-shadow: 0 8px 32px rgba(90, 24, 154, 0.2);
}

.ai-message {
  background: var(--glass-bg);
  backdrop-filter: blur(30px);
  padding: 1.25rem 1.5rem;
  border-radius: 18px 18px 18px 4px;
  max-width: 85%;
  border: 1px solid var(--glass-border);
  box-shadow: 0 8px 32px rgba(90, 24, 154, 0.2);
}

.message-header {
  font-weight: 700;
  font-size: 0.9rem;
  margin-bottom: 0.75rem;
  color: var(--primary-light);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.message-content {
  color: var(--text);
  line-height: 1.8;
  font-size: 1.05rem;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.typing-indicator {
  font-size: 0.7rem;
  color: var(--primary-light);
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 1; }
}

.cursor {
  animation: blink 1s infinite;
  color: var(--primary-light);
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

/* FIXED: Generation Status Indicators */
.generation-status {
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: 12px;
  padding: 1rem 1.5rem;
  margin-bottom: 1rem;
  animation: slideUp 0.3s ease-out;
}

.status-bar {
  width: 100%;
  height: 8px;
  background: rgba(90, 24, 154, 0.2);
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 0.75rem;
}

.status-progress {
  height: 100%;
  background: linear-gradient(90deg, var(--primary), var(--primary-light));
  border-radius: 10px;
  transition: width 0.3s ease;
  box-shadow: 0 0 15px var(--glow);
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.status-text {
  color: var(--primary-light);
  font-size: 0.95rem;
  font-weight: 600;
  text-align: center;
  animation: pulse 1.5s infinite;
}

.generation-complete {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(5, 150, 105, 0.1));
  border: 1px solid var(--success);
  border-radius: 12px;
  padding: 1rem 1.5rem;
  margin-bottom: 1rem;
  color: var(--success);
  font-weight: 600;
  text-align: center;
  animation: fadeInScale 0.4s ease-out;
  box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
}

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* INPUT SECTION - BOTTOM STICKY */
.input-section-bottom {
  position: sticky;
  bottom: 0;
  z-index: 100 !important;
  background: linear-gradient(to top, #000000 80%, rgba(0, 0, 0, 0.98) 95%, transparent 100%);
  backdrop-filter: blur(20px);
  padding: 1.5rem 0 1rem 0;
  margin: 0 -3rem -1rem -3rem;
  padding-left: 3rem;
  padding-right: 3rem;
  border-top: 1px solid var(--glass-border);
  box-shadow: 0 -10px 40px rgba(90, 24, 154, 0.2);
}

/* Media Preview */
.media-preview-container {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin: 0.75rem 0;
  position: relative;
  z-index: 10;
}

.media-preview-item {
  animation: fadeInScale 0.3s ease-out;
}

.media-type-badge {
  background: linear-gradient(135deg, rgba(90, 24, 154, 0.3), rgba(114, 9, 183, 0.2));
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text);
  border: 1px solid var(--glass-border);
  white-space: nowrap;
}

/* Buttons */
.stButton > button {
  background: linear-gradient(135deg, var(--primary), var(--primary-light)) !important;
  color: white !important;
  border: none !important;
  border-radius: 12px !important;
  padding: 0.875rem 1.5rem !important;
  font-weight: 600 !important;
  font-size: 1rem !important;
  box-shadow: 0 6px 20px var(--glow) !important;
  transition: all 0.2s ease !important;
  position: relative;
  z-index: 10;
}

.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 30px var(--glow) !important;
}

.stButton > button:active {
  transform: translateY(0) !important;
}

.stButton > button:disabled {
  opacity: 0.5 !important;
  cursor: not-allowed !important;
  transform: none !important;
}

/* Form Controls */
.stTextArea textarea,
.stTextInput input {
  background: rgba(20, 20, 30, 0.95) !important;
  border: 2px solid var(--glass-border) !important;
  border-radius: 14px !important;
  color: var(--text) !important;
  padding: 1rem !important;
  font-size: 1rem !important;
  position: relative;
  z-index: 10;
  transition: all 0.2s ease !important;
}

.stTextArea textarea:focus,
.stTextInput input:focus {
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 3px var(--glow) !important;
  outline: none !important;
}

[data-testid="stFileUploader"] {
  background: rgba(20, 20, 30, 0.7) !important;
  border: 2px dashed var(--glass-border) !important;
  border-radius: 12px !important;
  padding: 1rem !important;
  position: relative;
  z-index: 10;
  margin-bottom: 1rem !important;
  transition: all 0.2s ease !important;
}

[data-testid="stFileUploader"]:hover {
  border-color: var(--primary) !important;
  background: rgba(20, 20, 30, 0.9) !important;
}

/* Badges */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 8px 16px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 0.85rem;
  color: white;
  text-transform: capitalize;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
  position: relative;
  z-index: 10;
}

.badge-model {
  background: linear-gradient(135deg, var(--primary), var(--primary-light));
  box-shadow: 0 4px 16px var(--glow);
}

.badge-high {
  background: linear-gradient(135deg, #ef4444, #dc2626);
}

.badge-medium {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

.badge-low {
  background: linear-gradient(135deg, #10b981, #059669);
}

.badge-none {
  background: linear-gradient(135deg, #6b7280, #4b5563);
}

/* Expanders */
.streamlit-expanderHeader {
  background: rgba(90, 24, 154, 0.15) !important;
  border-radius: 12px !important;
  border: 1px solid var(--glass-border) !important;
  color: var(--text) !important;
  padding: 0.8rem 1rem !important;
  margin-bottom: 0.5rem !important;
  font-weight: 600 !important;
  position: relative;
  z-index: 10;
  transition: all 0.2s ease !important;
}

.streamlit-expanderHeader:hover {
  background: rgba(90, 24, 154, 0.25) !important;
  border-color: var(--primary) !important;
}

.streamlit-expanderContent {
  background: rgba(20, 20, 30, 0.5) !important;
  border: 1px solid var(--glass-border) !important;
  border-radius: 12px !important;
  padding: 1rem !important;
  margin-bottom: 1rem !important;
}

/* Images & Media - Compact Styling */
img {
  border-radius: 12px !important;
  border: 1px solid var(--glass-border) !important;
  box-shadow: 0 8px 32px rgba(90, 24, 154, 0.3) !important;
  position: relative;
  z-index: 10;
  max-height: 400px !important;
  object-fit: contain !important;
}

video {
  border-radius: 12px !important;
  border: 1px solid var(--glass-border) !important;
  box-shadow: 0 8px 32px rgba(90, 24, 154, 0.3) !important;
  max-height: 400px !important;
  width: 100% !important;
}

audio {
  width: 100% !important;
  margin: 0.5rem 0 !important;
}

/* Spinner */
.stSpinner > div {
  border-color: var(--primary) transparent transparent transparent !important;
}

/* Success/Error/Warning Messages */
.stSuccess, .stError, .stWarning, .stInfo {
  background: var(--glass-bg) !important;
  border: 1px solid var(--glass-border) !important;
  border-radius: 12px !important;
  padding: 1rem !important;
  margin: 1rem 0 !important;
}

/* Hide Streamlit Branding */
#MainMenu {
  visibility: hidden !important;
}

header {
  visibility: hidden !important;
}

footer {
  visibility: hidden !important;
}

/* Scrollbar */
::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  background: rgba(20, 20, 30, 0.5);
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, var(--primary), var(--primary-light));
  border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, var(--primary-light), var(--primary));
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .main .block-container {
    padding: 1rem 1.5rem 0.5rem 1.5rem !important;
  }
  
  .input-section-bottom {
    margin: 0 -1.5rem -0.5rem -1.5rem !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
  }
  
  .user-message,
  .ai-message {
    max-width: 95%;
  }
  
  img {
    max-height: 250px !important;
  }
  
  video {
    max-height: 250px !important;
  }
}

/* Smooth scroll and anchor */
html {
  scroll-behavior: smooth;
}

[data-testid="stAppViewContainer"] {
  scroll-behavior: smooth;
}

.scroll-anchor {
  display: block;
  height: 0;
  width: 0;
  margin-top: -100px;
  padding-top: 100px;
  visibility: hidden;
}
</style>
"""

def get_impact_badge(impact: str) -> str:
    """
    Return safe HTML span for an impact badge.
    Acceptable impacts: high, medium, low, none (case-insensitive).
    """
    if not impact:
        impact = "none"
    key = impact.strip().lower()
    cls = {
        "high": "badge-high",
        "critical": "badge-high",
        "medium": "badge-medium",
        "low": "badge-low",
        "none": "badge-none"
    }.get(key, "badge-none")

    label = escape(impact.title())
    return f'<span class="badge {cls}">{label}</span>'