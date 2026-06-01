# pages/set_cover_page.py
import streamlit as st
import pandas as pd

try:
    from algorithms.set_cover import greedy_set_cover
except ModuleNotFoundError:
    from set_cover import greedy_set_cover

st.title("📍 אופטימיזציית כיסוי אזורים (Set Cover) דינמי")
st.write("העלי קובץ אקסל עם פריסת הרובוטים הפוטנציאלית, והאלגוריתם יחשב את הכמות המינימלית הנדרשת לכיסוי.")

st.divider()

# רכיב ייעודי להעלאת קובץ אקסל של נתוני הכיסוי
uploaded_excel = st.file_uploader("📊 העלי קובץ אקסל (xlsx) של אזורי השירות:", type=["xlsx"])

if uploaded_excel is not None:
    try:
        # קריאת האקסל באמצעות pandas
        df = pd.read_excel(uploaded_excel)
        
        # וידאו שהאקסל מכיל לפחות שתי עמודות
        if df.shape[1] >= 2:
            # שינוי שמות העמודות לצורך עבודה נוחה בקוד
            df.columns = ["robot_name", "tables_covered"]
            
            # בניית ה-SETS וה-UNIVERSE בצורה אוטומטית לחלוטין מתוך האקסל
            DYNAMIC_SETS = {}
            dynamic_universe = set()
            
            for index, row in df.iterrows():
                r_name = str(row["robot_name"]).strip()
                # פירוק השולחנות לפי פסיקים והסרת רווחים מיותרים
                t_list = [t.strip() for t in str(row["tables_covered"]).split(",") if t.strip()]
                
                DYNAMIC_SETS[r_name] = set(t_list)
                dynamic_universe.update(t_list)
            
            st.success("✅ נתוני האקסל נקראו ונבנו בזיכרון בהצלחה!")
            
            # הרצת האלגוריתם החמדני על המבנה הדינמי שנוצר מהאקסל
            selected_sets = greedy_set_cover(dynamic_universe, DYNAMIC_SETS)
            
            st.divider()
            st.subheader("🎯 תוצאות פריסת הרובוטים האופטימלית")
            st.metric(label="🤖 כמות רובוטים מינימלית נדרשת:", value=f"{len(selected_sets)} רובוטים")
            
            # הצגת הרובוטים הנבחרים בעמודות דינמיות בהתאם לתוצאה
            cols = st.columns(len(selected_sets))
            for idx, set_name in enumerate(selected_sets):
                with cols[idx]:
                    st.info(f"""
                    **{set_name}**
                    * 🍽️ שולחנות מכוסים:
                    `{sorted(list(DYNAMIC_SETS[set_name]))}`
                    """)
                    
        else:
            st.error("❌ מבנה אקסל לא תקין. הקובץ חייב להכיל 2 עמודות: שם רובוט ושולחנות מכוסים.")
            
    except Exception as e:
        st.error(f"❌ שגיאה בעיבוד קובץ האקסל: {str(e)}")
else:
    st.info("💡 אנא העלי קובץ אקסל כדי להריץ את אלגוריתם ה-Set Cover באופן דינמי.")
