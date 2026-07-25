import os
import streamlit as st
from utils.gemini_client import ask_gemini, transcribe_audio
from utils.text_to_speech import text_to_speech

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Voice AI Assistant",
    page_icon="🎤",
    layout="wide"
)

st.title("🎙️ Voice AI Assistant")
st.caption("Talk naturally with Gemini AI")
st.divider()

st.markdown(
"""
<small style='color:gray'>
Powered by Python • Streamlit • Gemini AI
</small>
""",
unsafe_allow_html=True,
)

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_audio" not in st.session_state:
    st.session_state.last_audio = None

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.header("⚙️ Settings")

    st.metric("Status", "Online")

    conversation_count = len(st.session_state.messages) // 2
    st.metric("Conversations", conversation_count)
    st.markdown("---")

    st.metric("Model", "Gemini 3.5 Flash")

    st.metric("🎤 Voice", "Ready")
    st.metric("🔊 Speaker", "Ready")

    st.divider()

    if st.button("🗑 Clear Chat", use_container_width=True):
            
            st.session_state.messages = []
            st.session_state.last_audio = None
            st.rerun()

# -----------------------------
# Display Previous Chat
# -----------------------------
for message in st.session_state.messages:


    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant" and message.get("audio"):
            st.audio(message["audio"])

if len(st.session_state.messages) == 0:

    st.markdown(
    """
    ### 👋 Welcome

    Use the microphone 🎤 or type your question below.

    Your assistant can:

    - 🎤 Listen
    - 🤖 Understand
    - 💬 Reply
    - 🔊 Speak back
    """
    )

# -----------------------------
# Voice Input
# -----------------------------
st.divider()
st.subheader("🎤 Voice Input")

audio_value = st.audio_input("Click the microphone and speak")
if audio_value:
    st.write("Audio size:", len(audio_value.getvalue()))


# -----------------------------
# Text Chat
# -----------------------------
prompt = st.chat_input("Type your message...")

if prompt:

    with st.spinner("🤖 Thinking..."):

        answer = ask_gemini(prompt)
        audio_file = text_to_speech(answer)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "audio": audio_file
        }
    )

    st.rerun()


if audio_value:

    current_audio = audio_value.getvalue()

    if current_audio != st.session_state.last_audio:

        st.session_state.last_audio = current_audio

        os.makedirs("temp", exist_ok=True)

        audio_path = "temp/recorded_audio.wav"

        with open(audio_path, "wb") as f:
            f.write(audio_value.getbuffer())

        with st.spinner("🎤 Processing Voice..."):

            transcript = transcribe_audio(audio_path)

            if transcript and transcript.strip():

                answer = ask_gemini(transcript)
                audio_file = text_to_speech(answer)

                st.session_state.messages.append(
                    {
                        "role": "user",
                        "content": transcript
                    }
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "audio": audio_file
                    }
                )

                if os.path.exists(audio_path):
                    os.remove(audio_path)

                st.rerun()

            else:
                st.error("Couldn't understand your speech. Please try again.")


# -----------------------------
# Footer
# -----------------------------
st.divider()

st.markdown(
"""
<div style="text-align:center;color:gray;font-size:14px;">
Developed by <b>Nithin Vaspula</b><br>
Python • Streamlit • Gemini AI
</div>
""",
unsafe_allow_html=True,
)