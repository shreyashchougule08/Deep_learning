import streamlit as st
from loginBacked import add_user, check_password
import time
import tempfile
from loadfile import chunk_file_data
from langchain_community.document_loaders import PyPDFLoader

def login_ui():
    st.header("Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2, col3 = st.columns([1, 6, 1])

    with col1:
        if st.button("Login"):
            msg = check_password(username, password)
            if msg == "Login Successful!":
                st.session_state.login_status = True
                st.session_state.username = username
                with col2:
                    st.success(msg)
                time.sleep(1)
                st.rerun()
            else:
                with col2:
                    st.error(msg)
                time.sleep(1)
                st.rerun()

    with col3:
        if st.button("Sign Up"):
            st.session_state.current_page = "Signup"
            st.rerun()


def signup_ui():
    st.header("Signup Page")

    u = st.text_input("Choose Username")
    p = st.text_input("Choose Password", type="password")
    e= st.text_input("Enter Email")

    if st.button("Register") and u and p and e:
        add_user(u, p)
        st.session_state.current_page = "Login"
        time.sleep(1)
        st.rerun()

def login_completed_sidebar():
    with st.sidebar:
        st.success(f"Logged in as: {st.session_state.username}")
        st.divider()
        file = st.file_uploader("📂 Upload PDF", type=["pdf"])
        if file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                tmp_pdf.write(file.getbuffer())
                tmp_pdf_path = tmp_pdf.name

            documents = PyPDFLoader(tmp_pdf_path).load() 
            st.session_state.uploaded_file = file
            st.session_state.uploaded_file_path = tmp_pdf_path
            st.success(file.name)
            import re
            clean = ""
            for document in documents:
                clean += re.sub(r"\s+", " ", document.page_content).strip()
            file.seek(0)
            print(clean[:500])
            st.session_state.knowledge_base = clean
            # chunk_file_data([clean])

        st.divider()
        if st.button("+ New Chat", use_container_width=True):
            st.session_state.chat_sessions["New Chat"] = []
            st.session_state.current_chat = "New Chat"
            st.rerun()

        st.divider()


        st.subheader("🔍 Chat History")
        chat_keys = list(st.session_state.chat_sessions.keys())[::-1]

        

        selected = st.radio(
            "",
            chat_keys,
            index=chat_keys.index(st.session_state.current_chat)
        )

        st.session_state.current_chat = selected
        st.divider()
        page1=st.button("Log out",use_container_width=True)
        st.divider()
        page = "Chat"

        
        if page1:
            st.session_state.login_status = False
            st.session_state.username = None
            st.session_state.chat_sessions = {"New Chat": []}
            st.session_state.current_chat = "New Chat"
            st.session_state.current_page = "Login"
            st.session_state.uploaded_file = None
            st.rerun()

        return page


def start_message(option="LOGIN"):
    col1, col2 = st.columns([1, 7])

    with col1:
        st.image(
            "https://icons.iconarchive.com/icons/microsoft/fluentui-emoji-3d/512/Robot-3d-icon.png",
            width=60
        )

    with col2:
        st.title(f"{option} TO RISEY AI")