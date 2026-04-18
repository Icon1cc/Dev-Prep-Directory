"""
Interactive Python Dictionary Tool.
Supports: Add/Update, Remove (Pop), Search (Get), View Keys/Values, and Merge.
"""

class CustomDict:
    def __init__(self):
        self.data = {}

    # --- Basic CRUD Operations ---
    def add_or_update(self, key, value):
        """Adds a new pair or updates existing key."""
        # In dicts, adding and updating are the same syntax
        self.data[key] = value

    def remove(self, key):
        """Removes a key safely. Returns the value or None."""
        # .pop(key, default) prevents crashing if key is missing
        return self.data.pop(key, None)

    def get_value(self, key):
        """Gets value safely."""
        return self.data.get(key, "Not Found")

    def exists(self, key):
        """Checks if key exists."""
        return key in self.data

    # --- View Operations ---
    def show_keys(self):
        return list(self.data.keys())

    def show_values(self):
        return list(self.data.values())

    def show_items(self):
        return list(self.data.items())

    # --- Advanced Operation: Merge ---
    def merge(self, other_dict):
        """
        Merges another dictionary into this one.
        Note: If keys overlap, the new dictionary overrides the old one.
        """
        # Python 3.9+ supports the '|' operator for merging
        # For compatibility, we can also use .update()
        self.data.update(other_dict)

    def __str__(self):
        return str(self.data)

# --- Main Interactive Menu ---
if __name__ == "__main__":
    print("--- Dictionary Operations Tool ---")
    my_dict = CustomDict()
    
    # Pre-populate for fun
    my_dict.add_or_update("brand", "Ford")
    my_dict.add_or_update("model", "Mustang")
    my_dict.add_or_update("year", "1964")

    while True:
        print(f"\nCurrent Dictionary: {my_dict}")
        print("-" * 35)
        print("1. Add / Update Key-Value")
        print("2. Remove Key (Pop)")
        print("3. Get Value by Key")
        print("4. Check Key Existence")
        print("5. Show Keys / Values / Items")
        print("6. Merge Another Dictionary")
        print("7. Exit")
        
        choice = input("Choose operation (1-7): ").strip()

        if choice == '1':
            k = input("Enter Key: ")
            v = input("Enter Value: ")
            my_dict.add_or_update(k, v)
            print(f">> Updated '{k}'.")

        elif choice == '2':
            k = input("Enter Key to remove: ")
            removed_val = my_dict.remove(k)
            if removed_val:
                print(f">> Removed '{k}' (Value was: {removed_val})")
            else:
                print(f">> Key '{k}' not found.")

        elif choice == '3':
            k = input("Enter Key to search: ")
            val = my_dict.get_value(k)
            print(f">> Value: {val}")

        elif choice == '4':
            k = input("Enter Key check: ")
            exists = my_dict.exists(k)
            print(f">> Exists? {exists}")

        elif choice == '5':
            print(f"Keys:   {my_dict.show_keys()}")
            print(f"Values: {my_dict.show_values()}")
            print(f"Items:  {my_dict.show_items()}")

        elif choice == '6':
            print("--- Create a mini-dict to merge ---")
            temp_dict = {}
            raw = input("Enter pairs like 'color red, price 500': ").split(',')
            try:
                for pair in raw:
                    # Logic to split "color red" into key/val
                    parts = pair.strip().split()
                    if len(parts) >= 2:
                        temp_dict[parts[0]] = parts[1]
                
                print(f"Merging {temp_dict} into main...")
                my_dict.merge(temp_dict)
                print(">> Merge Complete.")
            except Exception:
                print("Invalid format. Try 'key value, key value'")

        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")