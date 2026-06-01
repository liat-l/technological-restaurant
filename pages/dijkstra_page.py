# pages/dijkstra_page.py
import streamlit as st

try:
    from data.restaurant_data import DIJKSTRA_DATA, SETS
    from algorithms.dijkstra import run_dijkstra
except ModuleNotFoundError:
    from restaurant_data import DIJKSTRA_DATA, SETS
    from dijkstra import run_dijkstra

st.title("⚡ ניווט רובוטים בזמן אמת (Dijkstra)")
st.write("סימולציית קריאות שירות: בחרי שולחן שהמנה שלו מוכנה במטבח, והמערכת תזניק את הרובוט המתאים במסלול הקצר ביותר.")

st.divider()

# 1. יצירת רשימה מסודרת של כל השולחנות במסעדה (T1 עד T16)
all_tables = [f"T{i}" for i in range(1, 17)]

# תיבת בחירה לשולחן שהמנה שלו מוכנה
selected_table = st.selectbox(
    "🍽️ לחצי לבחירת השולחן שהמנה שלו מוכנה כעת במטבח:",
    options=all_tables
)

st.divider()

# 2. מציאת הרובוט המתאים שאחראי על השולחן שנבחר (לפי ה-Set Cover)
assigned_robot_key = None

for robot_name, details in DIJKSTRA_DATA.items():
    # חילוץ שם הקבוצה הרלוונטית מתוך שם הרובוט (למשל מתוך "רובוט 1 (מתחם רביעיות - S3)" נחלץ את "S3")
    for set_key in SETS.keys():
        if set_key.split(' ')[0] in robot_name and selected_table in SETS[set_key]:
            assigned_robot_key = robot_name
            break
    if assigned_robot_key:
        break

# 3. הרצת האלגוריתם והצגת התוצאה
if assigned_robot_key:
    st.subheader("🤖 הזנקת רובוט שירות אוטונומי")
    st.success( f"השולחן הנבחר **{selected_table}** נמצא באזור האחריות של: **{assigned_robot_key}**")
    
    # שליפת נתוני הגרף של הרובוט הנבחר
    nodes = DIJKSTRA_DATA[assigned_robot_key]["nodes"]
    matrix = DIJKSTRA_DATA[assigned_robot_key]["matrix"]
    
    # הרצת דייקסטרה בזמן אמת מהמטבח
    distances, paths = run_dijkstra(nodes, matrix, start_node="מטבח")
    
    # הצגת כרטיס משימה תפעולי נקי
    st.info(f"""
    📋 **פרטי משימת הניווט האופטימלית:**
    * 🎯 **שולחן יעד:** {selected_table}
    * 📏 **מרחק נסיעה כולל:** {distances[selected_table]} יחידות מרחק
    * 🗺️ **נתיב תנועה מחושב (Dijkstra):** {paths[selected_table]}
    """)
    
else:
    st.warning("⚠️ לא נמצא רובוט המכסה את השולחן הזה בקובץ הנתונים. ודאי שקבוצות ה-SETS מעודכנות.")
