# pages/max_flow_page.py
import streamlit as st

try:
    from data.restaurant_data import MAX_FLOW_DATA
except ModuleNotFoundError:
    from restaurant_data import MAX_FLOW_DATA

st.title("🌊 אופטימיזציית זרימה מקסימלית (Max Flow)")
st.write("מערכת המידע מנתחת את קצב תזרים ההזמנות מקצה לקצה ומזהה צווארי בקבוק תפעוליים במסעדה.")

st.divider()

# שליפת נתוני הבסיס מתוך קובץ הנתונים
kitchen_cap = MAX_FLOW_DATA["קיבולת_מטבח"]
robots_data = MAX_FLOW_DATA["רובוטים"]

# הצגת נתוני פתיחה במטריקות נקיות
col1, col2 = st.columns(2)
with col1:
    st.metric(label="🍳 קיבולת ייצור מקסימלית של המטבח (ב-10 דק')", value=f"{kitchen_cap} הזמנות")
with col2:
    st.metric(label="🤖 רובוטי שירות פעילים ברשת", value=f"{len(robots_data)} רובוטים")

st.divider()

# כפתור להרצת סימולציית הזרימה האלגוריתמית
if st.button("📊 הרץ ניתוח זרימה מקסימלית ברשת", use_container_width=True):
    
    st.subheader("📋 פירוט הזרימה באזורי השירות השונים")
    
    total_max_flow = 0
    bottlenecks = []
    
    # מעבר על כל אזור וחישוב הזרימה האופטימלית (מינימום בין רובוט לשולחנות)
    for zone, caps in robots_data.items():
        r_cap = caps["קיבולת_רובוט"]
        t_cap = caps["שולחנות"]
        
        # חישוב הזרימה בפועל לאותו אזור לפי חוק המינימום
        zone_flow = min(r_cap, t_cap)
        total_max_flow += zone_flow
        
        # בדיקה אוטומטית: אם קיבולת השולחנות קטנה מקיבולת הרובוט - האזור הוא צוואר בקבוק
        if t_cap < r_cap:
            bottlenecks.append(f"**{zone}** (קיבולת שולחנות: {t_cap} מול קיבולת רובוט: {r_cap})")
        
        # הצגת הנתונים של האזור בצורה נקייה ומקצועית
        st.info(f"""
        📍 **אזור שירות: {zone}**
        * 🤖 קיבולת הובלה של הרובוט: {r_cap} הזמנות
        * 🍽️ קיבולת ספיגה לפי שולחנות: {t_cap} הזמנות
        * 🌊 **זרימת הזמנות בפועל באזור:** **{zone_flow} הזמנות**
        """)
        
    st.divider()
    
    st.subheader("🎯 סיכום תוצאות המודל")
    
    # הצגת המטריקות הסופיות של ה-Max Flow
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.metric(label="🔥 זרימה מקסימלית כוללת במערכת (Max Flow)", value=f"{total_max_flow} הזמנות")
    with res_col2:
        st.metric(label="📊 נצילות פוטנציאל המטבח", value=f"{int((total_max_flow / kitchen_cap) * 100)}%")
        
    st.divider()
    
    st.subheader("🛑 ניתוח צוואר בקבוק אוטומטי (Bottleneck Analysis)")

    # קבלת החלטה פלט-אלגוריתמית דינמית על בסיס הנתונים שחושבו
    if total_max_flow == kitchen_cap:
        st.error(f"🛑 **צוואר הבקבוק זוהה במטבח:** המטבח הגיע לניצול מלא של הקיבולת שלו ({kitchen_cap} הזמנות) ומגביל את המשך זרימת המנות ברשת.")
    elif bottlenecks:
        st.error("🛑 **צוואר הבקבוק זוהה באזורי השירות הבאים:**")
        for b in bottlenecks:
            st.write(f"* {b}")
        st.caption("💡 הסבר אלגוריתמי: באזורים אלו, קיבולת ספיגת השולחנות נמוכה מקיבולת ההובלה של הרובוט, ולכן הזרימה נחסמה ונעצרה על ערך המינימום של האזור.")
    else:
        st.success("✅ לא זוהו צווארי בקבוק נקודתיים חונקים ברשת. הזרימה מוגבלת על ידי סך קיבולות הרכיבים.")
