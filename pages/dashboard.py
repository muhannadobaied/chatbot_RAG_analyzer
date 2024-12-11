# import streamlit as st
# from streamlit_option_menu import option_menu
# import sqlite3
# import pandas as pd
# import plotly.express as px

# # Database connection
# def get_connection():
#     return sqlite3.connect("reputation_management.db")

# # Fetch data helper functions
# def fetch_data(query, params=None):
#     conn = get_connection()
#     df = pd.read_sql_query(query, conn, params=params)
#     conn.close()
#     return df

# def display_dashboard():
#     # st.set_page_config(layout="wide")

#     # Sidebar for navigation
    
#     selected = option_menu(
#         menu_title=None,
#         options=["Overview", "Reports", "Focus Areas", "Audience", "Social Media"],
#         icons=["bar-chart", "file-text", "map", "users", "globe"],
#         menu_icon="cast",
#         default_index=0,
#         orientation="horizontal",
        
#     )

#     if selected == "Overview":
#         st.title("System Overview")

#         col1, col2 = st.columns(2)

#         # Monitoring Data
#         with col1:
#             data = fetch_data("SELECT status, COUNT(*) as count FROM monitoring_data GROUP BY status")
#             fig = px.pie(data, names="status", values="count", title="Monitoring Data Status")
#             st.plotly_chart(fig)

#         # Sentiment Analysis
#         with col2:
#             data = fetch_data("SELECT overall_sentiment, COUNT(*) as count FROM sentiment GROUP BY overall_sentiment")
#             fig = px.bar(data, x="overall_sentiment", y="count", title="Sentiment Analysis", text="count")
#             st.plotly_chart(fig)

#     elif selected == "Reports":
#         st.title("Reports Overview")

#         data = fetch_data("SELECT report_type, COUNT(*) as count FROM saved_reports GROUP BY report_type")
#         fig = px.bar(data, x="report_type", y="count", title="Report Types", text="count")
#         st.plotly_chart(fig)

#         st.write("### Recent Reports")
#         reports = fetch_data("SELECT report_type, timestamp, overall_sentiment FROM saved_reports ORDER BY timestamp DESC LIMIT 5")
#         st.dataframe(reports)

#     elif selected == "Focus Areas":
#         st.title("Focus Areas")

#         data = fetch_data("SELECT media_type, COUNT(*) as count FROM focus_areas GROUP BY media_type")
#         fig = px.pie(data, names="media_type", values="count", title="Media Types Distribution")
#         st.plotly_chart(fig)

#         st.write("### Regional Sentiment")
#         regional_data = fetch_data("SELECT region, sentiment_sources FROM focus_areas")
#         st.dataframe(regional_data)

#     elif selected == "Audience":
#         st.title("Target Audience")

#         data = fetch_data("SELECT platforms, COUNT(*) as count FROM target_audience GROUP BY platforms")
#         fig = px.bar(data, x="platforms", y="count", title="Audience Platforms", text="count")
#         st.plotly_chart(fig)

#         st.write("### Influencers")
#         influencers = fetch_data("SELECT influencers FROM target_audience")
#         st.dataframe(influencers)

#     elif selected == "Social Media":
#         st.title("Social Media Overview")

#         col1, col2 = st.columns(2)

#         with col1:
#             st.write("### Static Insights")
#             st.markdown(
#                 """
#                 **Company Name**: ميساب  
#                 **Industry**: Technology  
#                 **Key Markets**: Middle East, North Africa  
#                 **Competitors**: TechCorp, Innovatech
#                 """
#             )

#         with col2:
#             st.write("### Social Media Stats")
#             fig = px.bar(
#                 pd.DataFrame({
#                     "Platform": ["Twitter", "Facebook", "Instagram"],
#                     "Engagement": [1200, 900, 750]
#                 }),
#                 x="Platform",
#                 y="Engagement",
#                 title="Engagement on Social Media",
#                 text="Engagement"
#             )
#             st.plotly_chart(fig)

# # Run the dashboard
# display_dashboard()

import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
import pandas as pd
import plotly.express as px

# Database connection
def get_connection():
    return sqlite3.connect("reputation_management.db")

# Fetch data helper functions
def fetch_data(query, params=None):
    conn = get_connection()
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def display_dashboard():
    # st.set_page_config(page_title="Reputation Management Dashboard", layout="wide", theme={"base": "light"})

    # Sidebar for navigation
    selected = option_menu(
        menu_title=None,
        options=["Overview", "Reports", "Focus Areas", "Audience", "Social Media"],
        icons=["bar-chart", "file-text", "map", "users", "globe"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    if selected == "Overview":
        st.title("System Overview")
        col1, col2 = st.columns(2)
        with col1:
            # Positive and Negative Comments
            st.write("### Positive Comments")
            st.markdown(
                """
                - "ميساب تقدم خدمات احترافية في وقت قياسي."
                - "أفضل شركة إنتاج إعلامي تعاملنا معها!"
                """
            )
        
        with col2:
            st.write("### Negative Comments")
            st.markdown(
                """
                - "التأخير في تسليم بعض المشاريع كان مزعجًا."
                - "نحتاج إلى دعم فني أكثر تفاعلًا وسرعة."
                """
            )

        # Charts for Company Reputation
        st.write("### Company Reputation Overview")

        col3, col4 = st.columns(2)

        with col3:
            data = pd.DataFrame({
                "Category": ["Positive", "Neutral", "Negative"],
                "Count": [60, 30, 10],
            })
            fig = px.pie(data, names="Category", values="Count", title="General Reputation")
            st.plotly_chart(fig)

        with col4:
            data = pd.DataFrame({
                "Category": ["Positive", "Neutral", "Negative"],
                "Count": [50, 30, 20],
            })
            fig = px.bar(data, x="Category", y="Count", title="Reputation in News Blogs", text="Count")
            st.plotly_chart(fig)

        
        data = pd.DataFrame({
            "Category": ["Positive", "Neutral", "Negative"],
            "Count": [70, 20, 10],
        })
        fig = px.funnel(data, x="Category", y="Count", title="Reputation in Social Media")
        st.plotly_chart(fig)

    elif selected == "Reports":
        st.title("Reports Overview")

        data = fetch_data("SELECT report_type, COUNT(*) as count FROM saved_reports GROUP BY report_type")
        fig = px.bar(data, x="report_type", y="count", title="Report Types", text="count")
        st.plotly_chart(fig)

        st.write("### Recent Reports")
        reports = fetch_data("SELECT report_type, timestamp, overall_sentiment FROM saved_reports ORDER BY timestamp DESC LIMIT 5")
        st.dataframe(reports)

    elif selected == "Focus Areas":
        st.title("Focus Areas")

        # Static Media Types Distribution
        media_data = pd.DataFrame({
            "Media Type": ["News Blogs", "Social Media", "Broadcast Media"],
            "Count": [40, 35, 25],
        })
        fig = px.pie(media_data, names="Media Type", values="Count", title="Media Types Distribution")
        st.plotly_chart(fig)

        st.write("### Regional Sentiment")
        regional_data = pd.DataFrame({
            "Region": ["Riyadh", "Jeddah", "Dammam", "Other Regions"],
            "Positive Sentiment": [60, 50, 40, 30],
            "Negative Sentiment": [10, 15, 20, 10],
        })
        st.bar_chart(regional_data.set_index("Region"))

    elif selected == "Audience":
        st.title("Target Audience")

        st.write("### Platforms")
        platforms_data = pd.DataFrame({
            "Platform": ["Twitter", "Facebook", "Instagram", "LinkedIn", "YouTube"],
            "User Count": [15000, 12000, 9000, 7000, 5000],
        })
        fig = px.bar(platforms_data, x="Platform", y="User Count", title="Audience Platforms", text="User Count")
        st.plotly_chart(fig)

        st.write("### Demographics")
        demographics_data = pd.DataFrame({
            "Age Group": ["18-24", "25-34", "35-44", "45+"],
            "Count": [5000, 10000, 7000, 3000],
        })
        fig = px.pie(demographics_data, names="Age Group", values="Count", title="Audience Age Demographics")
        st.plotly_chart(fig)

        st.write("### Influencers")
        st.markdown(
            """
            - **@TechGuru**: 500K followers on Twitter, known for tech reviews.
            - **@MediaExpert**: 300K followers on Instagram, focused on media trends.
            - **@SaudiVisionary**: 250K followers on LinkedIn, influencer in Saudi business circles.
            """
        )

    elif selected == "Social Media":
        st.title("Social Media Overview")

        col1, col2 = st.columns(2)

        with col1:
            st.write("### Static Insights")
            st.markdown(
                """
                **Company Name**: ميساب  
                **Industry**: Media and Production  
                **Key Markets**: Saudi Arabia, GCC  
                **Competitors**: TopMedia, VisionFilms
                """
            )

        with col2:
            st.write("### Social Media Stats")
            fig = px.bar(
                pd.DataFrame({
                    "Platform": ["Twitter", "Facebook", "Instagram"],
                    "Engagement": [1500, 1200, 900]
                }),
                x="Platform",
                y="Engagement",
                title="Engagement on Social Media",
                text="Engagement"
            )
            st.plotly_chart(fig)

# Run the dashboard
display_dashboard()
