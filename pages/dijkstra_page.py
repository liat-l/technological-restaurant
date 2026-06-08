import streamlit as st
import pandas as pd
import heapq

def run_dijkstra(graph, start_node):
    """
    אלגוריתם דייקסטרה למציאת המסלול הקצר ביותר מקודקוד מקור לכל שאר הקודקודים בגרף.
    """
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0
    priorities = [(0, start_node)]
    predecessors = {node: None for node in graph}
    
    while priorities:
        current_distance, current_node = heapq.heappop(priorities)
        
        if current_distance > distances[current_node]:
            continue
            
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(priorities, (distance, neighbor))
                
    return distances, predecessors

def get_shortest_path(predecessors, target_node):
    """
    שחזור מסלול הניווט צעד אחר צעד מהמקור אל קודקוד היעד.
    """
    path = []
    current = target_node
    while current is not None:
        path.append(current)
        current = predecessors[current]
    path.reverse()
    return path


st.title("⚡ Robo-Navigation")
st.subheader("מערכת ניווט דינמית בזמן אמת ומזעור מרחקי תנועה")
st.write("""
 **Robo-Navigation** ברוכים הבאים למודול

המערכת מממשת את אלגוריתם דייקסטרה למצאת המסלול הקצר היותר בגרף המשוקלל

כל קודקוד מייצג נקודת שירות במסעדה וכל קשת מייצגת נתיב תנועה עם עלות (מרחק)

האלגוריתם מחשב את המסלול בעל העלות המינימלית בין המטבח לבין יעד ההגשה שנבחר

""")

st.divider()

st.subheader("📥 העלאת נתוני רשת ומרחקים")
uploaded_matrix = st.file_uploader(
    "📊 העלי את קובץ האקסל המכיל את מטריצת המרחקים של המסעדה", 
    type=["xlsx"]
)

if uploaded_matrix is not None:
    try:
        # קריאת האקסל והגדרת העמודה הראשונה כאינדקס
        df = pd.read_excel(uploaded_matrix, index_col=0)
        
        # בניית מבנה הגרף בצורה דינמית מתוך האקסל
        graph = {}
        
        for source_node in df.index:
            s_name = str(source_node).strip()
            graph[s_name] = {}
            for target_node in df.columns:
                t_name = str(target_node).strip()
                val = df.loc[source_node, target_node]
                
                # תמיכה בערכים מספריים תקינים הגדולים מ-0
                if pd.notna(val) and str(val).lower() != 'inf' and float(val) > 0:
                    graph[s_name][t_name] = float(val)
        
        st.divider()
        st.subheader("🤖 סימולציית הזמנה ופקודות ניווט")
        
        # זיהוי אוטומטי של קודקוד המקור (המטבח)
        possible_sources = [node for node in graph.keys() if "מטבח" in node or "kitchen" in node.lower() or node == "0"]
        start_node = possible_sources[0] if possible_sources else list(graph.keys())[0]
        
        # סינון רשימת היעדים
        destinations = [node for node in graph.keys() if node != start_node]
        
        if destinations:
            # תיבת בחירה דינמית ומעוצבת לשולחן היעד
            selected_target = st.selectbox(
                "🍽️ בחרי את קודקוד היעד למשלוח המנה או לביצוע פקודת עבודה:", 
                sorted(destinations)
            )
            
            # הרצת אלגוריתם דייקסטרה
            distances, predecessors = run_dijkstra(graph, start_node)
            
            # שליפת מרחק ומסלול
            final_distance = distances.get(selected_target, float('inf'))
            final_path = get_shortest_path(predecessors, selected_target)
            
            st.write("---")
            
            if final_distance != float('inf'):
                # הצגת המדד המרכזי בעמודה אחת ממורכזת ונקייה
                st.metric(label="📏 מרחק נסיעה כולל ואופטימלי", value=f"{final_distance} מטרים")
                
                # הצגת נתיב החצים בתוך תיבת מידע יוקרתית
                path_visual = " ➔ ".join(final_path)
                st.info(f"📍 **נתיב הניווט המשוחזר עבור הרובוט:**\n\n`{path_visual}`")
            else:
                st.error(f"❌ לא נמצא מסלול תנועה פתוח בין {start_node} לבין שולחן {selected_target}. ודאי שאין חסימה פיזית ברשת המסעדה.")
        else:
            st.warning("⚠️ הקובץ שהועלה מכיל רק קודקוד אחד, לא ניתן לחשב מסלולי ניווט.")
            
    except Exception as e:
        st.error(f"❌ שגיאה בעיבוד מטריצת המרחקים מהאקסל: {str(e)}")
else:
    # הודעת הדרכה מעוצבת ומזמינה כשהמסך ריק ומחכה לקובץ
    st.info("""
    👋 **?מוכנים להפעיל את מערכת הניווט**
      העלו את קובל האקסל המכיל את מטריצת המרחקים והחיבורים בין נקודות השירות השונות במסעדה   
     מיד עם הטענת הקובץ, ייפתח פאנל השליטה לבחירת יעדי ההגשה והצגת נתיבי הנסיעה האופטימליים
    """)
    
    # הצגת דוגמה למבנה שהמשתמש יבין מה להעלות
    with st.expander("💡 לחצי כאן לצפייה במבנה מטריצת המרחקים הנדרשת (דוגמה)"):
        example_matrix = pd.DataFrame({
            "קודקוד": ["מטבח", "T1", "T2", "עמדת טעינה"],
            "מטבח": [0, 10, 15, "inf"],
            "T1": [10, 0, 5, "inf"],
            "T2": [15, 5, 0, 8],
            "עמדת טעינה": ["inf", "inf", 8, 0]
        })
        example_matrix.set_index("קודקוד", inplace=True)
        st.table(example_matrix)
        st.caption("""inf הערה: הערך 
        
        מייצג מצב שבו אין חיבור ישיר פתוח בין שני הקודקודים הללו ברשת""")
