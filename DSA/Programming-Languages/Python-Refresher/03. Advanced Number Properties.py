"""
Description: Write a function check_number(n) that takes a positive integer n and determines if it is a prime number, a perfect square, or both.
The function should return a formatted string with the result.
If prime and a perfect square: "n is both a prime and a perfect square."
If only prime: "n is a prime number."
If only a perfect square: "n is a perfect square."
If neither: "n is neither a prime nor a perfect square."
Example 1:
Input: n = 7
Output: "7 is a prime number."
Example 2:
Input: n = 49
Output: "49 is a perfect square." (Note: 49 is not prime)
Example 3:
Input: n = 10
Output: "10 is neither a prime nor a perfect square."
"""

def check_number(n):
	if n <= 0:
		return "Please enter a positive integer."

	def is_prime(num):
		if num <= 1:
			return False
		for i in range(2, int(num**0.5) + 1):
			if num % i == 0:
				return False
		return True

	def is_perfect_square(num):
		return int(num**0.5) ** 2 == num

	prime = is_prime(n)
	square = is_perfect_square(n)

	if prime and square:
		return f"{n} is both a prime and a perfect square."
	elif prime:
		return f"{n} is a prime number."
	elif square:
		return f"{n} is a perfect square."
	else:
		return f"{n} is neither a prime nor a perfect square."


n = int(input("Enter a positive number: "))
result = check_number(n)
print(result)

