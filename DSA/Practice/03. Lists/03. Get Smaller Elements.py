"""
Write a Python function that accepts a list and a number, and returns a new list containing
only the elements from the original list that are smaller than the given number.
"""

def get_smaller_elements(input_list, threshold):
    return [item for item in input_list if item < threshold]

try:
    user_input = input("Enter a list of numbers separated by commas: ")
    num_list = [int(num.strip()) for num in user_input.split(',')]
    threshold_input = int(input("Enter the threshold number: "))
    smaller_elements = get_smaller_elements(num_list, threshold_input)
    print(f"Elements smaller than {threshold_input}: {smaller_elements}")
except ValueError:
    print("Invalid input. Please enter numbers separated by commas and a valid threshold number.")