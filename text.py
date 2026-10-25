import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Page configuration
st.set_page_config(page_title="Orpheus Text-to-Speech", page_icon="🗣️", layout="centered")

st.title("🗣️ Orpheus Text-to-Speech")
st.caption("Powered by Groq & `canopylabs/orpheus-v1-english`")

# Get the API key stored in variable 'x'
api_key = os.getenv("x")

if not api_key:
    st.error("API key 'x' not found in your .env file. Please check your setup.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=api_key)

# Input section for text
st.subheader("Synthesize Speech")
st.markdown(
    "Tip: You can use optional bracketed vocal directions like `[cheerful]`, `[whisper]`, or `[dramatic]` "
    "to control the style of the speech."
)

# Voice selection dropdown
selected_voice = st.selectbox(
    "Select Voice:",
    ["autumn", "diana", "hannah", "austin", "daniel", "troy"],
    index=0
)

# Text area for user input
text_input = st.text_area(
    "Enter text to convert to speech:",
    value="[cheerful] Hello! Welcome to your custom text-to-speech application powered by Groq and Orpheus.",
    height=100
)

if st.button("🔊 Generate & Play Speech", type="primary"):
    if not text_input.strip():
        st.warning("Please enter some text to synthesize.")
    else:
        with st.spinner("Synthesizing speech..."):
            try:
                # Call Groq audio speech API endpoint with response_format="wav"
                response = client.audio.speech.create(
                    model="canopylabs/orpheus-v1-english",
                    input=text_input,
                    voice=selected_voice,
                    response_format="wav"
                )
                
                # Read audio content bytes from response
                audio_bytes = response.read()
                
                # Play audio in Streamlit with wav format
                st.audio(audio_bytes, format="audio/wav")
                st.success("Speech generated successfully!")
                
            except Exception as e:
                st.error(f"Error generating speech: {e}")