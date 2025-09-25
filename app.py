# =====================================================
# 🚀 CypherNova Chatbot - Alternative Entry Point
# =====================================================
# 
# DEPLOYMENT OPTIONS:
# 
# Option 1: Deploy groq.py directly (RECOMMENDED)
# - Main file path: chatbot/groq.py
# - Use this if you want to deploy the chatbot file directly
#
# Option 2: Use this app.py as entry point  
# - Main file path: app.py
# - This file will import and run groq.py
#
# For Streamlit Community Cloud deployment, you can choose either option.
# Most users prefer Option 1 for simplicity.

import streamlit as st

st.info("""
🚀 **CypherNova Chatbot Deployment Options**

**Option 1 (Recommended):** Deploy `chatbot/groq.py` directly
- Set Main file path to: `chatbot/groq.py`

**Option 2:** Use this `app.py` as entry point
- Set Main file path to: `app.py` 
- This will redirect to the main chatbot

Choose Option 1 for the best experience!
""")