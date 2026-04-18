"""
Write a function that takes an array of integers and returns a dictionary with the frequency of each element in the array.
"""

def element_frequencies(arr):
    frequency_dict = {}
    for num in arr:
        if num in frequency_dict:
            frequency_dict[num] += 1
        else:
            frequency_dict[num] = 1
    return frequency_dict

try:
    input = [int(x) for x in input("Enter integers separated by spaces: ").split()]
    frequencies = element_frequencies(input)    
    print("Frequencies of array elements:", frequencies)
except ValueError:
    print("Please enter valid integers.")