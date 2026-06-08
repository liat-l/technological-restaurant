import streamlit as st
st.markdown("""
<style>
section.main > div {
    direction: rtl;
    text-align: right;
}
</style>
""", unsafe_allow_html=True)
st.set_page_config(
    page_title="RoboServe Solutions",
    page_icon="🤖",
    layout="wide"
)

pages = [
    st.Page("pages/home_page.py", title="🏠 דף הבית ומבוא", default=True),
    st.Page("pages/set_cover_page.py", title="📍 Robo-Coverage (תכנון צי)"),
    st.Page("pages/dijkstra_page.py", title="⚡ Robo-Navigation (ניווט מהיר)"),
    st.Page("pages/max_flow_page.py", title="🌊 Robo-Flow (סימולטור עומסים)")
]

pg = st.navigation(pages)
pg.run()
