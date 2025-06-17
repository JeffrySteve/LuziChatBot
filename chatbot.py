# chatbot.py

import streamlit as st
from streamlit_chat import message

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load model & tokenizer (DialoGPT small)
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")
    return tokenizer, model

tokenizer, model = load_model()

st.title("🤖 LUZI")

# Store chat history in session
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'chat_history_ids' not in st.session_state:
    st.session_state['chat_history_ids'] = None

# User input
user_input = st.text_input("You:", key="input")

if user_input:
    # Encode the new user input, add to chat history
    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    # Append to past chat history
    bot_input_ids = torch.cat([st.session_state['chat_history_ids'], new_input_ids], dim=-1) if st.session_state['chat_history_ids'] is not None else new_input_ids

    # Generate a response
    st.session_state['chat_history_ids'] = model.generate(
        bot_input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id
    )

    # Decode response
    response = tokenizer.decode(st.session_state['chat_history_ids'][:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    # Save conversation
    st.session_state.past.append(user_input)
    st.session_state.generated.append(response)

# Display conversation
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
