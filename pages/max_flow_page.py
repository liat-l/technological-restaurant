import streamlit as st
import pandas as pd

def calculate_max_flow(kitchen_capacity, robot_data, robots_status):
    """
    אלגוריתם זרימה מקסימלית למסעדה.

    kitchen_capacity - קיבולת המטבח
    robot_data - נתוני האזורים והרובוטים
    robots_status - סטטוס הרובוטים
    """

    total_flow = 0
    bottlenecks = []
    zone_results = {}

    for zone, caps in robot_data.items():

        if robots_status[zone]:
            robot_capacity = 0
            status_text = "🔴 מושבת / תקלה תפעולית"
        else:
            robot_capacity = caps["קיבולת_רובוט"]
            status_text = "🟢 פעיל בשירות"

        tables_capacity = caps["שולחנות"]

        # Max Flow לפי החוליה החלשה במסלול
        zone_flow = min(
            robot_capacity,
            tables_capacity
        )

        total_flow += zone_flow

        zone_results[zone] = {
            "flow": zone_flow,
            "robot_capacity": robot_capacity,
            "tables_capacity": tables_capacity,
            "status": status_text
        }

        if tables_capacity < robot_capacity and not robots_status[zone]:
            bottlenecks.append(
                f"**{zone}** (קיבולת שולחנות: {tables_capacity} מול קיבולת רובוט: {robot_capacity})"
            )

        elif robots_status[zone]:
            bottlenecks.append(
                f"**{zone}** (הרובוט הושבת באופן יזום)"
            )

    final_flow = min(
        kitchen_capacity,
        total_flow
    )

    return final_flow, total_flow, bottlenecks, zone_results




st.title("🌊 Robo-Flow Simulator")
st.subheader("סימולטור זרימה מקסימלית בזמן אמת וניתוח צווארי בקבוק")
st.write("""
**Robo-Flow Simulator**  ברוכים הבאים למודול 

כלי ניהול ולוגיסטיקה דינמי זה מנתח את נפח ותזרים ההזמנות ברשת מהמטבח ועד לשולחן הסועד

המערכת מיישמת את חוק המינימום ומאפשרת לכם לבצע סימולציות עומס להשבית רובוטים ולזהות אוטומטית כשלים וצווארי בקבוק תפעוליים במערך ההפצה

""")

st.divider()

st.subheader("📥 העלאת נתוני קיבולת ורשת")
uploaded_flow = st.file_uploader(
    "📊 העלי את קובץ האקסל (xlsx) המכיל את נתוני הקיבולות של אזורי השירות והרובוטים:", 
    type=["xlsx"]
)

if uploaded_flow is not None:
    try:
        # קריאת קובץ האקסל באמצעות pandas
        df = pd.read_excel(uploaded_flow)
        
        if df.shape[1] >= 3:
            # הגדרת שמות עמודות אחידים לעבודה בקוד
            df.columns = ["zone_name", "robot_capacity", "tables_capacity"]
            
            # בניית מילון הנתונים בצורה דינמית מהאקסל
            DYNAMIC_ROBOTS = {}
            for index, row in df.iterrows():
                z_name = str(row["zone_name"]).strip()
                r_cap = int(row["robot_capacity"])
                t_cap = int(row["tables_capacity"])
                
                if z_name:
                    DYNAMIC_ROBOTS[z_name] = {"קיבולת_רובוט": r_cap, "שולחנות": t_cap}
            
            st.divider()
            
            # --- פאנל שליטה וסימולציה דינמי (Control Panel) ---
            st.subheader("🛠️ פאנל סימולציה ותקלות בזמן אמת")
            
            # 1. סליידר דינמי לקביעת קיבולת המטבח כעת
            kitchen_cap = st.slider(
                "🍳 כושר ייצור נוכחי של המטבח (הזמנות ב-10 דקות):",
                min_value=5,
                max_value=50,
                value=24,
                step=1
            )
            
            st.write("🤖 **סטטוס תפעולי של צי הרובוטים (סמני להשבתת רובוט עקב תקלה):**")
            robots_status = {}
            
            # 2. יצירת תיבות סימון דינמיות לבדיקת השבתת רובוטים לפי האזורים שבאקסל
            cols = st.columns(len(DYNAMIC_ROBOTS))
            for idx, zone in enumerate(DYNAMIC_ROBOTS.keys()):
                with cols[idx]:
                    short_name = zone.split(" ")[0]
                    is_disabled = st.checkbox(f"❌ השבת את {short_name}", key=f"disabled_{zone}")
                    robots_status[zone] = is_disabled
            
            st.divider()
            
            # --- הרצת אלגוריתם הזרימה הדינמי ---
            st.subheader("📋 פירוט תזרים ההזמנות הנוכחי ברשת")
            final_flow, total_max_flow, bottlenecks, zone_results = calculate_max_flow(
                kitchen_cap,
                DYNAMIC_ROBOTS,
                robots_status
            )
            
            for zone, data in zone_results.items():
            
                st.info(f"""
                📍 **אזור שירות: {zone}** | סטטוס: {data['status']}
                * 🤖 קיבולת הובלה של הרובוט: `{data['robot_capacity']}` הזמנות
                * 🍽️ קיבולת ספיגה לפי שולחנות: `{data['tables_capacity']}` הזמנות
                * 🌊 **זרימת הזמנות בפועל באזור:** **{data['flow']} הזמנות**
                """)
            

            st.divider()
            st.subheader("🎯 סיכום תוצאות המודל")
            
            # הצגת מטריקות סופיות דינמיות ומקצועיות
            res_col1, res_col2, res_col3 = st.columns(3)
            with res_col1:
                st.metric(label="🔥 זרימה מקסימלית בפועל (Max Flow)", value=f"{final_flow} הזמנות")
            with res_col2:
                st.metric(label="🍳 פלט המטבח הנוכחי", value=f"{kitchen_cap} הזמנות")
            with res_col3:
                # חישוב נצילות מוגן מחלוקה באפס
                efficiency = int((final_flow / kitchen_cap) * 100) if kitchen_cap > 0 else 0
                st.metric(label="📊 נצילות פוטנציאל המטבח", value=f"{efficiency}%")
            
            st.divider()
            
            # --- ניתוח צוואר בקבוק אוטומטי לחלוטין (Bottleneck Analysis) ---
            st.subheader("🛑 ניתוח צוואר בקבוק אוטומטי (Bottleneck Analysis)")
            
            if final_flow == kitchen_cap and final_flow < total_max_flow:
                st.error(f"🛑 **צוואר הבקבוק זוהה במטבח:** המטבח הנוכחי עמוס מדי ומייצר רק {kitchen_cap} מנות. צי הרובוטים והשולחנות מסוגלים לקלוט יותר ({total_max_flow}). מומלץ לתגבר טבחים!")
            elif final_flow < kitchen_cap:
                st.error(f"🛑 **צוואר הבקבוק זוהה במערך ההפצה והשולחנות:** המטבח ייצר {kitchen_cap} מנות, אך רק {final_flow} הצליחו להגיע לסועדים בשל המגבלות הבאות:")
                for b in bottlenecks:
                    st.write(f"* {b}")
                st.caption("💡 הסבר אלגוריתמי: באזורים אלו, הזרימה נחסמה ונעצרה על ערך המינימום – או בגלל שקיבולת ספיגת השולחנות חנקה את כושר ההובלה של הרובוט, או בשל השבתה תפעולית מלאה של הרובוט באותו האזור.")
            else:
                st.success("✅ **איזון מושלם ברשת:** קצב ייצור המטבח תואם בדיוק לקצב ההפצה המקסימלי של הרובוטים והשולחנות!")
                
        else:
            st.error("❌ מבנה קובץ לא תקין. על הקובץ להכיל 3 עמודות לפחות (שם האזור, קיבולת רובוט, קיבולת שולחנות).")
            
    except Exception as e:
        st.error(f"❌ שגיאה בתהליך עיבוד נתוני האקסל: {str(e)}")
else:
    # הודעת הדרכה מעוצבת ומזמינה כשהמסך ריק ומחכה לקובץ
    st.info("""
    👋 **?מוכנים להריץ את סימולציית התזרים**
    
   (`.xlsx`)  אנא עלה את קובץ אקסל
    המכיל את נתוני הקיבולת והאספקה של אזורי השירות השונים במסעדה
    מיד עם טעינת הקובץ, ייפתח פאנל השליטה האינטראקטיבי לניהול עומסי המטבח ובדיקת השבתות הצי
    """)
    
    # הצגת דוגמה למבנה שהמשתמש יבין מה להעלות
    with st.expander("💡 לחצי כאן לצפייה במבנה הנתונים הנדרש (דוגמה)"):
        example_df = pd.DataFrame({
            "שם אזור השירות": ["S3 (מתחם מרכזי)", "S4 (מתחם שישיות)", "S8 (מתחם VIP)"],
            "קיבולת רובוט": [8, 6, 6],
            "קיבולת שולחנות": [6, 4, 4]
        })
        st.table(example_df)
