"""
Implements Lomuto's partition scheme for quicksort.
"""
def lomuto_partition(arr, low, high):
    pivot = arr[high]  # Choose the last element as pivot
    i = low - 1  # Pointer for the smaller element

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1  # Increment index of smaller element
            arr[i], arr[j] = arr[j], arr[i]  # Swap

    arr[i + 1], arr[high] = arr[high], arr[i + 1]  # Place pivot in the correct position
    return i + 1  # Return the index of the pivot

try:
    arr = list(map(int, input("Enter elements of the array (space-separated): ").strip().split()))
    low = 0
    high = len(arr) - 1
    pivot_index = lomuto_partition(arr, low, high)
    print(f"Array after Lomuto's partitioning: {arr}")
    print(f"Pivot index: {pivot_index}, Pivot value: {arr[pivot_index]}")
except ValueError:
    print("Invalid input. Please enter integers only.")