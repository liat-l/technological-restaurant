# app.py
import streamlit as st
import types

# הגדרות עיצוב העמוד
st.set_page_config(
    page_title="אופטימיזציית מסעדה חכמה",
    page_icon="🤖",
    layout="wide"
)

# 1. טעינת נתוני ברירת המחדל למקרה שלא הועלה קובץ
import data.restaurant_data as default_data

if "DATA" not in st.session_state:
    st.session_state["DATA"] = default_data

# 2. רכיב העלאת קובץ נתונים דינמי בתפריט הצדדי
st.sidebar.header("📁 טעינת תשתית נתונים")
uploaded_file = st.sidebar.file_uploader(
    "העלי קובץ נתונים חלופי (.py):", 
    type=["py"], 
    help="ניתן להעלות קובץ במבנה של restaurant_data.py עם אזורים ומטריצות שונות"
)

# 3. אם הועלה קובץ, נטען אותו לזיכרון בזמן אמת (Dynamic Execution)
if uploaded_file is not None:
    try:
        # קריאת תוכן הקובץ כמחרוזת טקסט
        file_contents = uploaded_file.getvalue().decode("utf-8")
        
        # יצירת מודול פייתון וירטואלי בזיכרון
        dynamic_module = types.ModuleType("dynamic_data")
        exec(file_contents, dynamic_module.__dict__)
        
        # בדיקה שהקובץ מכיל את המשתנים ההכרחיים לאלגוריתמים
        required_vars = ["UNIVERSE", "SETS", "DIJKSTRA_DATA", "MAX_FLOW_DATA"]
        if all(hasattr(dynamic_module, var) for var in required_vars):
            st.session_state["DATA"] = dynamic_module
            st.sidebar.success("✅ קובץ הנתונים החדש נטען בהצלחה!")
        else:
            st.sidebar.error("❌ קובץ חסר משתני חובה (UNIVERSE, SETS וכדומה)")
    except Exception as e:
        st.sidebar.error(f"❌ שגיאה בקריאת הקובץ: {str(e)}")
else:
    st.sidebar.info("ℹ️ משתמש בקובץ הנתונים המקורי של המסעדה")

# הגדרת דפי המערכת
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
