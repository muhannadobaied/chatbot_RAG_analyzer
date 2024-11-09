# import streamlit as st
# from database import get_connection


# st.title("Company Profile Initialization")

# with st.form("company_profile_form"):
#     st.subheader("Step 1: Company Profile Details")
#     name = st.text_input("Company Name")
#     industry = st.text_input("Industry")
#     key_markets = st.text_area("Key Markets")
#     competitors = st.text_area("Competitors")
#     submit_company_profile = st.form_submit_button("Save Company Profile")
    
#     if submit_company_profile:
#         conn = get_connection()
#         conn.execute("INSERT INTO company_profile (name, industry, key_markets, competitors) VALUES (?, ?, ?, ?)",
#                      (name, industry, key_markets, competitors))
#         conn.commit()
#         conn.close()
#         st.success("Company profile saved successfully!")

# with st.form("focus_areas_form"):
#     st.subheader("Step 2: Define Focus Areas")
#     media_type = st.selectbox("Media Type", ["News", "Social Media", "Blogs"])
#     region = st.selectbox("Region", ["Local", "Regional", "Global"])
#     sentiment_sources = st.multiselect("Sentiment Sources", ["Positive", "Neutral", "Negative"])
#     submit_focus_areas = st.form_submit_button("Save Focus Areas")
    
#     if submit_focus_areas:
#         conn = get_connection()
#         conn.execute("INSERT INTO focus_areas (media_type, region, sentiment_sources) VALUES (?, ?, ?)",
#                      (media_type, region, ', '.join(sentiment_sources)))
#         conn.commit()
#         conn.close()
#         st.success("Focus areas saved!")

# with st.form("target_audience_form"):
#     st.subheader("Step 3: Target Audience and Influencers")
#     influencers = st.text_area("Influencers")
#     platforms = st.multiselect("Platforms for Tracking", ["Twitter", "Facebook", "Instagram", "LinkedIn"])
#     submit_target_audience = st.form_submit_button("Save Target Audience")
    
#     if submit_target_audience:
#         conn = get_connection()
#         conn.execute("INSERT INTO target_audience (influencers, platforms) VALUES (?, ?)",
#                      (influencers, ', '.join(platforms)))
#         conn.commit()
#         conn.close()
#         st.success("Target audience saved!")

import streamlit as st
import sqlite3

from database import init_db

# Database connection functions
def get_connection():
    conn = sqlite3.connect("reputation_management.db")
    return conn

def fetch_company_profile():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM company_profile")
    profile = cursor.fetchall()
    conn.close()
    return profile

def fetch_focus_areas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM focus_areas")
    areas = cursor.fetchall()
    conn.close()
    return areas

def fetch_target_audience():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM target_audience")
    audience = cursor.fetchall()
    conn.close()
    return audience

def add_or_update_company_profile(name, industry, key_markets, competitors, profile_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    if profile_id:
        cursor.execute("""
            UPDATE company_profile
            SET name = ?, industry = ?, key_markets = ?, competitors = ?
            WHERE id = ?
        """, (name, industry, key_markets, competitors, profile_id))
    else:
        cursor.execute("""
            INSERT INTO company_profile (name, industry, key_markets, competitors)
            VALUES (?, ?, ?, ?)
        """, (name, industry, key_markets, competitors))
    conn.commit()
    conn.close()

def add_or_update_focus_area(media_type, region, sentiment_sources, area_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    if area_id:
        cursor.execute("""
            UPDATE focus_areas
            SET media_type = ?, region = ?, sentiment_sources = ?
            WHERE id = ?
        """, (media_type, region, sentiment_sources, area_id))
    else:
        cursor.execute("""
            INSERT INTO focus_areas (media_type, region, sentiment_sources)
            VALUES (?, ?, ?)
        """, (media_type, region, sentiment_sources))
    conn.commit()
    conn.close()

def add_or_update_target_audience(influencers, platforms, audience_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    if audience_id:
        cursor.execute("""
            UPDATE target_audience
            SET influencers = ?, platforms = ?
            WHERE id = ?
        """, (influencers, platforms, audience_id))
    else:
        cursor.execute("""
            INSERT INTO target_audience (influencers, platforms)
            VALUES (?, ?)
        """, (influencers, platforms))
    conn.commit()
    conn.close()

# Page Layout and Logic
def show():
    st.title("Initialization and Setup")
    st.subheader("Company Profile")
    
    # Display and edit existing company profiles
    profiles = fetch_company_profile()
    for profile in profiles:
        st.write(f"Name: {profile[1]}")
        st.write(f"Industry: {profile[2]}")
        st.write(f"Key Markets: {profile[3]}")
        st.write(f"Competitors: {profile[4]}")
        
        if st.button(f"Edit Profile {profile[0]}", key=f"edit_profile_{profile[0]}"):
            with st.form(key=f"edit_profile_form_{profile[0]}"):
                name = st.text_input("Company Name", value=profile[1])
                industry = st.text_input("Industry", value=profile[2])
                key_markets = st.text_area("Key Markets", value=profile[3])
                competitors = st.text_area("Competitors", value=profile[4])
                submit = st.form_submit_button("Save Changes")
                if submit:
                    add_or_update_company_profile(name, industry, key_markets, competitors, profile[0])
                    st.success("Profile updated successfully.")
                    st.rerun()
                    
    # Form to add new company profile
    st.subheader("Add New Company Profile")
    with st.form(key="new_profile_form"):
        name = st.text_input("Company Name")
        industry = st.text_input("Industry")
        key_markets = st.text_area("Key Markets")
        competitors = st.text_area("Competitors")
        submit = st.form_submit_button("Add Profile")
        if submit:
            add_or_update_company_profile(name, industry, key_markets, competitors)
            st.success("New profile added successfully.")
            st.rerun()

    # Focus Areas Section
    st.subheader("Focus Areas")
    areas = fetch_focus_areas()
    for area in areas:
        st.write(f"Media Type: {area[1]}")
        st.write(f"Region: {area[2]}")
        st.write(f"Sentiment Sources: {area[3]}")
        
        if st.button(f"Edit Focus Area {area[0]}", key=f"edit_area_{area[0]}"):
            with st.form(key=f"edit_area_form_{area[0]}"):
                media_type = st.text_input("Media Type", value=area[1])
                region = st.text_input("Region", value=area[2])
                sentiment_sources = st.text_area("Sentiment Sources", value=area[3])
                submit = st.form_submit_button("Save Changes")
                if submit:
                    add_or_update_focus_area(media_type, region, sentiment_sources, area[0])
                    st.success("Focus area updated successfully.")
                    st.rerun()

    # Form to add new focus area
    st.subheader("Add New Focus Area")
    with st.form(key="new_area_form"):
        media_type = st.text_input("Media Type")
        region = st.text_input("Region")
        sentiment_sources = st.text_area("Sentiment Sources")
        submit = st.form_submit_button("Add Focus Area")
        if submit:
            add_or_update_focus_area(media_type, region, sentiment_sources)
            st.success("New focus area added successfully.")
            st.rerun()

    # Target Audience Section
    st.subheader("Target Audience")
    audience = fetch_target_audience()
    for aud in audience:
        st.write(f"Influencers: {aud[1]}")
        st.write(f"Platforms: {aud[2]}")
        
        if st.button(f"Edit Target Audience {aud[0]}", key=f"edit_audience_{aud[0]}"):
            with st.form(key=f"edit_audience_form_{aud[0]}"):
                influencers = st.text_area("Influencers", value=aud[1])
                platforms = st.text_area("Platforms", value=aud[2])
                submit = st.form_submit_button("Save Changes")
                if submit:
                    add_or_update_target_audience(influencers, platforms, aud[0])
                    st.success("Target audience updated successfully.")
                    st.rerun()

    # Form to add new target audience
    st.subheader("Add New Target Audience")
    with st.form(key="new_audience_form"):
        influencers = st.text_area("Influencers")
        platforms = st.text_area("Platforms")
        submit = st.form_submit_button("Add Target Audience")
        if submit:
            add_or_update_target_audience(influencers, platforms)
            st.success("New target audience added successfully.")
            st.rerun()
init_db()
show()