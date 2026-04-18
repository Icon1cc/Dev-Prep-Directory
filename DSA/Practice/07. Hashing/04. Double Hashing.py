"""
Implementation of Open Addressing using Double Hashing.
"""

# 1. Define the Tombstone for soft deletions
TOMBSTONE = object()

def is_prime(n):
    """Check if a number is prime."""
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def next_prime(n):
    """Find the first prime number greater than n."""
    if n <= 1: return 2
    while True:
        n += 1
        if is_prime(n):
            return n

class DoubleHashingHashTable:
    def __init__(self, size=11):
        # Size must be Prime for Double Hashing to work reliably
        self.size = size if is_prime(size) else next_prime(size)
        self.table = [None] * self.size
        self.count = 0 

    def _hash1(self, key):
        return abs(hash(key)) % self.size

    def _hash2(self, key):
        # Returns a step size. Must be > 0.
        # Ideally: 1 + (hash % (size - 1))
        # Since size is Prime, any step size in range [1, size-1] is valid (coprime).
        return 1 + (abs(hash(key)) % (self.size - 1))

    def insert(self, key, value):
        if self.count / self.size >= 0.7:
            self._resize()

        index = self._hash1(key)
        step_size = self._hash2(key)
        original_index = index
        first_tombstone_index = None

        while self.table[index] is not None:
            # Check for update
            if self.table[index] is not TOMBSTONE and self.table[index][0] == key:
                self.table[index] = (key, value)
                return
            
            # Remember the first tombstone (recyclable spot)
            if self.table[index] is TOMBSTONE and first_tombstone_index is None:
                first_tombstone_index = index

            index = (index + step_size) % self.size
            if index == original_index:
                raise Exception("Hash table full")

        # Insert at the first tombstone found, OR the empty slot
        target_index = first_tombstone_index if first_tombstone_index is not None else index
        
        self.table[target_index] = (key, value)
        self.count += 1

    def search(self, key):
        index = self._hash1(key)
        step_size = self._hash2(key)
        original_index = index

        while self.table[index] is not None:
            if self.table[index] is not TOMBSTONE and self.table[index][0] == key:
                return self.table[index][1]
            
            index = (index + step_size) % self.size
            if index == original_index:
                break
        return None

    def delete(self, key):
        index = self._hash1(key)
        step_size = self._hash2(key)
        original_index = index

        while self.table[index] is not None:
            if self.table[index] is not TOMBSTONE and self.table[index][0] == key:
                self.table[index] = TOMBSTONE  # Soft delete!
                self.count -= 1
                return True
            
            index = (index + step_size) % self.size
            if index == original_index:
                break
        return False

    def _resize(self):
        old_table = self.table
        # FIX: Find the next PRIME number, don't just multiply by 2
        self.size = next_prime(self.size * 2)
        self.table = [None] * self.size
        self.count = 0

        for item in old_table:
            # Only re-insert valid items (Skip None and Tombstones)
            if item is not None and item is not TOMBSTONE:
                self.insert(item[0], item[1])

# --- Main Execution ---
if __name__ == "__main__":
    ht = DoubleHashingHashTable(size=5) # Start small to force collision/resize logic

    print(f"Created table size: {ht.size}") # Should be 5 (Prime)

    ht.insert("apple", 100)
    ht.insert("banana", 200)
    ht.insert("cherry", 300)
    
    print("Search apple:", ht.search("apple")) # 100
    
    ht.delete("banana")
    print("Search banana (deleted):", ht.search("banana")) # None
    
    # This search would FAIL in your old code because of the "hole" left by banana
    # But here, it skips the Tombstone and finds cherry.
    print("Search cherry:", ht.search("cherry"))