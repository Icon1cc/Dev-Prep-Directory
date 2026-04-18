"""
Implementation of the Insertion Sort algorithm in Python.
"""

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        # Move elements of arr[0..i-1], that are greater than key,
        # to one position ahead of their current position
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr  
try:
    input_data = list(map(int, input("Enter numbers to sort, separated by spaces: ").split()))
    sorted_data = insertion_sort(input_data)
    print("Sorted array:", sorted_data)
except ValueError:
    print("Please enter valid integers separated by spaces.")