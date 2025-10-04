"""
ClarityNet - Enhanced UX with Bottom Input & Compact Media
FIXED: Clear generation feedback + Complete answer rendering
"""
import streamlit as st
from PIL import Image
import time
from backend import ClarityNetEngine
from config import APP_TITLE
from ui_styles import MAIN_CSS, get_impact_badge

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(MAIN_CSS, unsafe_allow_html=True)

# Space background
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

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_query" not in st.session_state:
    st.session_state.user_query = ""
if "processing" not in st.session_state:
    st.session_state.processing = False
if "message_count" not in st.session_state:
    st.session_state.message_count = 0
if "typing_response" not in st.session_state:
    st.session_state.typing_response = ""
if "is_typing" not in st.session_state:
    st.session_state.is_typing = False
if "current_char_index" not in st.session_state:
    st.session_state.current_char_index = 0
if "last_update_time" not in st.session_state:
    st.session_state.last_update_time = 0
if "generation_complete" not in st.session_state:
    st.session_state.generation_complete = False

@st.cache_resource
def get_engine():
    return ClarityNetEngine()

engine = get_engine()

# Hero Section (only on first load)
if len(st.session_state.chat_history) == 0:
    st.markdown("""
    <div class="hero-section">
      <h1 class="hero-title">✨ Welcome to ClarityNet</h1>
      <p class="hero-subtitle">
        Your intelligent AI companion with complete transparency.<br>
        Ask questions, upload media, and understand every decision.
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
    # Compact header when chat exists
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
      <h2 style="font-family: 'Space Grotesk', sans-serif; font-size: 1.8rem; font-weight: 800; 
                 background: linear-gradient(135deg, #ffffff, #7209B7); 
                 -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                 margin: 0;">✨ ClarityNet</h2>
    </div>
    """, unsafe_allow_html=True)

# ==================== CHAT HISTORY SECTION (TOP) ====================
if len(st.session_state.chat_history) > 0:
    st.markdown("<div class='chat-history-container'>", unsafe_allow_html=True)
    
    for idx, chat in enumerate(st.session_state.chat_history):
        # User message
        st.markdown(f"""
        <div class="chat-message slide-in-left" id="msg-{idx}" style="animation-delay: {idx * 0.05}s;">
          <div class="user-message">
            <div class="message-header">👤 You</div>
            <div class="message-content">{chat['query']}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Compact media display
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
        
        # AI response
        is_last_message = (idx == len(st.session_state.chat_history) - 1)
        is_typing = chat.get("is_typing", False) and is_last_message
        
        if is_typing:
            # Typewriter effect with auto-scroll and proper completion
            full_response = chat["response"]
            total_length = len(full_response)
            chars_per_update = 100  # Faster for better UX
            
            # Calculate actual progress
            progress_pct = min(99, int((st.session_state.current_char_index / max(total_length, 1)) * 100))
            
            if st.session_state.current_char_index < total_length:
                # Still typing
                next_index = min(st.session_state.current_char_index + chars_per_update, total_length)
                displayed_text = full_response[:next_index]
                chat["displayed_response"] = displayed_text
                st.session_state.current_char_index = next_index
                
                model_badge = f'<span class="badge badge-model">🤖 {chat["model_name"]}</span>'
                
                # Progress indicator
                st.markdown(f"""
                <div class="generation-status">
                    <div class="status-bar">
                        <div class="status-progress" style="width: {progress_pct}%"></div>
                    </div>
                    <div class="status-text">✨ Generating answer... {progress_pct}%</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Auto-scroll anchor at top of AI response
                st.markdown(f'<div id="ai-response-{idx}" class="scroll-anchor"></div>', unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="chat-message slide-in-right">
                  <div class="ai-message">
                    <div class="message-header">✨ ClarityNet <span class="typing-indicator">●●●</span></div>
                    <div class="message-content typewriter">{displayed_text}<span class="cursor">|</span></div>
                    <div style="margin-top: 1rem;">{model_badge}</div>
                  </div>
                </div>
                <script>
                  setTimeout(function() {{
                    const element = document.getElementById('ai-response-{idx}');
                    if (element) {{
                      element.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                    }}
                  }}, 100);
                </script>
                """, unsafe_allow_html=True)
                
                time.sleep(0.015)  # Smooth animation
                st.rerun()
            else:
                # Complete - show full response
                chat["is_typing"] = False
                chat["displayed_response"] = full_response
                st.session_state.is_typing = False
                st.session_state.current_char_index = 0
                st.rerun()
        else:
            # Normal display (complete message)
            displayed_response = chat.get("displayed_response", chat["response"])
            model_badge = f'<span class="badge badge-model">🤖 {chat["model_name"]}</span>'
            st.markdown(f"""
            <div class="chat-message slide-in-right" style="animation-delay: {idx * 0.05 + 0.1}s;">
              <div class="ai-message">
                <div class="message-header">✨ ClarityNet</div>
                <div class="message-content">{displayed_response}</div>
                <div style="margin-top: 1rem;">{model_badge}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Expandable sections (only when not typing)
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
                        impact_html = get_impact_badge(fdata["impact"])
                        st.markdown(impact_html, unsafe_allow_html=True)
        
        # Separator between messages
        if idx < len(st.session_state.chat_history) - 1:
            st.markdown("<div style='border-top: 1px solid rgba(90, 24, 154, 0.2); margin: 2rem 0;'></div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

# ==================== INPUT SECTION (BOTTOM) ====================
st.markdown("<div class='input-section-bottom'>", unsafe_allow_html=True)

# Divider before input
if len(st.session_state.chat_history) > 0:
    st.markdown("<div style='border-top: 2px solid rgba(90, 24, 154, 0.3); margin: 1rem 0 1.5rem 0;'></div>", unsafe_allow_html=True)

# Multi-file uploader
st.markdown("<div style='font-weight: 600; margin-bottom: 0.5rem; color: var(--text);'>📎 Attach Media (Optional)</div>", unsafe_allow_html=True)
uploaded_files = st.file_uploader(
    "Upload up to 2 images, or 1 video/audio file",
    type=['png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi', 'mp3', 'wav', 'ogg'],
    accept_multiple_files=True,
    help="Supports: Images (PNG, JPG), Videos (MP4, MOV, AVI), Audio (MP3, WAV, OGG)",
    label_visibility="collapsed",
    key=f"file_uploader_{st.session_state.message_count}",
    disabled=st.session_state.is_typing
)

# Process uploaded files
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
            <div class="media-preview-item" style="animation-delay: {idx * 0.1}s;">
                <div class="media-type-badge">🖼️ Image {idx + 1}</div>
            </div>
            """
        
        elif file_extension in ['mp4', 'mov', 'avi']:
            uploaded_video = file
            media_preview_html += f"""
            <div class="media-preview-item" style="animation-delay: {idx * 0.1}s;">
                <div class="media-type-badge">🎬 Video: {file.name[:25]}...</div>
            </div>
            """
        
        elif file_extension in ['mp3', 'wav', 'ogg']:
            uploaded_audio = file
            media_preview_html += f"""
            <div class="media-preview-item" style="animation-delay: {idx * 0.1}s;">
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
    placeholder="Ask me anything... Type your question here",
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
    **ClarityNet - Explainable AI Platform**
    
    Features:
    • 🧠 Smart model selection
    • 🔍 Transparent reasoning
    • 🎨 Multimodal support (images, video, audio)
    • ⚡ Real-time typewriter effect
    • 🎯 Decision factor analysis
    """)

if clear_clicked:
    st.session_state.chat_history = []
    st.session_state.user_query = ""
    st.session_state.processing = False
    st.session_state.is_typing = False
    st.session_state.message_count = 0
    st.session_state.current_char_index = 0
    st.session_state.generation_complete = False
    st.rerun()

if send_clicked:
    current_query = user_input.strip()
    
    if current_query:
        st.session_state.processing = True
        st.session_state.is_typing = True
        st.session_state.current_char_index = 0
        
        # Clear loading indicator with better messaging
        with st.spinner("🔮 Analyzing your request and generating complete response..."):
            try:
                result = engine.generate_response(
                    query=current_query,
                    images=uploaded_images if uploaded_images else None,
                    video=uploaded_video,
                    audio=uploaded_audio
                )
                
                if result["success"]:
                    factors = engine.get_influencing_factors(
                        result["analysis"],
                        result["response"],
                        current_query
                    )
                    
                    # Store complete response
                    st.session_state.typing_response = result["response"]
                    
                    st.session_state.chat_history.append({
                        "query": current_query,
                        "images": uploaded_images.copy() if uploaded_images else None,
                        "video": uploaded_video,
                        "audio": uploaded_audio,
                        "response": result["response"],
                        "explanation": result["answer_explanation"],
                        "model_name": result["analysis"]["model_name"],
                        "factors": factors,
                        "is_typing": True,
                        "displayed_response": ""
                    })
                    
                    st.session_state.user_query = ""
                    st.session_state.processing = False
                    st.session_state.message_count += 1
                    
                    # Add scroll script to go to new message
                    st.markdown("""
                    <script>
                        setTimeout(function() {
                            window.scrollTo({ top: 0, behavior: 'smooth' });
                        }, 200);
                    </script>
                    """, unsafe_allow_html=True)
                    
                    st.rerun()
                else:
                    st.error(f"❌ {result['error']}")
                    st.session_state.processing = False
                    st.session_state.is_typing = False
                    
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.session_state.processing = False
                st.session_state.is_typing = False
    else:
        st.warning("⚠️ Please enter a question before sending")

# Footer spacing
st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)