# import sqlite3

# def get_connection():
#     conn = sqlite3.connect("reputation_management.db")
#     return conn

# def init_db():
#     conn = get_connection()
#     cursor = conn.cursor()
    
#     # Define updated tables
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS company_profile (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT,
#         industry TEXT,
#         key_markets TEXT,
#         competitors TEXT
#     )
#     """)
    
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS focus_areas (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         media_type TEXT,
#         region TEXT,
#         sentiment_sources TEXT
#     )
#     """)
    
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS target_audience (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         influencers TEXT,
#         platforms TEXT
#     )
#     """)
    
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS monitoring_data (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         source TEXT,
#         content TEXT,
#         sentiment TEXT,
#         timestamp TEXT
#     )
#     """)
    
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS selected_data (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         source TEXT,
#         content TEXT,
#         sentiment TEXT,
#         timestamp TEXT
#     )
#     """)
    
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS influencer_data (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         influencer TEXT,
#         sentiment TEXT,
#         impact_score INTEGER,
#         status TEXT DEFAULT 'Unresolved'
#     )
#     """)
    
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS sources (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         link TEXT,
#         source_type TEXT,  -- e.g., 'competitor' or 'influencer'
#         description TEXT
#     )
#     """)
    
#     conn.commit()
#     conn.close()

# # Initialize the database
# init_db()

import sqlite3

def get_connection():
    conn = sqlite3.connect("reputation_management.db")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Define updated tables for the system
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS company_profile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        industry TEXT,
        key_markets TEXT,
        competitors TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS focus_areas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        media_type TEXT,
        region TEXT,
        sentiment_sources TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS target_audience (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        influencers TEXT,
        platforms TEXT
    )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS monitoring_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            content TEXT,
            validated INTEGER DEFAULT 0,
            timestamp TEXT,
            query TEXT,
            status TEXT DEFAULT 'Unresolved',
            priority INTEGER
        )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sentiment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        monitoring_data_id INTEGER,
        overall_sentiment TEXT,
        reasons TEXT,
        FOREIGN KEY(monitoring_data_id) REFERENCES monitoring_data(id)

    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reputation_impact (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        monitoring_data_id INTEGER,
        potential_impact TEXT,
        reasons TEXT,
        FOREIGN KEY(monitoring_data_id) REFERENCES monitoring_data(id)

    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS actionable_suggestions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        monitoring_data_id INTEGER,
        suggestions TEXT,
        rationale TEXT,
        FOREIGN KEY(monitoring_data_id) REFERENCES monitoring_data(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS selected_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        content TEXT,
        sentiment TEXT,
        timestamp TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS influencer_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        influencer TEXT,
        sentiment TEXT,
        impact_score INTEGER,
        status TEXT DEFAULT 'Unresolved'  -- Tracks if issue is resolved or not
    )
    """)
    
    # New table for storing sources (competitors and influencers)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        link TEXT,
        source_type TEXT,  -- 'competitor' or 'influencer'
        description TEXT
    )
    """)
    
    conn.commit()
    conn.close()

# Initialize the database
init_db()
