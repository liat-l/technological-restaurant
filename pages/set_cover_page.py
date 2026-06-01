# pages/set_cover_page.py
import streamlit as st
import pandas as pd

# --- מימוש ישיר של אלגוריתם Set Cover החמדני בתוך הדף למניעת שגיאות ייבוא ---
def greedy_set_cover(universe, subsets):
    """
    אלגוריתם חמדני לכיסוי קבוצה (Set Cover Heuristic).
    בכל שלב נבחרת הקבוצה שמכסה את מספר האלמנטים החדשים הגדול ביותר.
    """
    elements = set(universe)
    subsets_copy = {k: set(v) for k, v in subsets.items()}
    covered = set()
    selected_subsets = []

    while covered != elements:
        best_subset = None
        max_new_elements = -1
        
        for subset_name, subset_elements in subsets_copy.items():
            # חישוב האיברים החדשים שהקבוצה יכולה לתרום לכיסוי
            new_elements = subset_elements - covered
            if len(new_elements) > max_new_elements:
                max_new_elements = len(new_elements)
                best_subset = subset_name
                
        # אם הגענו למצב שאי אפשר לכסות יותר איברים חדשים, נעצור כדי למנוע לולאה אינסופית
        if max_new_elements <= 0 or best_subset is None:
            break
            
        selected_subsets.append(best_subset)
        covered.update(subsets_copy[best_subset])
        
    return selected_subsets

# --- תצוגת הדשבורד של Streamlit ---

st.title("📍 אופטימיזציית כיסוי אזורים (Set Cover) דינמי")
st.write("מערכת המידע מפעילה אלגוריתם חמדני (Greedy Heuristic) על בסיס קובץ נתונים מותאם אישית לקביעת פריסת צי הרובוטים המינימלי.")

st.divider()

# רכיב להעלאת קובץ האקסל ישירות בדף
uploaded_excel = st.file_uploader("📊 העלי קובץ אקסל (xlsx) של אזורי השירות והרובוטים הפוטנציאליים:", type=["xlsx"])

if uploaded_excel is not None:
    try:
        # קריאת קובץ האקסל באמצעות pandas
        df = pd.read_excel(uploaded_excel)
        
        if df.shape[1] >= 2:
            # הגדרת שמות עמודות אחידים לעבודה בקוד
            df.columns = ["robot_name", "tables_covered"]
            
            DYNAMIC_SETS = {}
            dynamic_universe = set()
            
            # עיבוד הנתונים מהטבלה ובניית המבנים הלוגיים
            for index, row in df.iterrows():
                r_name = str(row["robot_name"]).strip()
                # פירוק השולחנות המוזנים לפי פסיק ונרמול רווחים מיותרים
                t_list = [t.strip() for t in str(row["tables_covered"]).split(",") if t.strip()]
                
                if r_name and t_list:
                    # שמירה זמנית במילון הנתונים
                    DYNAMIC_SETS[r_name] = t_list
                    dynamic_universe.update(t_list)
            
            st.success(f"✅ קובץ הנתונים נטען בהצלחה! זוהו {len(dynamic_universe)} שולחנות ייחודיים ו-{len(DYNAMIC_SETS)} אזורי הצבה פוטנציאליים[cite: 11, 13].")
            
            # המרה מוחלטת ל-set עבור האלגוריתם החמדני
            clean_universe = set(dynamic_universe)
            clean_sets = {str(k): set(v) for k, v in DYNAMIC_SETS.items()}
            
            # הרצת האלגוריתם המובנה בקובץ
            selected_sets = greedy_set_cover(clean_universe, clean_sets)
            
            st.divider()
            st.subheader("🎯 תוצאות פריסת הרובוטים האופטימלית")
            st.success(f"🤖 האלגוריתם קבע כי יש צורך ב-**{len(selected_sets)} רובוטים** כדי להבטיח כיסוי שירות הרמטי לכל השולחנות[cite: 7].")
            
            # הצגת האזורים הנבחרים בעמודות דינמיות מתאימות
            cols = st.columns(len(selected_sets))
            for idx, set_name in enumerate(selected_sets):
                with cols[idx]:
                    st.info(f"""
                    **{set_name}**
                    * 🍽️ שולחנות מכוסים:
                    `{sorted(list(clean_sets[set_name]))}`
                    """)
                    
        else:
            st.error("❌ מבנה קובץ לא תקין. על הקובץ להכיל 2 עמודות לפחות (שם האזור/רובוט, רשימת שולחנות).")
            
    except Exception as e:
        st.error(f"❌ שגיאה בתהליך עיבוד נתוני האקסל: {str(e)}")
else:
    st.info("💡 אנא העלי קובץ אקסל (xlsx) המכיל את רשימת אזורי השירות והשולחנות כדי להריץ את ניתוח ה-Set Cover[cite: 11, 13].")
