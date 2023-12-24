import streamlit as st
from your_custom_module import GeminiProLLM, ConversationBufferMemory, ConversationChain

def load_chain():
    llm = GeminiProLLM()
    memory = ConversationBufferMemory()
    chain = ConversationChain(llm=llm, memory=memory)
    return chain

chatchain = load_chain()

if 'messages' not in st.session_state:
    st.session_state['messages'] = []
  
st.title('Chatbot')
for message in st.session_state['messages']:
    role = message["role"]
    content = message["content"]
    st.write(f"{role}: {content}")

prompt = st.text_input("You:")
if prompt:
    st.session_state['messages'].append({"role": "user", "content": prompt})
    # Call the method from your ConversationChain to get the response
    response = chatchain.get_response(prompt)  # Modify this line according to your ConversationChain's method
    st.session_state['messages'].append({"role": "assistant", "content": response})
