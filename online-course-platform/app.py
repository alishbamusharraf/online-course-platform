import streamlit as st
import json
import os
from dotenv import load_dotenv
from utils.auth import Auth
from utils.payment import PaymentProcessor

# Load environment variables
load_dotenv()

auth = Auth()
payment = PaymentProcessor()

st.set_page_config(page_title="📚 Online Course store", layout="centered")
st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>📚 Welcome to the Online Course store</h1>", unsafe_allow_html=True)
st.markdown("---")

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# Sidebar menu
menu_options = ["🔐 Login", "📝 Signup", "📖 Browse Books"]
if st.session_state.logged_in:
    menu_options.append("🚪 Logout")

menu = st.sidebar.selectbox("📋 Menu", menu_options)

# Login Page
if menu == "🔐 Login":
    st.subheader("🔐 Login to Your Account")
    email = st.text_input("📧 Email")
    password = st.text_input("🔑 Password", type="password")
    if st.button("Login ✅"):
        if auth.login(email, password):
            st.success("✅ Logged in successfully!")
            st.session_state.logged_in = True
            st.session_state.user_email = email
        else:
            st.error("❌ Invalid email or password.")

# Signup Page
elif menu == "📝 Signup":
    st.subheader("📝 Create a New Account")
    email = st.text_input("📧 New Email")
    password = st.text_input("🔑 New Password", type="password")
    if st.button("Signup ✅"):
        if auth.signup(email, password):
            st.success("🎉 Account created successfully! You can now log in.")
        else:
            st.error("⚠️ This email is already registered.")

# Browse Books Page
elif menu == "📖 Browse Books":
    st.subheader("📖 Explore Our Courses")
    try:
        with open("data/courses.json") as f:
            books = json.load(f)

        for book in books:
            st.markdown(f"### 📘 {book['title']}")
            st.markdown(f"👨‍🏫 **Instructor:** {book['instructor']}")
            st.markdown(f"💵 **Price:** ${book['price']}")
            st.markdown(f"📝 {book['description']}")
            if st.session_state.logged_in:
                if st.button(f"🛒 Buy Now - {book['title']} (${book['price']})", key=book['title']):
                    checkout_url = payment.create_checkout_session(
                        st.session_state.user_email,
                        float(book['price']),
                        book['title']
                    )
                    if checkout_url:
                        st.success("✅ Payment session created.")
                        st.markdown(
                            f"[💳 Click here to pay]({checkout_url})",
                            unsafe_allow_html=True
                        )
                    else:
                        st.error("❌ Payment session creation failed.")
            else:
                st.info("🔑 Please log in to make a purchase.")
            st.markdown("---")

    except FileNotFoundError:
        st.error("📁 Course file not found. Make sure `data/courses.json` exists.")

# Logout
elif menu == "🚪 Logout":
    st.session_state.logged_in = False
    st.session_state.user_email = ""
    st.success("👋 You have been logged out.")
