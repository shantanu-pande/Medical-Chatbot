import os
import json
import streamlit as st
import google.generativeai as genai

# Configure the Generative AI model
genai.configure(api_key="AIzaSyBALDT_VSBVW60zTfTR9ZAeUDVWSXFDCCg") #I know but. it is expired :)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="You are a medical chatbot that provides suggested treatments and recommended drugs based on user symptoms. Follow these rules:\\n\\n1. Only return the treatment plan and drug recommendations—no extra explanations.\\n2. Base your recommendations on established medical guidelines (WHO, CDC, FDA, etc.).\\n3. Clearly mention drug names along with general usage guidance but avoid specific dosages unless explicitly requested.\\n4. Include warnings about potential side effects and contraindications.\\n5. Always advise consulting a healthcare professional before taking any medication.\\n6. If symptoms suggest a severe or emergency condition, recommend seeking immediate medical attention.",
)

st.title("AI Medical dignosis chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input(""):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Create a chat session and get the response from the model
    chat_session = model.start_chat(
        history=[
            {"role": m["role"], "parts": [m["content"]]}
            for m in st.session_state.messages
        ]
    )
    response = chat_session.send_message(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response.text)

    st.session_state.messages.append({"role": "assistant", "content": response.text})
