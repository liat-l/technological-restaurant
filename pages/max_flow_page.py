# pages/max_flow_page.py
import streamlit as st

try:
    from data.restaurant_data import MAX_FLOW_DATA
except ModuleNotFoundError:
    from restaurant_data import MAX_FLOW_DATA

st.title("🌊 אופטימיזציית זרימה מקסימלית (Max Flow)")
st.write("מערכת המידע מנתחת את קצב תזרים ההזמנות מקצה לקצה ומזהה צווארי בקבוק תפעוליים במסעדה.")

st.divider()

# שליפת נתוני הבסיס
kitchen_cap = MAX_FLOW_DATA["קיבולת_מטבח"]
robots_data = MAX_FLOW_DATA["רובוטים"]

# הצגת נתוני פתיחה
col1, col2 = st.columns(2)
with col1:
    st.metric(label="🍳 קיבולת ייצור מקסימלית של המטבח (ב-10 דק')", value=f"{kitchen_cap} הזמנות")
with col2:
    st.metric(label="🤖 רובוטי שירות פעילים ברשת", value=f"{len(robots_data)} רובוטים")

st.divider()

# כפתור להרצת סימולציית הזרימה
if st.button("📊 הרץ ניתוח זרימה מקסימלית ברשת", use_container_width=True):
    
    st.subheader("📋 פירוט הזרימה באזורי השירות השונים")
    
    total_max_flow = 0
    
    # מעבר על כל אזור וחישוב הזרימה האופטימלית (מינימום בין רובוט לשולחנות)
    for zone, caps in robots_data.items():
        r_cap = caps["קיבולת_רובוט"]
        t_cap = caps["שולחנות"]
        
        # חישוב הזרימה בפועל לאותו אזור
        zone_flow = min(r_cap, t_cap)
        total_max_flow += zone_flow
        
        # הצגת הנתונים בצורה נקייה ומקצועית
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
        st.metric(label="📊 נצילות פוטנציאל המטבח", value=f"{int((total_max_flow/kitchen_cap)*100)}%")
        
    # הדגשת צוואר הבקבוק ההנדסי (מבוסס על המסקנה שלכן)
    st.error(f"""
    🛑 **ניתוח צוואר בקבוק הנדסי (Bottleneck Analysis):**
    למרות שהמטבח מסוגל לייצר עד **{kitchen_cap} הזמנות** ב-10 דקות, קיבולת המערכת בפועל מוגבלת ל-**{total_max_flow} הזמנות** בלבד! 
    צוואר הבקבוק אינו במטבח, אלא נובע מ**מגבלת הקיבולת הפיזית של אזורי השירות והשולחנות במסעדה**.
    """)
