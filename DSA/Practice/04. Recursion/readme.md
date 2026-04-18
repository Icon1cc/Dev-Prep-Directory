# Recursion Problems - Complete Reference Guide

## Table of Contents
1. [Print 1 to N](#print-1-to-n) - [Code: 01. Print 1 to N.py](./01.%20Print%201%20to%20N.py)
2. [Print N to 1](#print-n-to-1) - [Code: 02. Print N to 1.py](./02.%20Print%20N%20to%201.py)
3. [Factorial](#factorial) - [Code: 03. Factorial.py](./03.%20Factorial.py)
4. [Fibonacci Series](#fibonacci-series) - [Code: 04. Fibonacci series.py](./04.%20Fibonacci%20series.py)
5. [Sum of Digits](#sum-of-digits) - [Code: 05. Sum of digits.py](./05.%20Sum%20of%20digits.py)
6. [Palindrome Check](#palindrome-check) - [Code: 06. Palindrome.py](./06.%20Palindrome.py)
7. [Number Palindrome](#number-palindrome) - [Code: 07. Number Palindrome.py](./07.%20Number%20Palindrome.py)
8. [Understanding Recursion](#understanding-recursion)
9. [Comparison Summary](#comparison-summary)

---

## Understanding Recursion

### What is Recursion?
Recursion is a programming technique where a function calls itself to solve a problem by breaking it down into smaller, similar subproblems.

### Key Components of Recursion

1. **Base Case**: The condition that stops the recursion (prevents infinite loop)
2. **Recursive Case**: The part where function calls itself with modified parameters
3. **Progress Toward Base Case**: Each recursive call must move closer to the base case

### How Recursion Works
```

Function Call → Stack Frame Created
↓
Recursive Call → New Stack Frame
↓
... (more calls)
↓
Base Case Reached → Start Returning
↓
Previous Frames Resume → Stack Unwinding
↓
Original Call Completes

````

### Recursion vs Iteration

| Aspect | Recursion | Iteration |
|--------|-----------|-----------|
| **Space** | O(n) - Call stack | O(1) - Loop variables |
| **Readability** | Often more elegant | Can be more verbose |
| **Performance** | Function call overhead | Generally faster |
| **Use Case** | Tree/graph traversal, divide & conquer | Simple loops, counters |
| **Stack Overflow Risk** | Yes (deep recursion) | No |

---

## Print 1 to N
**📁 Implementation:** [01. Print 1 to N.py](./01.%20Print%201%20to%20N.py)

### Problem
Print numbers from 1 to N using recursion.

Example: N = 5 → Output: 1 2 3 4 5

### Logic
Use recursion to print numbers in increasing order. First make recursive calls to reach 1, then print while unwinding.

### How It Works
```python
def print_1_to_n(n):
    if n == 0:           # Base case
        return
    print_1_to_n(n - 1)  # Recursive call FIRST
    print(n)             # Print AFTER recursive call
````

**Execution Flow for n=3:**

```
print_1_to_n(3)
  → print_1_to_n(2)
    → print_1_to_n(1)
      → print_1_to_n(0)  [Base case, return]
      ← Print 1
    ← Print 2
  ← Print 3
Output: 1 2 3
```

### Key Insight

Printing **after** the recursive call ensures numbers print in ascending order.

### Time Complexity

| Case             | Complexity | Calculation                 |
| ---------------- | ---------- | --------------------------- |
| **Best Case**    | O(n)       | Must make n recursive calls |
| **Average Case** | O(n)       | Exactly n function calls    |
| **Worst Case**   | O(n)       | Always n calls regardless   |

### Space Complexity

* **Auxiliary Space**: O(n) - Recursion call stack depth is n

### Iterative Alternative

```python
for i in range(1, n+1):
    print(i)
```

**Time**: O(n), **Space**: O(1)

### When to Use Recursion Here

* Educational purposes (understanding recursion)
* Part of larger recursive algorithm
* When code elegance is preferred

**Note**: Iterative approach is more efficient for this simple task.

---

## Print N to 1

**📁 Implementation:** [02. Print N to 1.py](./02.%20Print%20N%20to%201.py)

### Problem

Print numbers from N to 1 using recursion.

Example: N = 5 → Output: 5 4 3 2 1

### Logic

Print the current number first, then make the recursive call with n-1.

### How It Works

```python
def print_n_to_1(n):
    if n == 0:           # Base case
        return
    print(n)             # Print BEFORE recursive call
    print_n_to_1(n - 1)  # Recursive call AFTER
```

**Execution Flow for n=3:**

```
print_n_to_1(3)
  Print 3
  → print_n_to_1(2)
    Print 2
    → print_n_to_1(1)
      Print 1
      → print_n_to_1(0)  [Base case, return]
Output: 3 2 1
```

### Key Insight

Printing **before** the recursive call ensures numbers print in descending order.

### Comparison with Print 1 to N

* **Print 1 to N**: Print after recursive call (ascending)
* **Print N to 1**: Print before recursive call (descending)

### Time Complexity

| Case             | Complexity | Calculation                 |
| ---------------- | ---------- | --------------------------- |
| **Best Case**    | O(n)       | Must make n recursive calls |
| **Average Case** | O(n)       | Exactly n function calls    |
| **Worst Case**   | O(n)       | Always n calls              |

### Space Complexity

* **Auxiliary Space**: O(n) - Recursion call stack depth is n

### Iterative Alternative

```python
for i in range(n, 0, -1):
    print(i)
```

**Time**: O(n), **Space**: O(1)

---

## Factorial

**📁 Implementation:** [03. Factorial.py](./03.%20Factorial.py)

### Problem

Calculate factorial of a number N (N! = N × (N-1) × (N-2) × ... × 1).

Example: 5! = 5 × 4 × 3 × 2 × 1 = 120

### Logic

Factorial has a natural recursive definition:

* **Base case**: 0! = 1, 1! = 1
* **Recursive case**: n! = n × (n-1)!

### How It Works

```python
def factorial(n):
    if n == 0 or n == 1:    # Base case
        return 1
    return n * factorial(n - 1)  # Recursive case
```

**Execution Flow for n=4:**

```
factorial(4)
  → 4 * factorial(3)
        → 3 * factorial(2)
              → 2 * factorial(1)
                    → 1 (base case)
              ← 2 * 1 = 2
        ← 3 * 2 = 6
  ← 4 * 6 = 24
Result: 24
```

### Mathematical Recurrence

```
T(n) = T(n-1) + O(1)
T(1) = O(1)
Solution: T(n) = O(n)
```

### Time Complexity

| Case             | Complexity | Calculation       |
| ---------------- | ---------- | ----------------- |
| **Best Case**    | O(1)       | When n = 0 or 1   |
| **Average Case** | O(n)       | n recursive calls |
| **Worst Case**   | O(n)       | Maximum n calls   |

### Space Complexity

* **Auxiliary Space**: O(n) - Call stack depth equals n

### Iterative Alternative

```python
def factorial_iterative(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```

**Time**: O(n), **Space**: O(1)

### Edge Cases

* **n = 0**: Returns 1 (by definition)
* **n = 1**: Returns 1
* **Large n**: Risk of integer overflow (Python handles big integers)
* **Negative n**: Mathematically undefined (should handle/validate)

### When to Use

* Mathematical calculations
* Permutation/combination formulas
* Probability calculations
* Classic recursion teaching example

---

## Fibonacci Series

**📁 Implementation:** [04. Fibonacci series.py](./04.%20Fibonacci%20series.py)

### Problem

Calculate the nth Fibonacci number where:

* F(0) = 0
* F(1) = 1
* F(n) = F(n-1) + F(n-2) for n ≥ 2

Example: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34...

### Logic

Fibonacci is a classic example of recursion with two recursive calls per function.

### How It Works (Naive Recursion)

```python
def fibonacci(n):
    if n <= 1:              # Base cases
        return n
    return fibonacci(n-1) + fibonacci(n-2)  # Two recursive calls
```

**Execution Tree for n=4:**

```
                    fib(4)
                   /      \
              fib(3)      fib(2)
             /     \      /     \
        fib(2)   fib(1) fib(1) fib(0)
       /     \
   fib(1)  fib(0)
```

### Time Complexity (Naive)

| Case             | Complexity | Calculation                                           |
| ---------------- | ---------- | ----------------------------------------------------- |
| **Best Case**    | O(1)       | When n = 0 or 1                                       |
| **Average Case** | O(2ⁿ)      | Exponential - each call makes 2 more calls            |
| **Worst Case**   | O(2ⁿ)      | T(n) = T(n-1) + T(n-2) + O(1) ≈ O(φⁿ) where φ ≈ 1.618 |

### Space Complexity (Naive)

* **Auxiliary Space**: O(n) - Maximum recursion depth is n

### Why Naive Recursion is Inefficient

Massive redundant calculations! Example for fib(5):

* fib(3) calculated 2 times
* fib(2) calculated 3 times
* fib(1) calculated 5 times

### Optimized Approaches

#### 1. Memoization (Top-Down DP)

```python
def fib_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]
```

**Time**: O(n), **Space**: O(n)

#### 2. Tabulation (Bottom-Up DP)

```python
def fib_dp(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]
```

**Time**: O(n), **Space**: O(n)

#### 3. Space-Optimized Iterative

```python
def fib_optimized(n):
    if n <= 1:
        return n
    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        current = prev1 + prev2
        prev2, prev1 = prev1, current
    return prev1
```

**Time**: O(n), **Space**: O(1)

### Complexity Comparison

| Approach        | Time  | Space | Notes                       |
| --------------- | ----- | ----- | --------------------------- |
| Naive Recursion | O(2ⁿ) | O(n)  | Very slow, educational only |
| Memoization     | O(n)  | O(n)  | Good for recursive thinking |
| Tabulation      | O(n)  | O(n)  | Classic DP                  |
| Space-Optimized | O(n)  | O(1)  | Best practical solution     |

### When to Use Each

* **Naive**: Only for learning/small n (< 20)
* **Memoization**: When recursion is natural to problem
* **Tabulation**: Standard DP problems
* **Optimized**: Production code, large n

---

## Sum of Digits

**📁 Implementation:** [05. Sum of digits.py](./05.%20Sum%20of%20digits.py)

### Problem

Calculate the sum of all digits in a number.

Example: 1234 → 1 + 2 + 3 + 4 = 10

### Logic

Extract the last digit (n % 10), add it to the sum of remaining digits (n // 10).

### How It Works

```python
def sum_of_digits(n):
    if n == 0:              # Base case
        return 0
    return (n % 10) + sum_of_digits(n // 10)
```

**Execution Flow for n=123:**

```
sum_of_digits(123)
  → 3 + sum_of_digits(12)
         → 2 + sum_of_digits(1)
                → 1 + sum_of_digits(0)
                       → 0 (base case)
                ← 1 + 0 = 1
         ← 2 + 1 = 3
  ← 3 + 3 = 6
Result: 6
```

### Step-by-Step Breakdown

For n = 1234:

1. 1234 % 10 = 4, remaining: 123
2. 123 % 10 = 3, remaining: 12
3. 12 % 10 = 2, remaining: 1
4. 1 % 10 = 1, remaining: 0
5. Base case: 0 returns 0
6. Sum: 4 + 3 + 2 + 1 + 0 = 10

### Time Complexity

| Case             | Complexity | Calculation                               |
| ---------------- | ---------- | ----------------------------------------- |
| **Best Case**    | O(1)       | Single digit (n < 10)                     |
| **Average Case** | O(log n)   | Number of digits = log₁₀(n)               |
| **Worst Case**   | O(log n)   | Recursive calls equal to number of digits |

**Why O(log n)?** Because we divide by 10 each time, similar to binary search dividing by 2.

### Space Complexity

* **Auxiliary Space**: O(log n) - Call stack depth equals number of digits

### Iterative Alternative

```python
def sum_of_digits_iterative(n):
    total = 0
    while n > 0:
        total += n % 10
        n //= 10
    return total
```

**Time**: O(log n), **Space**: O(1)

### Edge Cases

* **n = 0**: Returns 0
* **Single digit**: Returns that digit
* **Negative numbers**: Take absolute value first

### Applications

* Digital root calculation
* Checksum algorithms
* Number theory problems
* Validation algorithms (credit cards)

---

## Palindrome Check

**📁 Implementation:** [06. Palindrome.py](./06.%20Palindrome.py)

### Problem

Check if a string is a palindrome (reads same forwards and backwards).

Example: "racecar" → True, "hello" → False

### Logic

Compare first and last characters. If they match, recursively check the substring without those characters.

### How It Works

```python
def is_palindrome(s, start, end):
    if start >= end:        # Base case: single char or empty
        return True
    if s[start] != s[end]:  # Characters don't match
        return False
    return is_palindrome(s, start + 1, end - 1)  # Check middle
```

**Execution Flow for "racecar":**

```
is_palindrome("racecar", 0, 6)
  r == r ✓
  → is_palindrome("racecar", 1, 5)
      a == a ✓
      → is_palindrome("racecar", 2, 4)
          c == c ✓
          → is_palindrome("racecar", 3, 3)
              start >= end (base case)
              → True
          ← True
      ← True
  ← True
Result: True
```

### Time Complexity

| Case             | Complexity | Calculation                             |
| ---------------- | ---------- | --------------------------------------- |
| **Best Case**    | O(1)       | First and last chars don't match        |
| **Average Case** | O(n)       | Check approximately n/2 pairs           |
| **Worst Case**   | O(n)       | Perfect palindrome, check all n/2 pairs |

### Space Complexity

* **Auxiliary Space**: O(n) - Recursion depth is n/2 (each call removes 2 chars)

### Iterative Alternative (Two Pointer)

```python
def is_palindrome_iterative(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True
```

**Time**: O(n), **Space**: O(1)

### Variations

* **Ignore case**: Convert to lowercase first
* **Ignore spaces/punctuation**: Filter non-alphanumeric characters
* **Substring palindrome**: Find longest palindromic substring

### When to Use

* String validation
* Pattern matching
* Algorithm problems
* Data validation

---

## Number Palindrome

**📁 Implementation:** [07. Number Palindrome.py](./07.%20Number%20Palindrome.py)

### Problem

Check if a number is a palindrome (reads same forwards and backwards).

Example: 12321 → True, 12345 → False

### Approach 1: Convert to String

```python
def is_palindrome_string(n):
    s = str(n)
    return s == s[::-1]
```

**Time**: O(log n), **Space**: O(log n)

### Approach 2: Reverse Number Mathematically

```python
def is_palindrome_math(n):
    if n < 0:
        return False
    original = n
    reversed_num = 0
    while n > 0:
        reversed_num = reversed_num * 10 + (n % 10)
        n //= 10
    return original == reversed_num
```

### Approach 3: Recursive (Check Digits)

```python
def is_palindrome_recursive(n, divisor):
    if n < 10:
        return True
    # Compare first and last digits
    first = n // divisor
    last = n % 10
    if first != last:
        return False
    # Remove first and last digits
    n = (n % divisor) // 10
    return is_palindrome_recursive(n, divisor // 100)
```

### Time Complexity

| Approach          | Time     | Calculation                   |
| ----------------- | -------- | ----------------------------- |
| String Conversion | O(log n) | Create string of d digits     |
| Math Reversal     | O(log n) | d iterations where d = digits |
| Recursive         | O(log n) | d/2 recursive calls           |

### Space Complexity

| Approach          | Space    | Notes          |
| ----------------- | -------- | -------------- |
| String Conversion | O(log n) | String storage |
| Math Reversal     | O(1)     | Only variables |
| Recursive         | O(log n) | Call stack     |

### Edge Cases

* **Negative numbers**: Generally not palindromes (due to '-' sign)
* **Single digit**: Always palindrome
* **Trailing zeros**: 100 is not palindrome (reversed is 001 = 1)

### When to Use

* Number validation
* Mathematical problems
* Pattern recognition
* Algorithm challenges

---

## Comparison Summary

### Time & Space Complexity Table

| Problem           | Time     | Space    | Iterative Time | Iterative Space |
| ----------------- | -------- | -------- | -------------- | --------------- |
| Print 1 to N      | O(n)     | O(n)     | O(n)           | O(1)            |
| Print N to 1      | O(n)     | O(n)     | O(n)           | O(1)            |
| Factorial         | O(n)     | O(n)     | O(n)           | O(1)            |
| Fibonacci (Naive) | O(2ⁿ)    | O(n)     | O(n)           | O(1)*           |
| Sum of Digits     | O(log n) | O(log n) | O(log n)       | O(1)            |
| String Palindrome | O(n)     | O(n)     | O(n)           | O(1)            |
| Number Palindrome | O(log n) | O(log n) | O(log n)       | O(1)            |

*With space optimization

### When to Use Recursion

**Good Use Cases:**

* Problem has natural recursive structure (trees, graphs)
* Divide and conquer algorithms (merge sort, quick sort)
* Backtracking problems (N-Queens, Sudoku)
* Mathematical definitions (factorial, Fibonacci)
* Code readability is prioritized

**Avoid Recursion When:**

* Simple iteration suffices (print numbers)
* Stack overflow risk (very deep recursion)
* Performance is critical (function call overhead)
* Memory is constrained (call stack usage)

---

## Recursion Patterns

### Pattern 1: Linear Recursion (Single Call)

```python
# Example: Factorial
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

### Pattern 2: Binary Recursion (Two Calls)

```python
# Example: Fibonacci
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)
```

### Pattern 3: Tail Recursion (Last Operation)

```python
# Example: Tail-recursive factorial
def factorial_tail(n, acc=1):
    if n <= 1:
        return acc
    return factorial_tail(n-1, n * acc)
```

**Note**: Python doesn't optimize tail recursion, but pattern is useful

### Pattern 4: Multiple Base Cases

```python
# Example: String palindrome
def is_palindrome(s, start, end):
    if start >= end:          # Base case 1
        return True
    if s[start] != s[end]:    # Base case 2
        return False
    return is_palindrome(s, start+1, end-1)
```

---

## Common Recursion Mistakes

### 1. Missing Base Case

```python
# WRONG - Infinite recursion
def factorial(n):
    return n * factorial(n - 1)

# CORRECT
def factorial(n):
    if n <= 1:  # Base case
        return 1
    return n * factorial(n - 1)
```

### 2. Base Case Never Reached

```python
# WRONG - Progress in wrong direction
def print_n_to_1(n):
    if n == 0:
        return
    print(n)
    print_n_to_1(n + 1)  # Getting larger!

# CORRECT
def print_n_to_1(n):
    if n == 0:
        return
    print(n)
    print_n_to_1(n - 1)  # Moving toward base case
```

### 3. Stack Overflow

```python
# Problem: Too deep recursion
factorial(10000)  # May cause stack overflow

# Solution: Use iteration or increase recursion limit
import sys
sys.setrecursionlimit(15000)  # Use cautiously
```

### 4. Inefficient Recursion (Fibonacci)

```python
# WRONG - O(2^n) - Recalculates same values
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

# CORRECT - O(n) with memoization
def fib(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib(n-1, memo) + fib(n-2, memo)
    return memo[n]
```

---

## Debugging Recursion Tips

### 1. Trace Execution

Add print statements to see call flow:

```python
def factorial(n, depth=0):
    indent = "  " * depth
    print(f"{indent}factorial({n}) called")
    if n <= 1:
        print(f"{indent}returning 1")
        return 1
    result = n * factorial(n-1, depth+1)
    print(f"{indent}returning {result}")
    return result
```

### 2. Verify Base Cases

Test with smallest possible inputs:

* n = 0
* n = 1
* Empty string
* Single element

### 3. Check Progress

Ensure each recursive call moves toward base case:

* Parameters getting smaller
* String/array getting shorter
* Pointers converging

### 4. Visualize Call Stack

Draw the recursion tree for small inputs to understand flow.

---

## Advanced Recursion Concepts

### Memoization (Dynamic Programming)

Cache results to avoid redundant calculations:

```python
def expensive_recursion(n, memo={}):
    if n in memo:
        return memo[n]
    # ... compute result ...
    memo[n] = result
    return result
```

### Mutual Recursion

Two functions call each other:

```python
def is_even(n):
    if n == 0:
        return True
    return is_odd(n - 1)

def is_odd(n):
    if n == 0:
        return False
    return is_even(n - 1)
```

### Indirect Recursion

Function calls another which eventually calls the original:

```python
def func_a(n):
    if n > 0:
        func_b(n - 1)

def func_b(n):
    if n > 0:
        func_a(n - 1)
```

---
