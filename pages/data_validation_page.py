# import streamlit as st
# from database import get_connection

# def data_validation_page():
#     st.title("Data Validation and Selection")

#     # Display previously saved data
#     st.subheader("Saved Data View")
#     conn = get_connection()
#     cursor = conn.execute("SELECT id, source, content, sentiment, timestamp FROM monitoring_data ORDER BY timestamp DESC")
#     data = cursor.fetchall()
#     conn.close()

#     # Allow users to filter data by sentiment
#     sentiment_filter = st.multiselect("Filter by Sentiment", ["Positive", "Neutral", "Negative"], default=["Positive", "Neutral", "Negative"])
#     filtered_data = [d for d in data if d[3].lower() in [s.lower() for s in sentiment_filter]]

#     if filtered_data:
#         selected_ids = []
#         for row in filtered_data:
#             if st.checkbox(f"{row[1]} - {row[2][:50]}...", key=row[0]):
#                 selected_ids.append(row[0])

#         # Save selected data for reporting
#         if st.button("Confirm Selection for Report"):
#             conn = get_connection()
#             for data_id in selected_ids:
#                 conn.execute("INSERT INTO selected_data (monitoring_data_id) VALUES (?)", (data_id,))
#             conn.commit()
#             conn.close()
#             st.success("Data selected for report generation!")
#     else:
#         st.write("No data matching the selected sentiment.")


# data_validation_page()

# import streamlit as st
# import sqlite3

# # Connect to the database
# def get_connection():
#     return sqlite3.connect("reputation_management.db")

# # Retrieve unvalidated data
# def fetch_unvalidated_data():
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT id, source, content, sentiment FROM monitoring_data WHERE validated IS NULL OR validated = 0")
#     data = cursor.fetchall()
#     conn.close()
#     return data

# # Mark data as validated
# def mark_as_validated(data_id, valid):
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("UPDATE monitoring_data SET validated = ? WHERE id = ?", (1 if valid else 0, data_id))
#     conn.commit()
#     conn.close()

# # Display and validate data
# def display_data_validation():
#     st.title("Data Validation")

#     unvalidated_data = fetch_unvalidated_data()
#     if not unvalidated_data:
#         st.write("All data has been validated.")
#         return

#     for data in unvalidated_data:
#         data_id, source, content, sentiment = data
#         with st.expander(f"Source: {source}"):
#             st.write(f"**Content:** {content}")
#             st.write(f"**Sentiment:** {sentiment}")

#             if st.button("Mark as Valid", key=f"valid_{data_id}"):
#                 mark_as_validated(data_id, True)
#                 st.success("Data marked as valid.")
#                 st.rerun()

#             if st.button("Mark as Invalid", key=f"invalid_{data_id}"):
#                 mark_as_validated(data_id, False)
#                 st.warning("Data marked as invalid.")
#                 st.rerun()

# # Run the page function
# display_data_validation()

import streamlit as st
import sqlite3
from langchain_ollama import OllamaLLM  # Import the Ollama class
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents import AgentExecutor
import json
# Establish connection to the database
def get_connection():
    return sqlite3.connect("reputation_management.db")

# Fetch unvalidated data from the database
def fetch_unvalidated_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, source, content FROM monitoring_data WHERE validated IS NULL OR validated = 0")
    data = cursor.fetchall()
    conn.close()
    return data

# Save analysis results to the database
def save_analysis_results(data_id, sentiment, sentiment_reasons, impact, impact_reasons, suggestions, rationale, priority):
    conn = get_connection()
    cursor = conn.cursor()

    # Insert sentiment analysis results
    print("sentiment", sentiment)
    cursor.execute('''
        INSERT INTO sentiment (overall_sentiment, reasons, monitoring_data_id)
        VALUES (?, ?, ?)
    ''', (sentiment, json.dumps(sentiment_reasons), data_id))

    # Insert reputation impact analysis results
    print("potential_impact", impact)
    print("reasons", json.dumps(impact_reasons))
    cursor.execute('''
        INSERT INTO reputation_impact (potential_impact, reasons, monitoring_data_id)
        VALUES (?, ?, ?)
    ''', (impact, json.dumps(impact_reasons), data_id))

    # Insert actionable suggestions
    cursor.execute('''
        INSERT INTO actionable_suggestions (suggestions, rationale, monitoring_data_id)
        VALUES (?, ?, ?)
    ''', (json.dumps(suggestions), json.dumps(rationale), data_id))

    # Update the monitoring_data table with validation status and priority
    cursor.execute('''
        UPDATE monitoring_data
        SET validated = 1, priority = ?
        WHERE id = ?
    ''', (priority, data_id))

    conn.commit()
    conn.close()



# Mark a data entry as validated in the database
def mark_as_validated(data_id, valid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE monitoring_data SET validated = ? WHERE id = ?", (1 if valid else 0, data_id))
    conn.commit()
    conn.close()

# Initialize the model for analysis
def setup_model():
    model = OllamaLLM(
        model="llama3.1:8b", 
        num_ctx=16384, 
        temperature=0, 
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]), 
        base_url="https://109.199.116.46", 
        client_kwargs={'verify': False}, 
        verbose=True
    )
    return model

def run_analysis(content):
    # prompt = f"""
    # Analyze the following text for sentiment, potential reputation impact, and actionable suggestions:
    # "{content}"
    # Provide the analysis in JSON format with keys 'sentiment', 'reputation_impact', and 'actionable_suggestions'.
    # when respond use the Arabic language.
    # """
    
    prompt = f"""
    Analyze the following text for sentiment, potential reputation impact, and actionable suggestions:
    "{content}"
    Provide the analysis in JSON format with keys 'overall_sentiment', 'sentiment_reasons', 'potential_impact',
    'impact_reasons', 'suggestions', and 'rationale'.
    Respond in the Arabic language.
    Make the values as float number and make sure to follow these rules:
    1- the range is from -1.0 to 1.0.
    """
    model = setup_model()
    result = model.invoke(prompt)
    
    try:
        start_index = result.index('{')
        end_index = result.rindex('}') + 1
        json_string = result[start_index:end_index]
        parsed_result = json.loads(json_string)
    except (ValueError, json.JSONDecodeError):
        st.error("Failed to parse the analysis response.")
        st.write(result)
        return "Error", "Error", "Error", "Error", "Error", "Error", 2

    sentiment = parsed_result.get("overall_sentiment", {})
    sentiment_reasons = parsed_result.get("sentiment_reasons", [])
    impact = parsed_result.get("potential_impact", {})
    impact_reasons = parsed_result.get("impact_reasons", [])
    suggestions = parsed_result.get("suggestions", [])
    rationale = parsed_result.get("rationale", [])
    priority = 1 if suggestions != "لا توجد اقتراحات" else 2

    return sentiment, sentiment_reasons, impact, impact_reasons, suggestions, rationale, priority

# Display and validate data with analysis
def display_data_validation():
    st.title("Data Validation and Analysis")

    unvalidated_data = fetch_unvalidated_data()
    if not unvalidated_data:
        st.write("All data has been validated.")
        return
    # sentiment = None
    # sentiment_reasons = None
    # impact = None
    # impact_reasons = None
    # suggestions = None
    # rationale = None
    # priority = None
    
    for data in unvalidated_data:
        data_id, source, content = data
        with st.expander(f"Source: {source}"):
            st.write(f"**Content:** {content}")
            # st.write(f"**Sentiment (Initial):** {sentiment}")
            
            if st.button("Analyze Content", key=f"analyze_{data_id}"):
                with st.spinner("Analyzing content..."):
                    sentiment, sentiment_reasons, impact, impact_reasons, suggestions, rationale, priority = run_analysis(content)
                    save_analysis_results(data_id, sentiment, sentiment_reasons, impact, impact_reasons, suggestions, rationale, priority)
                    st.success("Analysis complete and results saved.")
                    st.write("### Analysis Report")
                    st.write(sentiment, sentiment_reasons, impact, impact_reasons, suggestions, rationale, priority)
                    # st.rerun()

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Mark as Valid", key=f"valid_{data_id}"):
                    mark_as_validated(data_id, True)
                    # save_analysis_results(data_id, sentiment, sentiment_reasons, impact, impact_reasons, suggestions, rationale, priority)
                    # st.success("Analysis complete and results saved.")
                    st.success("Data marked as valid.")
                    st.rerun()
            with col2:
                if st.button("Mark as Invalid", key=f"invalid_{data_id}"):
                    mark_as_validated(data_id, False)
                    st.warning("Data marked as invalid.")
                    st.rerun()

# Run the page function
display_data_validation()
