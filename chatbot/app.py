# use it for OpenAI API calls
# for free version of Ollama, use myollama.py




# importing the required libraries
from langchain_openai import ChatOpenAI   # ✅ Correct import
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.callbacks.base import BaseCallbackHandler

import streamlit as st

from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("LANGSMITH_API_KEY")
if not api_key:
    raise EnvironmentError("LANGSMITH_API_KEY is missing in the .env file.")

os.environ["LANGSMITH_API_KEY"] = api_key



# Similarly, use other keys as needed


# # LangChain tracking (optional)
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# --- Streaming Callback ---
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.text = ""

    def on_llm_new_token(self, token, **kwargs):
        self.text += token
        self.container.markdown(self.text)

# --- Streamlit App ---
st.title("⚡ Fast Chatbot with LangChain + Streamlit")
st.subheader("Ask me anything!")

# Input
input_text = st.text_input("Ask your question here")

if input_text:
    # Placeholder for streaming output
    response_container = st.empty()

    # Attach streaming handler
    stream_handler = StreamHandler(response_container)

    # Use a smaller/faster model if available (swap llama3.2 → llama3.1:8b or mistral)
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",   # 🔄 replace with "llama3.1:8b" if using Ollama
        temperature=0.3,
        streaming=True,
        callbacks=[stream_handler]
    )

    # Prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("user", "Question: {Question}")
    ])

    chain = prompt | llm | StrOutputParser()

    # Run chain
    chain.invoke({"Question": input_text})
