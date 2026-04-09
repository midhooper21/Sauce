import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Setup - Replace with your actual key or use streamlit secrets
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="The Unblocked Oracle", page_icon="💀")
st.title("🧠 The Unblocked Oracle")
st.caption("Homework helper, Artist, and Image Analyst. Use it wisely.")

# Sidebar for choosing the mode
mode = st.sidebar.selectbox("Choose your weapon:", ["Homework Help/Chat", "Create Pictures", "Analyze Image"])

# --- MODE 1: CHAT & HOMEWORK ---
if mode == "Homework Help/Chat":
    model = genai.GenerativeModel('gemini-2.0-flash')
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
           try:
            response = model.generate_content(prompt)
        st.markdown(response.text)
except Exception as e:
    if "429" in str(e) or "ResourceExhausted" in str(e):
        st.error("Chill out! The AI is catching its breath. Try again in 30 seconds.")
    else:
        st.error(f"Something went wrong: {e}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

# --- MODE 2: IMAGE GENERATION ---
elif mode == "Create Pictures":
    prompt = st.text_input("Describe the image you want:")
    if st.button("Generate"):
        if prompt:
            with st.spinner("Cooking up some pixels..."):
                # Note: Uses the Imagen/Nano-Banana integration
                imagen = genai.ImageGenerationModel("imagen-3.0-generate-001")
                result = imagen.generate_images(prompt=prompt)
                st.image(result.images[0]._pil_image)
        else:
            st.warning("Type something first, genius.")

# --- MODE 3: IMAGE ANALYSIS (Accepts Images) ---
elif mode == "Analyze Image":
    uploaded_file = st.file_uploader("Upload a photo of your homework/problem:", type=["jpg", "jpeg", "png"])
    user_task = st.text_input("What should I do with this image?", "Explain this or solve the problem.")
    
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption="Target Acquired", use_column_width=True)
        
        if st.button("Process"):
            model = genai.GenerativeModel('gemini-1.5-flash')
            with st.spinner("Scanning..."):
                response = model.generate_content([user_task, img])
                st.write(response.text)
