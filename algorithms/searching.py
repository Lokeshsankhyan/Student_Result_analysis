"""Linear Search implementation for student UID or name."""

def linear_search(records, query):
    """Return all records whose UID or name contains query (case-insensitive)."""
    matches = []
    for student in records:
        if query in student["uid"].lower() or query in student["name"].lower():
            matches.append(student)
    return matches
