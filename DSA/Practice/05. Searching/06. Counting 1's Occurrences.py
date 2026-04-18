"""
Write a program to count the number of occurrences of 1's in a sorted binary array (an array consisting of only 0's and 1's).
"""

def count_ones(arr):
    left = 0
    right = len(arr) - 1
    first_one_index = -1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == 1:
            first_one_index = mid
            right = mid - 1
        else:
            left = mid + 1

    if first_one_index == -1:
        return 0
    else:
        return len(arr) - first_one_index   
try: 
    binary_array = list(map(int, input("Enter a sorted binary array (space-separated 0's and 1's): ").split()))
    if any(x not in (0, 1) for x in binary_array):
        raise ValueError("Array must contain only 0's and 1's.")
    result = count_ones(binary_array)
    print(f"The number of occurrences of 1's in the array is: {result}")
except ValueError as e:
    print(f"Invalid input. {e}")
