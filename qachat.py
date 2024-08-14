import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Initialize Streamlit app
st.set_page_config(page_title="Q&A Demo")

# Initialize Google Generative AI model
api_key = os.getenv("GOOGLE_API_KEY")
if api_key is None:
    st.error("API key not found. Please set the GOOGLE_API_KEY environment variable.")
else:
    genai.configure(api_key=api_key)

    # Function to load Gemini Pro model and get response
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(history=[])

    def get_gemini_response(question):
        try:
            response = chat.send_message(question, stream=True)
            return response
        except Exception as e:
            st.error(f"An error occurred while getting the response: {e}")
            return []

    # Set up Streamlit page
    st.header("Gemini LLM Application")

    # Initialize session state for chat history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # Input text and submit button
    input_text = st.text_input("Input:", key="input")
    submit = st.button("Ask the question")

    if submit and input_text:
        response = get_gemini_response(input_text)

        # Add user query and response to session chat history
        st.session_state['chat_history'].append(("You", input_text))
        st.subheader("The Response is")
        for chunk in response:
            if hasattr(chunk, 'text'):
                st.write(chunk.text)
                st.session_state['chat_history'].append(("Bot", chunk.text))
            else:
                st.write("Unexpected response format received.")
        
        st.subheader("The chat history is")
        for role, text in st.session_state['chat_history']:
            st.write(f"{role}: {text}")
