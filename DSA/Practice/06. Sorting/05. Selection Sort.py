"""
Implementation of the Selection Sort algorithm in Python.
"""

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        # Assume the minimum is the first element of the unsorted part
        min_index = i
        # Iterate through the unsorted elements
        for j in range(i + 1, n):
            # Update min_index if the current element is smaller
            if arr[j] < arr[min_index]:
                min_index = j
        # Swap the found minimum element with the first element of the unsorted part
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr

try:
    input_data = list(map(int, input("Enter numbers to sort, separated by spaces: ").split()))
    sorted_data = selection_sort(input_data)
    print("Sorted array:", sorted_data)
except ValueError:
    print("Please enter valid integers separated by spaces.")
