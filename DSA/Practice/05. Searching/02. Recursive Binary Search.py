"""
Write a Python function that performs a recursive binary search on a sorted list to find the index of
"""

def recursive_binary_search(arr, target, left, right):
    mid = (left + right) // 2

    if left > right:
        return -1
    
    if arr[mid] == target:
        return mid
    
    elif target < arr[mid]:
        return recursive_binary_search(arr, target, left, mid - 1)
    else:
        return recursive_binary_search(arr, target, mid + 1, right)
    
try:
    sorted_list = list(map(int, input("Enter a sorted list of numbers (space-separated): ").split()))
    target_value = int(input("Enter the target value to search for: "))
    result = recursive_binary_search(sorted_list, target_value, 0, len(sorted_list) - 1)
    if result != -1:
        print(f"Target value {target_value} found at index {result}.")
    else:
        print(f"Target value {target_value} not found in the list.")
except ValueError:
    print("Invalid input. Please enter integers only.")    
    