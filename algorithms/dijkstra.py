# algorithms/dijkstra.py

def run_dijkstra(nodes, matrix, start_node="מטבח"):
    """
    מחשב את המסלולים הקצרים ביותר מקודקוד מקור לכל שאר הקודקודים בגרף.
    ערך של 99 או יותר נחשב כאין מעבר ישיר (אינסוף).
    """
    # אתחול מרחקים (אינסוף לכולם, 0 למקור)
    distances = {node: float('inf') for node in nodes}
    distances[start_node] = 0
    
    # שמירת קודקוד קודם בשביל לשחזר את המסלול
    predecessors = {node: None for node in nodes}
    
    # רשימת הקודקודים שטרם סיימנו לטפל בהם
    unvisited = list(nodes)

    while unvisited:
        # בחירת הקודקוד הלא-מבוקר בעל המרחק המינימלי מהמקור
        current_node = min(unvisited, key=lambda node: distances[node])
        
        # אם המרחק המינימלי הוא אינסוף, שאר הקודקודים אינם נגישים
        if distances[current_node] == float('inf'):
            break
            
        unvisited.remove(current_node)

        # עדכון המרחקים עבור השכנים של הקודקוד הנוכחי
        if current_node in matrix:
            for neighbor, weight in matrix[current_node].items():
                # התעלמות מקודקודים שכבר סיימנו או צלעות חסומות (ערך 99)
                if neighbor not in distances or weight >= 99:
                    continue
                    
                new_distance = distances[current_node] + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current_node

    # שחזור מסלולי הנסיעה המלאים לכל יעד
    paths = {}
    for target in nodes:
        if distances[target] == float('inf'):
            paths[target] = "אין מסלול נגיש"
            continue
            
        # בניית המסלול מהסוף להתחלה
        path = []
        curr = target
        while curr is not None:
            path.append(curr)
            curr = predecessors[curr]
        path.reverse()
        
        paths[target] = "  ➔  ".join(path)

    return distances, paths
