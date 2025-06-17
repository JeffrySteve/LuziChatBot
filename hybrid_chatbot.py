# hybrid_chatbot.py

import streamlit as st
from streamlit_chat import message
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import random

# -------------------------
# 1️⃣ Load local DialoGPT model
# -------------------------
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")
    return tokenizer, model

tokenizer, model = load_model()

# -------------------------
# 2️⃣ Your custom rule-based brain
# -------------------------
def custom_brain(user_input):
    user_input = user_input.lower()
    st.image("logo.ico", width=200)

    if "price" in user_input:
        return "💰 Our prices range from $10 to $200. Do you want a recommendation?"
    elif "delivery" in user_input or "shipping" in user_input:
        return "🚚 We deliver worldwide! Orders over $50 ship free."
    elif "hello" in user_input or "hi" in user_input:
        return random.choice([
            "Hey there! 👋 How can I assist you today?",
            "Hello! 😊 What can I help you with?",
            "Hi! 🤗 Looking for something special?"
        ])
    elif "refund" in user_input:
        return "🔄 We offer a 30-day money-back guarantee. Just contact support!"
    else:
        return None  # If no match, fallback to DialoGPT

# -------------------------
# 3️⃣ Streamlit UI setup
# -------------------------
st.title("🤖 LUZI the Chatbot")

# Initialize session state
if "generated" not in st.session_state:
    st.session_state.generated = []
if "past" not in st.session_state:
    st.session_state.past = []
if "chat_history_ids" not in st.session_state:
    st.session_state.chat_history_ids = None

# -------------------------
# 4️⃣ User input
# -------------------------
user_input = st.text_input("You:", key="input")

if user_input:
    # 1st: Try your custom brain
    response = custom_brain(user_input)

    if response is None:
        # 2nd: Fallback to DialoGPT
        new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")

        bot_input_ids = torch.cat(
            [st.session_state.chat_history_ids, new_input_ids], dim=-1
        ) if st.session_state.chat_history_ids is not None else new_input_ids

        st.session_state.chat_history_ids = model.generate(
            bot_input_ids,
            max_length=1000,
            pad_token_id=tokenizer.eos_token_id,
        )

        response = tokenizer.decode(
            st.session_state.chat_history_ids[:, bot_input_ids.shape[-1]:][0],
            skip_special_tokens=True,
        )

    # Store conversation
    st.session_state.past.append(user_input)
    st.session_state.generated.append(response)

# -------------------------
# 5️⃣ Show chat history
# -------------------------
if st.session_state.generated:
    for i in range(len(st.session_state.generated) - 1, -1, -1):
        message(st.session_state.generated[i], key=str(i))
        message(st.session_state.past[i], is_user=True, key=str(i) + "_user")
