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

import re
import streamlit as st
import sqlite3
import json
from langchain_ollama import OllamaLLM  # Import the Ollama class
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

# Setup model
def setup_model():
    model = OllamaLLM(
        model="llama3.1:8b", 
        num_ctx=18384, 
        temperature=0, 
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]), 
        base_url="https://109.199.116.46", 
        client_kwargs={'verify': False}, 
        verbose=True
    )
    return model

# Generate model suggestions for a monitoring issue with enhanced prompt
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


# Display unresolved high-impact issues from monitoring data
def display_monitoring_high_impact_issues():
    st.title("Monitoring Alerts and High-Impact Issues")

    conn = get_connection()
    cursor = conn.cursor()
    # Fix the SQL query to join all relevant tables
    cursor.execute("""
        SELECT 
            m.id, m.source, m.content, m.priority, 
            s.overall_sentiment, r.potential_impact, a.suggestions, 
            m.status
        FROM monitoring_data m
        LEFT JOIN sentiment s ON m.id = s.monitoring_data_id
        LEFT JOIN reputation_impact r ON m.id = r.monitoring_data_id
        LEFT JOIN actionable_suggestions a ON m.id = a.monitoring_data_id
        WHERE m.status = 'Unresolved'
        AND m.validated = 1
        AND m.priority >= 1  -- High-priority issues
    """)
    issues = cursor.fetchall()
    conn.close()

    if issues:
        for issue in issues:
            issue_id, source, content, priority, sentiment, potential_impact, actionable_suggestions, status = issue
            st.subheader(f"Issue from {source}")
            st.write(f"**Priority Level:** {priority}")
            st.write(f"**Status:** {status}")
            st.write(f"**Sentiment:** {sentiment}")
            st.write(f"**Potential Impact:** {potential_impact}")
            st.write(f"**Actionable Suggestions:** {json.loads(actionable_suggestions)}")
            st.write(f"**Content:** {content[:100]}...")  # Display a preview of the content

            with st.expander("View Full Issue Details"):
                st.write(f"Source: {source}")
                st.write(f"Sentiment: {sentiment}")
                st.write(f"Priority Level: {priority}")
                st.write(f"Potential Impact: {potential_impact}")
                st.write(f"Actionable Suggestions: {json.loads(actionable_suggestions)}")
                st.write(f"Content: {content}")

                # Button to generate model suggestions
                if st.button("Use Model to Suggest Solutions and Create Statements", key=f"monitor_suggest_{issue_id}"):
                    with st.spinner("Generating suggestions and statements..."):
                        returned_solutions  = generate_monitoring_model_suggestions(
                            source, sentiment, priority, content, potential_impact, json.loads(actionable_suggestions)
                        )
                        
                        # Display official statement
                        st.write("الحلول المقترحة ###")
                        st.write(returned_solutions)

                # Text area for manual or user-provided solution
                st.write("Provide a suggested solution or steps taken:")
                solution = st.text_area("Solution", key=f"monitor_solution_{issue_id}")

                # Button to mark issue as resolved
                if st.button("Mark as Resolved", key=f"monitor_resolve_{issue_id}"):
                    mark_monitoring_issue_as_resolved(issue_id)
                    st.success("Issue marked as resolved.")
                    st.rerun()  # Refresh the page to show updated status
    else:
        st.write("No high-impact issues to display.")

# Run the page function
display_monitoring_high_impact_issues()