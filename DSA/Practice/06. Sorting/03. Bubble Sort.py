"""
Implementation of the Bubble Sort algorithm in Python.
"""

def bubble_sort(arr):
    n = len(arr)
    for i in range(n-1):
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

try:
    input_data = input("Enter numbers separated by spaces: ")
    arr = list(map(int, input_data.split()))
    sorted_arr = bubble_sort(arr)
    print("Sorted array:", sorted_arr)
except ValueError:
    print("Invalid input. Please enter numbers only.")