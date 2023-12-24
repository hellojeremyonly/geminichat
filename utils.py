# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import inspect
import textwrap
import requests
import streamlit as st


def show_code(demo):
    """Showing the code of the demo."""
    show_code = st.sidebar.checkbox("Show code", True)
    if show_code:
        # Showing the code of the demo.
        st.markdown("## Code")
        sourcelines, _ = inspect.getsourcelines(demo)
        st.code(textwrap.dedent("".join(sourcelines[1:])))
        
def call_gemini_pro_api(prompt):
    """
    This function makes a POST request to the Gemini Pro API
    to generate content based on the given prompt.
    """
    # Replace these with your actual project and region values
    region = "your-region"
    project_id = "your-project-id"
    
    url = f"https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{region}/publishers/google/models/gemini-pro:streamGenerateContent"
    
    # Prepare headers and payload as required by the API
    headers = {
        'Authorization': 'Bearer YOUR_ACCESS_TOKEN',  # Ensure you have a valid token
        'Content-Type': 'application/json',
    }

    data = {
        'prompt': prompt,
        # Add other parameters as required by the API
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    # Handle the response
    if response.status_code == 200:
        # Parse the response content and return the text
        return response.json()
    else:
        # Handle errors (you could raise an exception or return an error message)
        return f"Error: {response.status_code} - {response.text}"
