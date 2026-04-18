"""
Print union of two sorted arrays.
"""

def union_of_sorted_arrays(arr1, arr2):
    i = j = 0
    while i < len(arr1) and j < len(arr2):
        if i > 0 and arr1[i] == arr1[i - 1]:
            i += 1
        elif j > 0 and arr2[j] == arr2[j - 1]:
            j += 1
        elif arr1[i] < arr2[j]:
            print(arr1[i], end=' ')
            i += 1
        elif arr1[i] > arr2[j]:
            print(arr2[j], end=' ')
            j += 1
        else:
            print(arr1[i], end=' ') # or arr2[j], since they are equal
            i += 1
            j += 1
    while i < len(arr1):
        if i == 0 or arr1[i] != arr1[i - 1]:
            print(arr1[i], end=' ')
        i += 1
    while j < len(arr2):
        if j == 0 or arr2[j] != arr2[j - 1]:
            print(arr2[j], end=' ')
        j += 1
try:
    arr1 = list(map(int, input("Enter elements of first sorted array (space-separated): ").strip().split()))
    arr2 = list(map(int, input("Enter elements of second sorted array (space-separated): ").strip().split()))
    print("Union of the two sorted arrays is:")
    union_of_sorted_arrays(arr1, arr2)
    print() # For a new line after the output
except ValueError:
    print("Invalid input. Please enter integers only.")