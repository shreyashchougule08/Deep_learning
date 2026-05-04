from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from dotenv import load_dotenv
import os
import streamlit as st
from tools import *
from langchain.tools import tool
load_dotenv()

llm=init_chat_model(
    model="openai/gpt-oss-120b",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("Groq_Api")
    )

@tool
def get_Sunbeam_data_tool(query: str):
        """ this tool gets  Sunbeam related data from the knowledge base. so any query related to Sunbeam can be answered using this tool.
        also if the question are related to any course(Apache Spark Mastery - Data Engineering With PySpark ,Aptitude ,C++ ,Core Java 
        ,Data Structures And Algorithms,Dev Ops ,Dream LLM ,Machine Learning ,Mastering GenAI ,Mastering MCQs ,MERN (FULL-STACK) DEVELOPMENT 
        ,MLOps & LLMOps ,Python Development etc) , internship , placement , pre-cat or contact details of Sunbeam then this tool can be used to get the answers.
        Input : A query related to Sunbeam in  a string format
        Output : Relevant information from Sunbeam knowledge base in string format
        Error Handling : If any error occurs during the process, it returns an error message.
        note: 1)if the user asks question where u need more than one info then divide the query into multiple sub-queries and call this tool multiple times with those sub-queries and then combine the answers and give it to the user.
              2) if the question is related like what is sunbeam then change it to tell about sunbeam 
              3) if the user asks about location , contact details then the query must be like "tell me the contact details of sunbeam"  etc
        """
        return get_Sunbeam_data(query)
@tool
def get_file_contain_tool_by_path(file_path):
    '''
     this tool is use to get file detials when a user gives path of the file note it can only acess .csv files nothing else

     paramether : this use a file path as parameter which is a string 

     responces: this gives a result containing file details  in a string format 

     expection : if it is not able to open file it gives a Error of   file not found  and if not able to find data or featch data it shows error of fail to featch data 

     instraction : the file path must have two backslashes together not single backslashe the path must be like this(eg. C:\\Users\\Aarth Shah\\OneDrive\\Desktop\\Sunbeam\\IIT_GenAI_94756\\Assignment_4\\Q2\\users.csv not like this  C:/Users/Aarth Shah/OneDrive/Desktop/Sunbeam/IIT_GenAI_94756 Assignment_4/Q2/users.csv ) 
    '''
    return get_file_contain_csv(file_path)

@tool
def weather_details_tool(city):
    '''
    weather_details  this function is used get the current weather detials of a city that detials are in json format 

    :parameter  city: this parameter takes in  city name as String 

    returns : this gives a json which contain all the the detials about the weather of the given city 

    expection : this gives error when it is not able give a response   

    instrustion : it only gives current detials about weather not past or future  
     '''
    return weather_details(city)

@tool
def calculater_tool(exprestion):
    '''
    Description this Tool is used to calucalate Mathamatical expreations which contain simple mathamatical operations like + , /,*,- only this much operations it can not ans anything beond this 

    parmeter : this takes in a String of exprestions

    return : this return a ouput of the exprestion in String format 

    error: if it fails to perform the action on  exprestion it returns error    
    '''
    return calculater(exprestion)

@tool
def get_user_uploaded_file_data_tool(query: str):
    """ this tool gets  User Uploaded File related data from the knowledge base. so any query related to User Uploaded File can be answered using this tool.
        Input : A query related to User Uploaded File in  a string format
        Output : Relevant information from User Uploaded File knowledge base in string format
        Error Handling : If any error occurs during the process, it returns an error message.
    """
    return get_file_data(query)

agent = create_agent(model=llm,tools=[get_Sunbeam_data_tool,get_file_contain_tool_by_path,weather_details_tool,calculater_tool,get_user_uploaded_file_data_tool],system_prompt="You are a helpful AI assistant mainly focused on Sunbeam InfoTech. Use the provided tool to answer questions related to Sunbeam InfoTech, its courses, internships, placements, pre-cat information, and contact details. If the question is not related to Sunbeam InfoTech, try to ans from Your Database if u cant get datafrom database then just ans the query from ur databased dont let the user Know from very the data came  .but u can also ans general questions if asked.")
def chat_model(messages):
    st.session_state.conversation.append({"role": "user", "content": messages})
    result=agent.invoke({"messages": st.session_state.conversation})
    print("Agent: ", result['messages'][-1].content)
    st.session_state.conversation.append({"role":"assistant", "content": result['messages'][-1].content})
    return result['messages'][-1].content

# def get_chat_history():
#     print(Conversation)
#     return

if __name__ == "__main__":
    Conversation=[]
    while True:
        Conversation.append({"role": "user", "content": input("User: ")})
        result=agent.invoke({"messages": Conversation})
        print("Agent: ", result['messages'][-1].content)
        print(result)
        Conversation.append({"role":"assistant", "content": result['messages'][-1].content})
        # Conversation=[result["messages"]]
        # get_chat_history()