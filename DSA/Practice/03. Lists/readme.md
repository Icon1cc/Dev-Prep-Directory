# Lists Operations - Complete Reference Guide

## Table of Contents
1. [Average or Mean of a List](#average-or-mean-of-a-list) - [Code: 01. Average or Mean of a list.py](./01.%20Average%20or%20Mean%20of%20a%20list.py)
2. [Separate Odd and Even](#separate-odd-and-even) - [Code: 02. Separate Odd Even.py](./02.%20Separate%20Odd%20Even.py)
3. [Get Smaller Elements](#get-smaller-elements) - [Code: 03. Get Smaller Elements.py](./03.%20Get%20Smaller%20Elements.py)
4. [Largest Element in a List](#largest-element-in-a-list) - [Code: 04. Largest Element in a list.py](./04.%20Largest%20Element%20in%20a%20list.py)
5. [Second Largest Element](#second-largest-element) - [Code: 05. Second largest element in a list.py](./05.%20Second%20largest%20element%20in%20a%20list.py)
6. [Check if List is Sorted](#check-if-list-is-sorted) - [Code: 06. Check if a list is sorted.py](./06.%20Check%20if%20a%20list%20is%20sorted.py)
7. [Reverse a List](#reverse-a-list) - [Code: 07. Reverse a list.py](./07.%20Reverse%20a%20list.py)
8. [Remove Duplicates from Sorted Array](#remove-duplicates-from-sorted-array) - [Code: 08. Remove Duplicates from a sorted array.py](./08.%20Remove%20Duplicates%20from%20a%20sorted%20array.py)
9. [Left Rotate a List by One](#left-rotate-a-list-by-one) - [Code: 09. Left rotate a list by one.py](./09.%20Left%20rotate%20a%20list%20by%20one.py)
10. [Reverse an Array](#reverse-an-array) - [Code: 10. Reverse an array.py](./10.%20Reverse%20an%20array.py)

---

## Average or Mean of a List
**📁 Implementation:** [01. Average or Mean of a list.py](./01.%20Average%20or%20Mean%20of%20a%20list.py)

### Problem
Calculate the average (mean) of all elements in a list.

Formula: `Average = Sum of all elements / Number of elements`

### Logic
Iterate through the list, sum all elements, and divide by the length of the list.

### How It Works
1. Initialize `sum = 0`
2. Traverse the list and add each element to sum
3. Calculate average: `average = sum / len(list)`
4. Return the average

### Time Complexity

| Case | Complexity | Calculation |
|------|------------|-------------|
| **Best Case** | O(n) | Must visit every element regardless |
| **Average Case** | O(n) | Single pass through all n elements |
| **Worst Case** | O(n) | Same - always processes entire list |

### Space Complexity
- **Auxiliary Space**: O(1) - Only stores sum and count variables

### Python Built-in Alternative
```python
average = sum(list) / len(list)
````

### Edge Cases

* Empty list: Should return 0 or raise error
* Single element: Returns that element
* Negative numbers: Works normally
* Floating-point numbers: Result will be float

### When to Use

* Statistical calculations
* Finding central tendency
* Data analysis
* Performance metrics

---

## Separate Odd and Even

**📁 Implementation:** [02. Separate Odd Even.py](./02.%20Separate%20Odd%20Even.py)

### Problem

Separate odd and even numbers in a list, typically grouping odds and evens together.

### Logic

Use partitioning logic similar to quicksort - rearrange elements so that all even numbers appear before all odd numbers (or vice versa).

### Approach 1: Two Lists (Naive)

1. Create two separate lists: `evens = []`, `odds = []`
2. Iterate through original list
3. Append to appropriate list based on `num % 2 == 0`
4. Concatenate: `result = evens + odds`

**Time**: O(n), **Space**: O(n)

### Approach 2: In-Place Partitioning (Efficient)

1. Use two pointers: `left = 0`, `right = n-1`
2. Move left pointer right until odd number found
3. Move right pointer left until even number found
4. Swap elements at left and right
5. Repeat until pointers meet

**Time**: O(n), **Space**: O(1)

### Time Complexity

| Case             | Complexity | Calculation                                 |
| ---------------- | ---------- | ------------------------------------------- |
| **Best Case**    | O(n)       | Already separated, still need to verify all |
| **Average Case** | O(n)       | Single pass with swaps                      |
| **Worst Case**   | O(n)       | All elements need to be moved               |

### Space Complexity

* **Naive Approach**: O(n) - Creates new lists
* **In-Place Approach**: O(1) - Only pointer variables

### When to Use

* Data preprocessing
* Partitioning problems
* Organizing data by property
* Filter and segregate operations

---

## Get Smaller Elements

**📁 Implementation:** [03. Get Smaller Elements.py](./03.%20Get%20Smaller%20Elements.py)

### Problem

For each element in a list, count how many elements are smaller than it. Or return all elements smaller than a given value.

### Interpretation 1: Count Smaller Elements for Each

Given: `arr = [5, 2, 8, 1, 9]`
Result: `[2, 1, 3, 0, 4]` (number of smaller elements for each)

### Interpretation 2: Get All Smaller Than X

Given: `arr = [5, 2, 8, 1, 9]`, `x = 6`
Result: `[5, 2, 1]` (all elements < 6)

### Logic (Interpretation 2 - Filter)

Simple filtering operation to extract elements below a threshold.

### How It Works

1. Create empty result list
2. Iterate through each element
3. If `element < threshold`, add to result
4. Return result list

### Time Complexity

| Case             | Complexity | Calculation              |
| ---------------- | ---------- | ------------------------ |
| **Best Case**    | O(n)       | Must check every element |
| **Average Case** | O(n)       | Single pass through list |
| **Worst Case**   | O(n)       | Process all n elements   |

### Space Complexity

* **Auxiliary Space**: O(k) where k is number of elements smaller than threshold (worst case O(n))

### Python Alternative

```python
result = [x for x in arr if x < threshold]
# or
result = list(filter(lambda x: x < threshold, arr))
```

### When to Use

* Filtering data
* Range queries
* Data preprocessing
* Statistical analysis (finding values below threshold)

---

## Largest Element in a List

**📁 Implementation:** [04. Largest Element in a list.py](./04.%20Largest%20Element%20in%20a%20list.py)

### Problem

Find the maximum element in a list.

### Logic

Traverse the list once, keeping track of the maximum element seen so far.

### How It Works

1. Initialize `max_element = arr[0]` (or negative infinity)
2. Iterate through remaining elements
3. If `current_element > max_element`, update `max_element`
4. Return `max_element` after traversal

### Time Complexity

| Case             | Complexity | Calculation                                     |
| ---------------- | ---------- | ----------------------------------------------- |
| **Best Case**    | O(n)       | Maximum at first position, still need to verify |
| **Average Case** | O(n)       | Must examine every element                      |
| **Worst Case**   | O(n)       | Maximum at last position                        |

### Space Complexity

* **Auxiliary Space**: O(1) - Only stores one variable for max

### Python Built-in Alternative

```python
largest = max(arr)
```

This also runs in O(n) time internally.

### Edge Cases

* Empty list: Should raise error or return None
* Single element: Returns that element
* All elements equal: Returns that value
* Negative numbers: Works correctly

### When to Use

* Finding maximum value
* Range detection
* Data analysis
* Optimization problems

---

## Second Largest Element

**📁 Implementation:** [05. Second largest element in a list.py](./05.%20Second%20largest%20element%20in%20a%20list.py)

### Problem

Find the second largest distinct element in a list.

Example: `arr = [10, 5, 20, 8, 20]` → Return 10 (not 20)

### Logic

Keep track of both the largest and second largest elements while traversing the list once.

### How It Works

1. Initialize `largest = arr[0]`, `second_largest = -infinity` (or None)
2. Iterate through the list:

   * If `current > largest`:

     * `second_largest = largest`
     * `largest = current`
   * Else if `current > second_largest` and `current != largest`:

     * `second_largest = current`
3. Return `second_largest`

### Naive Approach

1. Sort the array: O(n log n)
2. Return second element (considering duplicates)

**Time**: O(n log n), **Space**: O(1) or O(n) depending on sort

### Efficient Approach (Single Pass)

**Time**: O(n), **Space**: O(1)

### Time Complexity

| Case             | Complexity | Calculation                         |
| ---------------- | ---------- | ----------------------------------- |
| **Best Case**    | O(n)       | Must scan entire list to be certain |
| **Average Case** | O(n)       | Single traversal                    |
| **Worst Case**   | O(n)       | Second largest at end               |

### Space Complexity

* **Auxiliary Space**: O(1) - Only two variables

### Edge Cases

* Less than 2 elements: No second largest exists
* All elements same: No second largest
* Only one distinct value: Return None or handle appropriately
* Two elements: Second is automatically second largest

### When to Use

* Finding runner-up
* Top-k problems (k=2 case)
* Data analysis
* Ranking systems

---

## Check if List is Sorted

**📁 Implementation:** [06. Check if a list is sorted.py](./06.%20Check%20if%20a%20list%20is%20sorted.py)

### Problem

Determine if a list is sorted in non-decreasing order (ascending with duplicates allowed).

### Logic

Compare each adjacent pair of elements. If any element is greater than the next, the list is not sorted.

### How It Works

1. Iterate through list from index 0 to n-2
2. For each index i, check if `arr[i] > arr[i+1]`
3. If yes, return `False` (not sorted)
4. If loop completes, return `True` (sorted)

### Early Termination

The function can return as soon as it finds one pair out of order - no need to check remaining elements.

### Time Complexity

| Case             | Complexity | Calculation                                                  |
| ---------------- | ---------- | ------------------------------------------------------------ |
| **Best Case**    | O(1)       | First pair is out of order (immediate return)                |
| **Average Case** | O(n)       | Check approximately n/2 pairs on average                     |
| **Worst Case**   | O(n)       | List is sorted or unsorted pair at end - check all n-1 pairs |

### Space Complexity

* **Auxiliary Space**: O(1) - Only uses loop variable

### Variations

* **Strictly increasing**: Use `arr[i] >= arr[i+1]` (no duplicates allowed)
* **Descending order**: Use `arr[i] < arr[i+1]`
* **Strictly decreasing**: Use `arr[i] <= arr[i+1]`

### Python Built-in Alternative

```python
is_sorted = all(arr[i] <= arr[i+1] for i in range(len(arr)-1))
```

### When to Use

* Validating input data
* Algorithm prerequisites (binary search needs sorted array)
* Data quality checks
* Before applying sorting-dependent operations

---

## Reverse a List

**📁 Implementation:** [07. Reverse a list.py](./07.%20Reverse%20a%20list.py)

### Problem

Reverse the order of elements in a list.

Example: `[1, 2, 3, 4, 5]` → `[5, 4, 3, 2, 1]`

### Logic

Swap elements from both ends moving towards the center.

### How It Works (Two-Pointer Approach)

1. Initialize `left = 0`, `right = n-1`
2. While `left < right`:

   * Swap `arr[left]` and `arr[right]`
   * Increment `left`, decrement `right`
3. Continue until pointers meet/cross

### Time Complexity

| Case             | Complexity | Calculation                    |
| ---------------- | ---------- | ------------------------------ |
| **Best Case**    | O(n)       | Must swap n/2 pairs regardless |
| **Average Case** | O(n)       | Exactly n/2 swaps              |
| **Worst Case**   | O(n)       | Always performs n/2 swaps      |

### Space Complexity

* **Auxiliary Space**: O(1) - In-place reversal, only pointer variables

### Alternative Approaches

| Method            | Time | Space | Code                   |
| ----------------- | ---- | ----- | ---------------------- |
| Two-pointer       | O(n) | O(1)  | Manual swapping        |
| New list          | O(n) | O(n)  | `reversed = arr[::-1]` |
| Python reverse()  | O(n) | O(1)  | `arr.reverse()`        |
| Python reversed() | O(n) | O(n)  | `list(reversed(arr))`  |

### When to Use

* Data manipulation
* Algorithm requirements (reverse and check palindrome)
* Stack operations
* Undo functionality

---

## Remove Duplicates from Sorted Array

**📁 Implementation:** [08. Remove Duplicates from a sorted array.py](./08.%20Remove%20Duplicates%20from%20a%20sorted%20array.py)

### Problem

Remove duplicate elements from a **sorted array** in-place, returning the new length.

Example: `arr = [1, 1, 2, 2, 3, 4, 4]` → Modified: `[1, 2, 3, 4, ...]`, Return: 4

### Logic

Use two pointers: one to track unique elements position, another to scan the array. Since array is sorted, duplicates are adjacent.

### How It Works (Two-Pointer Technique)

1. If array is empty, return 0
2. Initialize `unique_index = 0` (position of last unique element)
3. Iterate with `i` from 1 to n-1:

   * If `arr[i] != arr[unique_index]` (found new unique element):

     * Increment `unique_index`
     * Copy `arr[i]` to `arr[unique_index]`
4. Return `unique_index + 1` (count of unique elements)

### Why Sorted Matters

**Sorted**: All duplicates are adjacent, O(n) single pass
**Unsorted**: Would need O(n²) comparison or O(n) with extra space (hash set)

### Time Complexity

| Case             | Complexity | Calculation                          |
| ---------------- | ---------- | ------------------------------------ |
| **Best Case**    | O(n)       | All elements unique, still scan all  |
| **Average Case** | O(n)       | Single pass through array            |
| **Worst Case**   | O(n)       | All elements same, scan entire array |

### Space Complexity

* **Auxiliary Space**: O(1) - In-place modification, only pointer variables

### Comparison with Unsorted Array

* **Sorted + Two Pointer**: O(n) time, O(1) space
* **Unsorted + Hash Set**: O(n) time, O(n) space
* **Unsorted + Nested Loop**: O(n²) time, O(1) space

### When to Use

* Deduplication after sorting
* Database query optimization
* Memory-efficient duplicate removal
* Preprocessing for algorithms requiring unique elements

---

## Left Rotate a List by One

**📁 Implementation:** [09. Left rotate a list by one.py](./09.%20Left%20rotate%20a%20list%20by%20one.py)

### Problem

Rotate array elements to the left by one position. First element moves to the end.

Example: `[1, 2, 3, 4, 5]` → `[2, 3, 4, 5, 1]`

### Logic

Store the first element temporarily, shift all elements one position left, then place the stored element at the end.

### How It Works

1. Store `temp = arr[0]`
2. Shift elements: For i from 0 to n-2, `arr[i] = arr[i+1]`
3. Place stored element at end: `arr[n-1] = temp`

### Alternative Approach (Python Slicing)

```python
arr = arr[1:] + [arr[0]]
```

Creates new list - O(n) space

### Time Complexity

| Case             | Complexity | Calculation                  |
| ---------------- | ---------- | ---------------------------- |
| **Best Case**    | O(n)       | Must shift all n-1 elements  |
| **Average Case** | O(n)       | Exactly n-1 shifts           |
| **Worst Case**   | O(n)       | Same - always n-1 operations |

### Space Complexity

* **Auxiliary Space**: O(1) - In-place with one temp variable (excluding Python slicing approach)

### Extension: Rotate by K Positions

To rotate left by k positions:

1. **Naive**: Call rotate-by-one k times → O(n*k)
2. **Efficient**: Use reversal algorithm → O(n)

   * Reverse first k elements
   * Reverse remaining n-k elements
   * Reverse entire array

### When to Use

* Circular arrays
* Queue implementations
* Scheduling algorithms (round-robin)
* Pattern matching

---

## Reverse an Array

**📁 Implementation:** [10. Reverse an array.py](./10.%20Reverse%20an%20array.py)

### Problem

Reverse the order of elements in an array.

Example: `[1, 2, 3, 4, 5]` → `[5, 4, 3, 2, 1]`

### Note

This appears to be the same as [Reverse a List](#reverse-a-list) (Item 7). The implementation may differ in:

* In-place vs creating new array
* Recursive vs iterative approach
* Array-specific optimizations

### Logic (Two-Pointer In-Place)

Use two pointers from opposite ends, swap elements, and move towards center.

### How It Works

1. Initialize `start = 0`, `end = n-1`
2. While `start < end`:

   * Swap `arr[start]` with `arr[end]`
   * Increment `start`
   * Decrement `end`
3. Array is reversed when pointers meet

### Recursive Approach

```python
def reverse(arr, start, end):
    if start >= end:
        return
    arr[start], arr[end] = arr[end], arr[start]
    reverse(arr, start+1, end-1)
```

### Time Complexity

| Case             | Complexity | Calculation            |
| ---------------- | ---------- | ---------------------- |
| **Best Case**    | O(n)       | Must perform n/2 swaps |
| **Average Case** | O(n)       | Exactly n/2 swaps      |
| **Worst Case**   | O(n)       | Always n/2 swaps       |

### Space Complexity

* **Iterative**: O(1) - Only pointer variables
* **Recursive**: O(n) - Call stack depth is n/2

### When to Use

* Data reversal operations
* Algorithm building blocks
* Palindrome checking
* Stack/queue operations

---

## Comparison Summary

### Time Complexity Table

| Operation                    | Best Case | Average Case | Worst Case | Space |
| ---------------------------- | --------- | ------------ | ---------- | ----- |
| Average/Mean                 | O(n)      | O(n)         | O(n)       | O(1)  |
| Separate Odd/Even (In-place) | O(n)      | O(n)         | O(n)       | O(1)  |
| Get Smaller Elements         | O(n)      | O(n)         | O(n)       | O(k)  |
| Largest Element              | O(n)      | O(n)         | O(n)       | O(1)  |
| Second Largest               | O(n)      | O(n)         | O(n)       | O(1)  |
| Check Sorted                 | O(1)      | O(n)         | O(n)       | O(1)  |
| Reverse                      | O(n)      | O(n)         | O(n)       | O(1)  |
| Remove Duplicates (Sorted)   | O(n)      | O(n)         | O(n)       | O(1)  |
| Left Rotate by One           | O(n)      | O(n)         | O(n)       | O(1)  |

### Common Patterns

**Single Pass Operations (O(n)):**
Most list operations require at least one complete traversal:

* Finding max/min/average
* Checking properties
* Transformations

**Two-Pointer Technique (O(n), O(1) space):**
Efficient for in-place modifications:

* Reversing
* Partitioning (odd/even)
* Removing duplicates from sorted array

**Early Termination:**
Some operations can exit early:

* Check if sorted (stop at first violation)
* Search operations

---

## Tips for Implementation

### 1. Edge Cases to Always Consider

* Empty array: `arr = []`
* Single element: `arr = [x]`
* Two elements: `arr = [x, y]`
* All elements same: `arr = [5, 5, 5, 5]`
* Already processed: (sorted, reversed, etc.)

### 2. In-Place vs New Array

**In-Place (O(1) space):**

* Modifies original array
* More memory efficient
* Use for: reverse, rotate, partition

**New Array (O(n) space):**

* Preserves original
* Often cleaner code
* Use for: filter, transform, when original needed

### 3. Python-Specific Optimizations

```python
# Instead of manual loop for sum
total = sum(arr)

# Instead of manual loop for max
maximum = max(arr)

# List comprehensions are optimized
evens = [x for x in arr if x % 2 == 0]

# Slicing creates new list but concise
reversed_arr = arr[::-1]
```

### 4. Index Boundary Awareness

```python
# Safe access
if i < len(arr) - 1:
    next_elem = arr[i + 1]

# Negative indices
last = arr[-1]  # Last element
second_last = arr[-2]  # Second last
```

### 5. Common Mistakes

* **Off-by-one errors**: Loop to `n-1` not `n` for pairs
* **Modifying during iteration**: Use index-based or copy
* **Not handling empty**: Check `if not arr:` first
* **Integer overflow**: Less common in Python but consider for very large sums

---

## When to Use Each Operation

### Data Analysis & Statistics

* Average/Mean
* Find largest/smallest
* Count elements meeting criteria

### Data Preprocessing

* Remove duplicates
* Separate by property (odd/even)
* Filter elements
* Reverse order

### Algorithm Building Blocks

* Check if sorted (before binary search)
* Reverse (palindrome checking)
* Rotate (circular arrays, scheduling)
* Partition (quicksort-like operations)

### Memory-Constrained Environments

Prefer O(1) space operations:

* In-place reverse
* In-place partition
* Two-pointer techniques

---