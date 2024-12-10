# import streamlit as st
# import datetime
# from database import get_connection

# def alerts_page():
#     st.title("Emergency Response and Alerts")

#     # Display flagged topics and trends
#     st.subheader("Flagged Topics and Trends")
#     conn = get_connection()
#     cursor = conn.execute("SELECT source, content, sentiment, timestamp FROM monitoring_data WHERE sentiment = 'negative' ORDER BY timestamp DESC LIMIT 5")
#     flagged_data = cursor.fetchall()
#     conn.close()

#     if flagged_data:
#         for entry in flagged_data:
#             st.write(f"Source: {entry[0]}, Content: {entry[1][:100]}..., Sentiment: {entry[2]}, Timestamp: {entry[3]}")
#     else:
#         st.write("No flagged data at the moment.")

#     # Set up alert notifications
#     st.subheader("Automated Alerts")
#     alert_threshold = st.number_input("Set Sentiment Alert Threshold", min_value=0, max_value=100, value=50, step=1)
#     st.write("Receive alerts if negative sentiment exceeds the threshold set.")

#     if st.button("Enable Alerts"):
#         # Placeholder for enabling alert notifications
#         st.success(f"Alert system enabled! Notifications will trigger if negative sentiment exceeds {alert_threshold}%.")


# # alerts_page()
# import streamlit as st
# import sqlite3

# # Connect to the database
# def get_connection():
#     return sqlite3.connect("reputation_management.db")

# # Mark issue as resolved
# def mark_as_resolved(issue_id):
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("UPDATE influencer_data SET status = 'Resolved' WHERE id = ?", (issue_id,))
#     conn.commit()
#     conn.close()

# # Display unresolved high-impact issues
# def display_high_impact_issues():
#     st.title("Alerts and High-Impact Issues")

#     conn = get_connection()
#     cursor = conn.cursor()
#     # Select issues with high impact score and status 'Unresolved'
#     cursor.execute("""
#         SELECT id, influencer, sentiment, impact_score
#         FROM influencer_data
#         WHERE impact_score >= ? AND status = 'Unresolved'
#     """, (8,))
#     issues = cursor.fetchall()
#     conn.close()

#     if issues:
#         for issue in issues:
#             issue_id, influencer, sentiment, impact_score = issue
#             st.subheader(f"Issue by {influencer}")
#             st.write(f"**Sentiment:** {sentiment}")
#             st.write(f"**Impact Score:** {impact_score}")

#             with st.expander("View Issue Details"):
#                 st.write(f"Influencer: {influencer}")
#                 st.write(f"Sentiment: {sentiment}")
#                 st.write(f"Impact Score: {impact_score}")
#                 st.write("Provide a suggested solution or steps taken:")
#                 solution = st.text_area("Solution", key=f"solution_{issue_id}")
                
#                 if st.button("Mark as Resolved", key=f"resolve_{issue_id}"):
#                     mark_as_resolved(issue_id)
#                     st.success("Issue marked as resolved.")
#                     st.rerun()  # Refresh the page to show updated status
#     else:
#         st.write("No high-impact issues to display.")

# # Run the page function
# display_high_impact_issues()

# import re
# import streamlit as st
# import sqlite3
# import json
# from langchain_ollama import OllamaLLM  # Import the Ollama class
# from langchain.callbacks.manager import CallbackManager
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# # Database connection
# def get_connection():
#     return sqlite3.connect("reputation_management.db")

# # Mark an issue as resolved
# def mark_monitoring_issue_as_resolved(issue_id):
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("UPDATE monitoring_data SET status = 'Resolved' WHERE id = ?", (issue_id,))
#     conn.commit()
#     conn.close()

# # Setup model
# def setup_model():
#     model = OllamaLLM(
#         model="llama3.1:8b", 
#         num_ctx=18384, 
#         temperature=0, 
#         callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]), 
#         base_url="https://109.199.116.46", 
#         client_kwargs={'verify': False}, 
#         verbose=True
#     )
#     return model

# # Generate model suggestions for a monitoring issue with enhanced prompt
# def generate_monitoring_model_suggestions(source, sentiment, priority, content, potential_impact, actionable_suggestions):
#     model = setup_model()
#     prompt = f"""
#     An issue has been identified with the following details:
#     - Source: {source}
#     - Sentiment: {sentiment}
#     - Priority: {priority}
#     - Content: {content}
#     - Potential Impact: {potential_impact}
#     - Actionable Suggestions: {actionable_suggestions}

#     Based on this information, please perform the following:
#     1. Suggest effective strategies to mitigate the impact of this issue on the company's reputation.
#     2. Prepare an official statement for a TV broadcast or public media event to address the issue.
#     3. Draft a sample social media post that the company can use on social media platforms to communicate with the public and manage the situation.

#     Ensure that the suggestions and statements are tailored to the context of the issue and maintain a professional tone suitable for a corporate response. Provide responses in Arabic, and ensure concise, clear, and impactful communication.
#     """
#     response = model.invoke(prompt)
    
    
#     return response


# # Display unresolved high-impact issues from monitoring data
# def display_monitoring_high_impact_issues():
#     st.title("Monitoring Alerts and High-Impact Issues")

#     conn = get_connection()
#     cursor = conn.cursor()
#     # Fix the SQL query to join all relevant tables
#     cursor.execute("""
#         SELECT 
#             m.id, m.source, m.content, m.priority, 
#             s.overall_sentiment, r.potential_impact, a.suggestions, 
#             m.status
#         FROM monitoring_data m
#         LEFT JOIN sentiment s ON m.id = s.monitoring_data_id
#         LEFT JOIN reputation_impact r ON m.id = r.monitoring_data_id
#         LEFT JOIN actionable_suggestions a ON m.id = a.monitoring_data_id
#         WHERE m.status = 'Unresolved'
#         AND m.validated = 1
#         AND m.priority >= 1  -- High-priority issues
#     """)
#     issues = cursor.fetchall()
#     conn.close()

#     if issues:
#         for issue in issues:
#             issue_id, source, content, priority, sentiment, potential_impact, actionable_suggestions, status = issue
#             st.subheader(f"Issue from {source}")
#             st.write(f"**Priority Level:** {priority}")
#             st.write(f"**Status:** {status}")
#             st.write(f"**Sentiment:** {sentiment}")
#             st.write(f"**Potential Impact:** {potential_impact}")
#             st.write(f"**Actionable Suggestions:** {json.loads(actionable_suggestions)}")
#             st.write(f"**Content:** {content[:100]}...")  # Display a preview of the content

#             with st.expander("View Full Issue Details"):
#                 st.write(f"Source: {source}")
#                 st.write(f"Sentiment: {sentiment}")
#                 st.write(f"Priority Level: {priority}")
#                 st.write(f"Potential Impact: {potential_impact}")
#                 st.write(f"Actionable Suggestions: {json.loads(actionable_suggestions)}")
#                 st.write(f"Content: {content}")

#                 # Button to generate model suggestions
#                 if st.button("Use Model to Suggest Solutions and Create Statements", key=f"monitor_suggest_{issue_id}"):
#                     with st.spinner("Generating suggestions and statements..."):
#                         returned_solutions  = generate_monitoring_model_suggestions(
#                             source, sentiment, priority, content, potential_impact, json.loads(actionable_suggestions)
#                         )
                        
#                         # Display official statement
#                         st.write("الحلول المقترحة ###")
#                         st.write(returned_solutions)

#                 # Text area for manual or user-provided solution
#                 st.write("Provide a suggested solution or steps taken:")
#                 solution = st.text_area("Solution", key=f"monitor_solution_{issue_id}")

#                 # Button to mark issue as resolved
#                 if st.button("Mark as Resolved", key=f"monitor_resolve_{issue_id}"):
#                     mark_monitoring_issue_as_resolved(issue_id)
#                     st.success("Issue marked as resolved.")
#                     st.rerun()  # Refresh the page to show updated status
#     else:
#         st.write("No high-impact issues to display.")

# # Run the page function
# display_monitoring_high_impact_issues()

import streamlit as st
import sqlite3
import json
import pandas as pd
import plotly.express as px
from langchain_ollama import OllamaLLM
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


# Database connection
def get_connection():
    return sqlite3.connect("reputation_management.db")


# Mark an issue as resolved
def mark_monitoring_issue_as_resolved(issue_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE monitoring_data SET status = 'Resolved' WHERE id = ?", (issue_id,))
    conn.commit()
    conn.close()


# Save selected solution to the database
def save_selected_solution(issue_id, solution):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO solutions_tracking (issue_id, selected_solution, evaluation) VALUES (?, ?, ?)",
        (issue_id, solution, None),
    )
    conn.commit()
    conn.close()


# Update solution evaluation
def evaluate_solution(issue_id, evaluation):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE solutions_tracking SET evaluation = ? WHERE issue_id = ?",
        (evaluation, issue_id),
    )
    conn.commit()
    conn.close()


# Setup the Ollama model
def setup_model():
    model = OllamaLLM(
        model="llama3.1:8b",
        num_ctx=18384,
        temperature=0,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        base_url="https://109.199.116.46",
        client_kwargs={'verify': False},
        verbose=True,
    )
    return model


# Generate model suggestions for a monitoring issue
def generate_monitoring_model_suggestions(source, sentiment, priority, content, potential_impact, actionable_suggestions):
    model = setup_model()
    prompt = f"""
    An issue has been identified with the following details:
    - Source: {source}
    - Sentiment: {sentiment}
    - Priority: {priority}
    - Content: {content}
    - Potential Impact: {potential_impact}
    - Actionable Suggestions: {actionable_suggestions}

    Based on this information, please perform the following:
    1. Suggest effective strategies to mitigate the impact of this issue on the company's reputation.
    2. Prepare an official statement for a TV broadcast or public media event to address the issue.
    3. Draft a sample social media post that the company can use on social media platforms to communicate with the public and manage the situation.

    Ensure that the suggestions and statements are tailored to the context of the issue and maintain a professional tone suitable for a corporate response. Provide responses in Arabic, and ensure concise, clear, and impactful communication.
    """
    response = model.invoke(prompt)
    return response


# # Fetch and filter issues
# def fetch_issues(status, source_filter=None, priority_filter=None, sentiment_filter=None, page=1, page_size=5):
#     conn = get_connection()
#     cursor = conn.cursor()

#     base_query = """
#         SELECT 
#             m.id, m.source, m.content, m.priority, 
#             s.overall_sentiment, r.potential_impact, a.suggestions, 
#             m.status
#         FROM monitoring_data m
#         LEFT JOIN sentiment s ON m.id = s.monitoring_data_id
#         LEFT JOIN reputation_impact r ON m.id = r.monitoring_data_id
#         LEFT JOIN actionable_suggestions a ON m.id = a.monitoring_data_id
#         WHERE m.status = ?
#     """

#     filters = []
#     params = [status]

#     if source_filter:
#         filters.append("m.source LIKE ?")
#         params.append(f"%{source_filter}%")
#     if priority_filter:
#         filters.append("m.priority = ?")
#         params.append(priority_filter)
#     if sentiment_filter:
#         filters.append("s.overall_sentiment = ?")
#         params.append(sentiment_filter)

#     if filters:
#         base_query += " AND " + " AND ".join(filters)

#     base_query += " LIMIT ? OFFSET ?"
#     params.extend([page_size, (page - 1) * page_size])

#     cursor.execute(base_query, tuple(params))
#     issues = cursor.fetchall()
#     conn.close()

#     return issues

# Fetch and filter issues with updated mappings
def fetch_issues(status, source_filter=None, priority_filter=None, sentiment_filter=None, page=1, page_size=5):
    conn = get_connection()
    cursor = conn.cursor()

    base_query = """
        SELECT 
            m.id, m.source, m.content, m.priority, 
            s.overall_sentiment, r.potential_impact, a.suggestions, 
            m.status
        FROM monitoring_data m
        LEFT JOIN sentiment s ON m.id = s.monitoring_data_id
        LEFT JOIN reputation_impact r ON m.id = r.monitoring_data_id
        LEFT JOIN actionable_suggestions a ON m.id = a.monitoring_data_id
        WHERE m.status = ?
    """

    filters = []
    params = [status]

    # Add filters
    if source_filter:
        filters.append("m.source LIKE ?")
        params.append(f"%{source_filter}%")
    if priority_filter:
        # Map human-readable priority to DB values
        priority_map = {"High": 1, "Medium": 2, "Low": 3}
        filters.append("m.priority = ?")
        params.append(priority_map[priority_filter])
    if sentiment_filter:
        # Map human-readable sentiment to DB query
        if sentiment_filter == "Positive":
            filters.append("s.overall_sentiment > 0")
        elif sentiment_filter == "Neutral":
            filters.append("s.overall_sentiment = 0")
        elif sentiment_filter == "Negative":
            filters.append("s.overall_sentiment < 0")

    if filters:
        base_query += " AND " + " AND ".join(filters)

    base_query += " LIMIT ? OFFSET ?"
    params.extend([page_size, (page - 1) * page_size])

    cursor.execute(base_query, tuple(params))
    issues = cursor.fetchall()
    conn.close()

    return issues


# Get total issue count for pagination
# def get_total_issue_count(status, source_filter, priority_filter, sentiment_filter):
#     connection = sqlite3.connect("reputation_management.db")
#     cursor = connection.cursor()

#     base_query = """
#         SELECT COUNT(*)
#         FROM monitoring_data m
#         LEFT JOIN sentiment s ON m.id = s.monitoring_data_id
#         WHERE m.status = ?
#     """
#     params = [status]

#     # Add filters dynamically
#     if source_filter:
#         base_query += " AND m.source LIKE ?"
#         params.append(f"%{source_filter}%")
#     if priority_filter:
#         base_query += " AND m.priority = ?"
#         params.append(priority_filter)
#     if sentiment_filter:
#         base_query += " AND s.overall_sentiment = ?"
#         params.append(sentiment_filter)

#     cursor.execute(base_query, tuple(params))
#     total_count = cursor.fetchone()[0]

#     connection.close()
#     return total_count

# Get total issue count with updated mappings
def get_total_issue_count(status, source_filter, priority_filter, sentiment_filter):
    connection = get_connection()
    cursor = connection.cursor()

    base_query = """
        SELECT COUNT(*)
        FROM monitoring_data m
        LEFT JOIN sentiment s ON m.id = s.monitoring_data_id
        WHERE m.status = ?
    """
    params = [status]

    # Add filters dynamically
    if source_filter:
        base_query += " AND m.source LIKE ?"
        params.append(f"%{source_filter}%")
    if priority_filter:
        priority_map = {"High": 1, "Medium": 2, "Low": 3}
        base_query += " AND m.priority = ?"
        params.append(priority_map[priority_filter])
    if sentiment_filter:
        if sentiment_filter == "Positive":
            base_query += " AND s.overall_sentiment > 0"
        elif sentiment_filter == "Neutral":
            base_query += " AND s.overall_sentiment = 0"
        elif sentiment_filter == "Negative":
            base_query += " AND s.overall_sentiment < 0"

    cursor.execute(base_query, tuple(params))
    total_count = cursor.fetchone()[0]

    connection.close()
    return total_count

# def display_issues(status):
#     # Filters Section
#     st.write("### Filters")
#     with st.form(key=f"filter_form_{status}"):
#         cols = st.columns(3)  # Create three columns for compact styling
#         with cols[0]:
#             source_filter = st.text_input("Source Filter", key=f"source_filter_{status}")
#         with cols[1]:
#             priority_filter = st.selectbox(
#                 "Priority Filter", ["", "High", "Medium", "Low"], key=f"priority_filter_{status}"
#             )
#         with cols[2]:
#             sentiment_filter = st.selectbox(
#                 "Sentiment Filter", ["", "Positive", "Neutral", "Negative"], key=f"sentiment_filter_{status}"
#             )
#         submitted = st.form_submit_button("Apply Filters")

#     page = st.number_input("Page", min_value=1, step=1, value=1, key=f"page_{status}")
#     page_size = 5

#     # Fetch issues based on filters and pagination
#     total_issues = get_total_issue_count(status, source_filter, priority_filter, sentiment_filter)
#     issues = fetch_issues(status, source_filter, priority_filter, sentiment_filter, page, page_size)

#     # Display Issues in Cards
#     for issue in issues:
#         issue_id, source, content, priority, sentiment, potential_impact, actionable_suggestions, issue_status = issue

#         # Display issue in a card
#         with st.container():
#             st.markdown(
#                 f"""
#                 <div style='border: 1px solid #ccc; padding: 15px; margin-bottom: 15px; border-radius: 8px;'>
#                     <h4>Issue from {source}</h4>
#                     <p><strong>Priority:</strong> {priority}</p>
#                     <p><strong>Sentiment:</strong> {sentiment}</p>
#                     <p><strong>Impact:</strong> {potential_impact}</p>
#                     <p><strong>Status:</strong> {issue_status}</p>
#                     <p><strong>Content:</strong> {content[:100]}...</p>
#                 </div>
#                 """,
#                 unsafe_allow_html=True,
#             )

#             with st.expander("View Details"):
#                 st.write(f"Source: {source}")
#                 st.write(f"Priority Level: {priority}")
#                 st.write(f"Potential Impact: {potential_impact}")
#                 st.write(f"Content: {content}")

#                 # Show actionable suggestions
#                 if actionable_suggestions:
#                     try:
#                         suggestions = json.loads(actionable_suggestions)
#                         st.write(f"**Actionable Suggestions:** {suggestions}")
#                     except json.JSONDecodeError:
#                         st.write("**Actionable Suggestions:** Invalid format.")
#                 else:
#                     st.write("**Actionable Suggestions:** None available.")

#                 # AI-Powered Solution Button
#                 if st.button(f"Get AI Solution for Issue #{issue_id}", key=f"ai_solution_{issue_id}"):
#                     solution = generate_monitoring_model_suggestions(content)  # Call your Ollama model
#                     st.write(f"**Suggested Solution:** {solution}")

#             # Mark as resolved button
#             if st.button("Mark as Resolved", key=f"resolve_{issue_id}"):
#                 mark_monitoring_issue_as_resolved(issue_id)
#                 st.success("Issue marked as resolved.")
#                 st.experimental_rerun()

#     # Pagination
#     total_pages = (total_issues - 1) // page_size + 1
#     st.write(f"Page {page} of {total_pages}")

# Display issues with human-readable mappings
def display_issues(status):
    st.write("### Filters")
    with st.form(key=f"filter_form_{status}"):
        cols = st.columns(3)
        with cols[0]:
            source_filter = st.text_input("Source Filter", key=f"source_filter_{status}")
        with cols[1]:
            priority_filter = st.selectbox(
                "Priority Filter", ["", "High", "Medium", "Low"], key=f"priority_filter_{status}"
            )
        with cols[2]:
            sentiment_filter = st.selectbox(
                "Sentiment Filter", ["", "Positive", "Neutral", "Negative"], key=f"sentiment_filter_{status}"
            )
        submitted = st.form_submit_button("Apply Filters")

    page = st.number_input("Page", min_value=1, step=1, value=1, key=f"page_{status}")
    page_size = 5

    # Fetch issues
    total_issues = get_total_issue_count(status, source_filter, priority_filter, sentiment_filter)
    issues = fetch_issues(status, source_filter, priority_filter, sentiment_filter, page, page_size)

    # Display issues
    for issue in issues:
        issue_id, source, content, priority, sentiment, potential_impact, actionable_suggestions, issue_status = issue

        # Convert priority to human-readable
        priority_map = {1: "High", 2: "Medium", 3: "Low"}
        priority_text = priority_map.get(priority, "Unknown")

        # Convert sentiment to human-readable
        if sentiment is not None:
            sentiment_text = (
                "Positive" if float(sentiment) > 0 else "Negative" if float(sentiment) < 0 else "Neutral"
            )
        else:
            sentiment_text = "Unknown"

        with st.container():
            st.markdown(
                f"""
                <div style='border: 1px solid #ccc; padding: 15px; margin-bottom: 15px; border-radius: 8px;'>
                    <h4>Issue from {source}</h4>
                    <p><strong>Priority:</strong> {priority}</p>
                    <p><strong>Sentiment:</strong> {sentiment}</p>
                    <p><strong>Impact:</strong> {potential_impact}</p>
                    <p><strong>Status:</strong> {issue_status}</p>
                    <p><strong>Content:</strong> {content[:100]}...</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.expander("View Details"):
                st.write(f"Source: {source}")
                st.write(f"Priority Level: {priority}")
                st.write(f"Potential Impact: {potential_impact}")
                st.write(f"Content: {content}")

                # Show actionable suggestions
                if actionable_suggestions:
                    try:
                        suggestions = json.loads(actionable_suggestions)
                        st.write(f"**Actionable Suggestions:** {suggestions}")
                    except json.JSONDecodeError:
                        st.write("**Actionable Suggestions:** Invalid format.")
                else:
                    st.write("**Actionable Suggestions:** None available.")

                # AI-Powered Solution Button
                if st.button(f"Get AI Solution for Issue #{issue_id}", key=f"ai_solution_{issue_id}"):
                    solution = generate_monitoring_model_suggestions(source, sentiment, priority, content, potential_impact, suggestions)  # Call your Ollama model
                    st.write(f"**Suggested Solution:** {solution}")

            # Mark as resolved button
            if st.button("Mark as Resolved", key=f"resolve_{issue_id}"):
                mark_monitoring_issue_as_resolved(issue_id)
                st.success("Issue marked as resolved.")
                st.experimental_rerun()

    # Pagination
    total_pages = (total_issues - 1) // page_size + 1
    st.write(f"Page {page} of {total_pages}")


# Display insights with graphs
def display_insights():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT m.source, m.priority, s.overall_sentiment, m.status 
        FROM monitoring_data m
        LEFT JOIN sentiment s ON m.id = s.monitoring_data_id
    """, conn)

    if not df.empty:
        st.write("### Insights")

        fig1 = px.bar(df.groupby("priority").size().reset_index(name="count"), x="priority", y="count",
                      title="Issues by Priority", color="priority")
        st.plotly_chart(fig1)

        fig2 = px.pie(df.groupby("status").size().reset_index(name="count"), names="status", values="count",
                      title="Resolved vs Unresolved Issues")
        st.plotly_chart(fig2)


# Main Application
st.title("Reputation Risk Management")

tab1, tab2, tab3 = st.tabs(["Unresolved Issues", "Resolved Issues", "Insights"])

with tab1:
    st.header("Unresolved Issues")
    display_issues("Unresolved")

with tab2:
    st.header("Resolved Issues")
    display_issues("Resolved")

with tab3:
    st.header("Insights")
    display_insights()

