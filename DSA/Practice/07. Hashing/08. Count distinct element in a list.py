"""
Write a python function to count the number of distinct elements in a list.
"""

def count_distinct_elements(input_list):
    seen = set()
    for element in input_list:
        seen.add(element)
    return len(seen)

try:
    user_input = input("Enter a list of elements separated by spaces: ")
    input_list = user_input.split()
    distinct_count = count_distinct_elements(input_list)
    print(f"Number of distinct elements: {distinct_count}")
except Exception as e:
    print(f"An error occurred: {e}")
    