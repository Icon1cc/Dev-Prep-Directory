# Hashing - Complete Reference Guide

## Table of Contents
1. [Direct Address Table](#direct-address-table) - [Code: 01. Direct address table.py](./01.%20Direct%20address%20table.py)
2. [Chaining](#chaining) - [Code: 02. Chaining.py](./02.%20Chaining.py)
3. [Open Addressing](#open-addressing) - [Code: 03. Open Addressing.py](./03.%20Open%20Addressing.py)
4. [Double Hashing](#double-hashing) - [Code: 04. Double Hashing.py](./04.%20Double%20Hashing.py)
5. [Frequencies of Array Elements](#frequencies-of-array-elements) - [Code: 05. Frequencies of Array Elements.py](./05.%20Frequencies%20of%20Array%20Elements.py)
6. [Set Operations](#set-operations) - [Code: 06. All operations in set.py](./06.%20All%20operations%20in%20set.py)
7. [Dictionary Operations](#dictionary-operations) - [Code: 07. All operations in a dictionary.py](./07.%20All%20operations%20in%20a%20dictionary.py)
8. [Count Distinct Elements](#count-distinct-elements) - [Code: 08. Count distinct element in a list.py](./08.%20Count%20distinct%20element%20in%20a%20list.py)

---

## Understanding Hashing

### What is Hashing?
Hashing is a technique to map data of arbitrary size to fixed-size values (hash codes) for efficient data retrieval, insertion, and deletion.

### Key Concepts

**Hash Function**: Converts a key into an array index
```
hash(key) → index in hash table
```

**Hash Table**: Array that stores key-value pairs using hash function

**Ideal Properties of Hash Function**:
1. **Deterministic**: Same input always produces same output
2. **Uniform Distribution**: Spreads keys evenly across table
3. **Fast Computation**: O(1) time to compute
4. **Minimize Collisions**: Different keys should map to different indices

### Collision Handling
When two keys hash to the same index:
- **Chaining**: Store multiple elements at same index (linked list)
- **Open Addressing**: Find another empty slot (linear probing, quadratic probing, double hashing)

---

## Direct Address Table
**📁 Implementation:** [01. Direct address table.py](./01.%20Direct%20address%20table.py)

### Problem
Store and retrieve elements where keys are small integers within a known range.

Example: Store presence of numbers 0-999

### Logic
Use an array where the key itself is the index. No hash function needed - direct mapping.

### How It Works
```python
class DirectAddressTable:
    def __init__(self, size):
        self.table = [None] * size
    
    def insert(self, key, value):
        self.table[key] = value
    
    def search(self, key):
        return self.table[key]
    
    def delete(self, key):
        self.table[key] = None
```

### Example
```
Keys: [5, 12, 8, 3]
Table: [None, None, None, 3, None, 5, None, None, 8, None, None, None, 12, ...]
Index:   0    1    2   3   4   5   6    7    8   9    10   11   12
```

### Time Complexity

| Operation | Complexity | Calculation |
|-----------|------------|-------------|
| Insert | O(1) | Direct index access |
| Search | O(1) | Direct index access |
| Delete | O(1) | Direct index access |

### Space Complexity
- **Space**: O(max_key) - Array size equals maximum key value

### Advantages
- Simplest hash table implementation
- O(1) operations guaranteed
- No collision handling needed

### Disadvantages
- **Wastes space** when key range is large but few keys used
- Only works with **integer keys** in small range
- Impractical for large key spaces (e.g., phone numbers)

### When to Use
- Keys are small non-negative integers (0 to n)
- Key range is reasonable (not too large)
- Need guaranteed O(1) operations
- Examples: Counting sort, boolean array for presence

---

## Chaining
**📁 Implementation:** [02. Chaining.py](./02.%20Chaining.py)

### Problem
Handle hash collisions by storing multiple elements at the same index.

### Logic
Each index in the hash table points to a linked list (or dynamic array) that stores all elements hashing to that index.

### How It Works
```python
class HashTableChaining:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]  # List of lists
    
    def hash_function(self, key):
        return key % self.size
    
    def insert(self, key, value):
        index = self.hash_function(key)
        # Check if key exists, update; otherwise append
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        self.table[index].append((key, value))
    
    def search(self, key):
        index = self.hash_function(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None
    
    def delete(self, key):
        index = self.hash_function(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                return True
        return False
```

### Visual Example
Hash table with size 7, hash function: `key % 7`

Insert: 10, 20, 15, 7, 12

```
Index 0: → [7] → [14] → [21]
Index 1: → [15]
Index 2: → 
Index 3: → [10]
Index 4: → 
Index 5: → [12]
Index 6: → [20]
```

### Time Complexity

| Operation | Average | Worst Case | Calculation |
|-----------|---------|------------|-------------|
| Insert | O(1) | O(n) | Average: constant chain length; Worst: all keys in one chain |
| Search | O(1 + α) | O(n) | α = load factor (n/m) |
| Delete | O(1 + α) | O(n) | Search + deletion |

**Load Factor (α)**: α = n/m where n = number of elements, m = table size

### Space Complexity
- **Space**: O(n + m) - n elements + m table slots

### Advantages
- Simple to implement
- Never fills up (can always add more elements)
- Good performance with good hash function
- Deletion is easy

### Disadvantages
- Extra space for links/pointers
- Cache performance may be poor (linked list traversal)
- Performance degrades if too many collisions

### When to Use
- Unknown number of elements
- Deletion is frequent
- Simple implementation preferred
- Can tolerate extra space for pointers

---

## Open Addressing
**📁 Implementation:** [03. Open Addressing.py](./03.%20Open%20Addressing.py)

### Problem
Handle collisions by finding another empty slot in the hash table itself (no external chaining).

### Probing Techniques

#### 1. Linear Probing
If slot `h(k)` is occupied, try `h(k) + 1`, `h(k) + 2`, ... until empty slot found.

```python
def linear_probe(key, i):
    return (hash(key) + i) % table_size
```

#### 2. Quadratic Probing
Use quadratic function: try `h(k)`, `h(k) + 1²`, `h(k) + 2²`, `h(k) + 3²`, ...

```python
def quadratic_probe(key, i):
    return (hash(key) + i * i) % table_size
```

#### 3. Double Hashing
Use second hash function: `h(k) + i × h2(k)`

```python
def double_hash_probe(key, i):
    return (hash1(key) + i * hash2(key)) % table_size
```

### Implementation (Linear Probing)
```python
class HashTableOpenAddressing:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size
        self.deleted = object()  # Sentinel for deleted slots
    
    def hash_function(self, key):
        return key % self.size
    
    def insert(self, key, value):
        index = self.hash_function(key)
        i = 0
        while self.table[(index + i) % self.size] is not None:
            if self.table[(index + i) % self.size] == self.deleted:
                break
            if self.table[(index + i) % self.size][0] == key:
                self.table[(index + i) % self.size] = (key, value)
                return
            i += 1
            if i == self.size:
                raise Exception("Hash table is full")
        self.table[(index + i) % self.size] = (key, value)
    
    def search(self, key):
        index = self.hash_function(key)
        i = 0
        while self.table[(index + i) % self.size] is not None:
            if self.table[(index + i) % self.size] != self.deleted:
                if self.table[(index + i) % self.size][0] == key:
                    return self.table[(index + i) % self.size][1]
            i += 1
            if i == self.size:
                return None
        return None
    
    def delete(self, key):
        index = self.hash_function(key)
        i = 0
        while self.table[(index + i) % self.size] is not None:
            if self.table[(index + i) % self.size] != self.deleted:
                if self.table[(index + i) % self.size][0] == key:
                    self.table[(index + i) % self.size] = self.deleted
                    return True
            i += 1
            if i == self.size:
                return False
        return False
```

### Time Complexity

| Operation | Average | Worst Case |
|-----------|---------|------------|
| Insert | O(1/(1-α)) | O(n) |
| Search | O(1/(1-α)) | O(n) |
| Delete | O(1/(1-α)) | O(n) |

Where α = load factor (should be < 0.7 for good performance)

### Space Complexity
- **Space**: O(m) - Only the table, no extra pointers

### Clustering Problem
**Primary Clustering (Linear Probing)**: Long chains of occupied slots form, increasing search time.

**Secondary Clustering (Quadratic Probing)**: Keys with same hash value follow same probe sequence.

**Solution**: Double hashing - different keys have different probe sequences.

### Advantages
- **Better cache performance** (data in contiguous memory)
- **No extra space** for pointers
- Simple implementation

### Disadvantages
- Table can become full
- **Performance degrades** as load factor increases
- Deletion is complex (need tombstones)
- Clustering issues

### When to Use
- Cache performance is critical
- Space is limited (no pointers)
- Load factor can be kept low
- Few deletions

---

## Double Hashing
**📁 Implementation:** [04. Double Hashing.py](./04.%20Double%20Hashing.py)

### Problem
Eliminate clustering in open addressing by using a second hash function for probing.

### Logic
Probe sequence: `(h1(key) + i × h2(key)) % table_size`

Two hash functions:
- **h1(key)**: Primary hash function
- **h2(key)**: Secondary hash function (determines step size)

### How It Works
```python
class DoubleHashing:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size
    
    def hash1(self, key):
        return key % self.size
    
    def hash2(self, key):
        # Should never return 0, use prime less than size
        prime = self.size - 1  # Assuming size is prime
        return prime - (key % prime)
    
    def probe(self, key, i):
        return (self.hash1(key) + i * self.hash2(key)) % self.size
    
    def insert(self, key, value):
        i = 0
        while i < self.size:
            index = self.probe(key, i)
            if self.table[index] is None:
                self.table[index] = (key, value)
                return
            i += 1
        raise Exception("Hash table is full")
```

### Example
Table size = 7, Insert: 19, 36, 5, 21

```
h1(k) = k % 7
h2(k) = 6 - (k % 6)

Insert 19:
  h1(19) = 5 → table[5] = 19

Insert 36:
  h1(36) = 1 → table[1] = 36

Insert 5:
  h1(5) = 5 (collision!)
  h2(5) = 6 - 5 = 1
  Try: (5 + 1×1) % 7 = 6 → table[6] = 5

Insert 21:
  h1(21) = 0 → table[0] = 21

Table: [21, 36, None, None, None, 19, 5]
```

### Requirements for h2(key)
1. **Never return 0** (would cause infinite loop)
2. **Relatively prime to table size** (ensures all slots probed)
3. Common choice: `h2(k) = prime - (k % prime)` where prime < table_size

### Time Complexity

| Operation | Average | Worst Case |
|-----------|---------|------------|
| Insert | O(1/(1-α)) | O(n) |
| Search | O(1/(1-α)) | O(n) |
| Delete | O(1/(1-α)) | O(n) |

Better than linear probing due to less clustering.

### Space Complexity
- **Space**: O(m) - Only the table

### Advantages
- **Eliminates primary clustering**
- **Better distribution** than linear/quadratic probing
- Still has cache benefits of open addressing

### Disadvantages
- More complex than linear probing
- Requires good second hash function
- Still can fill up

### When to Use
- Need better performance than linear probing
- Cache locality important
- Can design good second hash function

---

## Frequencies of Array Elements
**📁 Implementation:** [05. Frequencies of Array Elements.py](./05.%20Frequencies%20of%20Array%20Elements.py)

### Problem
Count the frequency (number of occurrences) of each element in an array.

Example: `[1, 2, 1, 3, 2, 1, 4]` → `{1: 3, 2: 2, 3: 1, 4: 1}`

### Approach 1: Using Dictionary/Hash Map (Best)
```python
def count_frequencies(arr):
    freq = {}
    for element in arr:
        freq[element] = freq.get(element, 0) + 1
    return freq
```

### Approach 2: Using Python Counter
```python
from collections import Counter

def count_frequencies(arr):
    return Counter(arr)
```

### Approach 3: Naive (Without Hashing)
```python
def count_frequencies_naive(arr):
    freq = []
    for element in arr:
        found = False
        for i, (el, count) in enumerate(freq):
            if el == element:
                freq[i] = (el, count + 1)
                found = True
                break
        if not found:
            freq.append((element, 1))
    return freq
```

### Time Complexity

| Approach | Complexity | Calculation |
|----------|------------|-------------|
| Hash Map | O(n) | Single pass through array, O(1) hash operations |
| Counter | O(n) | Built-in optimized hash implementation |
| Naive | O(n²) | For each element, search in frequency list |

### Space Complexity
- **Hash Map**: O(k) where k = number of distinct elements
- **Naive**: O(k)

### Example
```python
arr = [10, 20, 10, 30, 10, 20]

# Using hash map
freq = count_frequencies(arr)
# Output: {10: 3, 20: 2, 30: 1}

# Print frequencies
for element, count in freq.items():
    print(f"{element} appears {count} times")
```

### Applications
- Finding most frequent element
- Detecting duplicates
- Statistics and analysis
- Character frequency in strings
- Histogram generation

### When to Use
- Need to count occurrences efficiently
- Looking for modes/frequency patterns
- Checking for unique elements

---

## Set Operations
**📁 Implementation:** [06. All operations in set.py](./06.%20All%20operations%20in%20set.py)

### Problem
Perform various operations on sets: Add, Remove, Update, Union, Intersection, Difference, Symmetric Difference.

### Set Basics
A **set** is an unordered collection of unique elements. Implemented using hash tables for O(1) operations.

### Operations

#### 1. Add Element
```python
s = {1, 2, 3}
s.add(4)  # {1, 2, 3, 4}
s.add(2)  # {1, 2, 3, 4} (no duplicates)
```

#### 2. Remove Element
```python
s.remove(2)     # Removes 2, raises KeyError if not found
s.discard(2)    # Removes 2, no error if not found
element = s.pop()  # Removes and returns arbitrary element
```

#### 3. Update (Add Multiple)
```python
s.update([5, 6, 7])  # {1, 3, 4, 5, 6, 7}
s.update({8, 9}, [10])  # Can take multiple iterables
```

#### 4. Union (A ∪ B)
All elements from both sets
```python
a = {1, 2, 3}
b = {3, 4, 5}
result = a | b  # {1, 2, 3, 4, 5}
# or
result = a.union(b)
```

#### 5. Intersection (A ∩ B)
Common elements in both sets
```python
a = {1, 2, 3}
b = {2, 3, 4}
result = a & b  # {2, 3}
# or
result = a.intersection(b)
```

#### 6. Difference (A - B)
Elements in A but not in B
```python
a = {1, 2, 3}
b = {2, 3, 4}
result = a - b  # {1}
# or
result = a.difference(b)
```

#### 7. Symmetric Difference (A △ B)
Elements in either A or B, but not in both
```python
a = {1, 2, 3}
b = {2, 3, 4}
result = a ^ b  # {1, 4}
# or
result = a.symmetric_difference(b)
```

### Time Complexity

| Operation | Average | Worst Case |
|-----------|---------|------------|
| Add | O(1) | O(n) |
| Remove | O(1) | O(n) |
| Search (in) | O(1) | O(n) |
| Union | O(len(a) + len(b)) | O(len(a) × len(b)) |
| Intersection | O(min(len(a), len(b))) | O(len(a) × len(b)) |
| Difference | O(len(a)) | O(len(a) × len(b)) |

### Space Complexity
- O(n) for storing n elements

### Comprehensive Example
```python
# Create sets
a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}

# Add
a.add(10)  # {1, 2, 3, 4, 5, 10}

# Remove
a.remove(10)  # {1, 2, 3, 4, 5}

# Update
a.update([6, 7])  # {1, 2, 3, 4, 5, 6, 7}

# Union
union = a | b  # {1, 2, 3, 4, 5, 6, 7, 8}

# Intersection
intersection = a & b  # {4, 5, 6, 7}

# Difference
diff_a = a - b  # {1, 2, 3}
diff_b = b - a  # {8}

# Symmetric Difference
sym_diff = a ^ b  # {1, 2, 3, 8}

# Check membership
print(3 in a)  # True
print(10 in a)  # False

# Set size
print(len(a))
```

### Applications
- Removing duplicates from list: `unique = list(set(arr))`
- Finding common elements
- Checking subsets/supersets
- Mathematical set operations
- Unique character counting

---

## Dictionary Operations
**📁 Implementation:** [07. All operations in a dictionary.py](./07.%20All%20operations%20in%20a%20dictionary.py)

### Problem
Perform various operations on dictionaries: Add/Update, Remove (Pop), Search (Get), View Keys/Values, and Merge.

### Dictionary Basics
A **dictionary** stores key-value pairs using hash table implementation. Keys must be immutable and hashable.

### Operations

#### 1. Add/Update
```python
d = {'a': 1, 'b': 2}

# Add new key-value
d['c'] = 3  # {'a': 1, 'b': 2, 'c': 3}

# Update existing value
d['a'] = 10  # {'a': 10, 'b': 2, 'c': 3}

# Update with dictionary
d.update({'d': 4, 'e': 5})
```

#### 2. Remove (Pop)
```python
# Remove and return value
value = d.pop('a')  # Returns 10, d = {'b': 2, 'c': 3, 'd': 4, 'e': 5}

# Remove with default if key doesn't exist
value = d.pop('z', 0)  # Returns 0, no error

# Remove last inserted (Python 3.7+)
key, value = d.popitem()

# Delete without returning
del d['b']
```

#### 3. Search (Get)
```python
# Access value (raises KeyError if not found)
value = d['c']

# Safe access with default
value = d.get('c')     # Returns 3
value = d.get('z', 0)  # Returns 0 (default)

# Check if key exists
if 'c' in d:
    print("Key exists")
```

#### 4. View Keys/Values
```python
# Get all keys
keys = d.keys()  # dict_keys(['c', 'd', 'e'])

# Get all values
values = d.values()  # dict_values([3, 4, 5])

# Get all items (key-value pairs)
items = d.items()  # dict_items([('c', 3), ('d', 4), ('e', 5)])

# Iterate
for key in d:
    print(key, d[key])

for key, value in d.items():
    print(key, value)
```

#### 5. Merge Dictionaries
```python
d1 = {'a': 1, 'b': 2}
d2 = {'c': 3, 'd': 4}
d3 = {'b': 20, 'e': 5}

# Method 1: update() - modifies d1
d1.update(d2)  # d1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4}

# Method 2: Unpacking (Python 3.5+) - creates new dict
merged = {**d1, **d2, **d3}

# Method 3: Union operator (Python 3.9+)
merged = d1 | d2 | d3

# Later values overwrite earlier ones
# merged = {'a': 1, 'b': 20, 'c': 3, 'd': 4, 'e': 5}
```

### Time Complexity

| Operation | Average | Worst Case |
|-----------|---------|------------|
| Add/Update | O(1) | O(n) |
| Delete | O(1) | O(n) |
| Search/Get | O(1) | O(n) |
| Pop | O(1) | O(n) |
| Iterate Keys/Values | O(n) | O(n) |

### Space Complexity
- O(n) for storing n key-value pairs

### Comprehensive Example
```python
# Create dictionary
student = {
    'name': 'Alice',
    'age': 20,
    'grade': 'A'
}

# Add new field
student['major'] = 'Computer Science'

# Update existing
student['age'] = 21

# Search
name = student.get('name')  # 'Alice'
major = student.get('major', 'Undeclared')

# Remove
grade = student.pop('grade')  # Returns 'A'

# Check existence
if 'age' in student:
    print(f"Age: {student['age']}")

# View keys and values
print(student.keys())    # dict_keys(['name', 'age', 'major'])
print(student.values())  # dict_values(['Alice', 21, 'Computer Science'])

# Iterate
for key, value in student.items():
    print(f"{key}: {value}")

# Merge dictionaries
extra_info = {'year': 2024, 'semester': 'Spring'}
student.update(extra_info)

# Dictionary comprehension
squares = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

### Common Patterns

#### Frequency Counter
```python
def count_chars(s):
    freq = {}
    for char in s:
        freq[char] = freq.get(char, 0) + 1
    return freq
```

#### Grouping
```python
def group_by_length(words):
    groups = {}
    for word in words:
        length = len(word)
        if length not in groups:
            groups[length] = []
        groups[length].append(word)
    return groups
```

#### Default Dictionary Pattern
```python
from collections import defaultdict

# Automatically creates default value for missing keys
dd = defaultdict(list)
dd['key'].append('value')  # No KeyError
```

### Applications
- Caching/memoization
- Counting frequencies
- Grouping data
- Configuration storage
- JSON-like data structures

---

## Count Distinct Elements
**📁 Implementation:** [08. Count distinct element in a list.py](./08.%20Count%20distinct%20element%20in%20a%20list.py)

### Problem
Count the number of unique/distinct elements in a list.

Example: `[1, 2, 1, 3, 2, 1, 4]` → 4 distinct elements (1, 2, 3, 4)

### Approach 1: Using Set (Best)
```python
def count_distinct(arr):
    return len(set(arr))
```

**How it works**: Set automatically handles uniqueness, so converting to set and taking length gives distinct count.

### Approach 2: Using Dictionary
```python
def count_distinct_dict(arr):
    freq = {}
    for element in arr:
        freq[element] = True  # or freq[element] = 1
    return len(freq)
```

### Approach 3: Naive (Without Hashing)
```python
def count_distinct_naive(arr):
    distinct = []
    for element in arr:
        if element not in distinct:
            distinct.append(element)
    return len(distinct)
```

### Time Complexity

| Approach | Complexity | Calculation |
|----------|------------|-------------|
| Set | O(n) | Single pass, O(1) set operations |
| Dictionary | O(n) | Single pass, O(1) dict operations |
| Naive | O(n²) | For each element, search in list (O(n) search) |

### Space Complexity
- **Set/Dictionary**: O(k) where k = number of distinct elements
- **Naive**: O(k)

### Variations

#### Get Distinct Elements (Not Just Count)
```python
def get_distinct(arr):
    return list(set(arr))
    # Note: order not preserved

# To preserve order:
def get_distinct_ordered(arr):
    seen = set()
    result = []
    for element in arr:
        if element not in seen:
            seen.add(element)
            result.append(element)
    return result
```

#### Count Distinct in Range
```python
def count_distinct_in_range(arr, low, high):
    distinct = set()
    for element in arr:
        if low <= element <= high:
            distinct.add(element)
    return len(distinct)
```

### Example
```python
arr = [10, 20, 10, 30, 10, 20, 40]

# Count distinct
count = count_distinct(arr)
print(count)  # 4

# Get distinct elements
distinct = get_distinct(arr)
print(distinct)  # [40, 10, 20, 30] (order not guaranteed)

# Get distinct with preserved order
distinct_ordered = get_distinct_ordered(arr)
print(distinct_ordered)  # [10, 20, 30, 40]
```

### Applications
- Data deduplication
- Finding unique values
- Checking if all elements are unique: `len(arr) == len(set(arr))`
- Database DISTINCT operation
- Cardinality estimation

### Related Problems
- Check if array has duplicates: `len(arr) != len(set(arr))`
- Find first non-repeating element
- Find elements that appear only once

---

## Comparison Summary

### Time Complexity Table

| Operation | Best Approach | Time | Space | Notes |
|-----------|---------------|------|-------|-------|
| Direct Address Table | Array indexing | O(1) | O(max_key) | Only for small integer keys |
| Chaining - Insert | Linked list at index | O(1) avg | O(n+m) | m = table size |
| Open Addressing - Insert | Linear/Quadratic probe | O(1) avg | O(m) | Performance depends on load factor |
| Double Hashing - Insert | Two hash functions | O(1) avg | O(m) | Better than linear probing |
| Count Frequencies | Hash map | O(n) | O(k) | k = distinct elements |
| Set Operations | Hash set | O(1) per op | O(n) | Add, remove, search |
| Dictionary Operations | Hash map | O(1) per op | O(n) | Get, set, delete |
| Count Distinct | Convert to set | O(n) | O(k) | k = distinct elements |

---

## Hash Table Performance

### Load Factor (α)
```
α = n / m
where:
  n = number of elements
  m = table size
```

**Guidelines:**
- **Chaining**: Can exceed 1, typically keep α ≤ 1
- **Open Addressing**: Must be < 1, typically keep α ≤ 0.7

### Choosing Hash Function

**Good Hash Function Properties:**
1. Distributes keys uniformly
2. Fast to compute
3. Uses all available information in key
4. Minimizes collisions

**Common Hash Functions:**

#### Division Method
```python
hash(key) = key % table_size
```
- Simple and fast
- Table size should be prime
- Avoid powers of 2

#### Multiplication Method
```python
A = 0.6180339887  # (√5 - 1) / 2
hash(key) = floor(m * (key * A % 1))
```
- More uniform distribution
- Table size can be any value

#### Universal Hashing
```python
hash(key) = ((a * key + b) % p) % m
```
- a, b are random numbers
- p is large prime
- Provides theoretical guarantees

---

## Collision Resolution Comparison

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **Chaining** | Simple, never fills up, easy deletion | Extra space for pointers, poor cache | Unknown n, frequent deletions |
| **Linear Probing** | Cache-friendly, no pointers | Primary clustering, hard deletion | Low load factor, few deletions |
| **Quadratic Probing** | Reduces primary clustering | Secondary clustering, may not probe all | Medium load factor |
| **Double Hashing** | Best distribution | Complex, requires good h2() | High performance needed |

---

## Python Built-in Hashing

### Set Implementation
```python
# Python sets use hash tables
s = {1, 2, 3}

# Operations are O(1) average
s.add(4)        # O(1)
s.remove(2)     # O(1)
3 in s          # O(1)
```

### Dictionary Implementation
```python
# Python dicts use hash tables with open addressing
d = {'a': 1, 'b': 2}

# Operations are O(1) average
d['c'] = 3      # O(1)
d['a']          # O(1)
del d['b']      # O(1)
```

**Python's Hash Function:**
- Uses internal `hash()` function
- Integers: hash(n) = n (for small integers)
- Strings: Uses complex algorithm considering all characters
- Custom objects: Can override `__hash__()` and `__eq__()`

### Hashable vs Unhashable

**Hashable (can be dict keys/set elements):**
- Immutable types: int, float, str, tuple (of hashables), frozenset
- Custom objects (by default, based on id)

**Not Hashable:**
- Mutable types: list, dict, set
- These can't be used as dictionary keys or set elements

```python
# Valid
d = {1: 'a', 'key': 'value', (1, 2): 'tuple'}

# Invalid - will raise TypeError
# d = {[1, 2]: 'value'}  # list not hashable
# d = {{1, 2}: 'value'}  # set not hashable
```

---

## Common Hashing Patterns

### Pattern 1: Frequency Counter
```python
# Count occurrences
def count_frequency(arr):
    freq = {}
    for item in arr:
        freq[item] = freq.get(item, 0) + 1
    return freq

# Using Counter (cleaner)
from collections import Counter
freq = Counter(arr)
```

### Pattern 2: Two Sum Problem
```python
def two_sum(arr, target):
    seen = {}
    for i, num in enumerate(arr):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return None
```

### Pattern 3: Checking for Duplicates
```python
def has_duplicates(arr):
    return len(arr) != len(set(arr))

# Or within k distance
def has_nearby_duplicate(arr, k):
    seen = {}
    for i, num in enumerate(arr):
        if num in seen and i - seen[num] <= k:
            return True
        seen[num] = i
    return False
```

### Pattern 4: Grouping/Bucketing
```python
def group_anagrams(words):
    groups = {}
    for word in words:
        key = ''.join(sorted(word))
        if key not in groups:
            groups[key] = []
        groups[key].append(word)
    return list(groups.values())
```

### Pattern 5: Caching/Memoization
```python
def fibonacci_memo(n, cache={}):
    if n in cache:
        return cache[n]
    if n <= 1:
        return n
    cache[n] = fibonacci_memo(n-1, cache) + fibonacci_memo(n-2, cache)
    return cache[n]
```

---

## Advanced Topics

### Consistent Hashing
Used in distributed systems to minimize remapping when nodes are added/removed.

**Use Cases:**
- Load balancers
- Distributed caches (Memcached, Redis clusters)
- CDN routing

### Perfect Hashing
When the set of keys is known in advance, create a hash function with zero collisions.

**Properties:**
- O(1) worst-case lookup
- Used in compilers (keyword lookup)
- Requires preprocessing

### Bloom Filters
Space-efficient probabilistic data structure for set membership.

**Properties:**
- Can have false positives, never false negatives
- Uses multiple hash functions
- Very space efficient
- Used in: spell checkers, databases, network routers

---

## Common Problems Using Hashing

### Easy Problems
1. **Two Sum**: Find two numbers that add to target
2. **Contains Duplicate**: Check if array has duplicates
3. **Valid Anagram**: Check if two strings are anagrams
4. **First Unique Character**: Find first non-repeating character
5. **Intersection of Arrays**: Find common elements

### Medium Problems
1. **Group Anagrams**: Group strings that are anagrams
2. **Top K Frequent Elements**: Find k most frequent elements
3. **Longest Consecutive Sequence**: Find longest consecutive numbers
4. **Subarray Sum Equals K**: Count subarrays with sum k
5. **LRU Cache**: Implement cache with O(1) operations

### Hard Problems
1. **Longest Substring Without Repeating Characters**
2. **Minimum Window Substring**
3. **Substring with Concatenation of All Words**
4. **Design HashMap**: Implement from scratch

---

## Performance Tips

### 1. Choose Right Data Structure
```python
# For membership testing
use_set = set(arr)  # O(1) lookup
# Not: if x in arr  # O(n) lookup

# For counting
from collections import Counter
freq = Counter(arr)
# Not: manual dict with loops
```

### 2. Initialize with Expected Size
```python
# Python handles this automatically
# But for custom implementations, initialize with prime size
```

### 3. Monitor Load Factor
```python
# Keep load factor reasonable
# Rehash when α > 0.7 for open addressing
# or α > 1 for chaining
```

### 4. Use Appropriate Hash Function
```python
# For strings: Python's built-in hash() is good
# For custom objects: override __hash__() and __eq__()

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
```

### 5. Consider Memory vs Speed Trade-off
- **Chaining**: More memory, flexible
- **Open Addressing**: Less memory, faster with low load factor

---

## Edge Cases to Remember

### Always Consider
1. **Empty input**: `arr = []`
2. **Single element**: `arr = [x]`
3. **All duplicates**: `arr = [1, 1, 1, 1]`
4. **All unique**: No duplicates
5. **Hash collisions**: Test with keys that hash to same value
6. **Load factor**: What happens when table is nearly full?
7. **None/null values**: Can they be keys/values?
8. **Large datasets**: Memory constraints

### Python-Specific
1. **Unhashable types**: Can't use lists/sets as dict keys
2. **Dictionary order**: Preserved in Python 3.7+ but don't rely on it for logic
3. **Set iteration order**: Arbitrary, don't depend on it

---

## When to Use Hashing

### Use Hashing When:
- Need **O(1) average** lookup/insert/delete
- Searching for elements frequently
- Counting frequencies
- Detecting duplicates
- Implementing caches
- Group/partition data by key

### Don't Use Hashing When:
- Need **ordered** data (use BST or sorted array)
- Need **range queries** (use BST or segment tree)
- Need **O(1) worst-case** guarantees (use perfect hashing or other structures)
- Memory is extremely limited (consider bloom filters)
- Keys are sequential small integers (use direct address table)

---

## Comparison with Other Data Structures

| Operation | Hash Table | BST | Array (Sorted) |
|-----------|------------|-----|----------------|
| Search | O(1) avg, O(n) worst | O(log n) | O(log n) |
| Insert | O(1) avg, O(n) worst | O(log n) | O(n) |
| Delete | O(1) avg, O(n) worst | O(log n) | O(n) |
| Min/Max | O(n) | O(log n) | O(1) |
| Ordered Traversal | O(n log n) | O(n) | O(n) |
| Range Query | O(n) | O(log n + k) | O(log n + k) |
| Space | O(n) | O(n) | O(n) |

**Conclusion**: Hash tables excel at single-element operations but struggle with order-based queries.

---
