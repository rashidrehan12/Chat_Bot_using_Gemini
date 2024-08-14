import os

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

load_dotenv()
st.set_page_config(
    page_title="Chat with gemini"
)
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')


def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.user_messages = []

def display_chat_history():
    for message in st.session_state.chat_history:
        try:
            role = translate_role_for_streamlit(message.role)
        except AttributeError:
            role = "unknown"  # Default role if unavailable
        with st.chat_message(role):
            st.markdown(message.text)  # Assuming 'text' attribute holds the message content


st.title("Chat Bot")

display_chat_history()

user_prompt = st.chat_input("Ask Gemini-pro")
# ... (rest of your code)

if user_prompt:
    st.session_state.user_messages.append(user_prompt)
    st.chat_message("user").markdown(user_prompt)

    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    gemini_response = st.session_state.chat_session.send_message(user_prompt)
    st.session_state.chat_history.append(gemini_response)

    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
