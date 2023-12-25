import os
import json
import streamlit as st
import google.generativeai as genai
from datetime import datetime
from google.oauth2.service_account import Credentials

# Clients Credentials for Google
with open('/Users/hellojeremyonly/Documents/Env_Var/client_secret_461952724788-ts8ok57spkn1e7cpl8d67c58l2iiin7e.apps.googleusercontent.com.json', 'r') as file:
    json_credentials = json.load(file)
    
# Credentials authenticate
credentials = Credentials.from_service_account_info(json_credentials)

# Initialize Gemini-Pro 
genai.configure(api_key=os.getenv("GOOGLE_GEMINI_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Gemini uses 'model' for assistant; Streamlit uses 'assistant'
def role_to_streamlit(role):
    if role == "model":
        return "assistant"
    else:
        return role

# Add a Gemini Chat history object to Streamlit session state
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history = [])
    st.session_state.last_date = datetime.today().date()
    st.session_state.count = 0

# Display Form Title
st.title("Gemini-Pro")

# Display chat messages from history above current input box
for message in st.session_state.chat.history:
    with st.chat_message(role_to_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Check for rate limit
if st.session_state.count >= 60:
    st.error("Rate limit reached. Please try again tomorrow.")
else:
    # Accept user's next message, add to context, resubmit context to Gemini
    if prompt := st.chat_input("I possess a well of knowledge. What would you like to know?"):
        if len(prompt) > 500:  # User input validation
            st.warning("Your message is too long. Please keep it under 500 characters.")
        else:
            try:
                response = st.session_state.chat.send_message(prompt)
                st.session_state.count += 1  # Increment message count
                with st.chat_message("assistant"):
                    st.markdown(response.text)
            except Exception as e:
                st.error("An error occurred while sending the message. Please try again later.")
