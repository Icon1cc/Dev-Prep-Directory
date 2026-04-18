"""
Write a Python function to remove duplicates from a sorted array.
"""

def remove_duplicates(sorted_list):
    if not sorted_list:
        return []
    
    write_index = 1
    for read_index in range(1, len(sorted_list)):
        if sorted_list[read_index] != sorted_list[read_index - 1]:
            sorted_list[write_index] = sorted_list[read_index]
            write_index += 1
    return write_index

try:
    user_input = input("Enter a sorted list of numbers separated by commas: ")
    num_list = [int(num.strip()) for num in user_input.split(',')]
    new_length = remove_duplicates(num_list)
    print("List after removing duplicates:", num_list[:new_length])
except ValueError:
    print("Invalid input. Please enter numbers separated by commas.")  
