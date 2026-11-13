"""
Sorting algorithms implemented manually for DAA demonstration.
Both functions return a NEW list in ascending order.
"""

def quick_sort(items, key=lambda x: x):
    """Quick Sort: average O(n log n), worst O(n^2)."""
    if len(items) <= 1:
        return items[:]

    pivot = key(items[len(items) // 2])
    lower, equal, higher = [], [], []

    for item in items:
        item_key = key(item)
        if item_key < pivot:
            lower.append(item)
        elif item_key > pivot:
            higher.append(item)
        else:
            equal.append(item)

    return quick_sort(lower, key) + equal + quick_sort(higher, key)


def merge_sort(items, key=lambda x: x):
    """Merge Sort: O(n log n) time in best, average and worst cases."""
    if len(items) <= 1:
        return items[:]

    middle = len(items) // 2
    left = merge_sort(items[:middle], key)
    right = merge_sort(items[middle:], key)
    return _merge(left, right, key)


def _merge(left, right, key):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result
