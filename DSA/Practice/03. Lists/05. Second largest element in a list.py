"""
Write a Python function to find the second largest element in a list.
"""

def second_largest_element(input_list):
    if len(input_list) < 2:
        return None
    first, second = float('-inf'), float('-inf')
    for item in input_list:
        if item > first:
            second = first
            first = item
        elif first > item > second:
            second = item
    return second if second != float('-inf') else None

try:
    user_input = input("Enter a list of numbers separated by commas: ")
    num_list = [int(num.strip()) for num in user_input.split(',')]
    second_largest = second_largest_element(num_list)
    if second_largest is not None:
        print(f"The second largest element is: {second_largest}")
    else:
        print("The list does not have a second largest element.")
except ValueError:
    print("Invalid input. Please enter numbers separated by commas.")