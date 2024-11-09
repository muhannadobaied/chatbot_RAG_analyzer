import os
from typing import List, Union
import streamlit as st
from langchain_ollama import ChatOllama
# from langchain_community.chat_models import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain_core.messages.system import SystemMessage
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent, create_react_agent
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
# from langchain_google_community import GoogleSearchAPIWrapper, GoogleSearchResults
from langchain_google_community.search import  GoogleSearchResults, GoogleSearchAPIWrapper
from langchain.agents import Tool
from langchain_core.tools import tool
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts.chat import SystemMessagePromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
st.markdown("""
<style>
body, html {
    direction: RTL;
    unicode-bidi: bidi-override;
    text-align: right;
}

</style>
""", unsafe_allow_html=True)

os.environ['USER_AGENT'] = "MyCustomUserAgent/1.0 (compatible; OSH-Bot/1.0)"
# with st.sidebar:
#     company_name = st.text_input("اسم الشركة",key="company_name",type="default")
#     ("هذه جلسة خاصة بشركتك")
# st.html("")
st.title("شركة OSH")
st.write(
    "نظام ادارة السمعة والسوق للشركات"
)
# st.write(
#     "ابدء بكتابة اسم الشركة الرسمي التجاري."
# )
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "مرحبا كيف يمكنني مساعدتك"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

from goose3 import Goose
@tool
def scrape_webpages(urls: Union[List[str], str]) -> str:
    """Fetches content from specified URLs and returns scraped text as markdown for the user."""
    # Ensure `urls` is a list
    if isinstance(urls, str):
        urls = [urls]
    
    loader = WebBaseLoader(urls)
    docs = loader.load()

    g = Goose()
    scraped_articles = []
    for doc in docs:
        url = doc.metadata['source']
        article = g.extract(url=url)

        try:
            filename = f"scraped_{doc.metadata['title']}.docx"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(article.cleaned_text)
            print(f"Successfully scraped content from {url} and saved to {filename}")
        except Exception as e:
            print(f"Error scraping {url}: {e}")
        
        scraped_articles.append(f"<Document name='{article.title}'>\n{article.cleaned_text}\n</Document>")
    
    return "\n\n".join(scraped_articles)

@tool 
def pass_text(input: str) -> str:
    """Returns same text enter by user and you have to responed to the user using the same language the user use."""
    return input

if prompt := st.chat_input():
    GOOGLE_CSE_ID = os.getenv('GOOGLE_CSE_ID', 'b13bba6a528214af0')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', 'AIzaSyC_0LAqVIA0Z7YLbbWKSOHxY0_sMaqQAko')
    # tools = [WebResearchRetriever(num_search_results=3,search=GoogleSearchAPIWrapper(google_api_key=GOOGLE_API_KEY, google_cse_id=GOOGLE_CSE_ID), allow_dangerous_requests=True)]
    # tools = [GoogleSearchResults(num_results=4,api_wrapper=GoogleSearchAPIWrapper(google_api_key=GOOGLE_API_KEY, google_cse_id=GOOGLE_CSE_ID))]
    tools = [
        GoogleSearchResults(num_results=4,api_wrapper=GoogleSearchAPIWrapper(google_api_key=GOOGLE_API_KEY, google_cse_id=GOOGLE_CSE_ID)),
        Tool(
        name = "Scrape_Webpages",
        func=scrape_webpages,
        description="You are a research assistant who can scrape specified urls for more detailed information using the scrape_webpages function."
        ),
        Tool(
        name = "Pass_Text",
        func=pass_text,
        description="You are a assistant just pass the text. "
        )
    ]
    # 
    llm = ChatOllama(model="llama3.1:8b", num_ctx=16384, temperature = 0, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]), base_url="https://109.199.116.46", client_kwargs={'verify': False}).bind_tools(tools=tools)
    # aiprompt = hub.pull("hwchase17/openai-tools-agent")
    # aiprompt.messages[0] = SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], input_types={}, partial_variables={}, template='You are a helpful assistant with the personality of Socrates. Be super verbose and philosophical'))
    # memory = MemorySaver()
    # MEMORY_KEY = "chat_history"
    # prompts = hub.pull("hwchase17/openai-tools-agent")
    # prompts.messages[0] = SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], input_types={}, partial_variables={}, template="You are a powerful assistant created by OSH company. You can engage professionally in general conversations on any topic, responding in the user's language. Maintain a professional, analytical tone, and present both positive and negative insights based on gathered information in clear, well-formatted markdown. Use the tools *only* if the answer is missing or outdated in your knowledge, or if the user explicitly requests a web search."))
    # chat_history = []
    # MEMORY_KEY = "chat_history"
    prompts = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "You are a powerful assistant created by OSH (Open Source Handbook) company. "
                    "Engage professionally in conversations on any topic, always responding strictly in the user's language, including when using any tool. "
                    "Do not switch to another language unless explicitly requested by the user.\n\n"
                    "Maintain a professional, analytical tone, presenting both positive and negative insights in clear, well-formatted markdown.\n\n"
                    "Use the `pass_text` tool to echo user input or to handle tasks that do not require external information retrieval. "
                    "Use other tools only under these conditions, and ensure all responses are in the user's language:\n"
                    "- If information is missing or outdated in your knowledge base, use the `google_search_results_json` tool.\n"
                    "- If the user explicitly requests a web search, use the `google_search_results_json` tool.\n"
                    "- If the user requests the full source article, use the `Scrape_Webpages` tool."
                ),
            ),
            ("user", "{input}"),
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
        | llm
        | OpenAIToolsAgentOutputParser()
    )
    agent = create_tool_calling_agent(llm, tools, prompts)
    client = AgentExecutor(agent=agent, tools=tools, verbose=True)

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        # response = client.invoke(input={"input": st.session_state.messages, "chat_history": chat_history})
        response = client.invoke(input={"input": st.session_state.messages, "agent_scratchpad":"agent_scratchpad"})
        print("RESPONSE", response)
        msg = response["output"]
        st.session_state.messages.append({"role": "assistant", "content": msg})
        chat_history = st.session_state.messages
        print("chat_history \n", chat_history)
        st.chat_message("assistant").write(msg)  # Changed msg to response to avoid undefined variable
    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": str(e)})
        st.chat_message("assistant").write(str(e))
        print("Error invoking the client:", str(e))