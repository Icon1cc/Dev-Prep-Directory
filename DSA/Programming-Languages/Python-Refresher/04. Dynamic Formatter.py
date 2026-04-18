"""
Description: Write a function dynamic_logger(message, *args, **kwargs) that creates a formatted log string. The function accepts a primary message string, a variable number of positional arguments (*args), and a variable number of keyword arguments (**kwargs).
The output string should start with "[LOG] ", followed by the message, then all positional arguments separated by commas, and finally all keyword arguments formatted as "key=value" pairs, separated by commas.
Example:
Input: dynamic_logger("User action", "login", "success", user_id=101, ip="192.168.1.1")
Output: "[LOG] User action: login, success | Details: user_id=101, ip=192.168.1.1"
"""


def dynamic_logger(message, *args, **kwargs):
    args_str = ", ".join(args) if args else ""
    kwargs_str = ", ".join(f"{key}={value}" for key, value in kwargs.items()) if kwargs else ""
    log_parts = [f"[LOG] {message}"]
    if args_str:
        log_parts.append(f": {args_str}")
    if kwargs_str:
        log_parts.append(f" | Details: {kwargs_str}")
    return "".join(log_parts)

# Get the main message
message = input("Enter the main message: ").strip()

# Get positional arguments
args_input = input("Enter positional arguments separated by commas (or leave blank): ").strip()
if args_input:
    args = [item.strip() for item in args_input.split(",")]
else:
    args = []

# Get keyword arguments
kwargs_input = input("Enter keyword arguments (key=value) separated by commas (or leave blank): ").strip()
kwargs = {}
if kwargs_input:
    pairs = kwargs_input.split(",")
    for pair in pairs:
        if "=" in pair:
            key, value = pair.split("=")
            kwargs[key.strip()] = value.strip()

# Call the function with unpacked args and kwargs
result = dynamic_logger(message, *args, **kwargs)

# Print the log
print(result)