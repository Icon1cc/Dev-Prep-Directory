# Searching Algorithms - Complete Reference Guide

## Table of Contents
1. [Binary Search](#binary-search) - [Code: 01. Binary search.py](./01.%20Binary%20search.py)
2. [Recursive Binary Search](#recursive-binary-search) - [Code: 02. Recursive Binary Search.py](./02.%20Recursive%20Binary%20Search.py)
3. [Index of First Occurrence](#index-of-first-occurrence) - [Code: 03. Index of first occurence in a sorted array.py](./03.%20Index%20of%20first%20occurence%20in%20a%20sorted%20array.py)
4. [Index of Last Occurrence](#index-of-last-occurrence) - [Code: 04. Index of last occurence in a sorted array.py](./04.%20Index%20of%20last%20occurence%20in%20a%20sorted%20array.py)
5. [Count Occurrences](#count-occurrences) - [Code: 05. Count Occurrences of a target value.py](./05.%20Count%20Occurrences%20of%20a%20target%20value.py)
6. [Counting 1's in Binary Sorted Array](#counting-1s-in-binary-sorted-array) - [Code: 06. Counting 1's Occurrences.py](./06.%20Counting%201's%20Occurrences.py)
7. [Square Root using Binary Search](#square-root-using-binary-search) - [Code: 07. Calculate square root using binary search.py](./07.%20Calculate%20square%20root%20using%20binary%20search.py)
8. [Comparison Summary](#comparison-summary)

---

## Binary Search
**📁 Implementation:** [01. Binary search.py](./01.%20Binary%20search.py)

### Logic
Binary Search is an efficient algorithm for finding a target value within a **sorted array**. It works by repeatedly dividing the search interval in half. If the target value is less than the middle element, search the left half; if greater, search the right half.

### Prerequisites
- **Array must be sorted** (ascending or descending)
- Random access to elements (array-based structure)

### How It Works
1. Initialize two pointers: `low = 0` and `high = n-1`
2. Calculate middle index: `mid = (low + high) // 2`
3. Compare target with `arr[mid]`:
   - If `arr[mid] == target`: Found! Return `mid`
   - If `arr[mid] < target`: Search right half, set `low = mid + 1`
   - If `arr[mid] > target`: Search left half, set `high = mid - 1`
4. Repeat until `low > high` (element not found)

### Time Complexity

| Case | Complexity | Calculation |
|------|------------|-------------|
| **Best Case** | O(1) | Target is at middle position in first comparison |
| **Average Case** | O(log n) | On average, eliminates half the elements each iteration |
| **Worst Case** | O(log n) | Target at either end or not present. Max comparisons: log₂(n) + 1 |

**Why O(log n)?**
- Each comparison reduces search space by half
- n → n/2 → n/4 → n/8 → ... → 1
- Number of divisions: log₂(n)

### Space Complexity
- **Auxiliary Space**: O(1) - Only uses a few variables (iterative approach)

### When to Use
- Searching in sorted arrays
- Large datasets where linear search is too slow
- When dataset doesn't change frequently (sorting overhead)
- Dictionary lookups, database indexing

### Advantages
- Much faster than linear search for large datasets
- Simple to implement
- Guaranteed O(log n) performance

### Disadvantages
- **Requires sorted data** (sorting takes O(n log n))
- Requires random access (not efficient for linked lists)
- Not suitable for frequently changing data

---

## Recursive Binary Search
**📁 Implementation:** [02. Recursive Binary Search.py](./02.%20Recursive%20Binary%20Search.py)

### Logic
Same binary search algorithm but implemented using recursion instead of iteration. The function calls itself with updated bounds until the target is found or search space is exhausted.

### How It Works
1. Base case: If `low > high`, return -1 (not found)
2. Calculate `mid = (low + high) // 2`
3. If `arr[mid] == target`, return `mid`
4. If `arr[mid] < target`, recursively search right: `binarySearch(arr, mid+1, high, target)`
5. If `arr[mid] > target`, recursively search left: `binarySearch(arr, low, mid-1, target)`

### Time Complexity

| Case | Complexity | Calculation |
|------|------------|-------------|
| **Best Case** | O(1) | Target found at first middle element |
| **Average Case** | O(log n) | Same as iterative - halves search space each call |
| **Worst Case** | O(log n) | Maximum recursion depth: log₂(n) |

### Space Complexity
- **Auxiliary Space**: O(log n) - Recursion call stack depth proportional to number of halvings

### Comparison with Iterative
| Aspect | Iterative | Recursive |
|--------|-----------|-----------|
| Space | O(1) | O(log n) |
| Speed | Slightly faster (no function call overhead) | Slightly slower |
| Readability | More code | More elegant/concise |
| Stack Overflow Risk | None | Possible for very large arrays |

### When to Use
- When code elegance matters
- Small to medium-sized arrays (stack safe)
- Educational purposes
- When space is not a critical constraint

---

## Index of First Occurrence
**📁 Implementation:** [03. Index of first occurence in a sorted array.py](./03.%20Index%20of%20first%20occurence%20in%20a%20sorted%20array.py)

### Problem
Find the index of the **first occurrence** of a target element in a sorted array that may contain duplicates.

Example: `arr = [1, 2, 2, 2, 3, 4]`, target = 2 → Return 1 (not 2 or 3)

### Logic
Modified binary search that continues searching in the left half even after finding the target, to locate the leftmost occurrence.

### How It Works
1. Perform standard binary search
2. When `arr[mid] == target`:
   - **Don't return immediately**
   - Check if it's the first occurrence: `mid == 0` or `arr[mid-1] != target`
   - If yes, return `mid`
   - If no, continue searching left: `high = mid - 1`
3. Standard binary search for other cases

### Time Complexity

| Case | Complexity | Calculation |
|------|------------|-------------|
| **Best Case** | O(1) | First element is the target |
| **Average Case** | O(log n) | Binary search with extra left-side checks |
| **Worst Case** | O(log n) | All elements are the same as target, still log comparisons |

### Space Complexity
- **Auxiliary Space**: O(1) for iterative, O(log n) for recursive

### When to Use
- Finding first occurrence in sorted array with duplicates
- Range queries (start of range)
- Database queries with duplicate values

---

## Index of Last Occurrence
**📁 Implementation:** [04. Index of last occurence in a sorted array.py](./04.%20Index%20of%20last%20occurence%20in%20a%20sorted%20array.py)

### Problem
Find the index of the **last occurrence** of a target element in a sorted array that may contain duplicates.

Example: `arr = [1, 2, 2, 2, 3, 4]`, target = 2 → Return 3 (not 1 or 2)

### Logic
Modified binary search that continues searching in the right half even after finding the target, to locate the rightmost occurrence.

### How It Works
1. Perform standard binary search
2. When `arr[mid] == target`:
   - **Don't return immediately**
   - Check if it's the last occurrence: `mid == n-1` or `arr[mid+1] != target`
   - If yes, return `mid`
   - If no, continue searching right: `low = mid + 1`
3. Standard binary search for other cases

### Time Complexity

| Case | Complexity | Calculation |
|------|------------|-------------|
| **Best Case** | O(1) | Last element is the target |
| **Average Case** | O(log n) | Binary search with extra right-side checks |
| **Worst Case** | O(log n) | All elements are the same as target |

### Space Complexity
- **Auxiliary Space**: O(1) for iterative, O(log n) for recursive

### When to Use
- Finding last occurrence in sorted array with duplicates
- Range queries (end of range)
- Finding boundaries in duplicate sequences

---

## Count Occurrences
**📁 Implementation:** [05. Count Occurrences of a target value.py](./05.%20Count%20Occurrences%20of%20a%20target%20value.py)

### Problem
Count the total number of times a target element appears in a sorted array.

Example: `arr = [1, 2, 2, 2, 3, 4]`, target = 2 → Return 3

### Logic
Use the first and last occurrence finding algorithms. The count is:
```
count = (last_occurrence_index - first_occurrence_index) + 1
```

### How It Works
1. Find the index of first occurrence using modified binary search
2. Find the index of last occurrence using modified binary search
3. If target not found (first returns -1), return 0
4. Otherwise, calculate: `count = last - first + 1`

### Alternative Approach
Single pass modified binary search tracking count, but two-pass approach is cleaner and reuses existing functions.

### Time Complexity

| Case | Complexity | Calculation |
|------|------------|-------------|
| **Best Case** | O(log n) | Two binary searches: O(log n) + O(log n) = O(log n) |
| **Average Case** | O(log n) | Same - both operations are independent binary searches |
| **Worst Case** | O(log n) | Even if all elements match, still log comparisons |

### Space Complexity
- **Auxiliary Space**: O(1) for iterative implementations

### Naive Approach Comparison
- **Linear scan**: O(n) time - checks every element
- **Binary search approach**: O(log n) time - leverages sorted property

### When to Use
- Counting duplicates in sorted array
- Frequency analysis
- Statistics on sorted data

---

## Counting 1's in Binary Sorted Array
**📁 Implementation:** [06. Counting 1's Occurrences.py](./06.%20Counting%201's%20Occurrences.py)

### Problem
Count the number of 1's in a sorted binary array (containing only 0's and 1's).

Example: `arr = [0, 0, 0, 1, 1, 1, 1]` → Return 4

### Logic
This is a specialized case of counting occurrences. Since the array contains only 0's and 1's and is sorted, all 1's appear together at the end.

**Key insight**: If we find the index of the **first occurrence of 1**, the count is:
```
count = n - first_index_of_1
```

### How It Works
1. Use modified binary search to find first occurrence of 1
2. When `arr[mid] == 1`:
   - Check if it's the first 1: `mid == 0` or `arr[mid-1] == 0`
   - If yes, return `n - mid`
   - Otherwise, search left: `high = mid - 1`
3. If no 1 found, return 0

### Time Complexity

| Case | Complexity | Calculation |
|------|------------|-------------|
| **Best Case** | O(1) | First element is 1 (all 1's) |
| **Average Case** | O(log n) | Binary search to find first 1 |
| **Worst Case** | O(log n) | Last element is 1 (single 1) or no 1's |

### Space Complexity
- **Auxiliary Space**: O(1)

### Naive Approach Comparison
- **Linear scan**: O(n) - count all 1's by iterating
- **Binary search**: O(log n) - find boundary and calculate

### When to Use
- Binary arrays (0's and 1's)
- Boolean flags in sorted order
- Counting satisfied conditions in sorted boolean data

---

## Square Root using Binary Search
**📁 Implementation:** [07. Calculate square root using binary search.py](./07.%20Calculate%20square%20root%20using%20binary%20search.py)

### Problem
Find the square root of a number (integer part) without using built-in sqrt function.

Example: `n = 14` → Return 3 (since 3² = 9 ≤ 14 < 4² = 16)

### Logic
The square root of n lies between 1 and n. We can use binary search on this range to find the largest integer whose square is ≤ n.

### How It Works
1. Initialize search space: `low = 1`, `high = n`
2. While `low <= high`:
   - Calculate `mid = (low + high) // 2`
   - If `mid * mid == n`: Perfect square! Return `mid`
   - If `mid * mid < n`: Answer could be `mid` or larger, search right
     - Store `mid` as potential answer
     - Set `low = mid + 1`
   - If `mid * mid > n`: Answer must be smaller, search left
     - Set `high = mid - 1`
3. Return stored answer

### Time Complexity

| Case | Complexity | Calculation |
|------|------------|-------------|
| **Best Case** | O(1) | n is perfect square and found at first mid |
| **Average Case** | O(log n) | Binary search on range [1, n] |
| **Worst Case** | O(log n) | Maximum log₂(n) comparisons |

### Space Complexity
- **Auxiliary Space**: O(1) - Only uses a few variables

### Alternative Approaches

| Method | Time | Space | Notes |
|--------|------|-------|-------|
| Linear Search | O(n) | O(1) | Check 1, 2, 3, ... until i² > n |
| Binary Search | O(log n) | O(1) | Much more efficient |
| Newton's Method | O(log log n) | O(1) | Faster convergence but complex |
| Built-in sqrt() | O(1) | O(1) | Hardware/optimized implementation |

### Precision Note
This finds the **floor** of the square root (integer part). For decimal precision, continue binary search with floating-point arithmetic to desired decimal places.

### When to Use
- Computing integer square roots
- Mathematical problems without library functions
- Understanding binary search applications beyond arrays
- Competitive programming

---

## Comparison Summary

### Time Complexity Table

| Algorithm | Best Case | Average Case | Worst Case | Space |
|-----------|-----------|--------------|------------|-------|
| Binary Search (Iterative) | O(1) | O(log n) | O(log n) | O(1) |
| Binary Search (Recursive) | O(1) | O(log n) | O(log n) | O(log n) |
| First Occurrence | O(1) | O(log n) | O(log n) | O(1) |
| Last Occurrence | O(1) | O(log n) | O(log n) | O(1) |
| Count Occurrences | O(log n) | O(log n) | O(log n) | O(1) |
| Count 1's in Binary Array | O(1) | O(log n) | O(log n) | O(1) |
| Square Root | O(1) | O(log n) | O(log n) | O(1) |

### Key Principles

**Why Binary Search is O(log n):**
- Each comparison eliminates half the search space
- Recursive relation: T(n) = T(n/2) + O(1)
- Solving: T(n) = O(log n)

**Common Pattern:**
All binary search variants follow this structure:
1. Define search space with `low` and `high`
2. Calculate `mid`
3. Make decision based on comparison at `mid`
4. Narrow search space
5. Repeat until found or space exhausted

### Quick Decision Guide

**Use Binary Search when:**
- Data is sorted (or can be sorted once)
- Need O(log n) search time
- Random access is available (arrays)
- Dataset is large

**Use Linear Search when:**
- Data is unsorted and sorting is expensive
- Dataset is very small (< 20 elements)
- Searching linked lists
- One-time search on unsorted data

**Use Modified Binary Search for:**
- Finding boundaries (first/last occurrence)
- Counting in sorted arrays
- Non-array applications (square root, optimization problems)
- Peak finding, rotated arrays

---

## Applications of Binary Search

### Beyond Array Searching

1. **Mathematical Problems**
   - Square root, nth root calculation
   - Finding solutions to equations
   - Optimization problems

2. **Competitive Programming**
   - "Binary search on answer" technique
   - Finding minimum/maximum values satisfying conditions
   - Range queries

3. **Real-World Systems**
   - Database indexing (B-trees use binary search principle)
   - Dictionary lookups
   - File systems (finding files by timestamp)
   - Version control (git bisect)

4. **Advanced Variations**
   - Rotated sorted arrays
   - Peak element finding
   - Search in 2D sorted matrix
   - Median of two sorted arrays

---

## Implementation Tips

1. **Avoid Integer Overflow**: Use `mid = low + (high - low) // 2` instead of `mid = (low + high) // 2`

2. **Boundary Conditions**: Always check:
   - Empty array
   - Single element
   - Target at boundaries
   - All duplicates

3. **Loop Invariants**: Maintain clear invariants:
   - `arr[low..mid]` contains potential answer
   - `arr[mid+1..high]` contains potential answer
   - Keep track of what's been eliminated

4. **Recursive vs Iterative**:
   - Use iterative for production (better space)
   - Use recursive for clarity (if stack safe)

5. **Testing Edge Cases**:
   - Target not present
   - All elements same
   - Target at start/end
   - Array size 0, 1, 2

---

## Common Binary Search Patterns

### Pattern 1: Exact Match
```
Standard binary search - find exact element
```

### Pattern 2: Find Boundary
```
First/Last occurrence - find leftmost/rightmost
```

### Pattern 3: Binary Search on Answer
```
Square root - search for answer in a range
```

### Pattern 4: Modified Comparisons
```
Rotated arrays, peak finding - modified mid comparisons
```

---