# db_setup.py
import sqlite3

def create_db():
    conn = sqlite3.connect('company_reputation.db')
    c = conn.cursor()
    
    # Create the searches table if it doesn't exist, with an additional field for embeddings
    c.execute('''CREATE TABLE IF NOT EXISTS searches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_name TEXT,
                    source TEXT,
                    title TEXT,
                    link TEXT,
                    snippet TEXT,
                    full_content TEXT,
                    classification TEXT,
                    date TEXT,
                    search_group TEXT
                )''')
    conn.commit()
    conn.close()