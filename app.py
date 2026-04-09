import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- 1. SECURITY CONFIG ---
# Your private password
THE_PASSWORD = "Jaelin1102@" 

def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    
    if st.session_state.password_correct:
        return True

    st.title("🔒 The Sauce is Private")
    st.write("Authorized access only. Log in to use the Oracle.")
    
    pwd = st.text_input("Password", type="password")
    if st.button("Unlock"):
        if pwd == THE_PASSWORD:
            st.session_state.password_correct = True
            st.rerun()
        else:
            st.error("🚫 Access Denied.")
    return False

if not check_password():
    st.stop()

# --- 2. AI CONFIG (2026 UPDATE) ---
try:
    # Ensure GEMINI_API_KEY is in your Streamlit Cloud Secrets
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("API Key missing! Add GEMINI_API_KEY to your Streamlit Secrets.")
    st.stop()

# Using the stable 2026 model name to stop 404 errors
MODEL_NAME = 'gemini-2.5-flash'

st.set_page_config(page_title="The Private Oracle", page_icon="🏀")
st.title("🧠 The Private Oracle")
st.caption("Secure. Stable. Built for the SG transition.")

# Sidebar
st.sidebar.title("Controls")
mode = st.sidebar.selectbox("Mode:", ["Homework Help", "Analyze Image"])
if st.sidebar.button("Log Out"):
    st.session_state.password_correct = False
    st.rerun()

# --- 3. CHAT MODE ---
if mode == "Homework Help":
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {e}")

# --- 4. IMAGE MODE ---
elif mode == "Analyze Image":
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)
        instruction = st.text_input("Instructions:", "Solve and explain.")
        
        if st.button("Analyze"):
            with st.spinner("Thinking..."):
                try:
                    model = genai.GenerativeModel(MODEL_NAME)
                    response = model.generate_content([instruction, img])
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
