import streamlit as st

from st_pages import add_page_title, get_nav_from_toml
st.set_page_config(layout="wide")
st.markdown("""
<style>
body, html {
    direction: RTL;
    unicode-bidi: bidi-override;
    text-align: right;
}

</style>
""", unsafe_allow_html=True)
sections = st.sidebar.toggle("Sections", value=True, key="use_sections")

nav = get_nav_from_toml(
    ".streamlit/pages_sections.toml" if sections else ".streamlit/pages.toml"
)

# st.logo("logo.jpg")

pg = st.navigation(nav)

add_page_title(pg)

pg.run()