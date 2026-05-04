import streamlit as st
import pandas as pd
import csv
import os

def load_data(uploaded_file):
    df=pd.read_csv(uploaded_file)
    print(df.head())
    st.success("File uploaded successfully!")
    
    file_exists=os.path.isfile('userfile.csv')
    with open('userfile.csv', 'a' , newline='') as f:
            writer=csv.writer(f)
            if not file_exists:
                writer.writerow(["User","Filename","Timestamp"])
            writer.writerow([st.session_state.loged_user, uploaded_file.name, pd.Timestamp.now()])

    return df


def upload_file():
        try:
            st.header("Upload CSV File")
            uploaded_file=st.file_uploader("chosse a csv file",type=["csv"])
            if uploaded_file is not None:
                df=load_data(uploaded_file)
                st.session_state.file_uploaded[uploaded_file.name]=df
                display_data(df)
                st.button("Load my all  files", on_click=all_user_files)
                return df
        
        
        except Exception as e:
            st.error("Error uploading file.")

def load_files(file):
        df=st.session_state.file_uploaded[file]
        st.subheader(f"Data from file: {file}")
        display_data(df)

def all_user_files():
    for file, df in st.session_state.file_uploaded.items():
        st.write(f"File: {file}")
        display_data(df)

def add_user(user,pas):
    try :
        with open("users.csv","a",newline='') as f:
            writer=csv.writer(f)
            writer.writerow([user,pas])
        st.success("Account Created Sucessfully")
    except Exception as e:
        st.error("Falied to Create Account")


def display_data(df):
    st.dataframe(df)

def check_password(username, password):
   try: 
        pass_df=pd.read_csv("users.csv")
        username1=pass_df['username']
        password1=pass_df['password']
        for user, pwd in zip(username1, password1):
            if username == user and password == pwd:
                st.success("Login Successful!")
                st.session_state.login_status = True
                st.session_state.loged_user = username
                st.session_state.current_page = "Home"
                st.rerun()
                return
            
        st.error("Invalid username or password.")
        return
   except Exception as e:
        st.error("Error Checking user credentials.")
        return

    
def show_history():
    df=pd.read_csv("C:\\Users\\Aarth Shah\\OneDrive\\Desktop\\Sunbeam\\IIT_GenAI_94756\\Assignment_4\\Q2\\userfile.csv")
    name=st.session_state.loged_user
    st.write(df[df["User"] == name])


def change_state():
    st.session_state.current_page = "login"


st.title("CSV File Uploader and Viewer")

if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = {}
if 'login_status' not in st.session_state:
    st.session_state.login_status = False
if 'loged_user' not in st.session_state:
    st.session_state.loged_user = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = "login"


if st.session_state.login_status== True:
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Upload CSV", "History", "Logout"])
    st.session_state.current_page = page
else:
    st.sidebar.title("Please log in to access the app features.")
    page=st.sidebar.radio("Welcome", ["login", "signup"])
    st.session_state.current_page = page


if st.session_state.current_page == "login":
    st.header("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        check_password(username, password)

elif st.session_state.current_page == "signup":
    st.header("Signup Page")
    new_username = st.text_input("Choose a Username")
    new_password = st.text_input("Choose a Password", type="password")
    if st.button("Sign Up"):
        add_user(new_username,new_password)

elif st.session_state.current_page == "Home":
    st.title(f"Welcome, {st.session_state.loged_user}!")
    st.write("This is the home page.")
    st.write("Use the sidebar to navigate through the app.")

elif st.session_state.current_page == "Upload CSV":
    file=upload_file()

elif st.session_state.current_page =="History":
    show_history()
    
elif st.session_state.current_page =="Logout":
    st.session_state.login_status = False
    change_state()
    
    
    