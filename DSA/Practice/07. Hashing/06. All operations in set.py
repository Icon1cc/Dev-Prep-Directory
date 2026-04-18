"""
Interactive Python Set with Menu-Driven Operations.
Supports: Add, Remove, Update, Union, Intersection, Difference, Symmetric Diff.
"""

class CustomSet:
    def __init__(self, elements=None):
        self.data = set(elements) if elements else set()

    # --- Basic ---
    def add(self, element):
        self.data.add(element)
    
    def remove(self, element):
        self.data.remove(element)       # Raises Error if missing
    
    def discard(self, element):
        self.data.discard(element)      # Safe remove
        
    def update_val(self, old, new):
        if old in self.data:
            self.data.remove(old)
            self.data.add(new)
        else:
            print(f"Error: '{old}' not found.")

    # --- Math Operations ---
    def union(self, other):
        return self.data | other.data
    
    def intersection(self, other):
        return self.data & other.data
    
    def difference(self, other):
        return self.data - other.data
    
    def symmetric_difference(self, other):
        return self.data ^ other.data

    def __str__(self):
        return str(self.data)

# --- Main Interactive Menu ---
if __name__ == "__main__":
    print("--- Set Operations Tool ---")
    
    # 1. Get User Input for Two Sets
    in1 = input("Enter Set A elements (space-separated): ").split()
    in2 = input("Enter Set B elements (space-separated): ").split()
    
    set_a = CustomSet(in1)
    set_b = CustomSet(in2)
    
    while True:
        print(f"\nCurrent Set A: {set_a}")
        print(f"Current Set B: {set_b}")
        print("-" * 30)
        print("1. Union (|)")
        print("2. Intersection (&)")
        print("3. Difference (A - B)")
        print("4. Symmetric Difference (^)")
        print("5. Add to Set A")
        print("6. Remove from Set A")
        print("7. Exit")
        
        choice = input("Choose an operation (1-7): ").strip()
        
        if choice == '1':
            result = set_a.union(set_b)
            print(f"\n>> Union Result: {result}")
            
        elif choice == '2':
            result = set_a.intersection(set_b)
            print(f"\n>> Intersection Result: {result}")
            
        elif choice == '3':
            result = set_a.difference(set_b)
            print(f"\n>> Difference (A-B) Result: {result}")
            
        elif choice == '4':
            result = set_a.symmetric_difference(set_b)
            print(f"\n>> Symmetric Diff Result: {result}")
            
        elif choice == '5':
            val = input("Value to add to A: ")
            set_a.add(val)
            print(">> Added.")
            
        elif choice == '6':
            val = input("Value to remove from A: ")
            set_a.discard(val) # Using discard (safe)
            print(">> Removed (if existed).")
            
        elif choice == '7':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Try again.")