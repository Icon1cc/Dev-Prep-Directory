"""
Write a Python function that checks if a given list is sorted in ascending order. If the list is sorted, the function should print Yes; otherwise, it should print No.
"""

def is_list_sorted(input_list):
    for i in range(len(input_list) - 1):
        if input_list[i] > input_list[i + 1]:
            return False
    return True

try:
    user_input = input("Enter a list of numbers separated by commas: ")
    num_list = [int(num.strip()) for num in user_input.split(',')]
    if is_list_sorted(num_list):
        print("Yes")
    else:
        print("No")
except ValueError:
    print("Invalid input. Please enter numbers separated by commas.")