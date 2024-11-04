import streamlit as st
import sqlite3
from app_pages.db_setup import create_db  # Import the create_db function
from langchain_ollama import OllamaLLM  # Import the Ollama class from Langchain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents import AgentExecutor
from langchain_ollama import ChatOllama
# from langchain_ollama import OllamaEmbeddings
create_db()
st.title("View and Select Saved Searches")

# Persistent storage for selected search IDs and each category's "Select All" state
if 'selected_search_ids' not in st.session_state:
    st.session_state.selected_search_ids = set()
if 'select_all_states' not in st.session_state:
    st.session_state.select_all_states = {}

# Initialize the Ollama model
tools = []
model = ChatOllama(model="llama3.1:8b", num_ctx=16384, temperature = 0, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),base_url="https://109.199.116.46", client_kwargs={'verify': False}, verbose=True).bind_tools(tools=tools)  # Specify your model here
prompts = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful and very powerful assistant. You were created by OSH company. You are an analysis model tasked with evaluating the news articles. Please provide a detailed report that includes sentiment analysis (تحليل العواطف), trends (الترندات), potential impacts on reputation, and actionable suggestions based on the content. When responed use this language {language} and make sure to use it with out mistakes.",
            ),
            # MessagesPlaceholder(variable_name=MEMORY_KEY),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

agent = (
        {
            "language": lambda x: x["language"],
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
client = AgentExecutor(agent=agent, tools=tools, verbose=True)
# Retrieve and categorize saved searches
conn = sqlite3.connect('company_reputation.db')
c = conn.cursor()
c.execute("SELECT id, company_name, title, classification, date FROM searches")
searches = c.fetchall()
conn.close()

# Organize searches by classification
search_categories = {
    "Public": [],
    "Competitors": [],
    "Allies": [],
    "Enemies": []
}

for search in searches:
    search_id, company_name, title, classification, date = search
    search_data = (search_id, company_name, title, date)
    search_categories.get(classification, []).append(search_data)

# Function to display checkboxes for each search in a category
def display_searches(category_name, searches):
    # Initialize the "Select All" state for this category if not already
    if category_name not in st.session_state.select_all_states:
        st.session_state.select_all_states[category_name] = False

    # Capture the "Select All" checkbox state with a temporary variable
    select_all_key = f"{category_name}_select_all"
    select_all_temp = st.checkbox(f"Select All in {category_name}", key=select_all_key,
                                  value=st.session_state.select_all_states[category_name])

    # Update individual checkboxes if "Select All" state changes
    if select_all_temp != st.session_state.select_all_states[category_name]:
        st.session_state.select_all_states[category_name] = select_all_temp
        for search_id, *_ in searches:
            st.session_state[f"{search_id}_checkbox"] = select_all_temp
            if select_all_temp:
                st.session_state.selected_search_ids.add(search_id)
            else:
                st.session_state.selected_search_ids.discard(search_id)

    # Display each checkbox with the updated state
    for search_id, company_name, title, date in searches:
        checkbox_label = f"{title} ({company_name}) - on {date}"
        is_selected = st.session_state.get(f"{search_id}_checkbox", False)

        # Update session state on individual selection change
        if st.checkbox(checkbox_label, key=f"{search_id}_checkbox", value=is_selected):
            st.session_state.selected_search_ids.add(search_id)
            # Deselect "Select All" if any individual checkbox is unchecked
            if not all(st.session_state.get(f"{search_id}_checkbox", False) for search_id, *_ in searches):
                st.session_state.select_all_states[category_name] = False
        else:
            st.session_state.selected_search_ids.discard(search_id)
            # Update "Select All" checkbox if all items are checked
            if all(st.session_state.get(f"{search_id}_checkbox", False) for search_id, *_ in searches):
                st.session_state.select_all_states[category_name] = True

# Display categorized searches
for category, searches in search_categories.items():
    with st.expander(f"{category} Searches"):
        display_searches(category, searches)

# Button to pass selected searches to model
analyze_button = st.button("Analyze Selected Searches")

# Retrieve full content for selected searches
# Retrieve full content, source links, and timestamps for selected searches
def get_selected_content(selected_ids):
    conn = sqlite3.connect('company_reputation.db')
    c = conn.cursor()
    query = f"SELECT full_content, link, date, classification FROM searches WHERE id IN ({','.join(['?']*len(selected_ids))})"
    c.execute(query, selected_ids)
    content = c.fetchall()
    conn.close()
    return content

# Analyze the selected searches
if analyze_button and st.session_state.selected_search_ids:
    selected_content = get_selected_content(list(st.session_state.selected_search_ids))
    
    # Prepare the input for the model with specific instructions
    model_input = []

    for idx, (content, link, timestamp, classification) in enumerate(selected_content):
        model_input.append(f"News article content {idx+1}:\n{content}\nClassification: {classification}\nSource: {link}\nDate: {timestamp}")
    print("model_input", model_input)
    if isinstance(model_input, list) and all(isinstance(i, str) for i in model_input):
        # Send the prepared input to the Ollama model for analysis
        try:
            report = client.invoke(input={"language":"Arabic", "input":model_input, "agent_scratchpad":"agent_scratchpad"})  # Pass model_input as a list of strings
            
            # Display the generated report
            st.subheader("Generated Report:")
            st.write(report["output"])

        except Exception as e:
            st.error(f"An error occurred while communicating with the Ollama model: {e}")
    else:
        st.error("The input provided to the model is not a list of strings.")
else:
    if analyze_button:
        st.warning("No searches selected for analysis.")

# saved_searches.py
# import streamlit as st
# import sqlite3
# import pickle
# from app_pages.db_setup import create_db  # Import the create_db function
# from langchain_ollama import OllamaLLM, ChatOllama
# from langchain_ollama import OllamaEmbeddings
# from langchain.callbacks.manager import CallbackManager
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
# from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
# from langchain.agents import AgentExecutor

# # Database setup
# create_db()
# st.title("View and Select Saved Searches")

# # Initialize session states for selection and embedding model
# if 'selected_search_ids' not in st.session_state:
#     st.session_state.selected_search_ids = set()
# if 'select_all_states' not in st.session_state:
#     st.session_state.select_all_states = {}

# # Initialize the embedding and model
# embedding_model = OllamaEmbeddings(model="llama3.1:8b", base_url="https://109.199.116.46", client_kwargs={'verify': False})
# tools = []
# llama_model = ChatOllama(model="llama3.1:8b", num_ctx=16384, temperature=0, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]), base_url="https://109.199.116.46", client_kwargs={'verify': False}).bind_tools(tools=tools)

# prompts = ChatPromptTemplate.from_messages(
#     [
#         ("system", "You are a powerful analysis assistant. Provide a report including sentiment, trends, impact on reputation, and actionable insights."),
#         ("human", "{input}"),
#         MessagesPlaceholder(variable_name="agent_scratchpad"),
#     ]
# )

# agent = (
#     {
#         "input": lambda x: x["input"],
#         "agent_scratchpad": lambda x: format_to_openai_tool_messages(
#             x["intermediate_steps"]
#         ),
#     }
#     | prompts
#     | llama_model
#     | OpenAIToolsAgentOutputParser()
# )
# client = AgentExecutor(agent=agent, tools=tools, verbose=True)

# # Retrieve content and embeddings for selected searches
# def get_selected_content_and_embeddings(selected_ids):
#     conn = sqlite3.connect('company_reputation.db')
#     c = conn.cursor()
#     query = f"SELECT full_content, link, date, classification, embedding FROM searches WHERE id IN ({','.join(['?']*len(selected_ids))})"
#     c.execute(query, selected_ids)
#     content_data = c.fetchall()
#     conn.close()
    
#     # Deserialize embeddings
#     results = []
#     for content, link, date, classification, embedding_blob in content_data:
#         embedding_vector = pickle.loads(embedding_blob)
#         results.append((content, link, date, classification, embedding_vector))
    
#     return results

# # Fetch saved searches and categorize them
# conn = sqlite3.connect('company_reputation.db')
# c = conn.cursor()
# c.execute("SELECT id, company_name, title, classification, date FROM searches")
# searches = c.fetchall()
# conn.close()

# search_categories = {"Public": [], "Competitors": [], "Allies": [], "Enemies": []}
# for search in searches:
#     search_id, company_name, title, classification, date = search
#     search_data = (search_id, company_name, title, date)
#     search_categories.get(classification, []).append(search_data)

# # Display search checkboxes for each category
# def display_searches(category_name, searches):
#     select_all_key = f"{category_name}_select_all"
#     select_all_temp = st.checkbox(f"Select All in {category_name}", key=select_all_key, value=st.session_state.select_all_states.get(category_name, False))

#     if select_all_temp != st.session_state.select_all_states.get(category_name, False):
#         st.session_state.select_all_states[category_name] = select_all_temp
#         for search_id, *_ in searches:
#             st.session_state[f"{search_id}_checkbox"] = select_all_temp
#             if select_all_temp:
#                 st.session_state.selected_search_ids.add(search_id)
#             else:
#                 st.session_state.selected_search_ids.discard(search_id)

#     for search_id, company_name, title, date in searches:
#         checkbox_label = f"{title} ({company_name}) - on {date}"
#         is_selected = st.session_state.get(f"{search_id}_checkbox", False)

#         if st.checkbox(checkbox_label, key=f"{search_id}_checkbox", value=is_selected):
#             st.session_state.selected_search_ids.add(search_id)
#             if not all(st.session_state.get(f"{search_id}_checkbox", False) for search_id, *_ in searches):
#                 st.session_state.select_all_states[category_name] = False
#         else:
#             st.session_state.selected_search_ids.discard(search_id)
#             if all(st.session_state.get(f"{search_id}_checkbox", False) for search_id, *_ in searches):
#                 st.session_state.select_all_states[category_name] = True

# # Show categorized searches
# for category, searches in search_categories.items():
#     with st.expander(f"{category} Searches"):
#         display_searches(category, searches)

# # Analyze selected searches
# analyze_button = st.button("Analyze Selected Searches")
# if analyze_button and st.session_state.selected_search_ids:
#     selected_content = get_selected_content_and_embeddings(list(st.session_state.selected_search_ids))
    
#     model_input = []
#     for idx, (content, link, date, classification, embedding_vector) in enumerate(selected_content):
#         model_input.append(f"Content {idx+1}: {content}\nClassification: {classification}\nLink: {link}\nDate: {date}\nEmbedding: {embedding_vector}")
    
#     if isinstance(model_input, list) and all(isinstance(i, str) for i in model_input):
#         try:
#             report = client.invoke(input={"input": model_input})
#             st.subheader("Generated Report:")
#             st.write(report["output"])
#         except Exception as e:
#             st.error(f"Error communicating with Ollama model: {e}")
# else:
#     if analyze_button:
#         st.warning("No searches selected for analysis.")
