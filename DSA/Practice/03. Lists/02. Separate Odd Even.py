"""
Write a Python program to separate a list of numbers into odd and even lists.
"""

def separate_odd_even(numbers):
    odd_numbers = []
    even_numbers = []
    
    for number in numbers:
        if number % 2 == 0:
            even_numbers.append(number)
        else:
            odd_numbers.append(number)
    
    return odd_numbers, even_numbers

try:
    user_input = input("Enter numbers separated by commas: ")
    num_list = [int(num.strip()) for num in user_input.split(',')]
    odd_list, even_list = separate_odd_even(num_list)
    print(f"Odd numbers: {odd_list}")
    print(f"Even numbers: {even_list}")
except ValueError:
    print("Invalid input. Please enter numbers separated by commas.")