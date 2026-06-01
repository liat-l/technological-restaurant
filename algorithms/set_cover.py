# algorithms/set_cover.py

def greedy_set_cover(universe, sets):
    uncovered = universe.copy()
    selected_sets = []
    covered_elements = set()
    iterations = []

    while uncovered:
        best_set_name = None
        best_set_elements = set()
        max_new_elements = -1
        best_set_total_size = -1

        for name, elements in sets.items():
            if name in selected_sets:
                continue

            # מציאת השולחנות בקבוצה הזו שעדיין לא קיבלו שירות
            new_elements = elements.intersection(uncovered)
            count_new = len(new_elements)
            total_size = len(elements)

            # 1. בחירה חמדנית בקבוצה שמכסה הכי הרבה שולחנות חדשים
            if count_new > max_new_elements:
                max_new_elements = count_new
                best_set_name = name
                best_set_elements = new_elements
                best_set_total_size = total_size

            # 2. פתרון תיקו מתמטי בהתאם לניתוח ההנדסי של המסעדה
            elif count_new == max_new_elements and count_new > 0:
                if total_size > best_set_total_size:
                    best_set_name = name
                    best_set_elements = new_elements
                    best_set_total_size = total_size

        if best_set_name and max_new_elements > 0:
            selected_sets.append(best_set_name)
            uncovered -= best_set_elements
            covered_elements.update(best_set_elements)

            # שמירת נתוני השלב
            iterations.append({
                "selected": best_set_name,
                "covered": list(best_set_elements),
                "remaining": len(uncovered)
            })
        else:
            break

    return selected_sets, covered_elements, iterations
