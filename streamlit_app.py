import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain_core.messages.system import SystemMessage
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
import json
import requests
from ollama import Client
with st.sidebar:
    company_name = st.text_input("Company Name",key="company_name",type="default")
    ("this is your session for company")
st.title("OSH project for Reputation Management System")
st.write(
    "Start by typing your company name."
)
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
@tool 
def cat_facts():
    """Returns facts about cats"""
    return json.loads(requests.get("https://catfact.ninja/fact").text)["fact"]

if prompt := st.chat_input():
    if not company_name:
        st.info("Please add your company name to continue.")
        st.stop()
    tools = [cat_facts]
    client = Client(host="http://109.199.116.46")
    print("MMMMMM", st.session_state.messages)
    response =client.chat(model="llama3.2:latest", messages=[{"role": "user", "content": st.session_state.messages}], stream=True)
    # model = ChatOllama(model="llama3.2:latest", base_url="https://verifyaisy.com/ollama/").bind_tools(tools=tools)
    # prompt = hub.pull("hwchase17/openai-tools-agent")
    # agent = create_tool_calling_agent(model, tools, prompt)
    # client = AgentExecutor(agent=agent, tools=tools, verbose=True)
    # st.session_state.messages.append({"role": "user", "content": prompt})
    # st.chat_message("user").write(prompt)
    # response = client.invoke(input={
    #     "input" : st.session_state.messages
    # })
    print("RESPONSE", response)
    full_answer = ''
    for chunk in response:
        print(chunk['message']['content'], end='', flush=True)
        full_answer =''.join([full_answer,chunk['message']['content']])

    msg = full_answer
    msg = response
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)


    url = "http://109.199.116.46"
    headers = {
        "Authorization": "AAAAC3NzaC1lZDI1NTE5AAAAIG5PyAx3VlbI8441XShYE7BPHb2DA+b2D2n8Ku6PPaWx",  # If your API requires a key
        "Content-Type": "application/json",
    }

    data = {
        "messages": [{"role": "user", "content": "Hello!"}]
    }

    response = requests.post(url, headers=headers, json=data)
    st.session_state.messages.append({"role": "assistant", "content": response})
    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print("Error:", response.status_code, response.text)