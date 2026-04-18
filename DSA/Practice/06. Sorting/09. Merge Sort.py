"""
Implementation of the Merge Sort algorithm in Python.
"""
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2  # Finding the mid of the array
        L = arr[:mid]        # Dividing the array elements into 2 halves
        R = arr[mid:]

        merge_sort(L)        # Sorting the first half
        merge_sort(R)        # Sorting the second half

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr      
try:
    input_data = list(map(int, input("Enter numbers to sort, separated by spaces: ").split()))
    sorted_data = merge_sort(input_data)
    print("Sorted array:", sorted_data)
except ValueError:
    print("Please enter valid integers separated by spaces.")
