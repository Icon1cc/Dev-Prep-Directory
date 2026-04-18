"""
Write a python function to compute the square root of a given non-negative number using the binary search algorithm.
"""
def square_root(n):
    left = 1
    right = n
    mid = (left + right) // 2
    while left <= right:
        mid_squared = mid * mid
        if mid_squared == n:
            return mid
        elif mid_squared < n:
            left = mid + 1
        else:
            right = mid - 1
        mid = (left + right) // 2
    return right

try:
    number = float(input("Enter a non-negative number to find its square root: "))
    if number < 0:
        print("Please enter a non-negative number.")
    else:
        result = square_root(number)
        print(f"The square root of {number} is approximately {result}.")
except ValueError:
    print("Invalid input. Please enter a valid non-negative number.")