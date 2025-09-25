# =====================================================
# 📌 IMPORT REQUIRED LIBRARIES
# =====================================================
# LangChain imports for AI model integration and prompt handling
from langchain.prompts import ChatPromptTemplate  # For creating structured prompts
from langchain_core.output_parsers import StrOutputParser  # For parsing model responses
from langchain_groq import ChatGroq  # Groq AI model integration (fast inference)

# Standard Python libraries
import os  # For environment variable access
import streamlit as st  # Streamlit web app framework
from dotenv import load_dotenv  # For loading environment variables from .env file
import json  # For JSON data handling
import datetime  # For timestamp and duration tracking
from io import StringIO  # For string buffer operations
import time  # For response time measurement
from pathlib import Path  # For robust path handling

# Load environment variables from .env file
load_dotenv()

# =====================================================
# 📌 ENVIRONMENT VARIABLES CONFIGURATION
# =====================================================
# Get Groq API key from environment variables
# This key is required for accessing Groq's AI models
groq_api_key = os.getenv("GROQ_API_KEY")

# Validate that the API key exists
# If not found, display error and stop the application
if not groq_api_key:
    st.error("❌ GROQ_API_KEY not found in environment variables. Please add it to your .env file.")
    st.stop()  # Stop execution if API key is missing

# =====================================================
# 📌 INITIALIZE SESSION STATE (PHASE 1 FEATURES)
# =====================================================
# Session state persists data across Streamlit reruns
# Initialize theme preference (default: light theme)
if "dark_theme" not in st.session_state:
    st.session_state.dark_theme = False

# Initialize chat analytics tracking (Phase 1 feature)
# This dictionary stores various metrics about the chat session
if "chat_analytics" not in st.session_state:
    st.session_state.chat_analytics = {
        "total_messages": 0,           # Total messages exchanged
        "user_messages": 0,            # Messages sent by user
        "bot_messages": 0,             # Messages sent by bot
        "session_start": datetime.datetime.now(),  # Session start time
        "models_used": [],             # List of AI models used in session
        "avg_response_time": []        # List of response times for analytics
    }

# =====================================================
# 📌 STREAMLIT PAGE CONFIGURATION
# =====================================================
# Configure the main Streamlit page settings
# This must be called first, before any other Streamlit commands
st.set_page_config(
    page_title="CypherNova Chatbot",  # Browser tab title
    page_icon="🤖",                   # Browser tab icon
    layout="wide"                     # Use wide layout for better space utilization
)

# =====================================================
# 📌 THEME MANAGEMENT SYSTEM (PHASE 1 FEATURE)
# =====================================================
def apply_theme():
    """
    Apply custom CSS styling based on the selected theme (dark/light)
    This function injects CSS into the Streamlit app to customize appearance
    """
    if st.session_state.dark_theme:
        # COMPREHENSIVE DARK THEME STYLING
        st.markdown("""
        <style>
        /* Force dark theme on entire app */
        .stApp {
            background-color: #0e1117 !important;
            color: #fafafa !important;
        }
        
        /* Main container */
        .main .block-container {
            background-color: #0e1117 !important;
            color: #fafafa !important;
        }
        
        /* Header and toolbar */
        .stAppHeader, .stToolbar {
            background-color: #262730 !important;
        }
        
        /* Sidebar complete styling */
        .stSidebar {
            background-color: #262730 !important;
        }
        
        .stSidebar > div {
            background-color: #262730 !important;
        }
        
        /* All text elements */
        .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, span, div {
            color: #fafafa !important;
        }
        
        /* Input elements */
        .stSelectbox > div > div, .stSelectbox select {
            background-color: #262730 !important;
            color: #fafafa !important;
            border: 1px solid #4a4a4a !important;
        }
        
        .stSlider > div > div {
            background-color: #262730 !important;
        }
        
        .stTextInput > div > div > input {
            background-color: #262730 !important;
            color: #fafafa !important;
            border: 1px solid #4a4a4a !important;
        }
        
        /* Buttons */
        .stButton > button {
            background-color: #262730 !important;
            color: #fafafa !important;
            border: 1px solid #4a4a4a !important;
        }
        
        .stButton > button:hover {
            background-color: #363740 !important;
            color: #ffffff !important;
        }
        
        /* Chat messages */
        .stChatMessage {
            background-color: #1e1e2e !important;
            border: 1px solid #4a4a4a !important;
        }
        
        /* Chat input - Comprehensive coverage including outer containers */
        .stChatInput {
            background-color: #0e1117 !important;
        }
        
        .stChatInput > div {
            background-color: #0e1117 !important;
        }
        
        .stChatInput > div > div {
            background-color: #262730 !important;
            border: 1px solid #4a4a4a !important;
        }
        
        .stChatInput input {
            background-color: #262730 !important;
            color: #fafafa !important;
        }
        
        /* Chat input using data-testid - all containers */
        div[data-testid="stChatInput"] {
            background-color: #0e1117 !important;
        }
        
        div[data-testid="stChatInput"] > div {
            background-color: #0e1117 !important;
        }
        
        div[data-testid="stChatInput"] > div > div {
            background-color: #262730 !important;
            border: 1px solid #4a4a4a !important;
        }
        
        div[data-testid="stChatInput"] input {
            background-color: #262730 !important;
            color: #fafafa !important;
            border: 1px solid #4a4a4a !important;
        }
        
        /* Chat input textarea */
        div[data-testid="stChatInput"] textarea {
            background-color: #262730 !important;
            color: #fafafa !important;
            border: 1px solid #4a4a4a !important;
        }
        
        /* All possible chat input wrapper containers */
        .stBottom {
            background-color: #0e1117 !important;
        }
        
        .stBottom > div {
            background-color: #0e1117 !important;
        }
        
        /* Chat input form containers */
        form[data-testid="stChatInput"] {
            background-color: #0e1117 !important;
        }
        
        form[data-testid="stChatInput"] > div {
            background-color: #0e1117 !important;
        }
        
        /* Fixed bottom container */
        .stAppBottom {
            background-color: #0e1117 !important;
        }
        
        /* Chat input placeholder text */
        div[data-testid="stChatInput"] input::placeholder,
        div[data-testid="stChatInput"] textarea::placeholder {
            color: #888888 !important;
        }
        
        /* Metrics */
        .metric-container {
            background-color: #262730 !important;
        }
        
        /* Dividers */
        .stDivider > div {
            border-color: #4a4a4a !important;
        }
        
        /* Download button */
        .stDownloadButton > button {
            background-color: #262730 !important;
            color: #fafafa !important;
            border: 1px solid #4a4a4a !important;
        }
        
        /* Info boxes */
        .stInfo, .stSuccess, .stWarning, .stError {
            background-color: #262730 !important;
            color: #fafafa !important;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        # LIGHT THEME STYLING (Reset to default)
        st.markdown("""
        <style>
        /* Reset to light theme */
        .stApp {
            background-color: #ffffff !important;
            color: #262730 !important;
        }
        
        .main .block-container {
            background-color: #ffffff !important;
            color: #262730 !important;
        }
        </style>
        """, unsafe_allow_html=True)

# Apply the selected theme immediately
apply_theme()

# =====================================================
# 📌 SIDEBAR CONFIGURATION & BRANDING
# =====================================================
with st.sidebar:
    # CHATBOT BRANDING SECTION
    # Get the path to the image file relative to this script's location
    current_dir = Path(__file__).parent
    image_path = current_dir / "assets" / "chatbot.jpg"
    st.image(str(image_path), width=150)  # 🖼️ Chatbot logo/avatar
    st.markdown("### CypherNova")               # App name
    st.caption("Your personal AI assistant 🤖")  # App tagline
    
    # THEME TOGGLE SECTION (Phase 1 Feature)
    st.divider()  # Visual separator
    col1, col2 = st.columns([3, 1])  # Create two columns for layout
    
    with col1:
        st.markdown("### 🎨 Theme")  # Theme section header
    
    with col2:
        # Dynamic theme toggle button with appropriate icon
        theme_icon = "🌙" if not st.session_state.dark_theme else "☀️"
        if st.button(theme_icon, key="theme_toggle", help="Toggle between dark and light theme"):
            # Toggle theme state and trigger app rerun to apply changes
            st.session_state.dark_theme = not st.session_state.dark_theme
            st.rerun()  # Refresh app to apply new theme
    
    # AI MODEL SELECTION SECTION
    st.divider()  # Visual separator
    st.markdown("### 🤖 Model Settings")
    
    # Dropdown to select AI model
    # These are currently supported Groq models (updated for 2025)
    groq_model = st.selectbox(
        "Choose Groq Model:",
        [
            "llama-3.1-8b-instant",      # Fast, efficient model for general use
            "llama-3.1-70b-versatile",   # More powerful model for complex tasks
            "llama-3.2-1b-preview",      # Lightweight model for quick responses
            "llama-3.2-3b-preview",      # Balanced model for most use cases
            "mixtral-8x7b-32768",        # Mixture of experts model
            "gemma2-9b-it"               # Google's Gemma model
        ],
        index=0,  # Default to first model (llama-3.1-8b-instant)
        help="All models are free to use within Groq's free tier limits"
    )
    
    # AI MODEL PARAMETER CONTROLS
    # Temperature controls randomness/creativity of responses
    temperature = st.slider(
        "Temperature:",
        min_value=0.0,    # Most deterministic (consistent responses)
        max_value=1.0,    # Most creative (varied responses)
        value=0.2,        # Default: slightly creative but mostly consistent
        step=0.1,
        help="Lower = more deterministic, Higher = more creative"
    )
    
    # Max tokens controls length of AI responses
    max_tokens = st.slider(
        "Max Response Length:",
        min_value=100,     # Minimum response length
        max_value=4096,    # Maximum response length
        value=1024,        # Default: moderate length responses
        step=100,
        help="Maximum tokens in the response"
    )
    
    st.divider()  # Visual separator
    
    # CHAT MANAGEMENT BUTTONS (Phase 1 Features)
    col1, col2 = st.columns(2)  # Create two columns for buttons
    
    with col1:
        # CLEAR CHAT BUTTON
        if st.button("🗑️ Clear Chat", key="clear_chat"):
            # Reset chat messages to empty
            st.session_state.messages = []
            
            # Reset analytics for new session (Phase 1 feature)
            st.session_state.chat_analytics = {
                "total_messages": 0,
                "user_messages": 0,
                "bot_messages": 0,
                "session_start": datetime.datetime.now(),
                "models_used": [],
                "avg_response_time": []
            }
            st.rerun()  # Refresh the app to show cleared state
    
    with col2:
        # EXPORT CHAT BUTTON (Phase 1 Feature)
        if st.button("📥 Export Chat", key="export_chat"):
            # Check if there's meaningful chat history to export
            if len(st.session_state.messages) > 1:
                # Prepare export data structure (could be used for JSON export in future)
                export_data = {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "model_used": groq_model,
                    "conversation": st.session_state.messages,
                    "analytics": st.session_state.chat_analytics
                }
                
                # CREATE TEXT FORMAT FOR DOWNLOAD
                # Header with export timestamp
                chat_text = f"CypherNova Chat Export - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                chat_text += "=" * 60 + "\n\n"
                
                # Add all messages with role indicators
                for msg in st.session_state.messages:
                    role_emoji = "👤" if msg["role"] == "user" else "🤖"
                    chat_text += f"{role_emoji} {msg['role'].upper()}: {msg['content']}\n\n"
                
                # ADD ANALYTICS SECTION (Phase 1 feature)
                chat_text += "\n" + "=" * 60 + "\n"
                chat_text += "CHAT ANALYTICS:\n"
                chat_text += f"Total Messages: {st.session_state.chat_analytics['total_messages']}\n"
                chat_text += f"User Messages: {st.session_state.chat_analytics['user_messages']}\n"
                chat_text += f"Bot Messages: {st.session_state.chat_analytics['bot_messages']}\n"
                chat_text += f"Session Duration: {datetime.datetime.now() - st.session_state.chat_analytics['session_start']}\n"
                
                # Create download button with timestamped filename
                st.download_button(
                    label="Download Chat History",
                    data=chat_text,
                    file_name=f"cyphernova_chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain",
                    help="Download your conversation as a text file"
                )
            else:
                st.info("No chat history to export")  # Show info if no chat to export
    
    # SIDEBAR ANALYTICS SECTION (Phase 1 Feature)
    st.divider()  # Visual separator
    st.markdown("### 📊 Chat Analytics")
    
    # Display analytics if there are messages
    if st.session_state.chat_analytics["total_messages"] > 0:
        # Create two columns for metrics layout
        col1, col2 = st.columns(2)
        
        with col1:
            # Display total message count
            st.metric("Messages", st.session_state.chat_analytics["total_messages"])
        
        with col2:
            # Calculate and display session duration
            duration = datetime.datetime.now() - st.session_state.chat_analytics["session_start"]
            st.metric("Session", f"{duration.seconds//60}m")
        
        # Show average response time if we have response time data
        if st.session_state.chat_analytics["avg_response_time"]:
            avg_time = sum(st.session_state.chat_analytics["avg_response_time"]) / len(st.session_state.chat_analytics["avg_response_time"])
            st.metric("Avg Response", f"{avg_time:.1f}s")
    else:
        # Show info message when no chat data is available
        st.info("Start chatting to see analytics!")
    
    # GROQ API INFORMATION SECTION
    st.markdown("---")  # Horizontal line separator
    st.markdown("### ℹ️ Free Tier Info")
    
    # Display current Groq API limitations and benefits
    st.info("""
    **Groq Free Limits:**
    - 50 requests/minute
    - 10,000 tokens/minute
    - No credit card required
    """)

# =====================================================
# 📌 MAIN PAGE HEADER & TITLE
# =====================================================
# Display centered title and subtitle with custom HTML styling
st.markdown(
    """
    <div style='text-align: center; margin-bottom: 20px;'>
        <h1>CypherNova Chatbot With Groq Cloud</h1>
        <h3>Ask me anything! 🚀</h3>
        <p><i>Powered by Groq's fast LLMs - Running in the cloud ☁️</i></p>
    </div>
    """,
    unsafe_allow_html=True  # Allow HTML for custom styling
)

# =====================================================
# 📌 GROQ MODEL INITIALIZATION & CACHING
# =====================================================

def load_groq_model(model_name, temperature, max_tokens):
    """
    Initialize the Groq LLM model
    
    Args:
        model_name (str): Name of the Groq model to use
        temperature (float): Controls randomness in responses (0.0-1.0)
        max_tokens (int): Maximum length of model responses
    
    Returns:
        ChatGroq: Initialized Groq model object or None if error
    """
    try:
        # Initialize Groq model with provided parameters
        llm = ChatGroq(
            groq_api_key=groq_api_key,    # API key from environment
            model_name=model_name,         # Selected model
            temperature=temperature,       # Creativity level
            max_tokens=max_tokens         # Response length limit
        )
        return llm
    except Exception as e:
        # Display error if model initialization fails
        st.error(f"❌ Error initializing Groq model: {str(e)}")
        return None

# Initialize the model with current settings
llm = load_groq_model(groq_model, temperature, max_tokens)

# Stop execution if model initialization failed
if llm is None:
    st.stop()

# =====================================================
# 📌 CHAT SYSTEM INITIALIZATION
# =====================================================

# Initialize chat history in session state
# Session state persists data across user interactions
if "messages" not in st.session_state:
    # Start with a welcome message from the assistant
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "CypherNova is HERE! 🌸 How can I help you today?", 
            "timestamp": datetime.datetime.now().isoformat()  # Add timestamp for analytics
        }
    ]

# Clean up any corrupted messages (response objects instead of strings)
# This is a one-time cleanup for backward compatibility
if st.session_state.messages:
    cleaned_messages = []
    for msg in st.session_state.messages:
        if isinstance(msg.get("content"), str):
            cleaned_messages.append(msg)
        elif hasattr(msg.get("content"), 'content'):
            # Extract content from response object
            cleaned_msg = msg.copy()
            cleaned_msg["content"] = msg["content"].content
            cleaned_messages.append(cleaned_msg)
    st.session_state.messages = cleaned_messages

# =====================================================
# 📌 MESSAGE COPY FUNCTIONALITY (PHASE 1 FEATURE)
# =====================================================
def copy_message_button(message_content, message_id):
    """
    Create a copy button for each message (currently unused in favor of Streamlit buttons)
    
    This function creates JavaScript-based copy functionality.
    Currently using Streamlit's built-in button functionality instead.
    
    Args:
        message_content (str): The text content to copy
        message_id (str): Unique identifier for the message
    
    Returns:
        str: HTML/JavaScript code for copy button
    """
    copy_script = f"""
    <script>
    function copyToClipboard{message_id}() {{
        navigator.clipboard.writeText(`{message_content.replace('`', '\\`')}`).then(function() {{
            console.log('Copied to clipboard');
        }});
    }}
    </script>
    <button onclick="copyToClipboard{message_id}()" class="copy-button" 
            style="background: transparent; border: 1px solid #ccc; border-radius: 4px; padding: 4px 8px; 
                   font-size: 12px; cursor: pointer; margin-left: 10px;">
        📋 Copy
    </button>
    """
    return copy_script

# =====================================================
# 📌 DISPLAY CHAT HISTORY WITH COPY BUTTONS (PHASE 1)
# =====================================================
# Display all past messages (user + assistant) with copy functionality
for i, msg in enumerate(st.session_state.messages):
    # Use Streamlit's chat message container for proper styling
    with st.chat_message(msg["role"]):
        # Create two columns: main content and copy button
        col1, col2 = st.columns([10, 1])  # 10:1 ratio for content vs button
        
        with col1:
            # Display the message content
            st.markdown(msg["content"])
        
        with col2:
            # Copy button for each message (Phase 1 feature)
            if st.button("📋", key=f"copy_{i}", help="Copy message"):
                # Show success notification when button is clicked
                # Note: Actual clipboard functionality is handled by browser
                st.toast(f"Message copied! 📋", icon="✅")

# =====================================================
# 📌 CHAT INPUT HANDLING & USER MESSAGE PROCESSING
# =====================================================
# Chat input box - captures user input when submitted
if user_input := st.chat_input("Type your message here..."):
    
    # UPDATE ANALYTICS (Phase 1 Feature)
    # Track message counts for analytics dashboard
    st.session_state.chat_analytics["total_messages"] += 1
    st.session_state.chat_analytics["user_messages"] += 1
    
    # ADD USER MESSAGE TO CHAT HISTORY
    # Store message with metadata for future features
    st.session_state.messages.append({
        "role": "user", 
        "content": user_input, 
        "timestamp": datetime.datetime.now().isoformat()  # For analytics and export
    })
    
    # DISPLAY USER MESSAGE WITH COPY BUTTON
    with st.chat_message("user"):
        col1, col2 = st.columns([10, 1])  # Layout: content + copy button
        
        with col1:
            st.markdown(user_input)  # Display user's message
        
        with col2:
            # Copy button for user's own message (Phase 1 feature)
            if st.button("📋", key=f"copy_user_{len(st.session_state.messages)}", help="Copy message"):
                st.toast(f"Message copied! 📋", icon="✅")

    # =====================================================
    # 📌 PREPARE AI MODEL INPUT & CONVERSATION CONTEXT
    # =====================================================
    
    # CREATE CONVERSATION MESSAGES FOR THE AI MODEL
    # Start with system prompt to define AI personality and behavior
    conversation_messages = [
        ("system", "You are CypherNova Chatbot, a friendly and helpful AI assistant. "
                   "Always answer warmly and conversationally. Keep responses concise and helpful.")
    ]
    
    # ADD CONVERSATION HISTORY FOR CONTEXT
    # Include all previous messages except the current user input (it's already added separately)
    for msg in st.session_state.messages[:-1]:  # Exclude the last message (current user input)
        if msg["role"] in ["user", "assistant"]:
            # Handle both string content and response objects (for backward compatibility)
            content = msg["content"]
            if hasattr(content, 'content'):  # If it's a response object, extract content
                content = content.content
            elif not isinstance(content, str):  # If it's not a string, convert it
                content = str(content)
            
            # Escape any curly braces to prevent template variable issues
            content = content.replace("{", "{{").replace("}", "}}")
            conversation_messages.append((msg["role"], content))
    
    # ADD CURRENT USER INPUT
    # Escape any curly braces in user input to prevent template variable issues
    safe_user_input = user_input.replace("{", "{{").replace("}", "}}")
    conversation_messages.append(("user", safe_user_input))
    
    # CREATE LANGCHAIN PROMPT TEMPLATE
    # This structures the conversation for the AI model
    prompt = ChatPromptTemplate.from_messages(conversation_messages)

    # =====================================================
    # 📌 AI RESPONSE GENERATION & ANALYTICS TRACKING
    # =====================================================
    
    # GENERATE AI RESPONSE WITH ERROR HANDLING
    with st.chat_message("assistant"):
        try:
            # SHOW TYPING INDICATOR
            message_placeholder = st.empty()
            message_placeholder.markdown("⏳ Thinking...")
            
            # TRACK RESPONSE TIME (Phase 1 Analytics Feature)
            start_time = time.time()
            
            # GET AI RESPONSE
            # Format the prompt and get response from LLM directly
            formatted_messages = prompt.format_messages()
            ai_response = llm.invoke(formatted_messages)
            
            # Extract just the content from the response object
            response = ai_response.content
            
            # CALCULATE AND STORE RESPONSE TIME
            response_time = time.time() - start_time
            st.session_state.chat_analytics["avg_response_time"].append(response_time)
            st.session_state.chat_analytics["total_messages"] += 1
            st.session_state.chat_analytics["bot_messages"] += 1
            
            # TRACK MODEL USAGE FOR ANALYTICS
            if groq_model not in st.session_state.chat_analytics["models_used"]:
                st.session_state.chat_analytics["models_used"].append(groq_model)
            
            # DISPLAY RESPONSE WITH COPY BUTTON (Phase 1 Feature)
            col1, col2 = st.columns([10, 1])  # Layout: content + copy button
            
            with col1:
                message_placeholder.markdown(response)  # Show AI response
            
            with col2:
                # Copy button for AI response
                if st.button("📋", key=f"copy_assistant_{len(st.session_state.messages)}", help="Copy message"):
                    st.toast(f"Message copied! 📋", icon="✅")
            
            # ADD RESPONSE TO CHAT HISTORY WITH METADATA
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response, 
                "timestamp": datetime.datetime.now().isoformat(),  # For export and analytics
                "response_time": response_time,                    # Performance tracking
                "model": groq_model                               # Model used for this response
            })
            
        except Exception as e:
            # ERROR HANDLING & LOGGING
            error_msg = f"❌ Sorry, I encountered an error: {str(e)}"
            st.error(error_msg)  # Display error to user
            
            # ADD ERROR MESSAGE TO CHAT HISTORY
            st.session_state.messages.append({
                "role": "assistant", 
                "content": error_msg, 
                "timestamp": datetime.datetime.now().isoformat(),
                "error": True  # Flag to identify error messages
            })
            
            # UPDATE ERROR ANALYTICS
            st.session_state.chat_analytics["total_messages"] += 1
            st.session_state.chat_analytics["bot_messages"] += 1



