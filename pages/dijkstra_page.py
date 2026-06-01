# pages/dijkstra_page.py
import streamlit as st
import pandas as pd
import heapq

# --- מימוש ישיר של אלגוריתם דייקסטרה (Dijkstra) בתוך הדף למניעת שגיאות ייבוא ---
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

# --- תצוגת הדשבורד של Streamlit ---

st.title("⚡ ניווט רובוטים בזמן אמת (Dijkstra) דינמי")
st.write("מערכת המידע מחשבת את נתיב התנועה האופטימלי ומזעור מרחקי הנסיעה של הרובוט מהמטבח אל השולחנות על בסיס מטריצת מרחקים.")

st.divider()

# רכיב להעלאת קובץ האקסל של מטריצת המרחקים
uploaded_matrix = st.file_uploader("📊 העלי קובץ אקסל (xlsx) של מטריצת המרחקים במסעדה:", type=["xlsx"])

if uploaded_matrix is not None:
    try:
        # קריאת האקסל והגדרת העמודה הראשונה כאינדקס (שמות השורות)
        df = pd.read_excel(uploaded_matrix, index_col=0)
        
        # בניית מבנה הגרף (Adjacency List) בצורה דינמית מתוך האקסל
        graph = {}
        all_nodes = [str(col).strip() for col in df.columns]
        
        for source_node in df.index:
            s_name = str(source_node).strip()
            graph[s_name] = {}
            for target_node in df.columns:
                t_name = str(target_node).strip()
                val = df.loc[source_node, target_node]
                
                # אם הערך הוא מספר תקין (לא אינסוף ולא ריק) והוא גדול מ-0, נוסיף קשת בגרף
                if pd.notna(val) and str(val).lower() != 'inf' and float(val) > 0:
                    graph[s_name][t_name] = float(val)
        
        st.success("✅ מטריצת המרחקים נטענה ונבנתה כגרף בזיכרון בהצלחה!")
        
        st.divider()
        st.subheader("🤖 סימולציית ניווט והזמנת מנה")
        
        # קביעת קודקוד המקור (המטבח) אוטומטית מתוך הקודקודים הזמינים באקסל
        possible_sources = [node for node in graph.keys() if "מטבח" in node or "kitchen" in node.lower() or node == "0"]
        start_node = possible_sources[0] if possible_sources else list(graph.keys())[0]
        
        # סינון רשימת היעדים (כל הקודקודים שהם לא המטבח בעצמו)
        destinations = [node for node in graph.keys() if node != start_node]
        
        if destinations:
            # תיבת בחירה דינמית שמתעדכנת לבד לפי השולחנות שיש באקסל שלך
            selected_target = st.selectbox("🍽️ בחרי את שולחן היעד למשלוח המנה מהמטבח:", sorted(destinations))
            
            # הרצת אלגוריתם דייקסטרה על הגרף הדינמי מהאקסל
            distances, predecessors = run_dijkstra(graph, start_node)
            
            # שליפת המרחק והמסלול המשוחזר
            final_distance = distances.get(selected_target, float('inf'))
            final_path = get_shortest_path(predecessors, selected_target)
            
            if final_distance != float('inf'):
                # הצגת התוצאות במטריקות מעוצבות ונקיות
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.metric(label="📏 סך מרחק הנסיעה האופטימלי:", value=f"{final_distance} מטרים")
                with res_col2:
                    # הפיכת רשימת המסלול לחצים יפים (למשל: מטבח ➔ T1 ➔ T2)
                    path_visual = " ➔ ".join(final_path)
                    st.info(f"📍 **נתיב הניווט הנבחר:**\n`{path_visual}`")
            else:
                st.error(f"❌ לא נמצא מסלול תנועה פתוח בין {start_node} לבין שולחן {selected_target}. ודאי שאין חסימה ברשת.")
        else:
            st.warning("⚠️ הקובץ שהועלה מכיל רק קודקוד אחד, לא ניתן לחשב מסלולי ניווט.")
            
    except Exception as e:
        st.error(f"❌ שגיאה בעיבוד מטריצת המרחקים מהאקסל: {str(e)}")
else:
    # הודעת הסבר שמופיעה רק כשהמסך ריק ומחכה לקובץ (ונעלמת אוטומטית ברגע שהקובץ עולה!)
    st.info(f"💡 אנא העלי קובץ אקסל (xlsx) המכיל את מטריצת המרחקים של המסעדה כדי להפעיל את סימולציית דייקסטרה.")
