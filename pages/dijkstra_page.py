# pages/dijkstra_page.py
import streamlit as st

try:
    from algorithms.dijkstra import run_dijkstra
except ModuleNotFoundError:
    from dijkstra import run_dijkstra

# שליפת הנתונים הדינמיים מהזיכרון
data_source = st.session_state["DATA"]
DIJKSTRA_DATA = data_source.DIJKSTRA_DATA
SETS = data_source.SETS

st.title("⚡ ניווט רובוטים בזמן אמת (Dijkstra)")
# ... שאר הקוד שלך נשאר בדיוק אותו הדבר ללא שינוי! ...
