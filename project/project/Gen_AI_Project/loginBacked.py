import streamlit as st
import pandas as pd
import csv
import os

def add_user(user,pas):
    try :
        with open("AppData\\users.csv","a",newline='') as f:
            writer=csv.writer(f)
            writer.writerow([user,pas])
        st.success("Account Created Sucessfully")
    except Exception :
        st.error("Falied to Create Account")


def check_password(username, password):
   try: 
        pass_df=pd.read_csv("AppData\\users.csv")
        username1=pass_df['username']
        password1=pass_df['password']
        for user, pwd in zip(username1, password1):
            if username == user and password == pwd:
                # st.success("Login Successful!")
                st.session_state.login_status = True
                st.session_state.username = username
                st.session_state.current_page = "Home"
                # st.rerun()
                return ("Login Successful!")
            
        return ("Invalid username or password.")
        
   except Exception as e:
        return("Error Checking user credentials.")


    
def change_state():
    st.session_state.current_page = "login"


if __name__=="__main__":
    check_password('A','A')