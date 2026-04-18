"""
Implementation of own hash class using chaining for collision resolution.
"""

class HashTable:
    def __init__(self, size):
        # We use the size provided by the user
        self.size = size
        # Create 'size' number of empty buckets
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        # The hash function ensures the index is always within 0 to size-1
        return abs(hash(key)) % self.size

    def insert(self, key, value):
        index = self._hash(key)
        bucket = self.table[index]

        # Check if key exists to update it
        for i, (k, v) in enumerate(bucket):
            if k == key:
                print(f"   -> Key '{key}' exists. Updating value.")
                bucket[i] = (key, value)
                return

        # Collision handling: Append to the chain
        bucket.append((key, value))
        print(f"   -> Inserted ({key}: {value}) at index {index}")

    def get(self, key):
        index = self._hash(key)
        bucket = self.table[index]
        
        for k, v in bucket:
            if k == key:
                return v
        return None

    def delete(self, key):
        index = self._hash(key)
        bucket = self.table[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                print(f"   -> Deleted key '{key}'")
                return True
        return False

    def display(self):
        print(f"\n--- Hash Table (Size: {self.size}) ---")
        for i, bucket in enumerate(self.table):
            print(f"Index {i}: {bucket}")
        print("----------------------------------\n")


# --- Driver Code ---
if __name__ == "__main__":
    try:
        # STEP 1: Ask the user for the size explicitly
        user_size = int(input("Enter the size of the Hash Table: "))
        
        # Create the table with the user's chosen size
        ht = HashTable(user_size)
        print(f"Successfully created a Hash Table of size {user_size}.\n")

        while True:
            command = input("Enter command (insert, get, delete, show, exit): ").strip().lower()
            
            if command == "insert":
                key = input("  Key: ")
                val = input("  Value: ")
                ht.insert(key, val)
                
            elif command == "get":
                key = input("  Key: ")
                result = ht.get(key)
                print(f"   -> Value: {result}" if result else "   -> Key not found.")
                    
            elif command == "delete":
                key = input("  Key: ")
                if not ht.delete(key):
                    print("   -> Key not found.")
            
            elif command == "show":
                ht.display()
                
            elif command == "exit":
                break
            
            else:
                print("Invalid command.")
                
    except ValueError:
        print("Error: Please enter a valid integer for the size.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")