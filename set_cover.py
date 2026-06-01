

def greedy_set_cover(universe, sets):
    uncovered = universe.copy()
    selected_sets = []
    covered_elements = set()
    iterations = []

    while uncovered:
        best_set_name = None
        best_set_elements = set()
        max_new_elements = -1

        for name, elements in sets.items():
            if name in selected_sets:
                continue

            # מציאת השולחנות בקבוצה הזו שעדיין לא קיבלו שירות
            new_elements = elements.intersection(uncovered)
            count_new = len(new_elements)

            # בחירה חמדנית בקבוצה שמכסה הכי הרבה שולחנות חדשים
            if count_new > max_new_elements:
                max_new_elements = count_new
                best_set_name = name
                best_set_elements = new_elements

        if best_set_name and max_new_elements > 0:
            selected_sets.append(best_set_name)
            uncovered -= best_set_elements
            covered_elements.update(best_set_elements)

            # שמירת נתוני השלב הנוכחי לתצוגה חזותית
            iterations.append({
                "selected": best_set_name,
                "covered": list(best_set_elements),
                "remaining": len(uncovered)
            })
        else:
            break

    return selected_sets, covered_elements, iterations