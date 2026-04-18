"""
Description: Write a function count_word_frequency(filepath) that takes a string representing a file path. The function should read the text file, count the frequency of each word, and return the result as a dictionary.
The counting should be case-insensitive (e.g., "Python" and "python" are the same word). All punctuation (., ,, !, ?, etc.) should be ignored and not counted as part of a word.
Example: Assume a file named sample.txt contains the following text: "Hello world! This is a test. Hello again."
Input: count_word_frequency('sample.txt')
Output: {'hello': 2, 'world': 1, 'this': 1, 'is': 1, 'a': 1, 'test': 1, 'again': 1}
Constraints:
The function should handle the FileNotFoundError if the specified file does not exist.
"""

import string  # to remove punctuation

def count_word_frequency(filepath):
	try:
		with open(filepath, "r") as file:
			content = file.read().lower()
			
			# remove punctuation
			for char in string.punctuation:
				content = content.replace(char, "")
			
			counts = {}
			for word in content.split():
				if word not in counts:
					counts[word] = 1
				else:
					counts[word] += 1
		
		return counts

	except FileNotFoundError:
		print("File not found.")
		return False

filepath = input("Enter only the correct filepath: ")
print(count_word_frequency(filepath))