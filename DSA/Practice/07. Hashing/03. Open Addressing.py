"""
Complete Implementation of Open Addressing Hash Table (Linear Probing).
Features:
- Auto-resizing (Dynamic Capacity)
- Tombstone handling for Deletions
- Flexible/Default initialization size
"""

# Unique marker for deleted items ("Soft Delete").
# We cannot use 'None' because that breaks the search chain.
TOMBSTONE = object()

class OpenAddressingHashTable:
    def __init__(self, size=11):
        # Default size is 11 (Prime number), but user can override it.
        self.size = size
        self.table = [None] * size
        self.count = 0  # Tracks active items

    def _hash(self, key):
        # Maps a key to an index: 0 to size-1
        return abs(hash(key)) % self.size

    def insert(self, key, value):
        # 1. Check Load Factor (0.7) and Resize if needed
        if self.count / self.size >= 0.7:
            self._resize()

        index = self._hash(key)
        original_index = index
        first_tombstone_index = None

        # 2. Linear Probe: Find key to update OR find empty slot
        while self.table[index] is not None:
            # Case A: Key found! Update the value.
            if self.table[index] is not TOMBSTONE and self.table[index][0] == key:
                self.table[index] = (key, value)
                return
            
            # Case B: Found a Tombstone. Remember this spot!
            # We can recycle this index later if the key isn't found elsewhere.
            if self.table[index] is TOMBSTONE and first_tombstone_index is None:
                first_tombstone_index = index

            # Move to next slot (Linear Probing)
            index = (index + 1) % self.size
            
            # Safety check: Prevent infinite loop if table is full (unlikely due to resize)
            if index == original_index:
                raise Exception("Hash table is full")

        # 3. Final Insertion
        # If we saw a tombstone earlier, recycle that spot. 
        # Otherwise, use the empty (None) spot we just landed on.
        target_index = first_tombstone_index if first_tombstone_index is not None else index
        
        self.table[target_index] = (key, value)
        self.count += 1

    def search(self, key):
        index = self._hash(key)
        original_index = index

        while self.table[index] is not None:
            # Check if key matches (Ignore Tombstones)
            if self.table[index] is not TOMBSTONE and self.table[index][0] == key:
                return self.table[index][1]

            index = (index + 1) % self.size
            if index == original_index:
                break
        
        return None

    def delete(self, key):
        index = self._hash(key)
        original_index = index

        while self.table[index] is not None:
            # Check if key matches
            if self.table[index] is not TOMBSTONE and self.table[index][0] == key:
                # MARK AS DELETED (Do not set to None!)
                self.table[index] = TOMBSTONE
                self.count -= 1
                return True

            index = (index + 1) % self.size
            if index == original_index:
                break
        
        return False

    def _resize(self):
        print(f"   [System] Resizing table from {self.size} to {self.size * 2}...")
        old_table = self.table
        self.size *= 2
        self.table = [None] * self.size
        self.count = 0

        # Re-hash all valid items into the new, larger table
        for item in old_table:
            if item is not None and item is not TOMBSTONE:
                self.insert(item[0], item[1])

# --- Main Execution (Interactive) ---
if __name__ == "__main__":
    print("--- Open Addressing Hash Table (Linear Probing) ---")
    
    # 1. Setup the Table Size (Dynamic Input)
    try:
        user_input = input("Enter initial size (or press Enter for default 11): ").strip()
        if user_input:
            ht = OpenAddressingHashTable(int(user_input))
            print(f"-> Created Hash Table of size {int(user_input)}.\n")
        else:
            ht = OpenAddressingHashTable() # Uses default 11
            print(f"-> Created Hash Table of size {ht.size} (Default).\n")
    except ValueError:
        print("Invalid number. Using default size 11.")
        ht = OpenAddressingHashTable()

    # 2. Command Loop
    print("Commands: insert <key> <val>, search <key>, delete <key>, exit")
    
    while True:
        try:
            raw_input = input(">> ").strip().split()
            if not raw_input: continue
            
            cmd = raw_input[0].lower()

            if cmd == "exit":
                break

            elif cmd == "insert" and len(raw_input) == 3:
                key, val = raw_input[1], raw_input[2]
                ht.insert(key, val)
                print(f"   Inserted ({key}: {val})")

            elif cmd == "search" and len(raw_input) == 2:
                key = raw_input[1]
                result = ht.search(key)
                if result:
                    print(f"   Found: {result}")
                else:
                    print("   Key not found.")

            elif cmd == "delete" and len(raw_input) == 2:
                key = raw_input[1]
                if ht.delete(key):
                    print(f"   Deleted '{key}'.")
                else:
                    print("   Key not found.")
            
            else:
                print("   Invalid command. Usage: insert k v | search k | delete k")

        except Exception as e:
            print(f"   Error: {e}")