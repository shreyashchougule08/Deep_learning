import streamlit as st
import time


def home_page():
    st.write(f"# Hey {st.session_state.username} \n \t Welcome TO RISEY Ai..^_^")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    # first_message=st.text_area("### Start the Conversation ...", height=200)
    st.session_state.welcome_message_status=True
    time.sleep(1)
    # return first_message
    # st.button("Start..")


