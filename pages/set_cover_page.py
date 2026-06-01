# pages/set_cover_page.py
import streamlit as st
import pandas as pd

try:
    from algorithms.set_cover import greedy_set_cover
except ModuleNotFoundError:
    from set_cover import greedy_set_cover

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
            
            st.success(f"✅ קובץ הנתונים נטען בהצלחה! זוהו {len(dynamic_universe)} שולחנות ייחודיים ו-{len(DYNAMIC_SETS)} אזורי הצבה פוטנציאליים.")
            
            # --- המרה מוחלטת ל-set עבור האלגוריתם החמדני למניעת קריסות ותוצאות חלקיות ---
            clean_universe = set(dynamic_universe)
            clean_sets = {str(k): set(v) for k, v in DYNAMIC_SETS.items()}
            
            # הרצת האלגוריתם החמדני שלכן
            selected_sets = greedy_set_cover(clean_universe, clean_sets)
            
            st.divider()
            st.subheader("🎯 תוצאות פריסת הרובוטים האופטימלית")
            st.success(f"🤖 האלגוריתם קבע כי יש צורך ב-**{len(selected_sets)} רובוטים** כדי להבטיח כיסוי שירות הרמטי לכל השולחנות.")
            
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
    st.info("💡 אנא העלי קובץ אקסל (xlsx) המכיל את רשימת אזורי השירות והשולחנות כדי להריץ את ניתוח ה-Set Cover.")
