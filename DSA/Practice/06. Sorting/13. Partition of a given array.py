"""
Write a function to partition a given array around a pivot such that all elements less than the pivot are on the left side and all elements greater than the pivot are on the right side.
"""

def partition_array(arr, pivot):
    left = []
    right = []
    
    for element in arr:
        if element < pivot:
            left.append(element)
        else:
            right.append(element)
    
    return left + right
try:
    input_array = list(map(int, input("Enter the elements of the array separated by spaces: ").split()))
    pivot = int(input("Enter the pivot element: "))
    result = partition_array(input_array, pivot)
    print("Partitioned array:", result)
except ValueError:
    print("Invalid input. Please enter integers only.")