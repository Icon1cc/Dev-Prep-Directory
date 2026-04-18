"""
Description: Write a function compare_lists(list1, list2) that takes two lists as input. The function should return a tuple containing three sets:
A set of items that are unique to list1.
A set of items that are unique to list2.
A set of items that are common to both lists.
Example:
Input: list1 = [1, 2, 3, 4, 5], list2 = [4, 5, 6, 7, 8]
Output: ({1, 2, 3}, {6, 7, 8}, {4, 5})
"""

def compare_lists(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    newset1 = set1 - set2
    newset2 = set2 - set1
    newset3 = set1 & set2
    
    return (newset1, newset2, newset3)

list1 = input("Enter elements for list1 separated by spaces: ").split()
list2 = input("Enter elements for list2 separated by spaces: ").split()

list1 = [int(x) for x in list1]
list2 = [int(x) for x in list2]

result = compare_lists(list1, list2)

print("Unique to list1:", result[0])
print("Unique to list2:", result[1])
print("Common to both:", result[2])


    