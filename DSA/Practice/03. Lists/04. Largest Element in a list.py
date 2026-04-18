"""
Write a Python function to find the largest element in a list.
"""

def find_largest_element(input_list):
    if not input_list:
        return None
    largest = input_list[0]
    for item in input_list:
        if item > largest:
            largest = item
    return largest

try:
    user_input = input("Enter a list of numbers separated by commas: ")
    num_list = [int(num.strip()) for num in user_input.split(',')]
    largest_element = find_largest_element(num_list)
    if largest_element is not None:
        print(f"The largest element is: {largest_element}")
    else:
        print("The list is empty.")
except ValueError:
    print("Invalid input. Please enter numbers separated by commas.")
    
    