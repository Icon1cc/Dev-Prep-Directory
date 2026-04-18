"""
Write a python function to merge sorted subarrays within a single array into a single sorted array.
"""

def merge_subarrays(arr, start, mid, end):
    left = arr[start:mid + 1]
    right = arr[mid + 1:end + 1]

    merged_array = []
    i = j = 0

    n1 = len(left)
    n2 = len(right)

    k = start
    # Merge the two subarrays back into arr
    while i < n1 and j < n2:
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1  
    # Copy any remaining elements of left[], if any
    while i < n1:
        arr[k] = left[i]
        i += 1
        k += 1
    # Copy any remaining elements of right[], if any
    while j < n2:
        arr[k] = right[j]
        j += 1
        k += 1  
    return arr

try:    
    input_data = list(map(int, input("Enter numbers in the array, separated by spaces: ").split()))
    start_index = int(input("Enter the start index of the first subarray: "))
    mid_index = int(input("Enter the end index of the first subarray (mid index): "))
    end_index = int(input("Enter the end index of the second subarray: "))
    merged_data = merge_subarrays(input_data, start_index, mid_index, end_index)
    print("Array after merging subarrays:", merged_data)
except ValueError:
    print("Please enter valid integers and indices.")