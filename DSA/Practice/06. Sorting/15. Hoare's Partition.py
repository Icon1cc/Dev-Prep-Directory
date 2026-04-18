"""
Implements Lomuto's partition scheme for quicksort.
"""

def hoarse_partition(arr, low, high):
    pivot = arr[low]
    left = low -1 
    right = high + 1

    while True:
        left += 1
        while arr[left] < pivot:
            left += 1

        right -= 1
        while arr[right] > pivot:
            right -= 1

        if left >= right:
            return right

        arr[left], arr[right] = arr[right], arr[left]
try:
    arr = list(map(int, input("Enter elements of the array (space-separated): ").strip().split()))
    low = 0
    high = len(arr) - 1
    pivot_index = hoarse_partition(arr, low, high)
    print("Array after Hoare's partitioning:")
    print(arr)
    print(f"Pivot index returned: {pivot_index}")
except ValueError:
    print("Invalid input. Please enter integers only.")
