# Strings - Complete Reference Guide

## Table of Contents
1. [Strings in Python](#strings-in-python) - [Code: Strings in python.py](./01.%20Strings%20in%20python.py)
2. [Escape Sequences and Raw Strings](#escape-sequences-and-raw-strings) - [Code: Escape Sequences.py](./02.%20Escape%20Sequences.py)
3. [String Formatting](#string-formatting) - [Code: String formatting.py](./03.%20String%20formatting.py)
4. [String Comparison](#string-comparison) - [Code: String Comparison.py](./04.%20String%20Comparison.py)
5. [Substring Based Operations](#substring-based-operations) - [Code: String operations using substring.py](./05.%20String%20operations%20using%20substring.py)
6. [Common Built-in String Operations](#common-built-in-string-operations) - [Code: String operations (2).py](./06.%20String%20operations%20(2).py)
7. [Reverse a String](#reverse-a-string) - [Code: Reverse a string.py](./07.%20Reverse%20a%20string.py)
8. [Check if a String is Rotated](#check-if-a-string-is-rotated) - [Code: Check if a string is rotated.py](./08.%20Check%20if%20a%20string%20is%20rotated.py)
9. [Check for Palindrome](#check-for-palindrome) - [Code: Check for palindrome.py](./09.%20Check%20for%20palindrome.py)
10. [Check if a String is a Subsequence](#check-if-a-string-is-a-subsequence-of-another) - [Code: Check if a string is subsequence of other.py](./10.%20Check%20if%20a%20string%20is%20subsequence%20of%20other.py)
11. [Check for Anagram](#check-for-anagram) - [Code: Check for Anagram.py](./11.%20Check%20for%20Anagram.py)
12. [Leftmost Repeating Character](#leftmost-repeating-character) - [Code: Leftmost Repeating Character.py](./12.%20Leftmost%20Repeating%20Character.py)
13. [Leftmost Non-Repeating Character](#leftmost-non-repeating-character) - [Code: Leftmost Non-Repeating Character.py](./13.%20Leftmost%20Non-Repeating%20Character.py)
14. [Reverse Words in a String](#reverse-words-in-a-string) - [Code: Reverse words in a string.py](./14.%20Reverse%20words%20in%20a%20string.py)

---

## Understanding Strings

### What is a String?
A **string** is a sequence of characters enclosed in quotes. In Python, strings are:
- **Immutable**: Cannot be changed after creation
- **Iterable**: Can loop through characters
- **Indexed**: Access characters by position (0-based)

### String Creation
```python
s1 = "Hello"        # Double quotes
s2 = 'World'        # Single quotes
s3 = """Multi
line"""             # Triple quotes (preserves newlines)
```

---

## Strings in Python
**📁 Implementation:** [Strings in python.py](./01.%20Strings%20in%20python.py)

### Core Concepts

#### 1. String Indexing
Access individual characters using index positions.

```python
s = "Python"

# Positive indexing (left to right)
s[0]   # 'P' (first character)
s[1]   # 'y' (second character)

# Negative indexing (right to left)
s[-1]  # 'n' (last character)
s[-2]  # 'o' (second last)
```

**Index Range**: 0 to len(s)-1 or -len(s) to -1

#### 2. ASCII Conversion

**ord()**: Character → ASCII value
```python
ord('A')  # 65
ord('a')  # 97
ord('0')  # 48
```

**chr()**: ASCII value → Character
```python
chr(65)   # 'A'
chr(97)   # 'a'
chr(48)   # '0'
```

**Use Cases:**
- Character comparison (uppercase vs lowercase)
- Caesar cipher encryption
- Checking character types (digit, letter)

#### 3. Counting Unique Characters (Without Set)

**Logic**: Use a boolean array of size 256 (all ASCII characters).

```python
def count_unique_chars(s):
    char_seen = [False] * 256  # Direct address table
    count = 0
    
    for char in s:
        ascii_val = ord(char)
        if not char_seen[ascii_val]:
            char_seen[ascii_val] = True
            count += 1
    
    return count
```

**Why 256?** Standard ASCII has 256 characters (0-255).

**Time**: O(n), **Space**: O(1) - fixed size array

**Alternative (Using Set)**:
```python
def count_unique_simple(s):
    return len(set(s))
```

#### 4. String Immutability

Strings **cannot be modified** in place.

```python
s = "Hello"
s[0] = 'h'  # ❌ TypeError: 'str' object does not support item assignment

# Must create new string
s = 'h' + s[1:]  # ✅ "hello"
```

**Why Immutable?**
- **Security**: Strings used as dict keys, can't change
- **Optimization**: String interning (reuse identical strings)
- **Thread-safe**: No concurrent modification issues

**To Modify Strings:**
```python
# Convert to list, modify, convert back
chars = list(s)
chars[0] = 'h'
s = ''.join(chars)
```

---

## Escape Sequences and Raw Strings
**📁 Implementation:** [Escape Sequences.py](./02.%20Escape%20Sequences.py)

### Escape Sequences

Special characters preceded by backslash `\`.

| Sequence | Meaning | Example |
|----------|---------|---------|
| `\n` | Newline | `"Line1\nLine2"` |
| `\t` | Tab | `"Name:\tJohn"` |
| `\\` | Backslash | `"Path: C:\\folder"` |
| `\'` | Single quote | `'It\'s fine'` |
| `\"` | Double quote | `"He said \"Hi\""` |
| `\r` | Carriage return | (rarely used) |
| `\b` | Backspace | (rarely used) |

### Examples
```python
# Newline
print("Hello\nWorld")
# Output:
# Hello
# World

# Tab
print("Name:\tAlice\nAge:\t25")
# Output:
# Name:	Alice
# Age:	25

# Backslash (need to escape it)
print("C:\\Users\\Documents")  # C:\Users\Documents

# Quotes
print('It\'s a nice day')      # It's a nice day
print("She said \"Hello\"")    # She said "Hello"
```

### Raw Strings

Prefix string with `r` to treat backslashes literally (no escaping).

```python
# Regular string (needs escaping)
path1 = "C:\\Users\\Desktop\\file.txt"

# Raw string (no escaping needed)
path2 = r"C:\Users\Desktop\file.txt"

print(path1 == path2)  # True
```

**When to Use Raw Strings:**
- **File paths** (Windows)
- **Regular expressions** (contain many backslashes)
- **LaTeX strings**

```python
# Regular expression
import re
pattern = r"\d{3}-\d{2}-\d{4}"  # SSN format

# Without raw string (harder to read)
pattern = "\\d{3}-\\d{2}-\\d{4}"
```

**Note**: Raw strings still can't end with a single backslash.
```python
path = r"C:\folder\"  # ❌ SyntaxError
path = r"C:\folder" + "\\"  # ✅ Workaround
```

---

## String Formatting
**📁 Implementation:** [String formatting.py](./03.%20String%20formatting.py)

### 1. Old Style (% Operator) - C-style

```python
name = "Alice"
age = 25

# String interpolation
s = "Name: %s, Age: %d" % (name, age)
# "Name: Alice, Age: 25"

# Format specifiers:
"%s"   # String
"%d"   # Integer
"%f"   # Float
"%.2f" # Float with 2 decimals
```

**Pros**: Familiar to C programmers  
**Cons**: Hard to read with many variables

### 2. .format() Method - Python 2.6+

```python
name = "Alice"
age = 25

# Positional arguments
s = "Name: {}, Age: {}".format(name, age)

# Indexed arguments
s = "Name: {0}, Age: {1}".format(name, age)

# Named arguments
s = "Name: {n}, Age: {a}".format(n=name, a=age)

# Formatting options
pi = 3.14159
s = "Pi: {:.2f}".format(pi)  # "Pi: 3.14"
```

**Pros**: More flexible, readable  
**Cons**: Verbose for simple cases

### 3. f-strings (Formatted String Literals) - Python 3.6+

```python
name = "Alice"
age = 25

# Direct variable embedding
s = f"Name: {name}, Age: {age}"

# Expressions inside braces
s = f"Next year: {age + 1}"

# Format specifications
pi = 3.14159
s = f"Pi: {pi:.2f}"  # "Pi: 3.14"

# Debug format (Python 3.8+)
s = f"{name=}, {age=}"  # "name='Alice', age=25"
```

**Pros**: Fastest, most readable, concise  
**Cons**: Requires Python 3.6+

### Comparison

```python
name, age = "Alice", 25

# Old style
s = "Hello %s, you are %d" % (name, age)

# .format()
s = "Hello {}, you are {}".format(name, age)

# f-string (BEST)
s = f"Hello {name}, you are {age}"
```

**Recommendation**: Use f-strings whenever possible.

---

## String Comparison
**📁 Implementation:** [String Comparison.py](./04.%20String%20Comparison.py)

### Comparison Operators

Strings are compared **lexicographically** (dictionary order) using ASCII values.

```python
"apple" < "banana"   # True (a < b)
"apple" < "apricot"  # True (p < r)
"Apple" < "apple"    # True (A=65 < a=97)

"abc" == "abc"       # True
"abc" != "ABC"       # True
```

### How It Works

1. Compare character by character from left
2. First difference determines result
3. If one string is prefix of another, shorter < longer

```python
"cat" < "catalog"    # True (equal until end, then cat is shorter)
"abc" < "abd"        # True (c < d)
```

### Case-Insensitive Comparison

```python
s1 = "Hello"
s2 = "hello"

# Case-sensitive (different)
s1 == s2  # False

# Case-insensitive
s1.lower() == s2.lower()  # True
s1.upper() == s2.upper()  # True
```

### Sorting Strings

```python
words = ["banana", "Apple", "cherry"]

# Case-sensitive sort (uppercase first)
sorted(words)  # ['Apple', 'banana', 'cherry']

# Case-insensitive sort
sorted(words, key=str.lower)  # ['Apple', 'banana', 'cherry']
```

---

## Substring Based Operations
**📁 Implementation:** [String operations using substring.py](./05.%20String%20operations%20using%20substring.py)

### String Slicing

Syntax: `s[start:end:step]`
- **start**: Starting index (inclusive)
- **end**: Ending index (exclusive)
- **step**: Increment (default 1)

```python
s = "Python"

# Basic slicing
s[0:3]    # "Pyt" (indices 0, 1, 2)
s[2:5]    # "tho"
s[:3]     # "Pyt" (start omitted = 0)
s[3:]     # "hon" (end omitted = len(s))
s[:]      # "Python" (full copy)

# Negative indices
s[-3:]    # "hon" (last 3 characters)
s[:-2]    # "Pyth" (all but last 2)

# Step
s[::2]    # "Pto" (every 2nd character)
s[1::2]   # "yhn" (start at 1, every 2nd)
s[::-1]   # "nohtyP" (reverse)
```

### Membership Testing

```python
s = "Hello World"

# in operator (substring search)
"Hello" in s      # True
"hello" in s      # False (case-sensitive)
"World" in s      # True
"xyz" in s        # False

# not in operator
"xyz" not in s    # True
```

**Time Complexity**: O(n×m) where n = len(s), m = len(substring)

### Concatenation

```python
# Using + operator
s1 = "Hello"
s2 = "World"
result = s1 + " " + s2  # "Hello World"

# Using join() for multiple strings (more efficient)
words = ["Hello", "World", "!"]
result = " ".join(words)  # "Hello World !"

# Repetition with *
s = "Ha" * 3  # "HaHaHa"
```

**Performance Note**: Concatenation with `+` creates new string each time (O(n²) for loop). Use `join()` for multiple concatenations (O(n)).

---

## Common Built-in String Operations
**📁 Implementation:** [String operations (2).py](./06.%20String%20operations%20(2).py)

### 1. Length: len()
```python
s = "Hello"
len(s)  # 5
```

### 2. Case Conversion

```python
s = "Hello World"

s.upper()      # "HELLO WORLD"
s.lower()      # "hello world"
s.capitalize() # "Hello world" (first char uppercase)
s.title()      # "Hello World" (each word capitalized)
s.swapcase()   # "hELLO wORLD" (swap case)
```

### 3. Case Checking

```python
"HELLO".isupper()      # True
"hello".islower()      # True
"Hello".isupper()      # False
"123".isupper()        # False (no cased chars)
```

### 4. Prefix/Suffix Checking

```python
s = "hello.py"

s.startswith("hello")   # True
s.startswith("Hello")   # False (case-sensitive)
s.endswith(".py")       # True
s.endswith(".txt")      # False

# With position (start, end)
s.startswith("llo", 2)  # True (checks from index 2)
```

### 5. Split and Join

**split()**: String → List
```python
s = "Hello World Python"
s.split()              # ['Hello', 'World', 'Python']
s.split(' ')           # Same as above

s = "a,b,c,d"
s.split(',')           # ['a', 'b', 'c', 'd']

s = "one  two   three"
s.split()              # ['one', 'two', 'three'] (handles multiple spaces)

# Limit splits
s = "a-b-c-d"
s.split('-', 2)        # ['a', 'b', 'c-d'] (max 2 splits)
```

**join()**: List → String
```python
words = ['Hello', 'World']
' '.join(words)        # "Hello World"
','.join(words)        # "Hello,World"
''.join(words)         # "HelloWorld"

# Join with newline
lines = ['Line 1', 'Line 2', 'Line 3']
'\n'.join(lines)
```

### 6. Strip (Remove Whitespace/Characters)

```python
s = "  Hello World  "

s.strip()      # "Hello World" (both ends)
s.lstrip()     # "Hello World  " (left only)
s.rstrip()     # "  Hello World" (right only)

# Remove specific characters
s = "***Hello***"
s.strip('*')   # "Hello"

s = "www.example.com"
s.strip('wcom.')  # "example" (removes any of these chars)
```

### 7. Find (Search for Substring)

```python
s = "Hello World"

s.find("World")     # 6 (index where found)
s.find("world")     # -1 (not found, case-sensitive)
s.find("o")         # 4 (first occurrence)

# With start position
s.find("o", 5)      # 7 (find after index 5)

# With start and end
s.find("o", 0, 5)   # 4 (find between 0 and 5)
```

**find() vs index()**:
```python
s.find("xyz")       # -1 (returns -1 if not found)
s.index("xyz")      # ValueError (raises error if not found)
```

### Other Useful Methods

```python
# Replace
s = "Hello World"
s.replace("World", "Python")  # "Hello Python"
s.replace("o", "0")           # "Hell0 W0rld"

# Count occurrences
s = "hello"
s.count('l')       # 2
s.count('ll')      # 1

# Check character types
"123".isdigit()    # True
"abc".isalpha()    # True
"abc123".isalnum() # True
"   ".isspace()    # True
```

---

## Reverse a String
**📁 Implementation:** [Reverse a string.py](./07.%20Reverse%20a%20string.py)

### Problem
Reverse the order of characters in a string.

Example: "Hello" → "olleH"

### Approach 1: Slicing (Pythonic)
```python
def reverse_string(s):
    return s[::-1]
```

**Time**: O(n), **Space**: O(n) - creates new string

### Approach 2: Using reversed()
```python
def reverse_string(s):
    return ''.join(reversed(s))
```

### Approach 3: Manual (Two Pointers)
```python
def reverse_string(s):
    chars = list(s)  # Convert to list (mutable)
    left, right = 0, len(chars) - 1
    
    while left < right:
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1
    
    return ''.join(chars)
```

### Approach 4: Recursive
```python
def reverse_string(s):
    if len(s) <= 1:
        return s
    return s[-1] + reverse_string(s[:-1])
```

**Time**: O(n), **Space**: O(n) - recursion stack

### Time Complexity
All approaches: **O(n)** - must process each character

### Space Complexity
- **Slicing/Join**: O(n) - new string
- **Two Pointers**: O(n) - list conversion
- **Recursive**: O(n) - call stack

### When to Use
- **Slicing**: Simplest, most Pythonic
- **Two Pointers**: Interview questions (demonstrates algorithm)
- **Recursive**: Educational, not practical

---

## Check if a String is Rotated
**📁 Implementation:** [Check if a string is rotated.py](./08.%20Check%20if%20a%20string%20is%20rotated.py)

### Problem
Check if string s2 is a rotation of string s1.

Example: 
- s1 = "ABCD", s2 = "CDAB" → True (rotated by 2)
- s1 = "ABCD", s2 = "ACBD" → False (not a rotation)

### Logic (Clever Trick)
If s2 is a rotation of s1, then s2 will be a **substring of s1+s1**.

**Why?** Concatenating s1 with itself creates all possible rotations.

```python
s1 = "ABCD"
s1 + s1 = "ABCDABCD"

Possible rotations:
- "ABCD" (starting at index 0)
- "BCDA" (starting at index 1)
- "CDAB" (starting at index 2)
- "DABC" (starting at index 3)
```

### Implementation
```python
def is_rotation(s1, s2):
    # Must be same length
    if len(s1) != len(s2):
        return False
    
    # Check if s2 is substring of s1+s1
    return s2 in (s1 + s1)
```

### Time Complexity
- **Time**: O(n) - substring search in Python is optimized
- **Space**: O(n) - creating s1+s1

### Alternative: Manual Rotation Check
```python
def is_rotation_manual(s1, s2):
    if len(s1) != len(s2):
        return False
    
    # Try all rotation points
    for i in range(len(s1)):
        if s1[i:] + s1[:i] == s2:
            return True
    return False
```

**Time**: O(n²) - n rotations × n comparison

---

## Check for Palindrome
**📁 Implementation:** [Check for palindrome.py](./09.%20Check%20for%20palindrome.py)

### Problem
Check if a string reads the same forwards and backwards.

Example: "radar" → True, "hello" → False

### Approach 1: Slicing (Simplest)
```python
def is_palindrome(s):
    return s == s[::-1]
```

**Time**: O(n), **Space**: O(n)

### Approach 2: Two Pointers (Optimal)
```python
def is_palindrome(s):
    left, right = 0, len(s) - 1
    
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    
    return True
```

**Time**: O(n), **Space**: O(1)

### Approach 3: Recursive
```python
def is_palindrome(s):
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return is_palindrome(s[1:-1])
```

**Time**: O(n), **Space**: O(n) - recursion + string slicing

### Case-Insensitive Palindrome
```python
def is_palindrome_ignore_case(s):
    s = s.lower()
    return s == s[::-1]
```

### Ignore Non-Alphanumeric
```python
def is_palindrome_clean(s):
    # Keep only alphanumeric characters
    s = ''.join(c.lower() for c in s if c.isalnum())
    return s == s[::-1]

# Example
is_palindrome_clean("A man, a plan, a canal: Panama")  # True
```

---

## Check if a String is a Subsequence
**📁 Implementation:** [Check if a string is subsequence of other.py](./10.%20Check%20if%20a%20string%20is%20subsequence%20of%20other.py)

### Problem
Check if string s1 is a subsequence of string s2.

**Subsequence**: Characters of s1 appear in s2 in the same order (but not necessarily contiguous).

Example:
- s1 = "AXY", s2 = "ADXCPY" → True (A, X, Y appear in order)
- s1 = "AXY", s2 = "YADXCP" → False (Y appears before A)
- s1 = "gksrek", s2 = "geeksforgeeks" → True

### Logic (Two Pointers)
Use two pointers: one for s1, one for s2. Move through s2 trying to match all characters of s1 in order.

```python
def is_subsequence(s1, s2):
    i, j = 0, 0  # Pointers for s1 and s2
    
    while i < len(s1) and j < len(s2):
        if s1[i] == s2[j]:
            i += 1  # Match found, move s1 pointer
        j += 1      # Always move s2 pointer
    
    return i == len(s1)  # True if all of s1 matched
```

### How It Works
```
s1 = "AXY"
s2 = "ADXCPY"

i=0, j=0: s1[0]='A', s2[0]='A' ✓ → i=1, j=1
i=1, j=1: s1[1]='X', s2[1]='D' ✗ → i=1, j=2
i=1, j=2: s1[1]='X', s2[2]='X' ✓ → i=2, j=3
i=2, j=3: s1[2]='Y', s2[3]='C' ✗ → i=2, j=4
i=2, j=4: s1[2]='Y', s2[4]='P' ✗ → i=2, j=5
i=2, j=5: s1[2]='Y', s2[5]='Y' ✓ → i=3, j=6

i == len(s1) → True
```

### Time Complexity
- **Time**: O(n) where n = len(s2) - single pass through s2
- **Space**: O(1) - only two pointers

### Recursive Approach
```python
def is_subsequence_recursive(s1, s2, i=0, j=0):
    # Base cases
    if i == len(s1):  # All of s1 matched
        return True
    if j == len(s2):  # Reached end of s2 without matching all of s1
        return False
    
    # If characters match, advance both pointers
    if s1[i] == s2[j]:
        return is_subsequence_recursive(s1, s2, i+1, j+1)
    # Otherwise, only advance s2 pointer
    else:
        return is_subsequence_recursive(s1, s2, i, j+1)
```

---

## Check for Anagram
**📁 Implementation:** [Check for Anagram.py](./11.%20Check%20for%20Anagram.py)

### Problem
Check if two strings are anagrams (contain same characters with same frequencies).

Example:
- "listen" and "silent" → True
- "hello" and "world" → False

### Approach 1: Sorting (Simple)
```python
def are_anagrams(s1, s2):
    return sorted(s1) == sorted(s2)
```

**Time**: O(n log n) - sorting  
**Space**: O(n) - sorted lists

### Approach 2: Character Counting (Optimal)
```python
def are_anagrams(s1, s2):
    if len(s1) != len(s2):
        return False
    
    count = [0] * 256  # ASCII characters
    
    for char in s1:
        count[ord(char)] += 1
    
    for char in s2:
        count[ord(char)] -= 1
        if count[ord(char)] < 0:
            return False
    
    return True
```

**Time**: O(n)  
**Space**: O(1)

---

## Leftmost Non-Repeating Character
**📁 Implementation:** [Leftmost Non-Repeating Character.py](./13.%20Leftmost%20Non-Repeating%20Character.py)

### Problem
Find the index of the first character that appears exactly once.

Example: "geeksforgeeks" → 5 (f appears only once, first unique char)

### Approach 1: Nested Loop (Naive)
```python
def leftmost_non_repeating(s):
    for i in range(len(s)):
        is_unique = True
        for j in range(len(s)):
            if i != j and s[i] == s[j]:
                is_unique = False
                break
        if is_unique:
            return i
    return -1
```

**Time**: O(n²)  
**Space**: O(1)

### Approach 2: Two Pass with Count Array (Optimal)
```python
def leftmost_non_repeating(s):
    # First pass: count frequencies
    count = [0] * 256
    for char in s:
        count[ord(char)] += 1
    
    # Second pass: find first with count == 1
    for i, char in enumerate(s):
        if count[ord(char)] == 1:
            return i
    
    return -1
```

**Time**: O(n) - two passes  
**Space**: O(1) - fixed array

### Approach 3: Using Dictionary
```python
def leftmost_non_repeating_dict(s):
    from collections import Counter
    
    # Count frequencies
    freq = Counter(s)
    
    # Find first character with frequency 1
    for i, char in enumerate(s):
        if freq[char] == 1:
            return i
    
    return -1
```

**Time**: O(n)  
**Space**: O(k) where k = unique characters

### Difference from Leftmost Repeating
- **Repeating**: Character appears **more than once**, find first occurrence
- **Non-Repeating**: Character appears **exactly once**, find first such character

---

## Reverse Words in a String
**📁 Implementation:** [Reverse words in a string.py](./14.%20Reverse%20words%20in%20a%20string.py)

### Problem
Reverse the order of words in a string (not the characters).

Example: "Hello World Python" → "Python World Hello"

### Approach 1: Using split() and reverse (Pythonic)
```python
def reverse_words(s):
    words = s.split()
    return ' '.join(reversed(words))
```

**Alternative**:
```python
def reverse_words(s):
    return ' '.join(s.split()[::-1])
```

**Time**: O(n)  
**Space**: O(n) - list of words

### Approach 2: Manual Splitting and Reversing
```python
def reverse_words_manual(s):
    words = s.split()
    left, right = 0, len(words) - 1
    
    while left < right:
        words[left], words[right] = words[right], words[left]
        left += 1
        right -= 1
    
    return ' '.join(words)
```

### Approach 3: Without Built-in split()
```python
def reverse_words_custom(s):
    # Extract words manually
    words = []
    current_word = ""
    
    for char in s:
        if char == ' ':
            if current_word:
                words.append(current_word)
                current_word = ""
        else:
            current_word += char
    
    # Add last word
    if current_word:
        words.append(current_word)
    
    # Reverse words
    words.reverse()
    
    return ' '.join(words)
```

### Handling Edge Cases
```python
def reverse_words_robust(s):
    # Handle multiple spaces
    words = s.split()  # Automatically handles multiple spaces
    
    if not words:
        return ""
    
    return ' '.join(reversed(words))
```

Examples:
```python
reverse_words("Hello World")           # "World Hello"
reverse_words("  Hello   World  ")     # "World Hello"
reverse_words("a")                     # "a"
reverse_words("")                      # ""
```

### Time Complexity
- **All approaches**: O(n) where n = length of string
- Split, reverse, join each process the string once

### Space Complexity
- O(n) - storing list of words

---

## Comparison Summary

### Time Complexity Table

| Operation | Best Approach | Time | Space | Notes |
|-----------|---------------|------|-------|-------|
| Reverse String | Slicing `[::-1]` | O(n) | O(n) | Most Pythonic |
| Check Rotation | Substring in `s1+s1` | O(n) | O(n) | Clever trick |
| Palindrome | Two pointers | O(n) | O(1) | Optimal space |
| Is Subsequence | Two pointers | O(n) | O(1) | Single pass through s2 |
| Check Anagram | Count array | O(n) | O(1) | Faster than sorting |
| Leftmost Repeating | Two pass with array | O(n) | O(1) | Count then find |
| Leftmost Non-Repeating | Two pass with array | O(n) | O(1) | Count then find |
| Reverse Words | split() + reverse | O(n) | O(n) | Simple and clean |

---

## String Complexity Analysis

### Common Operations Time Complexity

| Operation | Complexity | Notes |
|-----------|------------|-------|
| Access `s[i]` | O(1) | Direct indexing |
| Slice `s[i:j]` | O(k) | k = slice length |
| Concatenation `s1 + s2` | O(n+m) | Creates new string |
| `in` operator | O(n×m) | Substring search |
| `len(s)` | O(1) | Stored as attribute |
| `s.upper()`, `s.lower()` | O(n) | Process each char |
| `s.split()` | O(n) | Single pass |
| `separator.join(list)` | O(n) | n = total chars |
| `s.find(sub)` | O(n×m) | Python optimized |
| `s.replace(old, new)` | O(n×m) | Find + replace |
| `sorted(s)` | O(n log n) | Timsort algorithm |

---