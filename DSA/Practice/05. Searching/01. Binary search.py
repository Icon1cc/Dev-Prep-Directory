"""
Write a Python function that performs a binary search on a sorted list to find the index of a given target value.
"""

def binary_search(arr, target):
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif target < arr[mid]:
            right = mid - 1
        else:
            left = mid + 1
    return -1   
try:
    sorted_list = list(map(int, input("Enter a sorted list of numbers (space-separated): ").split()))
    target_value = int(input("Enter the target value to search for: "))
    result = binary_search(sorted_list, target_value)
    if result != -1:
        print(f"Target value {target_value} found at index {result}.")
    else:
        print(f"Target value {target_value} not found in the list.")
except ValueError:
    print("Invalid input. Please enter integers only.")
