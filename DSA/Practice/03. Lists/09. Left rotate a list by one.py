"""
Write a Python function to left rotate a list by one.
"""
def myfunc(l):
    if len(l) <= 1:
        return l
    first_element = l[0]
    for i in range(len(l) - 1):
        l[i] = l[i + 1]
    l[-1] = first_element
    return l

try:
    user_input = input("Enter a list of elements separated by commas: ")
    elements = [elem.strip() for elem in user_input.split(',')]
    rotated_list = myfunc(elements)
    print("List after left rotation by one:", rotated_list)
except Exception as e:
    print("An error occurred:", e)