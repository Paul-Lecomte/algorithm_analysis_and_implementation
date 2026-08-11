from typing import List, Tuple, Dict

def bubble_sort(arr: List[int], count_ops: bool = False) -> Tuple[List[int], Dict[str, int]]:
    n = len(arr)

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr
