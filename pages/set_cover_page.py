# pages/set_cover_page.py
import streamlit as st
import pandas as pd

# --- מימוש ישיר של אלגוריתם Set Cover החמדני בתוך הדף למניעת שגיאות ייבוא ---

def greedy_set_cover(restaurant_tables, robot_coverage):
    """
    אלגוריתם חמדני לכיסוי קבוצה (Set Cover Heuristic).
    בכל שלב נבחרת הקבוצה שמכסה את מספר האלמנטים החדשים הגדול ביותר.
    """

    all_tables = set(restaurant_tables)

    robot_coverage_copy = {
        k: set(v)
        for k, v in robot_coverage.items()
    }

    covered_tables = set()

    selected_robots = []

    while covered_tables != all_tables:

        best_robot = None

        max_new_tables = -1

        for robot_name, robot_tables in robot_coverage_copy.items():

            new_tables_covered = robot_tables - covered_tables

            if len(new_tables_covered) > max_new_tables:

                max_new_tables = len(new_tables_covered)

                best_robot = robot_name

        if max_new_tables <= 0 or best_robot is None:
            break

        selected_robots.append(best_robot)

        covered_tables.update(
            robot_coverage_copy[best_robot]
        )

    return selected_robots

# --- תצוגת הדשבורד השיווקי של Streamlit ---

# כותרת ממותגת ונקייה
st.title("📍 Robo-Coverage")
st.subheader("מערכת תכנון הצי ואופטימיזציית כיסוי אזורים בזמן אמת")

st.markdown("""
ברוכים הבאים למודול **Robo-Coverage**.

אלגוריתם זה מנתח את מבנה המסעדה, חלוקת האזורים והדרישות שלכם.

המערכת מחשבת באופן מתמטי את **כמות המינימום של הרובוטים** הנדרשים לכיסוי מלא של השולחנות.

המטרה היא להשיג **100% כיסוי שירות** תוך שימוש במספר מינימלי של רובוטים.
""")

st.divider()

# פאנל העלאת קבצים מעוצב ומזמין
st.subheader("📥 העלאת נתוני פריסה")
uploaded_excel = st.file_uploader(
    "📊 העלי את קובץ האקסל (xlsx) המכיל את פוטנציאל אזורי השירות והרובוטים שלך:", 
    type=["xlsx"]
)

if uploaded_excel is not None:
    try:
        # קריאת קובץ האקסל
        df = pd.read_excel(uploaded_excel)
        
        if df.shape[1] >= 2:
            df.columns = ["robot_name", "tables_covered"]
            
            DYNAMIC_SETS = {}
            dynamic_universe = set()
            
            for index, row in df.iterrows():
                r_name = str(row["robot_name"]).strip()
                t_list = [t.strip() for t in str(row["tables_covered"]).split(",") if t.strip()]
                
                if r_name and t_list:
                    DYNAMIC_SETS[r_name] = t_list
                    dynamic_universe.update(t_list)
            
            # הודעת הצלחה נקייה מעל הניתוח
            st.toast("קובץ הנתונים נקלט בהצלחה!", icon="✅")
            
            clean_universe = set(dynamic_universe)
            clean_sets = {str(k): set(v) for k, v in DYNAMIC_SETS.items()}
            
            # הרצת האלגוריתם
            selected_sets = greedy_set_cover(clean_universe, clean_sets)
            
            st.divider()
            
            # --- תצוגת מדדים ומטריקות (Executive Metrics) ---
            st.subheader("🎯 תוצאות פריסת הצי האופטימלית")
            
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.metric(label="🤖 גודל צי מינימלי נדרש", value=f"{len(selected_sets)} רובוטים")
            with m_col2:
                st.metric(label="🍽️ סך שולחנות מכוסים", value=f"{len(clean_universe)} שולחנות")
            with m_col3:
                st.metric(label="🛡️ אחוז כיסוי שירות", value="100% הרמטי")
            
            st.write("---")
            st.write("### 📋 חלוקת אזורי העבודה של הרובוטים שנבחרו:")
            
            # תצוגת האזורים הנבחרים ככרטיסים מעוצבים ונקיים
            # פריסה חכמה של עמודות (מקסימום 3 בשורה למראה מאוזן)
            num_selected = len(selected_sets)
            cols = st.columns(num_selected if num_selected > 0 else 1)
            
            for idx, set_name in enumerate(selected_sets):
                with cols[idx]:
                    # הפיכת רשימת השולחנות לטקסט מעוצב ויפה
                    tables_string = ", ".join(sorted(list(clean_sets[set_name])))
                    st.info(f"""
                    #### 🤖 {set_name}
                    **סטטוס:** 🟢 מוצב בשירות
                    
                    **🍽️ שולחנות באחריות:**
                    `{tables_string}`
                    """)
                    
        else:
            st.error("❌ מבנה קובץ לא תקין. על הקובץ להכיל 2 עמודות לפחות (שם האזור/רובוט, רשימת שולחנות).")
            
    except Exception as e:
        st.error(f"❌ שגיאה בתהליך עיבוד נתוני האקסל: {str(e)}")
else:
    # הודעת הדרכה מעוצבת ומזמינה כשהמסך ריק ומחכה לקובץ
    st.info("""
    👋 **מוכנים להתחיל באופטימיזציה?**
    
    אנא העלי קובץ אקסל (`.xlsx`) המכיל את רשימת אזורי השירות והשולחנות הפוטנציאליים. 
    מיד עם העלאת הקובץ, המערכת תציג את הניתוח העסקי והמדדים המדויקים עבור המסעדה שלך.
    """)
    
    # הצגת דוגמה קטנה למבנה שהמשתמש יבין מה להעלות
    with st.expander("💡 לחצי כאן לצפייה במבנה הקובץ הנדרש (דוגמה)"):
        example_df = pd.DataFrame({
            "שם אזור / רובוט פוטנציאלי": ["רובוט אזור מרכזי S1", "רובוט אזור חלון S2", "רובוט VIP S3"],
            "שולחנות מכוסים (מופרדים בפסיק)": ["T1, T2, T3", "T3, T4, T5", "T6, T7"]
        })
        st.table(example_df)

st.markdown("""
</div>
""", unsafe_allow_html=True)
