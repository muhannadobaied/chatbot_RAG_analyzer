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

# import streamlit as st
# import sqlite3

# # Connect to the database
# def get_connection():
#     return sqlite3.connect("reputation_management.db")

# # Retrieve influencer data
# def fetch_influencer_data():
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT influencer, sentiment, impact_score FROM influencer_data ORDER BY impact_score DESC")
#     influencers = cursor.fetchall()
#     conn.close()
#     return influencers

# # Display influencer analysis
# def display_influencer_analysis():
#     st.title("Influencer Analysis")

#     influencers = fetch_influencer_data()
#     if not influencers:
#         st.write("No influencer data available.")
#         return

#     st.write("### Influencer Impact and Sentiment Analysis")
#     for influencer in influencers:
#         name, sentiment, impact_score = influencer
#         st.subheader(f"Influencer: {name}")
#         st.write(f"**Sentiment:** {sentiment}")
#         st.write(f"**Impact Score:** {impact_score}")
#         st.write("---")

# # Run the page function
# display_influencer_analysis()


from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import streamlit as st

def influencer_and_competitor_analysis_page():
    st.title("Influencer and Competitor Analysis")
    st.write("Analyze the performance and impact of influencers and competitors for the company **ميساب**.")

    # Tabs for Influencer and Competitor Analysis
    selected_tab = option_menu(
        menu_title=None,
        options=["Influencer Analysis", "Competitor Analysis", "Combined Insights"],
        icons=["people", "briefcase", "lightbulb"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    if selected_tab == "Influencer Analysis":
        st.subheader("Influencer Analysis")

        st.write("### Top Influencers Engaging with ميساب")
        influencers_data = pd.DataFrame({
            "Influencer": ["@TechGuru", "@MediaExpert", "@SaudiVisionary", "@TrendWatcher", "@ContentCreator"],
            "Followers": [500000, 300000, 250000, 200000, 150000],
            "Engagement Rate (%)": [15, 20, 12, 18, 22],
            "Platform": ["Twitter", "Instagram", "LinkedIn", "Facebook", "YouTube"]
        })
        st.dataframe(influencers_data)

        fig_influencer = px.bar(
            influencers_data,
            x="Influencer",
            y="Engagement Rate (%)",
            color="Platform",
            title="Influencer Engagement Rate by Platform",
            text="Engagement Rate (%)",
        )
        st.plotly_chart(fig_influencer)

        st.write("### Audience Overlap with Influencers")
        audience_overlap_data = pd.DataFrame({
            "Influencer": ["@TechGuru", "@MediaExpert", "@SaudiVisionary"],
            "Audience Overlap (%)": [40, 35, 25]
        })
        fig_audience_overlap = px.pie(
            audience_overlap_data,
            names="Influencer",
            values="Audience Overlap (%)",
            title="Audience Overlap with ميساب"
        )
        st.plotly_chart(fig_audience_overlap)

    elif selected_tab == "Competitor Analysis":
        st.subheader("Competitor Analysis")

        st.write("### Key Competitors in Media and Production")
        competitors_data = pd.DataFrame({
            "Competitor": ["TopMedia", "VisionFilms", "FutureProducers", "GCC Creatives"],
            "Market Share (%)": [30, 25, 20, 15],
            "Sentiment Score": [80, 75, 65, 70],
            "Social Engagement": [5000, 4500, 3000, 3500]
        })
        st.dataframe(competitors_data)

        fig_market_share = px.bar(
            competitors_data,
            x="Competitor",
            y="Market Share (%)",
            title="Competitor Market Share",
            text="Market Share (%)",
            color="Competitor",
        )
        st.plotly_chart(fig_market_share)

        fig_sentiment_score = px.scatter(
            competitors_data,
            x="Sentiment Score",
            y="Social Engagement",
            color="Competitor",
            size="Market Share (%)",
            hover_name="Competitor",
            title="Sentiment Score vs Social Engagement"
        )
        st.plotly_chart(fig_sentiment_score)

    elif selected_tab == "Combined Insights":
        st.subheader("Combined Influencer and Competitor Insights")

        st.write("### Regional Impact of Influencers and Competitors")
        regional_data = pd.DataFrame({
            "Region": ["Riyadh", "Jeddah", "Dammam", "Other Regions"],
            "Influencer Impact": [50, 45, 40, 35],
            "Competitor Presence": [30, 25, 20, 15]
        })
        fig_regional = px.bar(
            regional_data,
            x="Region",
            y=["Influencer Impact", "Competitor Presence"],
            title="Regional Impact: Influencers vs Competitors",
            barmode="group"
        )
        st.plotly_chart(fig_regional)

        # Insights section
        st.write("### Insights and Recommendations")
        st.markdown("""
        - **Influencers**: Focus on collaborating with high-engagement influencers like @MediaExpert and @ContentCreator to amplify the brand's reach.
        - **Competitors**: TopMedia holds the largest market share; targeted strategies to capture their audience in Riyadh and Jeddah can yield significant results.
        - **Regional Strategy**: Increase influencer campaigns in regions like Dammam and other less-explored markets for broader audience engagement.
        """)

# Run the page
influencer_and_competitor_analysis_page()
