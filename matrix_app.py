import streamlit as st
import os
from openai import OpenAI

# Page config
st.set_page_config(
    page_title="Matrix AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Simple Matrix-themed CSS (much lighter)
st.markdown("""
<style>
    .stApp {
        background-color: #0a0a0a;
        color: #00ff41;
    }
    
    .main-title {
        color: #00ff41;
        text-align: center;
        font-family: 'Courier New', monospace;
        font-size: 3rem;
        text-shadow: 0 0 10px #00ff41;
        margin-bottom: 20px;
    }
    
    .chat-message-user {
        background-color: #1e3c72;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #00ff41;
    }
    
    .chat-message-bot {
        background-color: #1a1a1a;
        color: #00ff41;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #00ff41;
        border: 1px solid #00ff41;
    }
    
    .stTextInput input {
        background-color: #1a1a1a;
        color: #00ff41;
        border: 2px solid #00ff41;
    }
    
    .stButton button {
        background-color: #00ff41;
        color: black;
        font-weight: bold;
        border: none;
        border-radius: 5px;
    }
    
    .setup-box {
        background-color: #2a2a2a;
        border: 2px solid #ff6b6b;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        color: #ff6b6b;
    }
    
    .success-box {
        background-color: #1a2a1a;
        border: 2px solid #00ff41;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
        color: #00ff41;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "openai_client" not in st.session_state:
    st.session_state.openai_client = None

def get_api_key():
    """Get API key from secrets or environment"""
    try:
        # Try Streamlit secrets first
        api_key = st.secrets.get("OPENAI_API_KEY", "")
        if api_key:
            return api_key
    except:
        pass
    
    # Try environment variable
    api_key = os.getenv("OPENAI_API_KEY", "")
    return api_key if api_key else None

def initialize_openai():
    """Initialize OpenAI client"""
    api_key = get_api_key()
    if api_key:
        try:
            st.session_state.openai_client = OpenAI(api_key=api_key)
            return True
        except Exception as e:
            st.error(f"Error initializing OpenAI: {e}")
            return False
    return False

def get_ai_response(user_message):
    """Get AI response with 100-word limit"""
    try:
        response = st.session_state.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant in the Matrix. Keep responses under 100 words. Be concise and helpful."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    # Title
    st.markdown('<h1 class="main-title">🤖 MATRIX AI CHATBOT 🤖</h1>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; color: #00ff41; margin-bottom: 30px;">Welcome to the Matrix</div>', unsafe_allow_html=True)
    
    # Check API key setup
    api_key = get_api_key()
    
    if not api_key:
        st.markdown("""
        <div class="setup-box">
            <h3>🔧 Setup Required</h3>
            <p><strong>OpenAI API Key Not Found!</strong></p>
            <p>Please add your API key using one of these methods:</p>
            
            <h4>Method 1: Environment Variable</h4>
            <p>In VS Code terminal, run:</p>
            <code>set OPENAI_API_KEY=sk-your-key-here</code> (Windows)<br>
            <code>export OPENAI_API_KEY=sk-your-key-here</code> (Mac/Linux)
            
            <h4>Method 2: Secrets File</h4>
            <p>Create <code>.streamlit/secrets.toml</code> with:</p>
            <code>OPENAI_API_KEY = "sk-your-key-here"</code>
            
            <p><a href="https://platform.openai.com/api-keys" target="_blank">Get your API key here</a></p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()
    
    # Initialize OpenAI
    if not st.session_state.openai_client:
        if not initialize_openai():
            st.error("Failed to initialize OpenAI client")
            st.stop()
    
    # Success message
    st.markdown("""
    <div class="success-box">
        ✅ <strong>Connected to OpenAI API</strong> - Ready to chat!
    </div>
    """, unsafe_allow_html=True)
    
    # Display chat history
    st.markdown("### 💬 Chat History")
    
    if st.session_state.messages:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message-user"><strong>🧑 You:</strong><br>{message["content"]}</div>', 
                           unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message-bot"><strong>🤖 Matrix AI:</strong><br>{message["content"]}</div>', 
                           unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align: center; color: #00ff41; font-style: italic;">Start your conversation...</div>', 
                   unsafe_allow_html=True)
    
    # Input section
    st.markdown("---")
    
    # User input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Your message:",
            placeholder="Enter your message...",
            key="user_input_field"
        )
    
    with col2:
        send_button = st.button("🚀 SEND", use_container_width=True)
    
    # Handle send button
    if send_button and user_input.strip():
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get AI response
        with st.spinner("🔄 Matrix AI is thinking..."):
            ai_response = get_ai_response(user_input)
        
        # Add AI response
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
        # Refresh the app
        st.rerun()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🛠️ Controls")
        
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("## ℹ️ Info")
        st.markdown(f"**Messages:** {len(st.session_state.messages)}")
        st.markdown(f"**API Key:** {'✅ Set' if api_key else '❌ Missing'}")
        
        st.markdown("---")
        st.markdown("**Features:**")
        st.markdown("- Matrix-themed UI")
        st.markdown("- OpenAI GPT-3.5-turbo")
        st.markdown("- 100-word response limit")
        st.markdown("- Chat history")

if __name__ == "__main__":
    main()