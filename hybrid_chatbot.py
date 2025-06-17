# hybrid_chatbot.py

import streamlit as st
from streamlit_chat import message
import random

#

# -------------------------
# 2️⃣ Your custom rule-based brain
# -------------------------
def custom_brain(user_input):
    user_input = user_input.lower()
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
    elif "support" in user_input or "help" in user_input:
        return "🛠️ Our support team is available 24/7. How can we assist you?"
    elif "hours" in user_input or "open" in user_input:
        return "⏰ We're open Monday to Friday, 9am to 6pm."
    elif "payment" in user_input or "pay" in user_input:
        return "💳 We accept Visa, MasterCard, PayPal, and Apple Pay."
    elif "thank" in user_input:
        return random.choice([
            "You're welcome! 😊",
            "Glad I could help! 👍",
            "Anytime! Let me know if you have more questions."
        ])
    elif "contact" in user_input or "email" in user_input or "phone" in user_input:
        return "📞 You can contact us at jeffrysteves@gmail.com or call (123) 456-7890."
    elif "order" in user_input or "purchase" in user_input:
        return "📝 To place an order, just let me know what you need or visit our website!"
    elif "cancel" in user_input:
        return "❌ To cancel your order, please provide your order number or contact support."
    elif "track" in user_input or "tracking" in user_input:
        return "🔎 You can track your order using the tracking link sent to your email."
    elif "recommend" in user_input or "suggest" in user_input:
        return "🤔 Tell me what you're looking for, and I'll recommend something!"
    elif "discount" in user_input or "coupon" in user_input or "promo" in user_input:
        return "🎉 We often have promotions! Check our website or subscribe to our newsletter for the latest deals."
    elif "job" in user_input or "career" in user_input or "hire" in user_input:
        return "💼 We're always looking for talent! Visit our Careers page for open positions."
    elif "feedback" in user_input or "complaint" in user_input:
        return "📝 We value your feedback. Please share your thoughts, and we'll do our best to improve."
    else:
        return "🤖 Sorry, I didn't understand that. Can you rephrase your question?"

# -------------------------
# 3️⃣ Streamlit UI setup
# -------------------------
st.title("🤖 LUZI the Chatbot")

# Initialize session state
if "generated" not in st.session_state:
    st.session_state.generated = []
if "past" not in st.session_state:
    st.session_state.past = []

# -------------------------
# 4️⃣ User input
# -------------------------
user_input = st.text_input("You:", key="input")

if user_input:
    response = custom_brain(user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(response)


# -------------------------
# 5️⃣ Show chat history
# -------------------------
if st.session_state.generated:
    for i in range(len(st.session_state.generated) - 1, -1, -1):
        message(st.session_state.generated[i], key=str(i))
        message(st.session_state.past[i], is_user=True, key=str(i) + "_user")
