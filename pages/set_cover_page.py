# pages/set_cover_page.py
import streamlit as st

try:
    from algorithms.set_cover import greedy_set_cover
except ModuleNotFoundError:
    from set_cover import greedy_set_cover

# שליפת הנתונים הדינמיים מהזיכרון
data_source = st.session_state["DATA"]
UNIVERSE = data_source.UNIVERSE
SETS = data_source.SETS

st.title("📍 אופטימיזציית כיסוי אזורים (Set Cover)")
# ... שאר הקוד שלך נשאר בדיוק אותו הדבר ללא שינוי! ...
