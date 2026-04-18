"""
Write a python function to find the intersection of two sorted arrays. The function should return a list of elements that are present in both arrays. Each element in the result should appear as many times as it shows in both arrays.
"""

def intersection_unique(arr1, arr2):
    i = j = 0
    
    while i < len(arr1) and j < len(arr2):
        # 1. Skip duplicates in arr1
        # We look 'backward' (i-1). If the current number is the same as the
        # one we just passed, we skip it to ensure we don't print it twice.
        if i > 0 and arr1[i] == arr1[i-1]:
            i += 1
            continue

        # 2. Skip duplicates in arr2
        # We look 'backward' (j-1). This is purely an optimization here,
        # but keeps the logic symmetric and efficient.
        if j > 0 and arr2[j] == arr2[j-1]:
            j += 1
            continue
            
        # 3. Standard Two-Pointer Logic
        if arr1[i] < arr2[j]:
            i += 1
        elif arr1[i] > arr2[j]:
            j += 1
        else:
            # Match found!
            print(arr1[i], end=" ")
            i += 1
            j += 1

try:
    input1 = list(map(int, input("Enter the first sorted array (space-separated): ").strip().split()))
    input2 = list(map(int, input("Enter the second sorted array (space-separated): ").strip().split()))
    print("Intersection of the two sorted arrays is:")
    intersection_unique(input1, input2)
    print()  # For a new line after the output
except ValueError:
    print("Invalid input. Please enter space-separated integers.")
