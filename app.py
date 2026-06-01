# app.py
import streamlit as st

# הגדרת עיצוב העמוד הראשי - חובה בשורה הראשונה
st.set_page_config(
    page_title="אופטימיזציית מסעדה חכמה",
    page_icon="🤖",
    layout="wide"
)

# הגדרת דפי המערכת ותפריט הניווט הצידי
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

# הצגת כותרת נקייה בתפריט הצדדי מעל הניווט
st.sidebar.header("⚙️ מערכת אופטימיזציה")
st.sidebar.info("ℹ️ ניתוח ביצועים ולוגיסטיקה בזמן אמת")

# הפעלת הניווט החלק בין הדפים
pg = st.navigation(pages)
pg.run()
