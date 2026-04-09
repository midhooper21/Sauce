import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- 1. CONFIG & SECURITY ---
# Change 'sauce_god_2026' to whatever password you want
THE_PASSWORD = "Jaelin11@" 

def check_password():
    """Returns True if the user had the correct password."""
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    
    if st.session_state.password_correct:
        return True

    st.title("🔒 The Sauce is Locked")
    pwd = st.text_input("Enter Password to Access the Oracle:", type="password")
    if st.button("Unlock"):
        if pwd == THE_PASSWORD:
            st.session_state.password_correct = True
            st.rerun()
        else:
            st.error("🚫 Access Denied. Go do your own homework.")
    return False

# Stop the rest of the app if not logged in
if not check_password():
    st.stop()

# --- 2. AI SETUP ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("API Key missing in Streamlit Secrets!")
    st.stop()

st.title("🧠 The Private Oracle")
st.caption("Locked down. Optimized. Only for the elite.")

# Sidebar
mode = st.sidebar.selectbox("Choose Mode:", ["Homework Help", "Create Pictures", "Analyze Image"])
if st.sidebar.button("Log Out"):
    st.session_state.password_correct = False
    st.rerun()

# --- 3. CHAT LOGIC ---
if mode == "Homework Help":
    model = genai.GenerativeModel('gemini-1.5-flash')
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Quota hit or error: {e}")

# --- 4. IMAGE ANALYSIS ---
elif mode == "Analyze Image":
    uploaded_file = st.file_uploader("Upload homework photo:", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Scanning...", use_container_width=True)
        user_task = st.text_input("What should I do with this?", "Solve and explain.")
        
        if st.button("Analyze"):
            model = genai.GenerativeModel('gemini-1.5-flash')
            with st.spinner("Processing..."):
                try:
                    response = model.generate_content([user_task, img])
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Failed: {e}")

# --- 5. IMAGE GEN ---
elif mode == "Create Pictures":
    st.info("Direct Image Gen requires a Pro API key, but you can ask for prompts here!")
    prompt = st.text_input("Describe your vision:")
    if st.button("Get Concept"):
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"Give me a visual description for: {prompt}")
        st.write(res.text)
