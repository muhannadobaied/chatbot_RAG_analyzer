# import streamlit as st
# from database import get_connection

# def sentiment_analysis_page():
#     st.title("Sentiment and Predictive Analysis")

#     conn = get_connection()
#     cursor = conn.execute("SELECT * FROM monitoring_data")
#     data = cursor.fetchall()
#     conn.close()

#     st.write("Sentiment Analysis of Collected Data:")
#     for entry in data:
#         st.write(f"Source: {entry[1]}, Content: {entry[2]}, Sentiment: {entry[3]}, Timestamp: {entry[4]}")
    
# sentiment_analysis_page()

import streamlit as st
# import sqlite3
# import pandas as pd
# import plotly.express as px

# # Connect to the database
# def get_connection():
#     return sqlite3.connect("reputation_management.db")

# # Fetch sentiment data over time
# def fetch_sentiment_data():
#     conn = get_connection()
#     query = """
#     SELECT timestamp, sentiment 
#     FROM monitoring_data 
#     WHERE validated = 1
#     """
#     data = pd.read_sql(query, conn, parse_dates=['timestamp'])
#     conn.close()
#     return data

# # Fetch influencer impact data
# def fetch_influencer_impact_data():
#     conn = get_connection()
#     query = """
#     SELECT influencer, impact_score 
#     FROM influencer_data
#     ORDER BY impact_score DESC
#     """
#     data = pd.read_sql(query, conn)
#     conn.close()
#     return data

# # Display analysis page
# def display_analysis():
#     st.title("Data Analysis")

#     # Sentiment Over Time Analysis
#     st.subheader("Sentiment Over Time")
#     sentiment_data = fetch_sentiment_data()
#     if not sentiment_data.empty:
#         sentiment_data['timestamp'] = pd.to_datetime(sentiment_data['timestamp'])
#         sentiment_count = sentiment_data.groupby([sentiment_data['timestamp'].dt.date, 'sentiment']).size().reset_index(name='count')

#         fig = px.line(
#             sentiment_count, 
#             x='timestamp', 
#             y='count', 
#             color='sentiment',
#             title="Sentiment Over Time"
#         )
#         st.plotly_chart(fig, use_container_width=True)
#     else:
#         st.write("No validated sentiment data available.")

#     # Influencer Impact Analysis
#     st.subheader("Top Influencers by Impact Score")
#     influencer_data = fetch_influencer_impact_data()
#     if not influencer_data.empty:
#         fig = px.bar(
#             influencer_data, 
#             x='impact_score', 
#             y='influencer', 
#             orientation='h',
#             title="Influencer Impact Scores",
#             labels={"impact_score": "Impact Score", "influencer": "Influencer"}
#         )
#         st.plotly_chart(fig, use_container_width=True)
#     else:
#         st.write("No influencer data available.")

# # Run the page function
# display_analysis()

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import json


# Database connection
def get_connection():
    return sqlite3.connect("reputation_management.db")


# Fetch sentiment data
def fetch_sentiment_data():
    conn = get_connection()
    query = """
    SELECT md.timestamp, s.overall_sentiment
    FROM monitoring_data md
    JOIN sentiment s ON md.id = s.monitoring_data_id
    WHERE md.validated = 1
    """
    data = pd.read_sql(query, conn, parse_dates=['timestamp'])
    conn.close()
    return data


# Fetch reasons for sentiments
def fetch_sentiment_reasons():
    conn = get_connection()
    query = """
    SELECT md.timestamp, s.reasons
    FROM monitoring_data md
    JOIN sentiment s ON md.id = s.monitoring_data_id
    WHERE md.validated = 1
    """
    data = pd.read_sql(query, conn, parse_dates=['timestamp'])
    conn.close()
    data['reasons'] = data['reasons'].apply(lambda x: json.loads(x) if x and isinstance(x, str) else [])
    return data


# Fetch potential impact data
def fetch_potential_impact_data():
    conn = get_connection()
    query = """
    SELECT md.timestamp, ri.potential_impact
    FROM monitoring_data md
    JOIN reputation_impact ri ON md.id = ri.monitoring_data_id
    WHERE md.validated = 1
    """
    data = pd.read_sql(query, conn, parse_dates=['timestamp'])
    conn.close()
    # Convert 'Impact Score' to numeric values, coercing errors to NaN
    data['potential_impact'] = pd.to_numeric(data['potential_impact'], errors='coerce')
    return data


# Page layout
st.title("Insights and Predictions")
st.markdown("View sentiment analysis and predictive insights.")
tabs = st.tabs(["Sentiment Analysis", "Predictive Analysis"])

# Sentiment Analysis Tab
with tabs[0]:
    st.subheader("Sentiment Analysis")
    st.markdown("View sentiment analysis of monitored data.")
    sentiment_data = fetch_sentiment_data()

    if not sentiment_data.empty:
        sentiment_data['timestamp'] = pd.to_datetime(sentiment_data['timestamp'])
        sentiment_data['sentiment_label'] = sentiment_data['overall_sentiment'].apply(
            lambda x: 'Unknown' if pd.isnull(x) else ('Negative' if float(x) < 0 else ('Positive' if float(x) > 0 else 'Neutral'))
        )

        # Sentiment distribution pie chart
        sentiment_distribution = sentiment_data['sentiment_label'].value_counts().reset_index()
        sentiment_distribution.columns = ['Sentiment', 'Count']

        fig_pie = px.pie(
            sentiment_distribution,
            names='Sentiment',
            values='Count',
            title="Overall Sentiment Distribution"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        # Sentiment trend stacked bar chart
        sentiment_count = sentiment_data.groupby([sentiment_data['timestamp'], 'sentiment_label']).size().reset_index(name='count')

        fig_bar = px.bar(
            sentiment_count,
            x='timestamp',
            y='count',
            color='sentiment_label',
            title="Sentiment Over Time",
            labels={'count': 'Sentiment Count', 'timestamp': 'Date'}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    else:
        st.write("No validated sentiment data available.")

# Predictive Analysis Tab
with tabs[1]:
    st.subheader("Predictive Analysis")
    st.markdown("View predictive insights based on analyzed data.")
    impact_data = fetch_potential_impact_data()

    if not impact_data.empty:
        impact_data['timestamp'] = pd.to_datetime(impact_data['timestamp'])
        impact_data.rename(columns={'timestamp': 'Date', 'potential_impact': 'Impact Score'}, inplace=True)

        # Heatmap for average impact over time (aggregated by month)
        impact_data['YearMonth'] = impact_data['Date'].dt.to_period('M')  # Group by Month
        impact_heatmap = impact_data.groupby('YearMonth')['Impact Score'].mean().reset_index()
        impact_heatmap['YearMonth'] = impact_heatmap['YearMonth'].astype(str)

        fig_heatmap = px.density_heatmap(
            impact_heatmap,
            x='YearMonth',
            y='Impact Score',
            title="Heatmap of Potential Impact Over Time",
            labels={'Impact Score': 'Average Impact Score', 'YearMonth': 'Month'},
            color_continuous_scale='Viridis',
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

        # Box plot to display distribution and outliers
        fig_box = px.box(
            impact_data,
            x=impact_data['Date'].dt.to_period('M').astype(str),
            y='Impact Score',
            title="Distribution of Potential Impact Scores",
            labels={'Impact Score': 'Impact Score', 'x': 'Month'},
            points="all"  # Include all data points for clarity
        )
        st.plotly_chart(fig_box, use_container_width=True)

    else:
        st.write("No validated potential impact data available.")