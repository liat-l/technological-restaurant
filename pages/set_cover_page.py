# pages/set_cover_page.py
import streamlit as st

try:
    from algorithms.set_cover import greedy_set_cover
except ModuleNotFoundError:
    from set_cover import greedy_set_cover

# 1. הגנת טעינה: אם הזיכרון ריק, נטען את ברירת המחדל
if "DATA" not in st.session_state:
    import data.restaurant_data as default_data
    st.session_state["DATA"] = default_data

# 2. שליפת הנתונים הדינמיים מהזיכרון הראשי (קובץ שהועלה או ברירת מחדל)
data_source = st.session_state["DATA"]
UNIVERSE = data_source.UNIVERSE
SETS = data_source.SETS

st.title("📍 אופטימיזציית כיסוי אזורים (Set Cover)")
st.write("מערכת המידע מפעילה אלגוריתם חמדני (Greedy Set Cover) למציאת כמות הרובוטים המינימלית הנדרשת לכסות את כל שולחנות המסעדה.")

st.divider()

# 3. הרצת אלגוריתם ה-Set Cover על הנתונים הדינמיים שנטענו בזיכרון
selected_sets = greedy_set_cover(UNIVERSE, SETS)

st.subheader("🎯 תוצאות פריסת הרובוטים האופטימלית")
st.success(f"🤖 האלגוריתם קבע כי יש צורך ב-**{len(selected_sets)} רובוטים** כדי לכסות את כל השולחנות במערכת.")

# 4. תצוגה דינמית וחסינת שגיאות של האזורים שנבחרו והשולחנות שהם מכסים
cols = st.columns(len(selected_sets))
for idx, set_name in enumerate(selected_sets):
    with cols[idx]:
        # חילוץ מפתחות השולחנות בצורה בטוחה בין אם זה מילון (dict) או קבוצה (set/list)
        raw_tables = SETS[set_name]
        if isinstance(raw_tables, dict):
            table_list = list(raw_tables.keys())
        else:
            table_list = list(raw_tables)
            
        # המרה נקייה של כל איבר למחרוזת ומיון אלפביתי (למשל T1, T2, T3...)
        sorted_tables = sorted([str(t) for t in table_list])
        
        # הצגת כרטיס מידע נקי עבור כל רובוט שנבחר
        st.info(f"""
        **{set_name}**
        * 🍽️ שולחנות מכוסים:
        `{sorted_tables}`
        """)

st.divider()

# 5. הצגת מפת התשתית (איור 2) במידה וקיימת בתיקיית הפרויקט
st.subheader("🗺️ תוכנית פריסת האזורים במסעדה")
try:
    st.image("pictures/picture2.png", caption="איור 2: חלוקת המסעדה לאזורי שירות (SETS) ותחנות עבודה", use_container_width=True)
except Exception:
    st.caption("ℹ️ מפת המסעדה (picture2.png) לא נמצאה בתיקיית pictures, אך האלגוריתם חושב והציג את הנתונים הדינמיים בהצלחה.")
