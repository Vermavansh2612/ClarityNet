"""
ClarityNet - Frontend Prototype (No Backend Required)
Built-in responses for demonstration purposes
"""
import streamlit as st
from PIL import Image
import time
import random

APP_TITLE = "ClarityNet"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== STYLES ====================
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

* {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

h1, h2, h3, h4, h5, h6, .hero-title, .logo-text {
  font-family: 'Space Grotesk', sans-serif !important;
}

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

.chat-history-container {
  position: relative;
  z-index: 10;
  padding-bottom: 2rem;
}

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

#MainMenu {
  visibility: hidden !important;
}

header {
  visibility: hidden !important;
}

footer {
  visibility: hidden !important;
}

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

st.markdown(MAIN_CSS, unsafe_allow_html=True)

# ==================== BUILT-IN RESPONSES ====================
DEMO_RESPONSES = {
    "default": {
        "response": "I'm a frontend prototype of ClarityNet! I can demonstrate the UI with pre-built responses. Try asking about AI, technology, science, or just say hello!",
        "explanation": "This is a demonstration response showing how ClarityNet analyzes queries and provides transparent reasoning. The actual system uses advanced AI models to route queries intelligently.",
        "model": "Demo Model",
        "factors": {
            "query_complexity": {"description": "Measures the complexity of the user's question", "impact": "medium"},
            "context_length": {"description": "Amount of context provided in the query", "impact": "low"},
            "media_presence": {"description": "Whether media files were uploaded", "impact": "none"}
        }
    },
    "hello": {
        "response": "Hello! 👋 Welcome to ClarityNet. I'm here to demonstrate our transparent AI interface. You can see how I process queries, make decisions, and provide clear explanations for everything I do. What would you like to explore?",
        "explanation": "Greeting queries are simple and conversational. They don't require complex reasoning, so I keep the response warm and welcoming while introducing the key features of the platform.",
        "model": "Conversational Model",
        "factors": {
            "query_type": {"description": "Identified as a greeting/social interaction", "impact": "high"},
            "response_tone": {"description": "Requires friendly, welcoming tone", "impact": "high"},
            "technical_depth": {"description": "Low technical complexity needed", "impact": "low"}
        }
    },
    "ai": {
        "response": "Artificial Intelligence is transforming how we interact with technology. Modern AI systems use neural networks trained on vast amounts of data to recognize patterns, make predictions, and generate human-like responses. The key breakthrough has been in deep learning, which allows models to learn hierarchical representations of data automatically.\n\nWhat makes ClarityNet special is our focus on transparency - you can see exactly how decisions are made, which factors influenced the response, and why a particular AI model was chosen for your query.",
        "explanation": "AI-related queries require balanced technical depth. I provide accessible explanations while highlighting ClarityNet's unique value proposition of transparency. The response combines general AI knowledge with specific platform benefits.",
        "model": "Technical Explainer Model",
        "factors": {
            "topic_complexity": {"description": "Technical subject requiring clear explanation", "impact": "high"},
            "audience_knowledge": {"description": "Assumed general audience, not specialists", "impact": "medium"},
            "explanation_depth": {"description": "Balanced between accuracy and accessibility", "impact": "high"}
        }
    },
    "how": {
        "response": "Great question! ClarityNet works through a multi-stage process:\n\n1. **Query Analysis**: When you submit a question, I analyze its complexity, topic, and context\n2. **Smart Routing**: Based on the analysis, I select the most appropriate AI model\n3. **Response Generation**: The chosen model generates a comprehensive answer\n4. **Transparency Layer**: I explain my reasoning and show you the decision factors\n5. **Delivery**: You receive not just an answer, but complete insight into how it was created\n\nThis prototype demonstrates the UI flow, while the full version connects to multiple AI models for optimal results.",
        "explanation": "Process questions need structured, step-by-step explanations. I break down the workflow into clear stages and emphasize both the 'what' and 'why' of each step. The transparency aspect is highlighted as a key differentiator.",
        "model": "Process Explainer Model",
        "factors": {
            "explanation_structure": {"description": "Requires step-by-step breakdown", "impact": "high"},
            "visual_clarity": {"description": "Uses formatting for better readability", "impact": "medium"},
            "completeness": {"description": "Covers the full workflow comprehensively", "impact": "high"}
        }
    },
    "image": {
        "response": "I can see you've uploaded an image! In the full version of ClarityNet, I would analyze the image content, identify objects, text, or patterns, and provide detailed insights. The system supports multiple images and can compare them, extract information, or answer questions about visual content.\n\nThis prototype demonstrates the UI for image handling, including the compact display and smooth interaction flow.",
        "explanation": "When images are detected, I acknowledge them explicitly and explain the multimodal capabilities. This builds user confidence that their media was processed and understood.",
        "model": "Multimodal Vision Model",
        "factors": {
            "media_type": {"description": "Image content requires visual processing", "impact": "high"},
            "multimodal_routing": {"description": "Activated vision-enabled model", "impact": "high"},
            "context_integration": {"description": "Combines visual and textual information", "impact": "medium"}
        }
    },
    "video": {
        "response": "Video uploaded! The full ClarityNet system can analyze video content frame-by-frame, extract audio, identify objects and actions, and even generate transcripts. This makes it perfect for understanding lectures, tutorials, presentations, or any video content.\n\nThe prototype shows how smoothly video uploads integrate into the conversational interface with our compact, elegant design.",
        "explanation": "Video analysis requires acknowledging the temporal nature of the content. I explain the comprehensive capabilities while being honest about this being a UI demonstration.",
        "model": "Multimodal Video Model",
        "factors": {
            "media_complexity": {"description": "Video processing requires specialized handling", "impact": "high"},
            "temporal_analysis": {"description": "Frame-by-frame processing capability", "impact": "high"},
            "resource_allocation": {"description": "Higher computational requirements", "impact": "medium"}
        }
    }
}

def get_demo_response(query, has_image=False, has_video=False, has_audio=False):
    """Generate appropriate demo response based on query content"""
    query_lower = query.lower()
    
    if has_image:
        return DEMO_RESPONSES["image"]
    elif has_video or has_audio:
        return DEMO_RESPONSES["video"]
    elif any(word in query_lower for word in ["hello", "hi", "hey", "greet"]):
        return DEMO_RESPONSES["hello"]
    elif any(word in query_lower for word in ["ai", "artificial", "intelligence", "machine learning", "neural"]):
        return DEMO_RESPONSES["ai"]
    elif any(word in query_lower for word in ["how", "work", "process", "explain how"]):
        return DEMO_RESPONSES["how"]
    else:
        return DEMO_RESPONSES["default"]

# ==================== INITIALIZE SESSION STATE ====================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_query" not in st.session_state:
    st.session_state.user_query = ""
if "processing" not in st.session_state:
    st.session_state.processing = False
if "message_count" not in st.session_state:
    st.session_state.message_count = 0
if "is_typing" not in st.session_state:
    st.session_state.is_typing = False
if "current_char_index" not in st.session_state:
    st.session_state.current_char_index = 0

# ==================== BACKGROUND ====================
st.markdown("""
<div class="space-bg"></div>
<div class="stars">
  <div class="star" style="top: 10%; left: 15%; animation-delay: 0s;"></div>
  <div class="star" style="top: 25%; left: 75%; animation-delay: 0.5s;"></div>
  <div class="star" style="top: 40%; left: 30%; animation-delay: 1s;"></div>
  <div class="star" style="top: 55%; left: 85%; animation-delay: 1.5s;"></div>
  <div class="star" style="top: 70%; left: 45%; animation-delay: 2s;"></div>
  <div class="star" style="top: 15%; left: 60%; animation-delay: 2.5s;"></div>
  <div class="star" style="top: 80%; left: 20%; animation-delay: 0.8s;"></div>
  <div class="star" style="top: 35%; left: 90%; animation-delay: 1.2s;"></div>
  <div class="star" style="top: 5%; left: 50%; animation-delay: 1.8s;"></div>
  <div class="star" style="top: 65%; left: 10%; animation-delay: 2.3s;"></div>
</div>
""", unsafe_allow_html=True)

# ==================== HERO SECTION ====================
if len(st.session_state.chat_history) == 0:
    st.markdown("""
    <div class="hero-section">
      <h1 class="hero-title">✨ Welcome to ClarityNet</h1>
      <p class="hero-subtitle">
        Your intelligent AI companion with complete transparency.<br>
        <strong>Frontend Prototype - No API Required</strong>
      </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
          <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">⚡</div>
          <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 0.5rem;">Smart Routing</div>
          <div style="color: var(--text-muted); font-size: 0.95rem;">
            Automatically selects the best AI model for your query
          </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
          <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">🔍</div>
          <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 0.5rem;">Full Transparency</div>
          <div style="color: var(--text-muted); font-size: 0.95rem;">
            See the reasoning behind every answer and decision
          </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
          <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">🎨</div>
          <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 0.5rem;">Multimodal</div>
          <div style="color: var(--text-muted); font-size: 0.95rem;">
            Handle text, images, videos, and audio seamlessly
          </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
      <h2 style="font-family: 'Space Grotesk', sans-serif; font-size: 1.8rem; font-weight: 800; 
                 background: linear-gradient(135deg, #ffffff, #7209B7); 
                 -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                 margin: 0;">✨ ClarityNet</h2>
    </div>
    """, unsafe_allow_html=True)

# ==================== CHAT HISTORY ====================
if len(st.session_state.chat_history) > 0:
    st.markdown("<div class='chat-history-container'>", unsafe_allow_html=True)
    
    for idx, chat in enumerate(st.session_state.chat_history):
        # User message
        st.markdown(f"""
        <div class="chat-message slide-in-left" id="msg-{idx}">
          <div class="user-message">
            <div class="message-header">👤 You</div>
            <div class="message-content">{chat['query']}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Media display
        if chat.get("images"):
            num_images = len(chat["images"])
            if num_images == 1:
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image(chat["images"][0], width=400, caption="Uploaded Image")
            else:
                cols = st.columns(min(num_images, 3))
                for img_idx, img in enumerate(chat["images"][:3]):
                    with cols[img_idx]:
                        st.image(img, width=250, caption=f"Image {img_idx + 1}")
        
        if chat.get("video"):
            col1, col2, col3 = st.columns([1, 3, 1])
            with col2:
                st.video(chat["video"])
        
        if chat.get("audio"):
            col1, col2, col3 = st.columns([1, 3, 1])
            with col2:
                st.audio(chat["audio"])
        
        # AI response with typewriter effect
        is_last_message = (idx == len(st.session_state.chat_history) - 1)
        is_typing = chat.get("is_typing", False) and is_last_message
        
        if is_typing:
            full_response = chat["response"]
            total_length = len(full_response)
            chars_per_update = 100
            
            progress_pct = min(99, int((st.session_state.current_char_index / max(total_length, 1)) * 100))
            
            if st.session_state.current_char_index < total_length:
                next_index = min(st.session_state.current_char_index + chars_per_update, total_length)
                displayed_text = full_response[:next_index]
                chat["displayed_response"] = displayed_text
                st.session_state.current_char_index = next_index
                
                model_badge = f'<span class="badge badge-model">🤖 {chat["model_name"]}</span>'
                
                st.markdown(f"""
                <div class="generation-status">
                    <div class="status-bar">
                        <div class="status-progress" style="width: {progress_pct}%"></div>
                    </div>
                    <div class="status-text">✨ Generating answer... {progress_pct}%</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f'<div id="ai-response-{idx}" class="scroll-anchor"></div>', unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="chat-message slide-in-right">
                  <div class="ai-message">
                    <div class="message-header">✨ ClarityNet <span class="typing-indicator">●●●</span></div>
                    <div class="message-content typewriter">{displayed_text}<span class="cursor">|</span></div>
                    <div style="margin-top: 1rem;">{model_badge}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
                
                time.sleep(0.015)
                st.rerun()
            else:
                chat["is_typing"] = False
                chat["displayed_response"] = full_response
                st.session_state.is_typing = False
                st.session_state.current_char_index = 0
                st.rerun()
        else:
            displayed_response = chat.get("displayed_response", chat["response"])
            model_badge = f'<span class="badge badge-model">🤖 {chat["model_name"]}</span>'
            st.markdown(f"""
            <div class="chat-message slide-in-right">
              <div class="ai-message">
                <div class="message-header">✨ ClarityNet</div>
                <div class="message-content">{displayed_response}</div>
                <div style="margin-top: 1rem;">{model_badge}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Expandable sections
        if not is_typing:
            with st.expander("💡 Reasoning Explained", expanded=False):
                st.markdown(
                    f"<div style='color: var(--text-muted); line-height: 1.8;'>{chat['explanation']}</div>",
                    unsafe_allow_html=True
                )
            
            with st.expander("📊 Decision Factors", expanded=False):
                for fname, fdata in chat["factors"].items():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"**{fname.replace('_', ' ').title()}**")
                        st.caption(fdata["description"])
                    with col2:
                        impact_class = {
                            "high": "badge-high",
                            "medium": "badge-medium",
                            "low": "badge-low",
                            "none": "badge-none"
                        }.get(fdata["impact"].lower(), "badge-none")
                        st.markdown(
                            f'<span class="badge {impact_class}">{fdata["impact"].title()}</span>',
                            unsafe_allow_html=True
                        )
        
        if idx < len(st.session_state.chat_history) - 1:
            st.markdown("<div style='border-top: 1px solid rgba(90, 24, 154, 0.2); margin: 2rem 0;'></div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

# ==================== INPUT SECTION ====================
st.markdown("<div class='input-section-bottom'>", unsafe_allow_html=True)

if len(st.session_state.chat_history) > 0:
    st.markdown("<div style='border-top: 2px solid rgba(90, 24, 154, 0.3); margin: 1rem 0 1.5rem 0;'></div>", unsafe_allow_html=True)

# File uploader
st.markdown("<div style='font-weight: 600; margin-bottom: 0.5rem; color: var(--text);'>📎 Attach Media (Optional)</div>", unsafe_allow_html=True)
uploaded_files = st.file_uploader(
    "Upload images, videos, or audio",
    type=['png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi', 'mp3', 'wav', 'ogg'],
    accept_multiple_files=True,
    help="Supports: Images (PNG, JPG), Videos (MP4, MOV, AVI), Audio (MP3, WAV, OGG)",
    label_visibility="collapsed",
    key=f"file_uploader_{st.session_state.message_count}",
    disabled=st.session_state.is_typing
)

# Process uploads
uploaded_images = []
uploaded_video = None
uploaded_audio = None
media_preview_html = ""

if uploaded_files:
    for idx, file in enumerate(uploaded_files[:2]):
        file_extension = file.name.split('.')[-1].lower()
        
        if file_extension in ['png', 'jpg', 'jpeg', 'gif']:
            img = Image.open(file)
            uploaded_images.append(img)
            media_preview_html += f"""
            <div class="media-preview-item">
                <div class="media-type-badge">🖼️ Image {idx + 1}</div>
            </div>
            """
        
        elif file_extension in ['mp4', 'mov', 'avi']:
            uploaded_video = file
            media_preview_html += f"""
            <div class="media-preview-item">
                <div class="media-type-badge">🎬 Video: {file.name[:25]}...</div>
            </div>
            """
        
        elif file_extension in ['mp3', 'wav', 'ogg']:
            uploaded_audio = file
            media_preview_html += f"""
            <div class="media-preview-item">
                <div class="media-type-badge">🎵 Audio: {file.name[:25]}...</div>
            </div>
            """
    
    if media_preview_html:
        st.markdown(f"""
        <div class="media-preview-container">
            {media_preview_html}
        </div>
        """, unsafe_allow_html=True)
        
        if uploaded_images:
            cols = st.columns(min(len(uploaded_images), 3))
            for idx, img in enumerate(uploaded_images):
                with cols[idx]:
                    st.image(img, width=200, caption=f"✅ Image {idx + 1}")
        
        if uploaded_video:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.video(uploaded_video)
        
        if uploaded_audio:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.audio(uploaded_audio)

# Text input
user_input = st.text_area(
    "Your question",
    placeholder="Ask me anything... Try: 'Hello', 'Tell me about AI', 'How does this work?'",
    value=st.session_state.user_query,
    height=100,
    label_visibility="collapsed",
    key=f"query_input_{st.session_state.message_count}",
    disabled=st.session_state.is_typing
)

# Action buttons
col1, col2, col3 = st.columns([4, 1, 1])

with col1:
    button_text = "⏳ Generating answer..." if st.session_state.is_typing else "🚀 Send Message"
    send_clicked = st.button(
        button_text,
        type="primary",
        use_container_width=True,
        disabled=st.session_state.processing or st.session_state.is_typing,
        key=f"send_btn_{st.session_state.message_count}"
    )

with col2:
    clear_clicked = st.button(
        "🗑️ Clear",
        use_container_width=True,
        disabled=st.session_state.processing or st.session_state.is_typing,
        help="Clear all chat history",
        key=f"clear_btn_{st.session_state.message_count}"
    )

with col3:
    about_clicked = st.button(
        "ℹ️ About",
        use_container_width=True,
        disabled=st.session_state.processing or st.session_state.is_typing,
        help="About ClarityNet",
        key=f"about_btn_{st.session_state.message_count}"
    )

st.markdown("</div>", unsafe_allow_html=True)

# ==================== BUTTON HANDLERS ====================
if about_clicked:
    st.info("""
    **ClarityNet - Explainable AI Platform (Frontend Prototype)**
    
    Features:
    • 🧠 Smart model selection
    • 🔍 Transparent reasoning
    • 🎨 Multimodal support (images, video, audio)
    • ⚡ Real-time typewriter effect
    • 🎯 Decision factor analysis
    
    **Note**: This is a frontend prototype with built-in demo responses.
    No backend API or external services are required!
    """)

if clear_clicked:
    st.session_state.chat_history = []
    st.session_state.user_query = ""
    st.session_state.processing = False
    st.session_state.is_typing = False
    st.session_state.message_count = 0
    st.session_state.current_char_index = 0
    st.rerun()

if send_clicked:
    current_query = user_input.strip()
    
    if current_query:
        st.session_state.processing = True
        st.session_state.is_typing = True
        st.session_state.current_char_index = 0
        
        # Simulate processing delay
        with st.spinner("🔮 Analyzing your request..."):
            time.sleep(0.8)  # Brief delay for realism
            
            # Get demo response
            demo_data = get_demo_response(
                current_query,
                has_image=len(uploaded_images) > 0,
                has_video=uploaded_video is not None,
                has_audio=uploaded_audio is not None
            )
            
            # Add to chat history
            st.session_state.chat_history.append({
                "query": current_query,
                "images": uploaded_images.copy() if uploaded_images else None,
                "video": uploaded_video,
                "audio": uploaded_audio,
                "response": demo_data["response"],
                "explanation": demo_data["explanation"],
                "model_name": demo_data["model"],
                "factors": demo_data["factors"],
                "is_typing": True,
                "displayed_response": ""
            })
            
            st.session_state.user_query = ""
            st.session_state.processing = False
            st.session_state.message_count += 1
            
            st.rerun()
    else:
        st.warning("⚠️ Please enter a question before sending")

# Footer
st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)