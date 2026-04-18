"""
Write a Python program to calculate the average (mean) of a list of numbers.
"""
"""
Write a Python program to calculate the average (mean) of a list of numbers.
"""

def average_func(mylist):
    sum = 0
    for i in mylist:
        sum = sum + i
    return sum/len(mylist)

"""
return (sum(mylist)/len(mylist))
"""

try:
    mylist = input("Enter the numbers separated by comma: ")
    x = [int(item.strip()) for item in mylist.split(',')]
    result = average_func(x)
    if result:
        print(f"The mean of the given list is: {result}")
except ValueError:
    print("Invalid input. Please enter a correct number and use commas for separation")