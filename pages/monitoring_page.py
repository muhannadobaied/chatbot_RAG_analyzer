# import streamlit as st
# from database import get_connection
# import datetime

# def monitoring_page():
#     st.title("Real-Time Monitoring and Data Collection")
#     search_query = st.text_input("Enter keywords for tracking")
#     date_range = st.date_input("Select date range", [])
    
#     if st.button("Start Monitoring"):
#         # Placeholder for data collection, store to monitoring_data table
#         sample_data = {
#             "source": "Twitter",
#             "content": "Sample tweet mentioning the company",
#             "sentiment": "neutral",
#             "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         }
#         conn = get_connection()
#         conn.execute("INSERT INTO monitoring_data (source, content, sentiment, timestamp) VALUES (?, ?, ?, ?)",
#                      (sample_data["source"], sample_data["content"], sample_data["sentiment"], sample_data["timestamp"]))
#         conn.commit()
#         conn.close()
#         st.success("Data collected and saved!")

# monitoring_page()



# import streamlit as st
# import datetime
# import sqlite3
# import requests
# from bs4 import BeautifulSoup
# from goose3 import Goose
# from io import BytesIO
# from docx import Document
# import urllib.parse

# from docx.oxml import OxmlElement
# from docx.oxml.ns import qn
# import docx

# # Title for the monitoring page
# st.title("Real-Time Monitoring and Data Collection")

# # Database connection
# def get_connection():
#     return sqlite3.connect("reputation_management.db")

# # Google Custom Search API function
# def google_search(query, date_filter_type=None, date_filter_value=None):
#     API_KEY = 'AIzaSyC_0LAqVIA0Z7YLbbWKSOHxY0_sMaqQAko'
#     CSE_ID = 'b13bba6a528214af0'
#     search_url = "https://www.googleapis.com/customsearch/v1"
    
#     dateRestrict = ""
#     if date_filter_type == "Days":
#         dateRestrict = f"d{date_filter_value}"
#     elif date_filter_type == "Weeks":
#         dateRestrict = f"w{date_filter_value}"
#     elif date_filter_type == "Months":
#         dateRestrict = f"m{date_filter_value}"
#     elif date_filter_type == "Years":
#         dateRestrict = f"y{date_filter_value}"
    
#     params = {
#         "key": API_KEY,
#         "cx": CSE_ID,
#         "q": f'allintitle:{query}',
#         "num": 5,
#         "dateRestrict": dateRestrict
#     }
    
#     response = requests.get(search_url, params=params)
#     return response.json() if response.status_code == 200 else None

# # Extract full content
# def extract_full_content(url):
#     try:
#         g = Goose()
#         article = g.extract(url=url)
#         return article.cleaned_text
#     except:
#         return "Could not extract content."

# # Function to clean the links
# def clean_link(link):
#     try:
#         cleaned = urllib.parse.unquote(link, encoding='utf-8')
#     except UnicodeDecodeError:
#         cleaned = urllib.parse.unquote(link, encoding='iso-8859-1')
#     return cleaned

# # Save monitoring data in the database
# def save_monitoring_data(source, content, sentiment, timestamp, query):
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute('''
#         INSERT INTO monitoring_data (source, content, sentiment, timestamp, query)
#         VALUES (?, ?, ?, ?, ?)
#     ''', (source, content, sentiment, timestamp, query))
#     conn.commit()
#     conn.close()

# # Input fields for monitoring criteria
# search_query = st.text_input("Enter keywords for tracking")
# date_filter_type = st.selectbox("Choose Time Range", ["No Filter", "Days", "Weeks", "Months", "Years"])
# date_filter_value = st.number_input("Specify the number of selected units (e.g., days, weeks)", min_value=1, value=1)
# start_monitoring = st.button("Start Monitoring")

# if start_monitoring and search_query:
#     st.write(f"Monitoring for **{search_query}**...")
#     results = google_search(search_query, date_filter_type, date_filter_value)
    
#     if results:
#         for item in results.get("items", []):
#             title = item['title']
#             link = clean_link(item['link'])
#             snippet = item['snippet']
#             full_content = extract_full_content(link)
#             timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
#             # Display monitoring result
#             st.write(f"**Title:** {title}")
#             st.write(f"**Link:** {link}")
#             st.write(f"**Snippet:** {snippet}")
#             st.write(f"**Content:** {full_content}")
#             st.write("---")
            
#             # Save monitoring data to the database
#             save_monitoring_data("Google Search", full_content, "unknown", timestamp, search_query)
        
#         st.success("Monitoring data collected and saved!")
#     else:
#         st.warning("No results found.")


# def add_hyperlink(paragraph, url, text):
#     """
#     A function that places a hyperlink within a paragraph object.
#     :param paragraph: The docx paragraph object where the link should be added.
#     :param url: The web link (string) to add.
#     :param text: The text that will display for the link.
#     :return: The modified paragraph object with a hyperlink.
#     """
#     # Create the hyperlink tag
#     part = paragraph.part
#     r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

#     # Create the w:hyperlink tag and add needed values
#     hyperlink = OxmlElement('w:hyperlink')
#     hyperlink.set(qn('r:id'), r_id)

#     # Create a w:r element and a new w:rPr element
#     new_run = OxmlElement('w:r')
#     r_pr = OxmlElement('w:rPr')

#     # Join all the parts together
#     new_run.append(r_pr)
#     new_run.text = text
#     hyperlink.append(new_run)

#     # Append the hyperlink to the paragraph
#     paragraph._element.append(hyperlink)

#     return paragraph

# # Function to create a DOCX file with monitoring data
# def create_docx_file(results):
#     doc = Document()
#     doc.add_heading("Monitoring Results", 0)
    
#     for result in results:
#         doc.add_heading(result[0], level=1)  # Add title
#         p = doc.add_paragraph("Link: ")
#         add_hyperlink(p, result[1], result[1])  # Add clickable link
#         doc.add_paragraph(f"Snippet: {result[2]}")  # Add snippet
#         doc.add_paragraph("Content:")  # Add content label
#         doc.add_paragraph(result[3])  # Add the full content
#         doc.add_page_break()
    
#     buffer = BytesIO()
#     doc.save(buffer)
#     buffer.seek(0)
#     return buffer

# # Generate downloadable DOCX file
# if start_monitoring and results:
#     docx_content = create_docx_file([(item['title'], clean_link(item['link']), item['snippet'], extract_full_content(item['link'])) for item in results.get("items", [])])
#     st.download_button(
#         label="Download Monitoring Results as DOCX",
#         data=docx_content,
#         file_name="monitoring_results.docx",
#         mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
#     )
import streamlit as st
import datetime
import sqlite3
import requests
from goose3 import Goose
from io import BytesIO
from docx import Document
import urllib.parse
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import docx

# Title for the monitoring page
st.title("Real-Time Monitoring and Data Collection")

# Database connection
def get_connection():
    return sqlite3.connect("reputation_management.db")

# Google Custom Search API function
def google_search(query, date_filter_type=None, date_filter_value=None):
    API_KEY = 'AIzaSyC_0LAqVIA0Z7YLbbWKSOHxY0_sMaqQAko'
    CSE_ID = 'b13bba6a528214af0'
    search_url = "https://www.googleapis.com/customsearch/v1"
    
    dateRestrict = ""
    if date_filter_type == "Days":
        dateRestrict = f"d{date_filter_value}"
    elif date_filter_type == "Weeks":
        dateRestrict = f"w{date_filter_value}"
    elif date_filter_type == "Months":
        dateRestrict = f"m{date_filter_value}"
    elif date_filter_type == "Years":
        dateRestrict = f"y{date_filter_value}"
    
    params = {
        "key": API_KEY,
        "cx": CSE_ID,
        "q": f'allintitle:{query}',
        "num": 5,
        "dateRestrict": dateRestrict
    }
    
    response = requests.get(search_url, params=params)
    return response.json() if response.status_code == 200 else None

# Extract full content
def extract_full_content(url):
    try:
        g = Goose()
        article = g.extract(url=url)
        return article.cleaned_text
    except:
        return "Could not extract content."

# Function to clean the links
def clean_link(link):
    try:
        cleaned = urllib.parse.unquote(link, encoding='utf-8')
    except UnicodeDecodeError:
        cleaned = urllib.parse.unquote(link, encoding='iso-8859-1')
    return cleaned

# Save monitoring data in the database
def save_monitoring_data(results, query):
    conn = get_connection()
    cursor = conn.cursor()
    for result in results:
        if not result["content"] == "" or "Could not extract content.":
            cursor.execute('''
                INSERT INTO monitoring_data (source, content, timestamp, query)
                VALUES (?, ?, ?, ?)
            ''', ("Google Search", result["content"], result["timestamp"], query))
    conn.commit()
    conn.close()

# Function to add hyperlink in DOCX
def add_hyperlink(paragraph, url, text):
    part = paragraph.part
    r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)
    new_run = OxmlElement('w:r')
    r_pr = OxmlElement('w:rPr')
    new_run.append(r_pr)
    new_run.text = text
    hyperlink.append(new_run)
    paragraph._element.append(hyperlink)
    return paragraph

# Function to create a DOCX file with monitoring data
def create_docx_file(results):
    doc = Document()
    doc.add_heading("Monitoring Results", 0)
    
    for result in results:
        doc.add_heading(result["title"], level=1)
        p = doc.add_paragraph("Link: ")
        add_hyperlink(p, result["link"], result["link"])
        doc.add_paragraph(f"Snippet: {result['snippet']}")
        doc.add_paragraph("Content:")
        doc.add_paragraph(result["content"])
        doc.add_page_break()
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# Input fields for monitoring criteria
search_query = st.text_input("Enter keywords for tracking")
date_filter_type = st.selectbox("Choose Time Range", ["No Filter", "Days", "Weeks", "Months", "Years"])
date_filter_value = st.number_input("Specify the number of selected units (e.g., days, weeks)", min_value=1, value=1)
start_monitoring = st.button("Start Monitoring")

# Fetch results if "Start Monitoring" is clicked
if start_monitoring and search_query:
    st.write(f"Monitoring for **{search_query}**...")
    results = google_search(search_query, date_filter_type, date_filter_value)
    
    if results:
        # Store results in session state
        st.session_state["results_data"] = [
            {
                "title": item['title'],
                "link": clean_link(item['link']),
                "snippet": item['snippet'],
                "content": extract_full_content(item['link']),
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            } for item in results.get("items", [])
        ]
        st.success("Results fetched successfully.")
    else:
        st.warning("No results found.")

# Display results if available
if "results_data" in st.session_state:
    for item in st.session_state["results_data"]:
        st.write(f"**Title:** {item['title']}")
        st.write(f"**Link:** {item['link']}")
        st.write(f"**Snippet:** {item['snippet']}")
        st.write(f"**Content:** {item['content']}")
        st.write("---")

# Button to save all results in the database
if st.button("Save All Results to Database"):
    if "results_data" in st.session_state:
        save_monitoring_data(st.session_state["results_data"], search_query)
        st.success("All results saved to the database.")
    else:
        st.warning("No results to save.")

# Button to create a DOCX file for all results
if st.button("Download All Results as DOCX"):
    if "results_data" in st.session_state:
        docx_content = create_docx_file(st.session_state["results_data"])
        st.download_button(
            label="Download Monitoring Results as DOCX",
            data=docx_content,
            file_name="monitoring_results.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    else:
        st.warning("No results to download.")
