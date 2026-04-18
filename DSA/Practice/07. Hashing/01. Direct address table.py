"""
Implement a direct address table that supports insertion, deletion, and search operations for a set of integer keys within a fixed range.
"""

class DirectAddressTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def insert(self, key):
        if 0 <= key < self.size:
            self.table[key] = key
        else:
            print("Key out of bounds")

    def delete(self, key):
        if 0 <= key < self.size:
            self.table[key] = None
        else:
            print("Key out of bounds")

    def search(self, key):
        if 0 <= key < self.size:
            return self.table[key] is not None
        else:
            print("Key out of bounds")
            return False 
try:
    size = int(input("Enter the size of the direct address table: "))
    dat = DirectAddressTable(size)

    while True:
        operation = input("Enter operation (insert, delete, search, exit): ").strip().lower()
        if operation == "insert":
            key = int(input("Enter key to insert: "))
            dat.insert(key)
        elif operation == "delete":
            key = int(input("Enter key to delete: "))
            dat.delete(key)
        elif operation == "search":
            key = int(input("Enter key to search: "))
            found = dat.search(key)
            print(f"Key {key} found: {found}")
        elif operation == "exit":
            break
        else:
            print("Invalid operation. Please try again.")
except ValueError:
    print("Invalid input. Please enter integers only.")