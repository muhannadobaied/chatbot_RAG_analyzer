# # reporting_page.py
# import json
# import streamlit as st
# import sqlite3
# import pandas as pd
# from datetime import datetime

# # Utility function to get a database connection
# def get_connection():
#     return sqlite3.connect("reputation_management.db")

# # Fetch data for reporting
# def fetch_analyzed_data(start_date=None, end_date=None):
#     conn = get_connection()
#     cursor = conn.cursor()
#     query = """
#         SELECT md.source, md.content, s.overall_sentiment, r.potential_impact, a.suggestions, md.timestamp
#         FROM monitoring_data md
#         LEFT JOIN sentiment s ON md.id = s.monitoring_data_id
#         LEFT JOIN reputation_impact r ON md.id = r.monitoring_data_id
#         LEFT JOIN actionable_suggestions a ON md.id = a.monitoring_data_id
#         WHERE md.validated = 1
#     """
#     params = []

#     if start_date:
#         query += " AND md.timestamp >= ?"
#         params.append(start_date)
#     if end_date:
#         query += " AND md.timestamp <= ?"
#         params.append(end_date)

#     cursor.execute(query, tuple(params))
#     data = cursor.fetchall()
#     conn.close()
#     return data

# # Display analyzed data in a report format
# def generate_total_report(data):
#     if data:
#         st.write("### Total Report Summary")
#         report_df = pd.DataFrame(data, columns=[
#             "Source", "Content", "Sentiment", "Potential Impact", "Suggestions", "Timestamp"
#         ])
        
#         # Display data summary
#         st.dataframe(report_df, use_container_width=True)

#         # Summary statistics
#         st.write("#### Sentiment Summary")
#         sentiment_summary = report_df['Sentiment'].astype(float).describe()
#         st.write(sentiment_summary)

#         st.write("#### Potential Impact Summary")
#         impact_summary = report_df['Potential Impact'].astype(float).describe()
#         st.write(impact_summary)

#         # Optional visualization
#         st.write("#### Sentiment Distribution")
#         st.bar_chart(report_df['Sentiment'].astype(float))

#         st.write("#### Potential Impact Distribution")
#         st.bar_chart(report_df['Potential Impact'].astype(float))

#         # Extract unique suggestions from the DataFrame
#         suggestions_list = report_df["Suggestions"].dropna().unique()
        
#         st.write("### Unique Suggestions")
#         for suggestion in suggestions_list:
#             try:
#                 # Attempt to load suggestion string as JSON
#                 parsed_suggestion = json.loads(suggestion)
#                 # Display the parsed suggestion (assumes it can be a list or similar structure)
#                 if isinstance(parsed_suggestion, list):
#                     for item in parsed_suggestion:
#                         st.write(f"- {item}")
#                 else:
#                     # If parsed suggestion is not a list, display it as a string
#                     st.write(f"- {parsed_suggestion}")
#             except json.JSONDecodeError:
#                 # If loading as JSON fails, display the raw suggestion string
#                 st.write(f"- {suggestion}")

#     else:
#         st.warning("No data available for the selected date range.")

# # Main reporting page function
# def display_reporting():
#     st.title("Reporting")

#     st.subheader("Filter by Date")
#     start_date = st.date_input("Start Date", value=None)
#     end_date = st.date_input("End Date", value=None)

#     if st.button("Generate Report"):
#         data = fetch_analyzed_data(
#             start_date=start_date.isoformat() if start_date else None,
#             end_date=end_date.isoformat() if end_date else None
#         )
#         generate_total_report(data)

# # Run the page function
# display_reporting()


# reporting_page.py
import json
import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from langchain_ollama import OllamaLLM  # Import the Ollama class
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# Utility function to get a database connection
def get_connection():
    return sqlite3.connect("reputation_management.db")

# Fetch data for reporting
def fetch_analyzed_data(start_date=None, end_date=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT md.source, md.content, s.overall_sentiment, r.potential_impact, a.suggestions, md.timestamp
        FROM monitoring_data md
        LEFT JOIN sentiment s ON md.id = s.monitoring_data_id
        LEFT JOIN reputation_impact r ON md.id = r.monitoring_data_id
        LEFT JOIN actionable_suggestions a ON md.id = a.monitoring_data_id
        WHERE md.validated = 1
    """
    params = []

    if start_date:
        query += " AND md.timestamp >= ?"
        params.append(start_date)
    if end_date:
        query += " AND md.timestamp <= ?"
        params.append(end_date)

    cursor.execute(query, tuple(params))
    data = cursor.fetchall()
    conn.close()
    return data

# Model setup function
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

# Run analysis on content using the model
def run_analysis(content):
    prompt = f"""
    Analyze the following text for sentiment, potential reputation impact, and actionable suggestions:
    "{content}"
    Provide the analysis in JSON format with keys 'overall_sentiment', 'sentiment_reasons', 'potential_impact',
    'impact_reasons', 'suggestions', and 'rationale'.
    Respond in the Arabic language.
    Make the values as float numbers and make sure to follow these rules:
    1- The range is from -1.0 to 1.0.
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

# Generate total report and display data
def generate_total_report(data):
    if data:
        st.write("### Total Report Summary")
        report_df = pd.DataFrame(data, columns=[
            "Source", "Content", "Sentiment", "Potential Impact", "Suggestions", "Timestamp"
        ])
        
        # Display data summary
        st.dataframe(report_df, use_container_width=True)

        # Summary statistics
        st.write("#### Sentiment Summary")
        sentiment_summary = report_df['Sentiment'].astype(float).describe()
        st.write(sentiment_summary)

        st.write("#### Potential Impact Summary")
        impact_summary = report_df['Potential Impact'].astype(float).describe()
        st.write(impact_summary)

        # Optional visualization
        st.write("#### Sentiment Distribution")
        st.bar_chart(report_df['Sentiment'].astype(float))

        st.write("#### Potential Impact Distribution")
        st.bar_chart(report_df['Potential Impact'].astype(float))

        # Extract unique suggestions from the DataFrame
        suggestions_list = report_df["Suggestions"].dropna().unique()
        
        st.write("### Unique Suggestions")
        for suggestion in suggestions_list:
            try:
                # Attempt to load suggestion string as JSON
                parsed_suggestion = json.loads(suggestion)
                if isinstance(parsed_suggestion, list):
                    for item in parsed_suggestion:
                        st.write(f"- {item}")
                else:
                    st.write(f"- {parsed_suggestion}")
            except json.JSONDecodeError:
                st.write(f"- {suggestion}")

    else:
        st.warning("No data available for the selected date range.")

# Generate model analysis report
def generate_model_analysis(data):
    report_df = pd.DataFrame(data, columns=[
        "Source", "Content", "Sentiment", "Potential Impact", "Suggestions", "Timestamp"
    ])
    
    combined_content = " ".join(report_df["Content"].dropna().astype(str).tolist())
    st.write("### Model Analysis on Combined Content")
    with st.spinner("Running model analysis..."):
        sentiment, sentiment_reasons, impact, impact_reasons, suggestions, rationale, priority = run_analysis(combined_content)
        st.write(f"- **Overall Sentiment:** {sentiment}")
        st.write(f"- **Sentiment Reasons:** {sentiment_reasons}")
        st.write(f"- **Potential Impact:** {impact}")
        st.write(f"- **Impact Reasons:** {impact_reasons}")
        st.write(f"- **Suggestions:** {suggestions}")
        st.write(f"- **Rationale:** {rationale}")
        st.write(f"- **Priority Level:** {priority}")

# Main reporting page function
def display_reporting():
    st.title("Reporting")

    st.subheader("Filter by Date")
    start_date = st.date_input("Start Date", value=None)
    end_date = st.date_input("End Date", value=None)

    if st.button("Generate Report"):
        data = fetch_analyzed_data(
            start_date=start_date.isoformat() if start_date else None,
            end_date=end_date.isoformat() if end_date else None
        )
        generate_total_report(data)

    if st.button("Run Model Analysis"):
        data = fetch_analyzed_data(
            start_date=start_date.isoformat() if start_date else None,
            end_date=end_date.isoformat() if end_date else None
        )
        if data:
            generate_model_analysis(data)
        else:
            st.warning("No data available to analyze.")

# Run the page function
display_reporting()
