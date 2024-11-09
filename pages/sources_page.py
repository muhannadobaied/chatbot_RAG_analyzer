import streamlit as st
import sqlite3

def get_connection():
    conn = sqlite3.connect("reputation_management.db")
    return conn

def add_source(link, source_type, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sources (link, source_type, description) VALUES (?, ?, ?)",
                   (link, source_type, description))
    conn.commit()
    conn.close()

def get_sources():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sources")
    sources = cursor.fetchall()
    conn.close()
    return sources

def show():
    st.title("Sources Management")

    # Add new source
    with st.form("add_source"):
        st.write("Add New Source")
        link = st.text_input("Link")
        source_type = st.selectbox("Source Type", ["competitor", "influencer"])
        description = st.text_input("Description")
        if st.form_submit_button("Add Source"):
            add_source(link, source_type, description)
            st.success("Source added!")
    
    # View sources
    st.write("Current Sources")
    sources = get_sources()
    for source in sources:
        st.write(f"Link: {source[1]}, Type: {source[2]}, Description: {source[3]}")
