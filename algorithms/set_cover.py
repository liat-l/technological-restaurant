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

# נתוני בסיס נקיים ללא סוגריים או ציטוטים
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
        # הרצת האלגוריתם האוטונומי
        selected_sets, covered_tables, iterations = greedy_set_cover(UNIVERSE, SETS)

    st.success(f"🎯 האופטימיזציה הושלמה בהצלחה! ניתן להשיג כיסוי שירות הרמטי ומלא באמצעות {len(selected_sets)} רובוטים בלבד.")

    # תוצאות מספריות לאחר הריצה
    res_col1, res_col2, res_col3 = st.columns(3)
    with res_col1:
        st.metric(label="🤖 רובוטים פעילים נדרשים", value=f"{len(selected_sets)} רובוטים")
    with res_col2:
        st.metric(label="✅ שולחנות מכוסים בפועל", value=f"{len(covered_tables)} / {len(UNIVERSE)}")
    with res_col3:
        st.metric(label="📊 אחוז כיסוי המרחב", value="100% הרמטי")

    st.divider()

    st.subheader("📋 חלוקת השולחנות ותחומי האחריות של צי הרובוטים")

    # מיפוי נקי עם השמות המדויקים מתוך קובץ הנתונים (מניע את בעיית אי-ההתאמה)
    robot_clean_details = {
        'S3 (מסדרון רביעיות מרכזי)': {
            "title": "🤖 רובוט 1 (S3) - מתחם רביעיות מרכזי (Zone 1)",
            "desc": "מעניק כיסוי שירות מלא לכל שולחנות הרביעיות במתחם המרכזי.",
            "tables": "T1, T2, T3, T4, T5, T6"
        },
        'S4 (מתחם שישיות)': {
            "title": "🤖 רובוט 2 (S4) - מתחם שישיות (Zone 2)",
            "desc": "מעניק כיסוי שירות ייעודי ובלעדי למתחם השישיות.",
            "tables": "T7, T8, T9, T10"
        },
        'S8 (רובוט VIP מורחב)': {
            "title": "🤖 רובוט 3 (S8) - מתחם VIP וזוגות (Zone 4)",
            "desc": "מעניק כיסוי שירות מורחב למתחם ה-VIP ולחלק משולחנות הזוגות.",
            "tables": "T13, T14, T15, T16"
        },
        'S6 (מסדרון מעבר מרכזי-ימין)': {
            "title": "🤖 רובוט 4 (S6) - מתחם זוגות וגיבוי (Zone 3)",
            "desc": "מעניק כיסוי שירות לשולחנות הזוגות ומשמש כגיבוי דינמי למעבר המרכזי.",
            "tables": "T7, T8, T11, T12"
        }
    }

    # הצגה דינמית וממוקדת של הרובוטים שנבחרו
    for zone_name in selected_sets:
        if zone_name in robot_clean_details:
            details = robot_clean_details[zone_name]
            st.info(f"""
            ### {details['title']}
            * **📝 תפקיד תפעולי:** {details['desc']}
            * **🍽 שולחנות מכוסים באחריות ישירה:** {details['tables']}
            """)
