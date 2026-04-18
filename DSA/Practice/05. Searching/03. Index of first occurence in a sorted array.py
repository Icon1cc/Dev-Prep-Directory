"""
Write a python function that finds the index of the first occurrence of a target value in a sorted array.
If the element is not found, return -1.
"""

def index_of_first_occurrence(arr, target):
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            if mid == 0 or arr[mid - 1] != arr[mid]:
                return mid
            else:
                right = mid - 1
        elif target < arr[mid]:
            right = mid - 1
        else:
            left = mid + 1
    return -1

try:
    sorted_list = list(map(int, input("Enter a sorted list of numbers (space-separated): ").split()))
    target_value = int(input("Enter the target value to search for: "))
    result = index_of_first_occurrence(sorted_list, target_value)
    if result != -1:
        print(f"First occurrence of target value {target_value} found at index {result}.")
    else:
        print(f"Target value {target_value} not found in the list.")
except ValueError:
    print("Invalid input. Please enter integers only.")