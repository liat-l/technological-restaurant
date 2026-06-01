# app.py
import streamlit as st

# הגדרות עיצוב העמוד
st.set_page_config(
    page_title="אופטימיזציית מסעדה חכמה",
    page_icon="🤖",
    layout="wide"
)

pages = {
    "מסך ראשי": [
        st.Page("pages/home_page.py", title="🏠 דף הבית", default=True)
    ],
    "מודלים של אופטימיזציה": [
        st.Page("pages/set_cover_page.py", title="📍 פריסת רובוטים (Set Cover)")
    ]
}


# הפעלת הניווט בין הדפים
pg = st.navigation(pages)
pg.run()
