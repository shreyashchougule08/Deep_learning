import streamlit as st
from loginUI import login_ui, signup_ui, start_message, login_completed_sidebar
from Welcome_Home_UI import home_page
from Chat_page import chat_screen


st.set_page_config(
    page_title="Risey AI",
    page_icon="https://cdn3d.iconscout.com/3d/premium/thumb/robot-3d-icon-png-download-7746765.png"

)
def change_page_status(status):
    st.session_state.current_page = status


if "current_page" not in st.session_state:
    st.session_state.current_page = "Login"

if "login_status" not in st.session_state:
    st.session_state.login_status = False

if "username" not in st.session_state:
    st.session_state.username = None

if "welcome_message_status" not in st.session_state:
    st.session_state.welcome_message_status = False

if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {"Chat 1": []}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

if "knowledge_base" not in st.session_state:
    st.session_state.knowledge_base = " "

if not st.session_state.login_status:

    if st.session_state.current_page == "Login":
        start_message()
        login_ui()

    elif st.session_state.current_page == "Signup":
        start_message("Signup")
        signup_ui()

else:
    page = login_completed_sidebar()

    if page == "Chat":

        if not st.session_state.welcome_message_status:
            home_page()
            st.session_state.welcome_message_status = True
            st.rerun()

        chat_screen()