"""
Write a python function that reverses a given array. The function should return the reversed array.
"""

def reverse_array(arr, n):
    start = 0
    end = n - 1
    while start < end:
        arr[start], arr[end] = arr[end], arr[start]
        start += 1
        end -= 1
    return arr
try:
    user_input = input("Enter the elements of the array separated by spaces: ")
    arr = [int(x) for x in user_input.split()]
    n = len(arr)
    reversed_arr = reverse_array(arr, n)
    print("Reversed array:", reversed_arr)
except ValueError:
    print("Invalid input. Please enter integers separated by spaces.")