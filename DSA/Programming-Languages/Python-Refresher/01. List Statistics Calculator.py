"""
List Statistics Calculator
Description: Given a list of integers numbers, write a function analyze_list(numbers) that calculates and returns its primary statistical properties.
The function must return a dictionary with three keys:
"mean": The average of the numbers.
"median": The middle value of the sorted list. If the list has an even number of elements, the median is the average of the two middle elements.
"mode": The number that appears most frequently in the list. If there is a tie for the most frequent number, you may return any one of the most frequent numbers.
Example:
Input: numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
Output: {'mean': 4.0, 'median': 4, 'mode': 5}
Notes:
You should handle the case of an empty input list gracefully (e.g., by returning a dictionary with None values or raising an error).
"""

def analyze_list(numbers):
	if not numbers: 
		return False

	mean = sum(numbers) / len(numbers)
	n = len(numbers)
	sorted_num = sorted(numbers)

	# median
	if n % 2 == 0:
		median = (sorted_num[n//2 - 1] + sorted_num[n//2]) / 2
	else:
		median = sorted_num[n//2]

	# mode
	counts = {}
	for num in numbers:
		if num not in counts:
			counts[num] = 1
		else:
			counts[num] += 1

	max_count = max(counts.values())
	mode = [num for num, freq in counts.items() if freq == max_count]

	return {"mean": mean, "median": median, "mode": mode}


numbers = input("Enter the numbers separated by commas: ")
x = [int(x.strip()) for x in numbers.split(',')]
print(analyze_list(x))
