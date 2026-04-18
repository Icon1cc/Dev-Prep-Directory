"""
Write a pythong program to check if a string is a rotated version of another string.
example: "abcd" and "cdab" are rotated versions of each other.
"""

def is_rotated(str1, str2):
    if len(str1) != len(str2):
        return False
    temp = str1 + str1
    return str2 in temp

try:
    string1 = input("Enter the first string: ")
    string2 = input("Enter the second string: ")
    if is_rotated(string1, string2):
        print(f'"{string2}" is a rotated version of "{string1}".')
    else:
        print(f'"{string2}" is not a rotated version of "{string1}".')
except Exception as e:
    print(f"An error occurred: {e}")