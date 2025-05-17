# app.py (for online course platform)
import streamlit as st
import json
from utils.auth import Auth
from utils.payment import PaymentProcessor
from models.course import Course

auth = Auth()
payment = PaymentProcessor()

st.title("🎓 Online Course Platform")

menu = st.sidebar.selectbox("Menu", ["Login", "Signup", "Browse Courses"])

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if menu == "Login":
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if auth.login(email, password):
            st.success("Logged in!")
            st.session_state.logged_in = True
        else:
            st.error("Invalid credentials")

elif menu == "Signup":
    email = st.text_input("New Email")
    password = st.text_input("New Password", type="password")
    if st.button("Signup"):
        if auth.signup(email, password):
            st.success("Signup successful!")
        else:
            st.error("Email already registered")

elif menu == "Browse Courses" and st.session_state.logged_in:
    st.header("Available Courses")
    with open("data/courses.json") as f:
        courses = json.load(f)
    for c in courses:
        course = Course(**c)
        st.subheader(course.title)
        st.write(f"Instructor: {course.instructor}")
        st.write(f"Price: ${course.price}")
        if st.button(f"Enroll in {course.title}", key=course.id):
            payment.process_payment(email, course.price)
            st.success(f"Enrolled in {course.title}!")
