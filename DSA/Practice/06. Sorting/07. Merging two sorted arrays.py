"""
Write a python function to merge two sorted arrays into a single sorted array.
"""

def merge_sorted_arrays(arr1, arr2):
    merged_array = []
    i = j = 0

    # Traverse both arrays and insert smaller of both elements into merged_array
    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            merged_array.append(arr1[i])
            i += 1
        else:
            merged_array.append(arr2[j])
            j += 1

    # If there are remaining elements in arr1, add them to merged_array
    while i < len(arr1):
        merged_array.append(arr1[i])
        i += 1

    # If there are remaining elements in arr2, add them to merged_array
    while j < len(arr2):
        merged_array.append(arr2[j])
        j += 1

    return merged_array

try:
    input_data1 = list(map(int, input("Enter numbers for the first sorted array, separated by spaces: ").split()))
    input_data2 = list(map(int, input("Enter numbers for the second sorted array, separated by spaces: ").split()))
    merged_data = merge_sorted_arrays(input_data1, input_data2)
    print("Merged sorted array:", merged_data)
except ValueError:
    print("Please enter valid integers separated by spaces.")