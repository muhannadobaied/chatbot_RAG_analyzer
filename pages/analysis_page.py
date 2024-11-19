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

# Connect to the database
def get_connection():
    return sqlite3.connect("reputation_management.db")

# Fetch sentiment data over time
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
    
    # Debug print
    st.write("Sentiment Data Sample:")
    st.write(data.head())
    
    return data

# # Fetch reasons for sentiments
# def fetch_sentiment_reasons():
#     conn = get_connection()
#     query = """
#     SELECT md.timestamp, s.reasons
#     FROM monitoring_data md
#     JOIN sentiment s ON md.id = s.monitoring_data_id
#     WHERE md.validated = 1
#     """
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM sentiment")
#     data = cursor.fetchall()
#     print("Q", data)
#     data = pd.read_sql(query, conn, parse_dates=['timestamp'])
#     conn.close()
    
#     # Debug print before parsing JSON
#     st.write("Raw Sentiment Reasons Data:")
#     st.write(data.head())

#     # Expand JSON reasons for display
#     data['reasons'] = data['reasons'].apply(lambda x: json.loads(x) if x and isinstance(x, str) else [])
    
#     # Debug print after parsing JSON
#     st.write("Parsed Sentiment Reasons Data:")
#     st.write(data.head())
    
#     return data

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
    
    # # Debug print before parsing JSON
    # st.write("Raw Sentiment Reasons Data:")
    # st.write(data.head())

    # Safely expand JSON reasons for display
    data['reasons'] = data['reasons'].apply(lambda x: json.loads(x) if x and isinstance(x, str) else [])

    # Debug print after parsing JSON
    st.write("Parsed Sentiment Reasons Data:")
    st.write(data.head())
    
    return data

# Fetch reasons for reputation impact
def fetch_reputation_impact_reasons():
    conn = get_connection()
    query = """
    SELECT md.timestamp, ri.reasons
    FROM monitoring_data md
    JOIN reputation_impact ri ON md.id = ri.monitoring_data_id
    WHERE md.validated = 1
    """
    data = pd.read_sql(query, conn, parse_dates=['timestamp'])
    conn.close()

    # # Debug print before parsing JSON
    # st.write("Raw Reputation Impact Reasons Data:")
    # st.write(data.head())

    # Safely expand JSON reasons for display
    data['reasons'] = data['reasons'].apply(lambda x: json.loads(x) if x and isinstance(x, str) else [])

    # Debug print after parsing JSON
    st.write("Parsed Reputation Impact Reasons Data:")
    st.write(data.head())
    
    return data

# Fetch potential impact data over time
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
    return data

# Fetch reasons for reputation impact
def fetch_reputation_impact_reasons():
    conn = get_connection()
    query = """
    SELECT md.timestamp, ri.reasons
    FROM monitoring_data md
    JOIN reputation_impact ri ON md.id = ri.monitoring_data_id
    WHERE md.validated = 1
    """
    data = pd.read_sql(query, conn, parse_dates=['timestamp'])
    conn.close()

    # # Debug print before parsing JSON
    # st.write("Raw Reputation Impact Reasons Data:")
    # st.write(data.head())

    # Safely expand JSON reasons for display
    data['reasons'] = data['reasons'].apply(lambda x: json.loads(x) if x and isinstance(x, str) else [])

    # Debug print after parsing JSON
    st.write("Parsed Reputation Impact Reasons Data:")
    st.write(data.head())
    
    return data

# Display analysis page
def display_analysis():
    st.title("Data Analysis")

    # Sentiment Over Time Analysis
    st.subheader("Sentiment Over Time")
    sentiment_data = fetch_sentiment_data()
    if not sentiment_data.empty:
        sentiment_data['timestamp'] = pd.to_datetime(sentiment_data['timestamp'])
        sentiment_data['sentiment_label'] = sentiment_data['overall_sentiment'].apply(
            lambda x: 'Unknown' if pd.isnull(x) else ('Negative' if float(x) < 0 else ('Positive' if float(x) > 0 else 'Neutral'))
        )

        # Group by timestamp and sentiment label (with more granularity)
        sentiment_count = sentiment_data.groupby([sentiment_data['timestamp'], 'sentiment_label']).size().reset_index(name='count')

        # Fill gaps in the data
        sentiment_count['timestamp'] = pd.to_datetime(sentiment_count['timestamp'])
        sentiment_count = sentiment_count.set_index('timestamp').resample('D').sum().fillna(0).reset_index()

        # Debug: Check data after resampling
        st.write("Sentiment Count after Resampling:")
        st.write(sentiment_count.head())

        # Create a scatter plot for better visualization
        fig = px.scatter(
            sentiment_count, 
            x='timestamp', 
            y='count', 
            color='sentiment_label',
            title="Sentiment Over Time"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No validated sentiment data available.")

    # Sentiment Reasons Display
    st.subheader("Sentiment Reasons")
    sentiment_reasons_data = fetch_sentiment_reasons()
    
    if not sentiment_reasons_data.empty:
        for _, row in sentiment_reasons_data.iterrows():
            st.markdown(f"**Date**: {row['timestamp'].date()}")
            st.markdown("**Reasons**:")
            
            # Check if 'reasons' column is null or empty
            if not row['reasons']:
                st.write("No reasons provided.")
            else:
                for reason in row['reasons']:
                    st.write(f"- {reason}")
    else:
        st.write("No sentiment reasons available.")

    # Potential Impact Over Time Analysis
    st.subheader("Potential Impact Over Time")
    impact_data = fetch_potential_impact_data()
    
    if not impact_data.empty:
        impact_data['timestamp'] = pd.to_datetime(impact_data['timestamp'])
        impact_data.rename(columns={'timestamp': 'Date', 'potential_impact': 'Impact Score'}, inplace=True)
    
        # Enhanced line chart with markers and a smoother curve
        fig = px.line(
            impact_data,
            x='Date',
            y='Impact Score',
            title="Potential Impact Over Time",
            labels={'Impact Score': 'Impact Score'},
            template='plotly_white',
            trendline="ols"  # Adding a trendline to illustrate the overall trend
        )
        fig.update_traces(mode='lines+markers')
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Impact Score",
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No validated potential impact data available.")
    
    # Reputation Impact Reasons Display
    st.subheader("Reputation Impact Reasons")
    reputation_impact_reasons_data = fetch_reputation_impact_reasons()

    if not reputation_impact_reasons_data.empty:
        for _, row in reputation_impact_reasons_data.iterrows():
            st.markdown(f"**Date**: {row['timestamp'].date()}")
            st.markdown("**Reputation Impact Reasons**:")

            # Check if 'reasons' column is null or empty
            if not row['reasons']:
                st.write("No reasons provided.")
            else:
                for reason in row['reasons']:
                    st.write(f"- {reason}")
    else:
        st.write("No reputation impact reasons available.")



# Run the page function
display_analysis()