from typing import Any, ClassVar
import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from langchain.tools import tool
from langchain.utilities import GoogleSearchAPIWrapper

from pydantic import BaseModel, Field 
GOOGLE_CSE_ID = 'b13bba6a528214af0'
GOOGLE_API_KEY = 'AIzaSyC_0LAqVIA0Z7YLbbWKSOHxY0_sMaqQAko'
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
# # Define the search tool and bind it to the LLM
# class GetSearchResults(BaseModel):
#     '''Search for the time in countries the user asks about'''
    
#     Results: str = Field(..., description="The search results")
    
#     GOOGLE_CSE_ID: ClassVar = GOOGLE_CSE_ID
#     GOOGLE_API_KEY: ClassVar = GOOGLE_API_KEY
#     search: ClassVar = GoogleSearchAPIWrapper(google_api_key=GOOGLE_API_KEY, google_cse_id=GOOGLE_CSE_ID)

#     @tool
#     @classmethod
#     def search_for_time_in_country(cls, query: str) -> str:
#         """Search for the time in countries the user asks."""
#         return cls.search.run(query)
from langchain_community.utilities import GoogleSearchAPIWrapper
@tool
def search_for_time_in_country(query: str) -> str:
    """Search for the time in countries the user asks."""
    search = GoogleSearchAPIWrapper(google_api_key=GOOGLE_API_KEY, google_cse_id=GOOGLE_CSE_ID)
    result = search.run(query)
    print("TOOOOOOOOOT",result)
    return result

llm_with_tools = llm.bind_tools([search_for_time_in_country])

mm = llm_with_tools.invoke(input="search for the time in Yemen right now.")
print("MMMMMMMM", mm)

st.title("LLM-Powered Google Search Tool")
# User input for query
query = st.text_input("Enter your search query", "time in Yemen")

if st.button("Search"):
    # Use the LLM with tools to invoke the search functionality based on user input
    response = llm_with_tools.invoke(query)
    
    # Display the results from the LLM with the tool
    st.write("LLM Response:", response)
# st.title("شركة OSH")
# st.write(
#     "نظام ادارة السمعة للشركات"
# )

# if "messages" not in st.session_state:
#     st.session_state["messages"] = [{"role": "assistant", "content": "مرحبا كيف يمكنني مساعدتك"}]

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

# if prompt := st.chat_input():
