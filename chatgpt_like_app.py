import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load env variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="ChatGPT Clone (FREE)", page_icon="🤖")
st.title("🤖 ChatGPT-like Clone (GROQ – FREE)")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        stream = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ UPDATED MODEL
            messages=st.session_state.messages,
            temperature=0.7,
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                placeholder.markdown(full_response)

    # Save response
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )
