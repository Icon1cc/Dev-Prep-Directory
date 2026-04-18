"""
Write a python fuction to count inversions in an array. An inversion is a pair of indices (i, j) such that i < j and arr[i] > arr[j].
"""

# def countinversion(arr):
#     n = len(arr)
#     count = 0
    
#     for i in range(n - 1):
#         for j in range(i+1,n):
#             if arr[i] > arr[j]:
#                 count += 1
#     return count

def merge_sort_inversion(arr):
    if len(arr) <= 1:
        return 0
    mid = len(arr) // 2
    L = arr[:mid]
    R = arr[mid:]

    a = merge_sort_inversion(L)
    b = merge_sort_inversion(R)

    count = a + b

    i = j = k = 0
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
            count += (len(L) - i)
        k += 1
    while i < len(L):
        arr[k] = L[i]
        i += 1
        k += 1
    while j < len(R):
        arr[k] = R[j]
        j += 1
        k += 1
    return count    

try:
    input_array = list(map(int, input("Enter the elements of the array separated by spaces: ").split()))
    result = merge_sort_inversion(input_array)
    print("Number of inversions in the array:", result)
except ValueError:
    print("Invalid input. Please enter integers only.")