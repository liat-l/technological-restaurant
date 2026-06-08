import streamlit as st
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    direction: rtl;
}

[data-testid="stMarkdownContainer"] {
    text-align: right;
}

h1, h2, h3, h4, h5, h6, p {
    text-align: right !important;
}
</style>
""", unsafe_allow_html=True)

pages = [
    st.Page("pages/home_page.py", title="🏠 דף הבית ומבוא", default=True),
    st.Page("pages/set_cover_page.py", title="📍 Robo-Coverage (תכנון צי)"),
    st.Page("pages/dijkstra_page.py", title="⚡ Robo-Navigation (ניווט מהיר)"),
    st.Page("pages/max_flow_page.py", title="🌊 Robo-Flow (סימולטור עומסים)")
]

pg = st.navigation(pages)
pg.run()
