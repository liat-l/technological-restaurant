# pages/set_cover_page.py
import streamlit as st

# הגנת טעינה: אם משום מה הזיכרון הריק, נטען את ברירת המחדל
if "DATA" not in st.session_state:
    import data.restaurant_data as default_data
    st.session_state["DATA"] = default_data

# שליפת הנתונים הדינמיים מהזיכרון הראשי
data_source = st.session_state["DATA"]
UNIVERSE = data_source.UNIVERSE
SETS = data_source.SETS

st.title("📍 אופטימיזציית כיסוי אזורים (Set Cover)")
st.write("מערכת המידע מפעילה אלגוריתם חמדני (Greedy Set Cover) למציאת כמות הרובוטים המינימלית הנדרשת.")

# --- כאן שאר הקוד המקורי שלך (האלגוריתם, הציורים וההדפסות) ממשיך כרגיל ---
