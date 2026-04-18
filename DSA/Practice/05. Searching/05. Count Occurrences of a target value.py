"""
Write a python function that finds the number of occurrences of a target value in a sorted array.
"""

def count_occurrences(arr, target):
    def find_first_occurence(arr, target):
        left = 0
        right = len(arr) - 1
        
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                if mid == 0 or arr[mid - 1] != arr [mid]:
                    return mid
                else:
                    right = mid - 1
            elif target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        return -1
    
    def find_last_occurence(arr, target):

        left = 0
        right = len(arr) - 1

        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                if mid == len(arr) - 1 or arr[mid] != arr[mid + 1]:
                    return mid
                else:
                    left = mid + 1
            elif target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        return -1
    
    first_index = find_first_occurence(arr, target)
    if first_index == -1:
        return 0    
    last_index = find_last_occurence(arr, target)
    return last_index - first_index + 1
try:
    sorted_list = list(map(int, input("Enter a sorted list of numbers (space-separated): ").split()))
    target_value = int(input("Enter the target value to search for: "))
    result = count_occurrences(sorted_list, target_value)
    print(f"Target value {target_value} occurs {result} time(s) in the list.")
except ValueError:
    print("Invalid input. Please enter integers only.")