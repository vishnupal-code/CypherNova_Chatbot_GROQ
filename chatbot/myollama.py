# =====================================================
# 📌 Import Required Libraries
# =====================================================
from langchain.prompts import ChatPromptTemplate   # ✅ fixed import
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# =====================================================
# 📌 Environment Variables (Optional Setup)
# =====================================================
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# os.environ["OLLAMA_API_KEY"] = os.getenv("OLLAMA_API_KEY")

langchain_key = os.getenv("LANGCHAIN_API_KEY")
if langchain_key:
    os.environ["LANGCHAIN_API_KEY"] = langchain_key


# =====================================================
# 📌 UI SECTION (Design & Layout)
# =====================================================

# Page settings (title, icon, layout)
st.set_page_config(page_title="CypherNova Chatbot", page_icon="🤖", layout="wide")

with st.sidebar:
    st.image("chatbot/assets/chatbot.jpg", width=150)


   # 🖼️ Replace with your logo/photo
    st.markdown("### CypherNova")
    st.caption("Your personal AI assistant 🤖")
    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Centered title & subtitle
st.markdown(
    """
    <div style='text-align: center; margin-bottom: 20px;'>
        <h1>CypherNova Chatbot With Ollama</h1>
        <h3>Ask me anything!</h3>
    </div>
    """,
    unsafe_allow_html=True
)


# =====================================================
# 📌 Chatbot Logic (No changes here, kept as is)
# =====================================================

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "CypherNova is HERE! 🌸 How can I help you today?"}
    ]

# Display past messages (user + assistant)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input box
if user_input := st.chat_input("Type your message here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Create chatbot prompt dynamically with history
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are CypherNova Chatbot, a friendly and helpful AI assistant. "
                       "Always answer warmly and conversationally."),
            *[(m["role"], m["content"]) for m in st.session_state.messages if m["role"] != "system"]
        ]
    )

    # LLM + chain
    llm = Ollama(model="llama3.2", temperature=0.2)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser

    # Get response
    response = chain.invoke({"Question": user_input})

    # Show response
    with st.chat_message("assistant"):
        st.markdown(response)

    # Add response to history
    st.session_state.messages.append({"role": "assistant", "content": response})

# redeploy fix

# =====================================================
#enjoy using it