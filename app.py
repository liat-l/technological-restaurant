# app.py
import streamlit as st

# הגדרות עיצוב העמוד
st.set_page_config(
    page_title="אופטימיזציית מסעדה חכמה",
    page_icon="🤖",
    layout="wide"
)

# הגדרת דפי המערכת - כולל דף דייקסטרה החדש שהוספנו
# הגדרת דפי המערכת - הגרסה המלאה והסופית הכוללת את 3 המודלים
pages = {
    "מסך ראשי": [
        st.Page("pages/home_page.py", title="🏠 דף הבית", default=True)
    ],
    "מודלים של אופטימיזציה": [
        st.Page("pages/set_cover_page.py", title="📍 פריסת רובוטים (Set Cover)"),
        st.Page("pages/dijkstra_page.py", title="⚡ ניווט בזמן אמת (Dijkstra)"),
        st.Page("pages/max_flow_page.py", title="🌊 זרימה מקסימלית (Max Flow)")
    ]
}

# הפעלת הניווט בין הדפים
pg = st.navigation(pages)
pg.run()
