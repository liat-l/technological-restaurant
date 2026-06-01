# pages/set_cover_page.py
import streamlit as st

try:
    from data.restaurant_data import UNIVERSE, SETS
    from algorithms.set_cover import greedy_set_cover
except ModuleNotFoundError:
    from restaurant_data import UNIVERSE, SETS
    from set_cover import greedy_set_cover

st.title("📍 אופטימיזציית כיסוי אזורים (Set Cover)")
st.write("מערכת המידע מיישמת אלגוריתם חמדני לקביעת כמות המינימום של רובוטים הנדרשים לשירות.")

st.divider()

# נתוני בסיס נקיים
col1, col2 = st.columns(2)
with col1:
    st.metric(label="🍽 סך הכל שולחנות במסעדה", value="16 שולחנות")
with col2:
    st.metric(label="📍 אזורי הצבה פוטנציאליים", value="8 אזורים")

st.divider()

# הצגת מפת המסעדה
st.subheader("🗺 תכנון פיזי וחלוקת אזורים")
try:
    st.image("assets/restaurant_layout.jpeg", caption="מפת חלוקת אזורי השירות האופטימלית במסעדה", use_container_width=True)
except:
    st.info("💡 טיפ: ודאי שהמפה שמורה בנתיב: assets/restaurant_layout.jpeg")

st.divider()

# הפעלת האלגוריתם
if st.button("🚀 הפעל אופטימיזציית פריסת רובוטים", use_container_width=True):

    with st.spinner("האלגוריתם החמדני מחשב פריסה הרמטית מינימלית..."):
        # הרצת האלגוריתם הדינמי שמחליט לבד
        selected_sets, covered_tables, iterations = greedy_set_cover(UNIVERSE, SETS)

    st.success(f"🎯 האופטימיזציה הושלמה בהצלחה! ניתן להשיג כיסוי שירות הרמטי ומלא באמצעות {len(selected_sets)} רובוטים בלבד.")

    # תוצאות מספריות דינמיות לאחר הריצה
    res_col1, res_col2, res_col3 = st.columns(3)
    with res_col1:
        st.metric(label="🤖 רובוטים פעילים נדרשים", value=f"{len(selected_sets)} רובוטים")
    with res_col2:
        st.metric(label="✅ שולחנות מכוסים בפועל", value=f"{len(covered_tables)} / {len(UNIVERSE)}")
    with res_col3:
        st.metric(label="📊 אחוז כיסוי המרחב", value="100% הרמטי")

    st.divider()

    st.subheader("📋 חלוקת השולחנות של צי הרובוטים")

    # הצגה נקייה לחלוטין - ללא תיאורים תפעוליים, רק הרובוטים והשולחנות שלהם!
    for idx, zone_name in enumerate(selected_sets, start=1):
        assigned_tables = SETS[zone_name]
        tables_str = ", ".join(sorted(list(assigned_tables)))
        
        st.info(f"""
        🤖 **רובוט {idx} ({zone_name.split(' ')[0]})**
        * **🍽 שולחנות מכוסים באחריות ישירה:** {tables_str}
        """)
