"""
Bitwise Permission Manager
Description: You are building a permission system where user permissions are stored in a single integer. The permissions are defined as follows: READ = 4, WRITE = 2, EXECUTE = 1. Write a function manage_permissions(current_permissions, action, permission_type) that modifies the permissions.
current_permissions: An integer representing the current permission set.
action: A string, either "ADD" or "REMOVE".
permission_type: An integer, one of READ, WRITE, or EXECUTE.
The function should return the new integer representing the updated permissions.
Example 1:
Input: current_permissions = 5 (READ + EXECUTE), action = "ADD", permission_type = 2 (WRITE)
Output: 7 (READ + WRITE + EXECUTE)
Example 2:
Input: current_permissions = 7 (READ + WRITE + EXECUTE), action = "REMOVE", permission_type = 4 (READ)
Output: 3 (WRITE + EXECUTE)
"""
def manage_permissions(current_permissions, action, permission_type):
    READ = 4
    WRITE = 2
    EXECUTE = 1

    if action == "ADD":
        result = current_permissions | permission_type
    else:
        result = current_permissions & ~permission_type

    return result

current_permissions = int(input("Enter current permissions: "))
action = input("Enter action (ADD or REMOVE): ").strip().upper()
permission_type = int(input("Enter permission type (4=READ, 2=WRITE, 1=EXECUTE): "))

new_permissions = manage_permissions(current_permissions, action, permission_type)

print("Updated permissions:", new_permissions)

