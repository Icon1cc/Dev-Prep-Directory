"""
Description: Write a Python decorator named time_it. When this decorator is applied to any function, it should print the time the function took to execute, in seconds, before returning the function's result.
"""

import time

def time_it(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"The time taken by the function to execute is {end - start:.4f} seconds")
        return result
    return wrapper


@time_it
def greet_user():
    name = input("Enter your name: ")
    print(f"Hello, {name}!")

greet_user()