import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- 1. SECURITY CONFIG ---
# Change this to whatever you want your private password to be
THE_PASSWORD = "Jaelin11@" 

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
            st.error("🚫 Wrong password. Practice your jump shot instead.")
    return False

# Stop execution if not logged in
if not check_password():
    st.stop()

# --- 2. AI CONFIG ---
try:
    # Make sure 'GEMINI_API_KEY' is set in your Streamlit Cloud Secrets
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("Missing API Key! Go to Streamlit Settings > Secrets and add: GEMINI_API_KEY = 'your_key'")
    st.stop()

# Use 'gemini-1.5-flash-latest' to avoid the 404 errors you were seeing
MODEL_NAME = 'gemini-1.5-flash-latest'

st.set_page_config(page_title="The Private Oracle", page_icon="🏀")
st.title("🧠 The Private Oracle")
st.caption("Secure. Fast. Unblocked. Built for Jaelin.")

# Sidebar
st.sidebar.title("Controls")
mode = st.sidebar.selectbox("Mode:", ["Homework Help", "Analyze Image"])
if st.sidebar.button("Log Out"):
    st.session_state.password_correct = False
    st.rerun()

# --- 3. MODE: HOMEWORK HELP (CHAT) ---
if mode == "Homework Help":
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question..."):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display assistant response
        with st.chat_message("assistant"):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                if "429" in str(e):
                    st.error("Slow down! You're hitting the free limit. Wait 30 seconds.")
                else:
                    st.error(f"Error: {e}")

# --- 4. MODE: ANALYZE IMAGE ---
elif mode == "Analyze Image":
    st.write("Take a photo of your homework or meal prep and I'll break it down.")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Scanning...", use_container_width=True)
        instruction = st.text_input("Instructions:", "Solve this and explain how it works.")
        
        if st.button("Analyze"):
            with st.spinner("Thinking..."):
                try:
                    model = genai.GenerativeModel(MODEL_NAME)
                    response = model.generate_content([instruction, img])
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
