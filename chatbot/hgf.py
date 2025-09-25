# =====================================================
# 📌 Import Required Libraries
# =====================================================
from huggingface_hub import InferenceClient
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Get Hugging Face token
try:
    hf_token = st.secrets["HF_API_TOKEN"]
except KeyError:
    hf_token = os.getenv("HF_API_TOKEN") 

# =====================================================
# 📌 UI SECTION
# =====================================================
st.set_page_config(page_title="CypherNova Chatbot", page_icon="🤖", layout="wide")

with st.sidebar:
    st.image("chatbot/assets/chatbot.jpg", width=150)
    st.markdown("### CypherNova")
    st.caption("Your personal AI assistant 🤖")
    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

st.markdown(
    """
    <div style='text-align: center; margin-bottom: 20px;'>
        <h1>CypherNova Chatbot With HuggingFace</h1>
        <h3>Ask me anything!</h3>
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================
# 📌 Chatbot Logic
# =====================================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "CypherNova is HERE! 🌸 I'm powered by state-of-the-art AI models. How can I help you today?"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

def get_llm_response(user_input):
    """Use the best performing free Hugging Face models"""
    try:
        client = InferenceClient(token=hf_token)
        
        # Build conversation history
        conversation = ""
        for msg in st.session_state.messages[-6:]:  # Last 3 exchanges
            if msg["role"] == "user":
                conversation += f"User: {msg['content']}\n"
            elif msg["role"] == "assistant":
                conversation += f"Assistant: {msg['content']}\n"
        
        prompt = f"""You are CypherNova, a helpful and intelligent AI assistant. Provide detailed, accurate, and helpful responses.

{conversation}User: {user_input}
Assistant:"""
        
        # Try the best performing models in order
        high_performance_models = [
            "mistralai/Mistral-7B-Instruct-v0.3",  # Newest Mistral - excellent
            "mistralai/Mistral-7B-Instruct-v0.2",  # Very reliable
            "HuggingFaceH4/zephyr-7b-beta",        # High quality
            "google/gemma-7b-it",                  # Google's model
            "meta-llama/Llama-2-7b-chat-hf",       # Llama 2
        ]
        
        for model in high_performance_models:
            try:
                response = client.text_generation(
                    prompt=prompt,
                    model=model,
                    max_new_tokens=500,
                    temperature=0.7,
                    do_sample=True,
                    return_full_text=False
                )
                
                if response and response.strip():
                    return response.strip()
                    
            except Exception as e:
                continue  # Try next model
        
        # If specific models fail, try without model specification
        response = client.text_generation(
            prompt=prompt,
            max_new_tokens=400,
            temperature=0.7
        )
        return response.strip()
        
    except Exception as e:
        # Simple fallback that doesn't mention errors
        return "I'm here to help! What specific information are you looking for?"

# Chat logic
if user_input := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            response = get_llm_response(user_input)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})