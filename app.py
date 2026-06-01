# app.py
import streamlit as st

# הגדרת עיצוב העמוד הראשי
st.set_page_config(
    page_title="RoboServe Solutions",
    page_icon="🤖",
    layout="wide"
)

# הגדרת רשימת דפים שטוחה וישרה (בלי קטגוריות וכותרות מפרידות)
pages = [
    st.Page("pages/home_page.py", title="🏠 דף הבית ומבוא", default=True),
    st.Page("pages/set_cover_page.py", title="📍 Robo-Coverage (תכנון צי)"),
    st.Page("pages/dijkstra_page.py", title="⚡ Robo-Navigation (ניווט מהיר)"),
    st.Page("pages/max_flow_page.py", title="🌊 Robo-Flow (סימולטור עומסים)")
]

# הפעלת מערכת הניווט החלקה
pg = st.navigation(pages)
pg.run()
