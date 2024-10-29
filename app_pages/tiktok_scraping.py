import streamlit as st
from TikTokApi import TikTokApi
import asyncio
import os

# Replace with your actual API key (consider using environment variables)
api_key = os.environ.get("TIKTOK_API_KEY", "x5Az6QCGYjRG-eXEAQNfcdk3RJRoNLr2-bP7j7AO0uPC7F72DNDQK6TkDUwRjdpWa0GP7gXpywUZ9wgRs8_M0gKmYzAWwEwsdNexK9mS7-rSg6zqGixP_qgndxCRXAokmPXXJ8hCGTOXrpVnHdSa")  # Retrieve from environment

async def search_tiktok(query):
    try:
        if not api_key:
            raise Exception("Please set the 'TIKTOK_API_KEY' environment variable.")
        async with TikTokApi() as api:
            await api.set_user_agent("MyTikTokApp")  # Set a custom user agent
            await api.create_sessions(ms_tokens=[api_key], num_sessions=1, sleep_after=3)
            tag = api.hashtag(name=query)
            videos = []  # List to store video data
            async for video in tag.videos(count=2):  # Retrieve 2 videos by default
                video_data = video.as_dict
                videos.append({
                    "title": video_data.get('desc', 'N/A'),
                    "author": f"@{video_data['author']['uniqueId']}",
                    "url": f"https://www.tiktok.com/@{video_data['author']['uniqueId']}/video/{video_data['id']}",
                })
            return videos  # Return a list of dictionaries containing video information

    except Exception as e:
        return {"error": str(e)}  # Return an error dictionary for handling


@st.cache_data
def run_search_tiktok(search_term):
    """Wrapper function to run search_tiktok asynchronously within Streamlit"""
    loop = asyncio.new_event_loop()
    data = loop.run_until_complete(search_tiktok(search_term))
    loop.close()
    return data


st.title("TikTok Search")

search_term = st.text_input("Enter a hashtag to search:")

if search_term:
    st.write("Searching...")
    cached_data = run_search_tiktok(search_term)

    if "error" in cached_data:
        st.error(cached_data["error"])
    else:
        for video_data in cached_data:
            st.write(f"- Title: {video_data['title']}")
            st.write(f"- Author: {video_data['author']}")
            st.write(f"- Video URL: {video_data['url']}")
            st.video(video_data['url'])  # Display video using Streamlit video element