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
# import json
# import streamlit as st
# import sqlite3
# import pandas as pd
# from datetime import datetime
# from langchain_ollama import OllamaLLM  # Import the Ollama class
# from langchain.callbacks.manager import CallbackManager
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
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

# # Model setup function
# def setup_model():
#     model = OllamaLLM(
#         model="llama3.1:8b", 
#         num_ctx=16384, 
#         temperature=0, 
#         callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]), 
#         base_url="https://109.199.116.46", 
#         client_kwargs={'verify': False}, 
#         verbose=True
#     )
#     return model

# # Run analysis on content using the model
# def run_analysis(content):
#     prompt = f"""
#     Analyze the following text for sentiment, potential reputation impact, and actionable suggestions:
#     "{content}"
#     Provide the analysis in JSON format with keys 'overall_sentiment', 'sentiment_reasons', 'potential_impact',
#     'impact_reasons', 'suggestions', and 'rationale'.
#     Respond in the Arabic language.
#     Make the values as float numbers and make sure to follow these rules:
#     1- The range is from -1.0 to 1.0.
#     """
#     model = setup_model()
#     result = model.invoke(prompt)
    
#     try:
#         start_index = result.index('{')
#         end_index = result.rindex('}') + 1
#         json_string = result[start_index:end_index]
#         parsed_result = json.loads(json_string)
#     except (ValueError, json.JSONDecodeError):
#         st.error("Failed to parse the analysis response.")
#         st.write(result)
#         return "Error", "Error", "Error", "Error", "Error", "Error", 2

#     sentiment = parsed_result.get("overall_sentiment", {})
#     sentiment_reasons = parsed_result.get("sentiment_reasons", [])
#     impact = parsed_result.get("potential_impact", {})
#     impact_reasons = parsed_result.get("impact_reasons", [])
#     suggestions = parsed_result.get("suggestions", [])
#     rationale = parsed_result.get("rationale", [])
#     priority = 1 if suggestions != "لا توجد اقتراحات" else 2

#     return sentiment, sentiment_reasons, impact, impact_reasons, suggestions, rationale, priority

# # Generate total report and display data
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
#                 if isinstance(parsed_suggestion, list):
#                     for item in parsed_suggestion:
#                         st.write(f"- {item}")
#                 else:
#                     st.write(f"- {parsed_suggestion}")
#             except json.JSONDecodeError:
#                 st.write(f"- {suggestion}")

#     else:
#         st.warning("No data available for the selected date range.")

# # Generate model analysis report
# def generate_model_analysis(data):
#     report_df = pd.DataFrame(data, columns=[
#         "Source", "Content", "Sentiment", "Potential Impact", "Suggestions", "Timestamp"
#     ])
    
#     combined_content = " ".join(report_df["Content"].dropna().astype(str).tolist())
#     st.write("### Model Analysis on Combined Content")
#     with st.spinner("Running model analysis..."):
#         sentiment, sentiment_reasons, impact, impact_reasons, suggestions, rationale, priority = run_analysis(combined_content)
#         st.write(f"- **Overall Sentiment:** {sentiment}")
#         st.write(f"- **Sentiment Reasons:** {sentiment_reasons}")
#         st.write(f"- **Potential Impact:** {impact}")
#         st.write(f"- **Impact Reasons:** {impact_reasons}")
#         st.write(f"- **Suggestions:** {suggestions}")
#         st.write(f"- **Rationale:** {rationale}")
#         st.write(f"- **Priority Level:** {priority}")

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

#     if st.button("Run Model Analysis"):
#         data = fetch_analyzed_data(
#             start_date=start_date.isoformat() if start_date else None,
#             end_date=end_date.isoformat() if end_date else None
#         )
#         if data:
#             generate_model_analysis(data)
#         else:
#             st.warning("No data available to analyze.")

# # Run the page function
# display_reporting()

import json
import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from streamlit_option_menu import option_menu
from langchain_ollama import OllamaLLM
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Utility function to get a database connection
def get_connection():
    return sqlite3.connect("reputation_management.db")

# Create the `saved_reports` table
def create_saved_reports_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_type TEXT NOT NULL,
            overall_sentiment TEXT,
            potential_impact TEXT,
            suggestions TEXT,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Call this function once to ensure the table is created
create_saved_reports_table()

# Fetch filtered saved reports
def fetch_filtered_reports(report_type=None, start_date=None, end_date=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT id, report_type, overall_sentiment, potential_impact, suggestions, timestamp 
        FROM saved_reports
        WHERE 1=1
    """
    params = []

    if report_type:
        query += " AND report_type = ?"
        params.append(report_type)
    if start_date:
        query += " AND DATE(timestamp) >= ?"
        params.append(start_date)
    if end_date:
        query += " AND DATE(timestamp) <= ?"
        params.append(end_date)

    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.close()
    return data

# Utility to display a single report in a structured format
def display_saved_report(report):
    st.write(f"### Report ID: {report[0]}")
    st.write(f"**Report Type:** {report[1]}")
    st.write(f"**Overall Sentiment:** {report[2]}")
    st.write(f"**Potential Impact:** {report[3]}")
    st.write("#### Suggestions:")
    for suggestion in json.loads(report[4]):
        st.markdown(f"- {suggestion}")
    st.write(f"**Generated At:** {report[5]}")
    st.markdown("---")

# Save report results
def save_report(report_type, overall_sentiment, potential_impact, suggestions, timestamp):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO saved_reports (report_type, overall_sentiment, potential_impact, suggestions, timestamp) 
        VALUES (?, ?, ?, ?, ?)
    """, (report_type, overall_sentiment, potential_impact, json.dumps(suggestions), timestamp))
    conn.commit()
    conn.close()

# Enhanced Charts Function
def enhanced_charts(data, title, x_label, y_label):
    df = pd.DataFrame(data, columns=[x_label, y_label])
    st.write(f"#### {title}")
    st.bar_chart(data=df, x=x_label, y=y_label)

# Styled Unique Suggestions
def styled_suggestions(suggestions):
    st.write("### Unique Suggestions")
    for suggestion in suggestions:
        st.markdown(f"✔️ **{suggestion}**", unsafe_allow_html=True)

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

# Enhanced Report Analysis
def run_analysis_with_type(content, report_type):
    prompt = f"""
        Analyze the following text for {report_type}. Respond in valid JSON format with keys:
        - overall_sentiment (string)
        - potential_impact (string)
        - suggestions (array of strings)

        "{content}"
        Respond in Arabic.
        """

    model = OllamaLLM(
        model="llama3.1:8b", 
        num_ctx=16384, 
        temperature=0, 
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]), 
        base_url="https://109.199.116.46", 
        client_kwargs={'verify': False}, 
        verbose=True
    )
    result = model.invoke(prompt)
    try:
        parsed_result = json.loads(result)
    except json.JSONDecodeError:
        st.error("Failed to parse the analysis response.")
        return None
    return parsed_result

# Generate Report Functionality
def generate_report(start_date, end_date):
    # Simulate data fetching and processing
    st.info("Fetching data...")
    raw_data = fetch_data_for_date_range(start_date, end_date)
    
    if raw_data:
        st.success("Data fetched successfully!")
        
        # Process raw data
        processed_summary = process_raw_data(raw_data)
        
        # Display summary
        st.write("### Summary of the Report")
        st.write(processed_summary)
        
        # Example chart
        if "category_distribution" in processed_summary:
            enhanced_charts(
                processed_summary["category_distribution"], 
                title="Category Distribution", 
                x_label="Category", 
                y_label="Count"
            )
    else:
        st.warning("No data found for the selected date range.")

def fetch_data_for_date_range(start_date, end_date):
    sample_data = [
        {"date": "2024-12-01", "category": "Positive"},
        {"date": "2024-12-02", "category": "Negative"},
        {"date": "2024-12-03", "category": "Neutral"},
    ]
    
    # Parse the string dates in `sample_data` into `datetime.date` objects
    parsed_data = [
        {"date": datetime.strptime(item["date"], "%Y-%m-%d").date(), "category": item["category"]}
        for item in sample_data
    ]
    
    # Filter the data based on the date range
    return [item for item in parsed_data if start_date <= item["date"] <= end_date]

def process_raw_data(data):
    category_counts = {}
    for item in data:
        category = item["category"]
        category_counts[category] = category_counts.get(category, 0) + 1
    return {
        "category_distribution": list(category_counts.items()),
        "total_items": len(data),
    }

# Tabs Implementation
selected_tab = option_menu(
    menu_title=None,
    options=["Generate Reports", "Saved Reports"],
    icons=["file-plus", "archive"],
    default_index=0,
    orientation="horizontal",
)

if selected_tab == "Generate Reports":
    st.title("Generate Reports")

    # Filters
    report_type = st.selectbox("Select Report Type", ["Sentiment Analysis", "Trend Analysis", "Impact Assessment"])
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    # Generate Report Button
    if st.button("Generate Report"):
        generate_report(start_date, end_date)

    # Run Model Analysis Button
    if st.button("Run Model Analysis"):
        content_data = fetch_analyzed_data(start_date,end_date)  # Fetch content logic goes here
        if content_data:
            analysis_results = run_analysis_with_type(content_data, report_type)
            if analysis_results:
                overall_sentiment = analysis_results.get("overall_sentiment")
                potential_impact = analysis_results.get("potential_impact")
                suggestions = analysis_results.get("suggestions")
                timestamp = datetime.now().isoformat()
                
                save_report(report_type, overall_sentiment, potential_impact, suggestions, timestamp)
                st.success("Report saved successfully!")
        else:
            st.warning("No data to analyze.")

# Saved Reports Tab
elif selected_tab == "Saved Reports":
    st.title("Saved Reports")

    # Sidebar Filters
    st.sidebar.header("Filter Reports")
    report_type_filter = st.sidebar.selectbox(
        "Filter by Report Type",
        options=["All", "Sentiment Analysis", "Trend Analysis", "Impact Assessment"],
        index=0
    )
    if report_type_filter == "All":
        report_type_filter = None

    start_date_filter = st.sidebar.date_input("Start Date", value=None)
    end_date_filter = st.sidebar.date_input("End Date", value=None)

    # Fetch filtered reports dynamically
    filtered_reports = fetch_filtered_reports(
        report_type=report_type_filter,
        start_date=start_date_filter,
        end_date=end_date_filter
    )

    if filtered_reports:
        for report in filtered_reports:
            display_saved_report(report)
    else:
        st.warning("No saved reports found for the selected filters.")