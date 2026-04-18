"""
Implement the QuickSort algorithm using the Hoare partitioning scheme.
"""
def hoare_partition(arr, low, high):
    pivot = arr[low]
    left = low - 1
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
def quicksort(arr, low, high):
    if low < high:
        pivot_index = hoare_partition(arr, low, high)
        quicksort(arr, low, pivot_index)
        quicksort(arr, pivot_index + 1, high)   
try:
    arr = list(map(int, input("Enter elements of the array (space-separated): ").strip().split()))
    quicksort(arr, 0, len(arr) - 1)
    print("Sorted array using QuickSort with Hoare's partitioning:")
    print(arr)
except ValueError:
    print("Invalid input. Please enter integers only.")