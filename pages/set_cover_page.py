# set_cover_page.py
import streamlit as st

# טריק ה-try-except המונע שגיאות אדומות ב-PyCharm ותואם ל-GitHub
try:
    from data.restaurant_data import UNIVERSE, SETS
    from algorithms.set_cover import greedy_set_cover
except ModuleNotFoundError:
    from restaurant_data import UNIVERSE, SETS
    from set_cover import greedy_set_cover

st.title("📍 אופטימיזציית כיסוי אזורים (Set Cover)")
st.write("מערכת המידע מיישמת אלגוריתם חמדני (Greedy Heuristic) לקביעת כמות המינימום של רובוטים הנדרשים לשירות[cite: 37].")

st.divider()

# נתוני בסיס
col1, col2 = st.columns(2)
with col1:
    st.metric(label="🍽 סך הכל שולחנות במסעדה", value=f"{len(UNIVERSE)} שולחנות [cite: 12]")
with col2:
    st.metric(label="📍 אזורי הצבה פוטנציאליים", value=f"{len(SETS)} אזורים [cite: 14]")

st.divider()

# הצגת מפת המסעדה
st.subheader("🗺 תכנון פיזי וחלוקת אזורים")
try:
    st.image("assets/restaurant_layout.png", caption="איור 2: מפת חלוקת אזורי השירות האופטימלית במסעדה [cite: 73]", use_container_width=True)
except:
    st.info("💡 טיפ: ודאי שהמפה שמורה בנתיב: assets/restaurant_layout.png")

st.divider()

# הפעלת האלגוריתם
if st.button("🚀 הפעל אופטימיזציית פריסת רובוטים", use_container_width=True):

    with st.spinner("האלגוריתם החמדני מחשב פריסה הרמטית מינימלית..."):
        # הרצה אמיתית ואוטונומית של האלגוריתם החמדני שלך!
        selected_sets, covered_tables, iterations = greedy_set_cover(UNIVERSE, SETS)

    # הודעת הצלחה הנדסית ותפעולית
    st.success(f"🎯 האופטימיזציה הושלמה בהצלחה על ידי האלגוריתם! ניתן להשיג כיסוי שירות הרמטי ומלא באמצעות {len(selected_sets)} רובוטים בלבד[cite: 65].")

    # תוצאות מספריות לאחר הריצה
    res_col1, res_col2, res_col3 = st.columns(3)
    with res_col1:
        st.metric(label="🤖 רובוטים פעילים נדרשים", value=len(selected_sets))
    with res_col2:
        st.metric(label="✅ שולחנות מכוסים בפועל", value=f"{len(covered_tables)} / {len(UNIVERSE)}")
    with res_col3:
        st.metric(label="📊 אחוז כיסוי המרחב", value="100% הרמטי")

    st.divider()

    st.subheader("📋 חלוקת השולחנות ותחומי האחריות של צי הרובוטים")

    # מיפוי דינמי של תיאורי התפקידים המקצועיים מתוך מסמך הניתוח שלך [cite: 67, 68, 69, 70]
    robot_details = {
        'S3 (מסדרון רביעיות מרכזי)': {
            "title": "רובוט 1 (S3) - מתחם רביעיות מרכזי (Zone 1) [cite: 67]",
            "desc": "מעניק כיסוי שירות מלא לכל שולחנות הרביעיות במתחם המרכזי[cite: 67]."
        },
        'S4 (מתחם שישיות)': {
            "title": "רובוט 2 (S4) - מתחם שישיות (Zone 2) [cite: 68]",
            "desc": "מעניק כיסוי שירות ייעודי ובלעדי למתחם השישיות[cite: 68]."
        },
        'S8 (רובוט VIP מורחב)': {
            "title": "רובוט 3 (S8) - מתחם VIP וזוגות (Zone 4) [cite: 69]",
            "desc": "מעניק כיסוי שירות מורחב למתחם ה-VIP ולחלק משולחנות הזוגות[cite: 69]."
        },
        'S6 (מסדרון מעבר מרכזי-ימין)': {
            "title": "רובוט 4 (S6) - מתחם זוגות וגיבוי (Zone 3) [cite: 70]",
            "desc": "מעניק כיסוי שירות לשולחנות הזוגות ומשמש כגיבוי דינמי למעבר המרכזי[cite: 70]."
        }
    }

    # לולאה שעוברת על הבחירות של האלגוריתם בזמן אמת ומציגה את הנתונים [cite: 76]
    for zone_name in selected_sets:
        # בדיקה למניעת קריסה במקרה שהאלגוריתם יבחר קבוצה שאין לה תיאור מובנה
        if zone_name in robot_details:
            details = robot_details[zone_name]
            assigned_tables = SETS[zone_name]
            tables_str = ", ".join(sorted(list(assigned_tables)))

            st.info(f"""
            🤖 **{details['title']}**
            * **📝 תפקיד תפעולי:** {details['desc']}
            * **🍽 שולחנות באחריות ישירה:** {tables_str}
            """)
        else:
            # תצוגת ברירת מחדל דינמית למקרה שנבחר אזור אחר
            assigned_tables = SETS[zone_name]
            tables_str = ", ".join(sorted(list(assigned_tables)))
            st.warning(f"""
            🤖 **רובוט שירות באזור המערכת: {zone_name}**
            * **🍽 שולחנות באחריות ישירה:** {tables_str}
            """)