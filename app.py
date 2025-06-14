import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("STABILITY_API_KEY")

# UI title
st.title("🎨 AI Image Generation Chatbot")
st.markdown("Enter your prompt and select a model to generate stunning images using Stability AI.")

# Prompt input
prompt = st.text_input("📝 Enter your prompt:", placeholder="e.g. A futuristic city at sunset in the style of Studio Ghibli")

# Model selection dropdown
model_choice = st.selectbox("🧠 Choose model", ["core", "ultra", "sd3"])

# Map model name to actual endpoint
model_endpoints = {
    "core": "https://api.stability.ai/v2beta/stable-image/generate/core",
    "ultra": "https://api.stability.ai/v2beta/stable-image/generate/ultra",
    "sd3": "https://api.stability.ai/v2beta/stable-image/generate/sd3"
}

def generate_image(prompt, model):
    url = model_endpoints[model]
    headers = {
        "authorization": f"Bearer {API_KEY}",
        "accept": "image/*"
    }
    data = {
        "prompt": prompt,
        "output_format": "jpeg"
    }

    response = requests.post(url, headers=headers, files={"none": ''}, data=data)

    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        st.error(f"❌ Error {response.status_code}: {response.text}")
        return None

if st.button("🚀 Generate Image"):
    if not prompt:
        st.warning("⚠️ Please enter a prompt.")
    else:
        image = generate_image(prompt, model_choice)
        if image:
            st.image(image, caption="Generated Image", use_column_width=True)

