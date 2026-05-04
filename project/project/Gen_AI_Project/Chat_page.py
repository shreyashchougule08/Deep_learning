import streamlit as st
import time
from Agent import chat_model

def reset_data():
    from scrapping.load_scrapper import reload_scrapping
    reload_scrapping()

def thinking_animation():
    placeholder = st.empty()
    for i in range(3):
        placeholder.markdown("🤔 *Risey AI is thinking*" + "." * i)
        time.sleep(0.4)
    placeholder.empty()

def stream_response(text):
    for char in text:
        yield char
        time.sleep(0.03)

def show_chat_history():
    col1 , col2 = st.columns([6,2])
    with col1:
      st.title("Welcome to  Risey Ai...")
    with col2:
        if st.button("ReScrap Data") :
            st.warning("Rescrapping may take a few minutes. Please wait...")
            if  st.button("Begin Rescrapping", on_click=reset_data):
                  st.success("Rescrapping Completed!")
            st.button("Cancel")      
                
        
    for msg in st.session_state.chat_sessions[st.session_state.current_chat]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

 
def chat_screen():
    show_chat_history()

    user_input = st.chat_input("Ask something...")

    if user_input:
        current_chat = st.session_state.current_chat

       
        if current_chat == "New Chat" and len(st.session_state.chat_sessions[current_chat]) == 0:
            title = user_input.strip()[:30]
            st.session_state.chat_sessions[title] = []
            del st.session_state.chat_sessions["New Chat"]
            st.session_state.current_chat = title
            current_chat = title

  
        with st.chat_message("user"):
            st.write(user_input)

     
        st.session_state.chat_sessions[current_chat].append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("assistant"):
            thinking_animation()

            response = chat_model(user_input)

            st.write_stream(stream_response(response))

        st.session_state.chat_sessions[current_chat].append({
            "role": "assistant",
            "content": response
        })

        st.rerun()