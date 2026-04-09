import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 1. Setup - Pulls the key from your Streamlit "Secrets"
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("API Key missing! Add GEMINI_API_KEY to your Streamlit Secrets.")

st.set_page_config(page_title="The Unblocked Oracle", page_icon="🧠")
st.title("🧠 The Unblocked Oracle")
st.caption("Homework helper, Artist, and Image Analyst. Built for the grind.")

# Sidebar for mode selection
mode = st.sidebar.selectbox("Choose your weapon:", ["Homework Help", "Create Pictures", "Analyze Image"])

# --- MODE 1: CHAT & HOMEWORK ---
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
                st.error(f"The Oracle is tired. Wait 30 seconds and try again. (Error: {e})")

# --- MODE 2: IMAGE GENERATION ---
elif mode == "Create Pictures":
    prompt = st.text_input("Describe the image you want:")
    if st.button("Generate"):
        if prompt:
            with st.spinner("Mixing the paint..."):
                try:
                    # Note: Requires Gemini API access to Imagen
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(f"Describe a detailed image prompt for: {prompt}")
                    st.info(f"Generating based on: {response.text[:100]}...")
                    st.warning("Image generation via API requires specific permissions. Check your Google AI Studio tier.")
                except Exception as e:
                    st.error(f"Image generation failed: {e}")
        else:
            st.warning("You gotta type something first.")

# --- MODE 3: IMAGE ANALYSIS ---
elif mode == "Analyze Image":
    uploaded_file = st.file_uploader("Upload homework photo:", type=["jpg", "jpeg", "png"])
    user_task = st.text_input("Instruction:", "Solve this and explain the steps.")
    
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption="Scanning...", use_container_width=True)
        
        if st.button("Analyze"):
            model = genai.GenerativeModel('gemini-1.5-flash')
            with st.spinner("Processing pixels..."):
                try:
                    response = model.generate_content([user_task, img])
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
