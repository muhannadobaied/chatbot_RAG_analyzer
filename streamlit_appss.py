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
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
st.markdown("""
<style>
body, html {
    direction: RTL;
    unicode-bidi: bidi-override;
    text-align: right;
}

</style>
""", unsafe_allow_html=True)
with st.sidebar:
    company_name = st.text_input("اسم الشركة",key="company_name",type="default")
    ("هذه جلسة خاصة بشركتك")
# st.html("")
st.title("شركة OSH")
st.write(
    "نظام ادارة السمعة للشركات"
)
st.write(
    "ابدء بكتابة اسم الشركة الرسمي التجاري."
)
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "مرحبا كيف يمكنني مساعدتك"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
@tool 
def cat_facts():
    """Returns facts about cats"""
    return "nice fact"

if prompt := st.chat_input():
    if not company_name:
        st.info("لطفا قم بادخال اسم شركتك")
        st.stop()
    tools = []
    # client = Client(host="http://109.199.116.46", verify=False)
    # print("MMMMMM", st.session_state.messages)
    # response =client.chat(model="llama3.2:latest", messages=[{"role": "user", "content": st.session_state.messages}], stream=True)

    # model = ChatOllama(model="llama3.2", base_url="http://109.199.116.46",client_kwargs={'verify': False}).bind_tools(tools=tools)
    # prompt = hub.pull("hwchase17/openai-tools-agent")
    # agent = create_tool_calling_agent(model, tools, prompt)
    # client = AgentExecutor(agent=agent, tools=tools, verbose=True)
    # st.session_state.messages.append({"role": "user", "content": prompt})
    # st.chat_message("user").write(prompt)
    # try:
    #     response = client.invoke(input={"input": st.session_state.messages})
    #     print("RESPONSE", response)
    #     st.session_state.messages.append({"role": "assistant", "content": response})
    #     st.chat_message("assistant").write(msg)
    # except Exception as e:
    #     st.session_state.messages.append({"role": "assistant", "content": str(e)})
    #     st.chat_message("assistant").write(str(e))
    #     print("Error invoking the client:", str(e))

    # full_answer = ''
    # for chunk in response:
    #     print(chunk['message']['content'], end='', flush=True)
    #     full_answer =''.join([full_answer,chunk['message']['content']])

    # msg = full_answer
    # msg = response
    # st.session_state.messages.append({"role": "assistant", "content": response})
    # st.chat_message("assistant").write(msg)


    # url = "http://109.199.116.46"
    # headers = {
    #     "Authorization": "AAAAC3NzaC1lZDI1NTE5AAAAIG5PyAx3VlbI8441XShYE7BPHb2DA+b2D2n8Ku6PPaWx",  # If your API requires a key
    #     "Content-Type": "application/json",
    # }

    # data = {
    # }
    
    
    # model = ChatOllama(model="llama3.1:8b", temperature = 0, base_url="https://109.199.116.46", client_kwargs={'verify': False}).bind_tools(tools=tools)
    # aiprompt = hub.pull("hwchase17/openai-tools-agent")
    # agent = create_tool_calling_agent(model, tools, aiprompt)
    # client = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    
    
    model = ChatOllama(model="llama3.1:8b", num_ctx=16384, temperature = 0, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),base_url="https://109.199.116.46", client_kwargs={'verify': False}).bind_tools(tools=tools)
    aiprompt = hub.pull("hwchase17/openai-tools-agent")
    # memory = MemorySaver()
    # MEMORY_KEY = "chat_history"
    prompts = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful and very powerful assistant. You were created by OSH company. Maintain a professional journalist's tone and return nicely formatted markdown strings. Do not limit your responses words make it as needed. you can use the cat_facts tool only if the user asked you to bring cat facts.",
            ),
            # MessagesPlaceholder(variable_name=MEMORY_KEY),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    # chat_history = []


    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
            # "chat_history": lambda x: x["chat_history"],
        }
        | prompts
        | model
        | OpenAIToolsAgentOutputParser()
    )
    # AI_message = """
    # You are a highly helpful AI assistant developed by OSH. Your name is Verify in English, and in Arabic, it translates to "تأكد". You can perform various tasks, including interacting with humans in conversation.
    # You are designed to chat with humans in a very friendly manner about anything.
    # """
    # agent_executor = create_tool_calling_agent(model=model, prompt=prompts, tools=tools)
    # agent = create_tool_calling_agent(model, tools, prompts)
    client = AgentExecutor(agent=agent, tools=tools, verbose=True)

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        # response = client.invoke(input={"input": st.session_state.messages, "chat_history": chat_history})
        response = client.invoke(input={"input": st.session_state.messages})
        print("RESPONSE", response)
        msg = response["output"]
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)  # Changed msg to response to avoid undefined variable
    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": str(e)})
        st.chat_message("assistant").write(str(e))
        print("Error invoking the client:", str(e))
    # response = requests.post(url, verify=False)
    # print("RESRRSRSRS", response)
    # st.session_state.messages.append({"role": "assistant", "content": response})
    # if response.status_code == 200:
    #     print("Success:", response)
    # else:
    #     print("Error:", response.status_code, response.text)
    
    # headers = {
    # "Content-Type": "application/json",
    # }

    # data = {
    #     "model": "llama3.2"
    # }

    # response = requests.post("https://109.199.116.46/api/chat", json=data, headers=headers, verify=False)

    # print("Response:", response)