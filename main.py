import streamlit as st
import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from typing import Any, List, Mapping, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from vertexai.preview.generative_models import GenerativeModel

project_id = st.secrets["gproject_id"]
init(project=project_id)
gemini_pro_model = GenerativeModel("gemini-pro")

class GeminiProLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "gemini-pro"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        
        gemini_pro_model = GenerativeModel("gemini-pro")

        
        model_response = gemini_pro_model.generate_content(
            prompt, 
            generation_config={"temperature": 0.1}
        )
        text_content = model_response.candidates[0].content.parts[0].text
        return text_content

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model_id": "gemini-pro", "temperature": 0.1}

@st.cache_resource
def load_chain():
    llm = GeminiProLLM()
    memory = ConversationBufferMemory()
    chain = ConversationChain(llm=llm, memory=memory)
    return chain

chatchain = load_chain()

# Initialise session state variables
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Display previous messages
for message in st.session_state['messages']:
    role = message["role"]
    content = message["content"]
    with st.chat_message(role):
        st.markdown(content)

# Chat input
prompt = st.chat_input("You:")
if prompt:
    st.session_state['messages'].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = chatchain(prompt)["response"]
    st.session_state['messages'].append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
