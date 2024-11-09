# import streamlit as st
# from database import get_connection

# def influencer_analysis_page():
#     st.title("Performance Comparison and Influencer Analysis")

#     # Competitive Analysis Dashboard
#     st.subheader("Competitive Analysis")
#     conn = get_connection()
#     competitors_data = conn.execute("SELECT name, sentiment, COUNT(*) FROM monitoring_data GROUP BY name, sentiment").fetchall()
#     conn.close()

#     # Display competitor sentiment comparison
#     competitor_dict = {}
#     for row in competitors_data:
#         company, sentiment, count = row
#         if company not in competitor_dict:
#             competitor_dict[company] = {"Positive": 0, "Neutral": 0, "Negative": 0}
#         competitor_dict[company][sentiment] += count

#     st.write("Sentiment Analysis by Competitor")
#     for company, sentiments in competitor_dict.items():
#         st.write(f"{company}: {sentiments}")

#     # Influencer Impact Console
#     st.subheader("Influencer Impact")
#     influencers_data = [
#         ("Influencer A", "Positive", "Influential statement about company"),
#         ("Influencer B", "Negative", "Critique impacting public sentiment"),
#         # Sample data, replace with actual influencer data from the database
#     ]

#     for influencer in influencers_data:
#         st.write(f"{influencer[0]} - Sentiment: {influencer[1]}")
#         st.write(f"Statement: {influencer[2]}")

#     # Add charts or other visuals as needed for deeper insights
#     st.write("Further analytics coming soon.")


# influencer_analysis_page()

import streamlit as st
import sqlite3

# Connect to the database
def get_connection():
    return sqlite3.connect("reputation_management.db")

# Retrieve influencer data
def fetch_influencer_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT influencer, sentiment, impact_score FROM influencer_data ORDER BY impact_score DESC")
    influencers = cursor.fetchall()
    conn.close()
    return influencers

# Display influencer analysis
def display_influencer_analysis():
    st.title("Influencer Analysis")

    influencers = fetch_influencer_data()
    if not influencers:
        st.write("No influencer data available.")
        return

    st.write("### Influencer Impact and Sentiment Analysis")
    for influencer in influencers:
        name, sentiment, impact_score = influencer
        st.subheader(f"Influencer: {name}")
        st.write(f"**Sentiment:** {sentiment}")
        st.write(f"**Impact Score:** {impact_score}")
        st.write("---")

# Run the page function
display_influencer_analysis()

