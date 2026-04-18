"""
Write a Python function that reverses a given list. The function should return the reversed list.
"""

def reverse_list(input_list):
    # return input_list[::-1]
    # reversed_list = []
    # for i in range(len(input_list) - 1, -1, -1):
    #     reversed_list.append(input_list[i])
    # return reversed_list
    s = 0
    e = len(input_list) - 1
    while s < e:
        input_list[s], input_list[e] = input_list[e], input_list[s]
        s += 1
        e -= 1
    return input_list

try:
    user_input = input("Enter a list of numbers separated by commas: ")
    num_list = [int(num.strip()) for num in user_input.split(',')]
    reversed_list = reverse_list(num_list)
    print("Reversed list:", reversed_list)
except ValueError:
    print("Invalid input. Please enter numbers separated by commas.")
