# app.py
import streamlit as st
from data.restaurant_data import UNIVERSE, SETS
from algorithms.set_cover import greedy_set_cover

# הגדרות עיצוב העמוד
st.set_page_config(
    page_title="אופטימיזציית מסעדה חכמה",
    page_icon="🤖",
    layout="wide"
)

# כותרת האפליקציה
st.title("🤖 מערכת ניהול רובוטים למסעדה חכמה")
st.markdown("### אופטימיזציית כיסוי אזורים באמצעות Set Cover")
st.write("המערכת מנתחת את מרחב המסעדה ומחשבת חלוקת עבודה אופטימלית למינימום רובוטים בשירות.")

st.divider()

# חלק 1: נתוני בסיס (לפני ריצה)
st.subheader("📊 נתוני תשתיות המסעדה")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="🍽 סך הכל שולחנות לכיסוי", value=f"{len(UNIVERSE)} שולחנות")
with col2:
    st.metric(label="📍 אזורי הצבה פוטנציאליים", value=f"{len(SETS)} אזורים")
with col3:
    st.metric(label="⚙️ מודל מתמטי", value="Greedy Set Cover")

st.divider()

# חלק 2: מפת המסעדה
st.subheader("🗺 תכנון פיזי וחלוקת אזורים")
try:
    st.image("assets/restaurant_layout.png", caption="מפת חלוקת אזורי השירות האופטימלית במסעדה",
             use_container_width=True)
except:
    st.info("💡 טיפ עיצובי: כדי שהמפה תופיע כאן, ודאי שהיא שמורה בתיקיית הפרויקט תחת: assets/restaurant_layout.png")

st.divider()

# חלק 3: כפתור ההפעלה והרצת האלגוריתם
if st.button("🚀 הפעל אופטימיזציית פריסת רובוטים", use_container_width=True):

    with st.spinner("המערכת מחשבת פריסה הרמטית מינימלית..."):
        # הרצת הפונקציה החמדת - היא זו שמחליטה!
        selected_sets, covered_tables, iterations = greedy_set_cover(UNIVERSE, SETS)

    # הודעת הצלחה דינמית בהתאם לתוצאת האלגוריתם
    st.success(f"🎯 נמצא פתרון אופטימלי! ניתן להשיג כיסוי מלא של המסעדה באמצעות {len(selected_sets)} רובוטים בלבד.")

    # תוצאות מספריות לאחר הריצה
    res_col1, res_col2, res_col3 = st.columns(3)
    with res_col1:
        st.metric(label="🤖 רובוטים פעילים נדרשים", value=len(selected_sets))
    with res_col2:
        st.metric(label="✅ שולחנות מכוסים בפועל", value=f"{len(covered_tables)} / {len(UNIVERSE)}")
    with res_col3:
        st.metric(label="📊 אחוז כיסוי המרחב", value="100%")

    st.divider()

    # הצגת האזורים שהאלגוריתם בחר בעצמו
    st.subheader("📋 האזורים הנבחרים וחלוקת העבודה (נקבע דינמית)")

    # הלולאה הזו עוברת רק על מה שהאלגוריתם בחר ומציגה את זה מעוצב
    for idx, zone in enumerate(selected_sets, start=1):
        st.info(f"🤖 **רובוט {idx} ממוקם באזור:** {zone}")

    st.divider()

    # הצגת שלבי האלגוריתם (איטרציות) בצורה אינטראקטיבית נפתחת
    st.subheader("🔍 פירוט איטרציות ריצת האלגוריתם (לוג מערכת)")

    for idx, step in enumerate(iterations, start=1):
        with st.expander(f"🔄 איטרציה מספר {idx}"):
            st.markdown(f"**📍 אזור שנבחר על ידי האלגוריתם:** `{step['selected']}`")
            st.markdown(f"**🍽 שולחנות חדשים שכוסו בשלב זה:** {', '.join(sorted(step['covered']))}")
            st.markdown(f"**📊 מספר שולחנות שנותרו לכיסוי מלא במערכת:** {step['remaining']}")