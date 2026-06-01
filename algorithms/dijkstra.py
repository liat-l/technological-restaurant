# algorithms/dijkstra.py

def run_dijkstra(nodes, matrix, start_node="מטבח"):
    # אתחול מרחקים
    distances = {node: float('inf') for node in nodes}
    distances[start_node] = 0
    predecessors = {node: None for node in nodes}
    unvisited = set(nodes)

    iterations_log = []

    while unvisited:
        # בחירת קודקוד בעל המרחק המינימלי
        current_node = min(unvisited, key=lambda node: distances[node])

        if distances[current_node] == float('inf'):
            break

        unvisited.remove(current_node)

        # שמירה לאיטרציות למטרת הצגה באפליקציה
        iterations_log.append({
            "node": current_node,
            "distance": distances[current_node],
            "path_to_here": get_path_string(predecessors, current_node, start_node)
        })

        # עדכון שכנים
        if current_node in matrix:
            for neighbor, weight in matrix[current_node].items():
                if neighbor in unvisited:
                    new_dist = distances[current_node] + weight
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        predecessors[neighbor] = current_node

    return distances, predecessors, iterations_log


def get_path_string(predecessors, node, start_node):
    path = []
    curr = node
    while curr is not None:
        path.insert(0, curr)
        curr = predecessors[curr]
    return " ➔ ".join(path) if path[0] == start_node else node