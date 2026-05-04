from embedding import create_embedding
from chroma import get_data_for_Embed_query
import pandas as pd
import os
from dotenv import load_dotenv
import requests
import json
from loadfile import get_data_from_file
import streamlit as st

def get_Sunbeam_data(query: str) -> str:
    try:
        embedding = create_embedding([query])
        result = get_data_for_Embed_query(embedding, option="sunbeam")
        return str(result["documents"])
    except Exception as e:
        return f"An error occurred: {e}"
    
def calculater(exprestion):
     
     return (str(eval(exprestion)))

def weather_details(city):

     API_key = os.getenv("OpenWeather_API_key")
     print(API_key)
     url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
 
     try:
        response=requests.get(url)
        response=response.json()

        return json.dumps(response)
     except Exception as e :
         return ("Erorr to featch data ")
       
def get_file_contain_csv(file_path):
    try :
        df=pd.read_csv(file_path)
        print(df.head())
        return df
    except Exception :
        return "Error to featch data from the file "
    
def get_file_data(query: str) -> str:
    if 'knowledge_base' not in st.session_state:
        return "No file data available."
    return f"{st.session_state.knowledge_base} "
