from typing import List, Tuple, Dict
import random


def quicksort(arr: List[int], in_place: bool = False, count_ops: bool = False) -> Tuple[List[int], Dict[str, int]]:
    ops = {"comparisons": 0, "swaps": 0}
    a = arr if in_place else list(arr)

    def _quicksort(low: int, high: int) -> None:
        if low >= high:
            return

        # Partition step: choose a random pivot and move it to the end
        pivot_idx = random.randint(low, high)
        a[pivot_idx], a[high] = a[high], a[pivot_idx]
        if count_ops:
            ops["swaps"] += 1
        pivot = a[high]
        i = low
        for j in range(low, high):
            if count_ops:
                ops["comparisons"] += 1
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                if count_ops:
                    ops["swaps"] += 1
                i += 1

        # Move pivot to correct position
        a[i], a[high] = a[high], a[i]
        if count_ops:
            ops["swaps"] += 1

        # Recurse
        _quicksort(low, i - 1)
        _quicksort(i + 1, high)

    _quicksort(0, len(a) - 1)
    return a, ops