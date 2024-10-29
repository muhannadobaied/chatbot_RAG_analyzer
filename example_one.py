# st.write("`streamlit_app.py` contents:")
# code = Path("streamlit_app.py").read_text()

# st.code(code, language="python")

# location = "pages_sections.toml" if st.session_state["use_sections"] else "pages.toml"
# st.write(f"`{location}` contents:")
# toml_code = Path(f".streamlit/{location}").read_text()
# st.code(toml_code, language="toml")

from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory
import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain_core.messages.system import SystemMessage
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
import json
import requests
# from ollama import Client
# from pathlib import Path

from st_pages import add_page_title, get_nav_from_toml

# with st.sidebar:
#     company_name = st.text_input("اسم الشركة",key="company_name",type="default")
#     ("هذه جلسة خاصة بشركتك")
# st.html("")
st.title("شركة OSH")
st.write(
    "نظام ادارة السمعة للشركات"
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "مرحبا كيف يمكنني مساعدتك"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
@tool 
def cat_facts():
    """Returns facts about cats"""
    return json.loads(requests.get("https://catfact.ninja/fact").text)["fact"]

if prompt := st.chat_input():
    # if not company_name:
    #     st.info("لطفا قم بادخال اسم شركتك")
    #     st.stop()
    tools = [cat_facts]
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
    llm=ChatGoogleGenerativeAI(
        google_api_key="AIzaSyBMEtfqwol-6mvbHiX-5Mk7bOySpIHNK9k",
        model="gemini-1.5-flash-latest",
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.OFF,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.OFF,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.OFF,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.OFF,
        },
        convert_system_message_to_human=True,
        )
    model = ChatOllama(model="llama3.2", temperature = 0, base_url="https://109.199.116.46", client_kwargs={'verify': False}).bind_tools(tools=tools)
    aiprompt = hub.pull("hwchase17/openai-tools-agent")
    agent = create_tool_calling_agent(model, tools, aiprompt)
    client = AgentExecutor(agent=agent, tools=tools, verbose=True)

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        response = client.invoke(input={"input": st.session_state.messages})
        msg = response["output"]
        print("MASSSSAAAGGEEE", msg)
        response = llm.invoke(input=f"Just check if there are any mistake in this response correct it with out changing any contecxt or worde just if there wrong word replace it with correct word and if you find any wrong information make it right:{msg} ")
        print("RESPONSE", response)
        st.session_state.messages.append({"role": "assistant", "content": response})
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