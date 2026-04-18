# Mathematics Problems - Complete Reference Guide

## Table of Contents

1. [Sum of N Natural Numbers](#sum-of-n-natural-numbers) - [Code: 01. Sum of n Natural Numbers.py](./01.%20Sum%20of%20n%20Natural%20Numbers.py)
2. [Count Digits](#count-digits) - [Code: 02. Count Digits.py](./02.%20Count%20Digits.py)
3. [Palindrome Number](#palindrome-number) - [Code: 03. Palindrome Number.py](./03.%20Palindrome%20Number.py)
4. [Factorial Number](#factorial-number) - [Code: 04. Factorial Number.py](./04.%20Factorial%20Number.py)
5. [GCD or HCF](#gcd-or-hcf) - [Code: 05. GCD or HCF of two numbers.py](./05.%20GCD%20or%20HCF%20of%20two%20numbers.py)
6. [LCM](#lcm) - [Code: 06. LCM of two numbers.py](./06.%20LCM%20of%20two%20numbers.py)
7. [Check for Prime](#check-for-prime) - [Code: 07. Check for prime.py](./07.%20Check%20for%20prime.py)
8. [Prime Factorization](#prime-factorization) - [Code: 08. Prime Factorization.py](./08.%20Prime%20Factorization.py)
9. [All Divisors](#all-divisors) - [Code: 09. All Divisors of a Number.py](./09.%20All%20Divisors%20of%20a%20Number.py)
10. [Sieve of Eratosthenes](#sieve-of-eratosthenes) - [Code: 10. Sieve of Eratosthenes.py](./10.%20Sieve%20of%20Eratosthenes.py)
11. [Computing Power](#computing-power) - [Code: 11. Computing Power.py](./11.%20Computing%20Power.py)
12. [Iterative Power](#iterative-power) - [Code: 12. Iterative Power.py](./12.%20Iterative%20Power.py)
13. [Modular Multiplicative Inverse](#modular-multiplicative-inverse) - [Code: 13. Modular Multiplicative Inverse.py](./13.%20Modular%20Multiplicative%20Inverse.py)

---

## Sum of N Natural Numbers

**📁 Implementation:** [01. Sum of n Natural Numbers.py](./01.%20Sum%20of%20n%20Natural%20Numbers.py)

### Problem

Calculate the sum of first N natural numbers: 1 + 2 + 3 + ... + N

Example: N = 5 → 1 + 2 + 3 + 4 + 5 = 15

### Mathematical Formula

```
Sum = N × (N + 1) / 2
```

### Approach 1: Direct Formula (Best)

```python
def sum_natural(n):
    return n * (n + 1) // 2
```

**Time**: O(1), **Space**: O(1)

### Approach 2: Iterative Loop

```python
def sum_natural_loop(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total
```

**Time**: O(n), **Space**: O(1)

### Approach 3: Recursive

```python
def sum_natural_recursive(n):
    if n == 0:
        return 0
    return n + sum_natural_recursive(n - 1)
```

**Time**: O(n), **Space**: O(n) - call stack

### Time Complexity

| Approach  | Best/Avg/Worst | Calculation                   |
| --------- | -------------- | ----------------------------- |
| Formula   | O(1)           | Direct arithmetic calculation |
| Loop      | O(n)           | n iterations                  |
| Recursive | O(n)           | n recursive calls             |

### Space Complexity

* **Formula**: O(1) - No extra space
* **Loop**: O(1) - Only counter variable
* **Recursive**: O(n) - Call stack depth

### Proof of Formula

Using arithmetic progression:

```
Sum = 1 + 2 + 3 + ... + n
Sum = n + (n-1) + (n-2) + ... + 1  (reverse)
2×Sum = (n+1) + (n+1) + ... + (n+1)  (n terms)
2×Sum = n × (n+1)
Sum = n × (n+1) / 2
```

### When to Use

* Quick calculation of series sum
* Mathematical formulas (combinations, permutations)
* Algorithm complexity analysis
* **Always use formula approach** - it's most efficient

---

## Count Digits

**📁 Implementation:** [02. Count Digits.py](./02.%20Count%20Digits.py)

### Problem

Count the number of digits in a number.

Example: 12345 → 5 digits, 100 → 3 digits

### Approach 1: Logarithm (Best for positive numbers)

```python
import math
def count_digits_log(n):
    if n == 0:
        return 1
    return math.floor(math.log10(abs(n))) + 1
```

**Time**: O(1), **Space**: O(1)

### Approach 2: Convert to String

```python
def count_digits_string(n):
    return len(str(abs(n)))
```

**Time**: O(log n), **Space**: O(log n)

### Approach 3: Iterative Division

```python
def count_digits_iterative(n):
    if n == 0:
        return 1
    count = 0
    n = abs(n)
    while n > 0:
        count += 1
        n //= 10
    return count
```

**Time**: O(log n), **Space**: O(1)

### Time Complexity

| Approach          | Complexity | Calculation                             |
| ----------------- | ---------- | --------------------------------------- |
| Logarithm         | O(1)       | Single math operation                   |
| String Conversion | O(log n)   | Converting d digits to string           |
| Iterative         | O(log n)   | d iterations where d = number of digits |

**Why O(log n)?** Dividing by 10 repeatedly reduces n logarithmically (log₁₀ n gives number of digits).

### Space Complexity

* **Logarithm**: O(1)
* **String**: O(log n) - stores string
* **Iterative**: O(1)

### Edge Cases

* **n = 0**: Has 1 digit by convention
* **Negative numbers**: Count absolute value (ignore sign)
* **Single digit**: Returns 1

### Applications

* Input validation
* Number formatting
* Digit manipulation algorithms
* Mathematical computations

---

## Palindrome Number

**📁 Implementation:** [03. Palindrome Number.py](./03.%20Palindrome%20Number.py)

### Problem

Check if a number reads the same forwards and backwards.

Example: 12321 → True, 12345 → False

### Approach 1: Reverse and Compare

```python
def is_palindrome(n):
    if n < 0:
        return False
    original = n
    reversed_num = 0
    while n > 0:
        reversed_num = reversed_num * 10 + (n % 10)
        n //= 10
    return original == reversed_num
```

### Approach 2: String Comparison

```python
def is_palindrome_string(n):
    s = str(n)
    return s == s[::-1]
```

### Approach 3: Compare First and Last Digits

```python
def is_palindrome_math(n):
    if n < 0:
        return False
    
    # Find number of digits
    divisor = 1
    temp = n
    while temp >= 10:
        temp //= 10
        divisor *= 10
    
    while n > 0:
        first = n // divisor
        last = n % 10
        if first != last:
            return False
        # Remove first and last digits
        n = (n % divisor) // 10
        divisor //= 100
    return True
```

### Time Complexity

| Approach       | Complexity | Calculation                |
| -------------- | ---------- | -------------------------- |
| Reverse Number | O(log n)   | d iterations for d digits  |
| String         | O(log n)   | Create string + comparison |
| Math           | O(log n)   | Check d/2 digit pairs      |

### Space Complexity

* **Reverse Number**: O(1) - Only variables
* **String**: O(log n) - String storage
* **Math**: O(1) - Only variables

### Edge Cases

* Negative numbers: Not palindromes (due to '-' sign)
* Single digit: Always palindrome
* Numbers with trailing zeros: 100 → reversed is 1, not palindrome

### When to Use

* Number validation
* Pattern recognition problems
* Mathematical puzzles

---

## Factorial Number

**📁 Implementation:** [04. Factorial Number.py](./04.%20Factorial%20Number.py)

### Problem

Calculate N! = N × (N-1) × (N-2) × ... × 1

Example: 5! = 5 × 4 × 3 × 2 × 1 = 120

### Approach 1: Iterative (Best)

```python
def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```

**Time**: O(n), **Space**: O(1)

### Approach 2: Recursive

```python
def factorial_recursive(n):
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)
```

**Time**: O(n), **Space**: O(n) - call stack

### Time Complexity

| Approach  | Complexity | Calculation         |
| --------- | ---------- | ------------------- |
| Iterative | O(n)       | n-1 multiplications |
| Recursive | O(n)       | n recursive calls   |

### Space Complexity

* **Iterative**: O(1) - Only result variable
* **Recursive**: O(n) - Recursion stack depth

### Large Factorials

* Python handles arbitrary precision integers
* Factorial grows very quickly: 20! = 2,432,902,008,176,640,000
* For modular arithmetic: `(a * b) % m = ((a % m) * (b % m)) % m`

### Applications

* Permutations: P(n,r) = n! / (n-r)!
* Combinations: C(n,r) = n! / (r! × (n-r)!)
* Probability calculations
* Mathematical analysis

---

## GCD or HCF

**📁 Implementation:** [05. GCD or HCF of two numbers.py](./05.%20GCD%20or%20HCF%20of%20two%20numbers.py)

### Problem

Find the Greatest Common Divisor (GCD) or Highest Common Factor (HCF) of two numbers.

**Definition**: Largest positive integer that divides both numbers without remainder.

Example: GCD(12, 18) = 6

### Approach 1: Euclidean Algorithm (Best)

Based on: GCD(a, b) = GCD(b, a % b)

```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
```

**Time**: O(log min(a,b)), **Space**: O(1)

### Approach 2: Recursive Euclidean

```python
def gcd_recursive(a, b):
    if b == 0:
        return a
    return gcd_recursive(b, a % b)
```

**Time**: O(log min(a,b)), **Space**: O(log min(a,b))

### Approach 3: Naive (Finding all divisors)

```python
def gcd_naive(a, b):
    result = min(a, b)
    while result > 0:
        if a % result == 0 and b % result == 0:
            return result
        result -= 1
```

**Time**: O(min(a,b)), **Space**: O(1)

### Time Complexity

| Approach  | Complexity      | Calculation                              |
| --------- | --------------- | ---------------------------------------- |
| Euclidean | O(log min(a,b)) | Number of divisions until remainder is 0 |
| Recursive | O(log min(a,b)) | Same as iterative but with call stack    |
| Naive     | O(min(a,b))     | Check every number from min down to 1    |

### Why Euclidean is O(log n)?

Each iteration at least halves one of the numbers (proven by Fibonacci numbers being worst case).

### Space Complexity

* **Euclidean**: O(1)
* **Recursive**: O(log min(a,b))
* **Naive**: O(1)

### How Euclidean Algorithm Works

Example: GCD(48, 18)

```
GCD(48, 18)
  → 48 % 18 = 12
GCD(18, 12)
  → 18 % 12 = 6
GCD(12, 6)
  → 12 % 6 = 0
GCD(6, 0)
  → 6
```

### Properties

* GCD(a, 0) = a
* GCD(a, b) = GCD(b, a)
* GCD(a, b) = GCD(a-b, b) when a > b

### Applications

* Simplifying fractions
* Finding LCM
* Cryptography (RSA algorithm)
* Number theory problems

---

## LCM

**📁 Implementation:** [06. LCM of two numbers.py](./06.%20LCM%20of%20two%20numbers.py)

### Problem

Find the Least Common Multiple (LCM) of two numbers.

**Definition**: Smallest positive integer divisible by both numbers.

Example: LCM(4, 6) = 12

### Key Relationship

```
LCM(a, b) × GCD(a, b) = a × b

Therefore:
LCM(a, b) = (a × b) / GCD(a, b)
```

### Approach 1: Using GCD Formula (Best)

```python
def lcm(a, b):
    return (a * b) // gcd(a, b)
```

**Time**: O(log min(a,b)), **Space**: O(1)

### Approach 2: Naive (Multiples)

```python
def lcm_naive(a, b):
    max_num = max(a, b)
    while True:
        if max_num % a == 0 and max_num % b == 0:
            return max_num
        max_num += max(a, b)
```

**Time**: O(a × b / GCD(a,b)), **Space**: O(1)

### Time Complexity

| Approach    | Complexity      | Calculation                  |
| ----------- | --------------- | ---------------------------- |
| GCD Formula | O(log min(a,b)) | Dominated by GCD calculation |
| Naive       | O(a×b/GCD(a,b)) | Could be very large          |

### Space Complexity

* **GCD Formula**: O(1)
* **Naive**: O(1)

### Why the Formula Works

**Mathematical Proof:**

* Every common multiple is a multiple of LCM
* a × b contains all prime factors of both numbers (with maximum powers)
* GCD contains common prime factors
* Dividing removes the overcounting

Example: LCM(12, 18)

```
12 = 2² × 3
18 = 2 × 3²
GCD = 2 × 3 = 6
LCM = (12 × 18) / 6 = 216 / 6 = 36
LCM = 2² × 3² = 36 ✓
```

### Avoiding Overflow

For large numbers, compute as:

```python
def lcm_safe(a, b):
    return a // gcd(a, b) * b  # Divide first to prevent overflow
```

### Extension: LCM of Multiple Numbers

```python
from functools import reduce

def lcm_multiple(numbers):
    return reduce(lambda a, b: (a * b) // gcd(a, b), numbers)
```

### Applications

* Time synchronization problems
* Repeating patterns
* Scheduling
* Music theory (rhythm patterns)

---

## Check for Prime

**📁 Implementation:** [07. Check for prime.py](./07.%20Check%20for%20prime.py)

### Problem

Determine if a number is prime (only divisible by 1 and itself).

Example: 7 → Prime, 9 → Not Prime (divisible by 3)

### Approach 1: Trial Division up to √n (Best)

```python
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
```

**Time**: O(√n), **Space**: O(1)

### Why Check Only Up to √n?

If n = a × b and a ≤ b, then a ≤ √n.
So if n has a divisor, at least one must be ≤ √n.

Example: Is 37 prime?

* Check up to √37 ≈ 6.08
* Test: 2, 3, 5 (no need to test 4, 6 as they're even)
* None divide 37 → Prime!

### Approach 2: Naive (Check All)

```python
def is_prime_naive(n):
    if n <= 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True
```

**Time**: O(n), **Space**: O(1)

### Optimized Approach Explanation

1. Handle edge cases: n ≤ 1 (not prime), n = 2,3 (prime)
2. Check divisibility by 2 and 3
3. All primes > 3 are of form 6k±1
4. Check only numbers of form 6k±1 up to √n

**Why 6k±1?**

* 6k: divisible by 6
* 6k+2, 6k+4: divisible by 2
* 6k+3: divisible by 3
* Only 6k+1 and 6k+5 (= 6(k+1)-1) can be prime

### Time Complexity

| Approach          | Complexity | Calculation                     |
| ----------------- | ---------- | ------------------------------- |
| Naive             | O(n)       | Check all numbers from 2 to n-1 |
| √n Check          | O(√n)      | Check divisors up to √n         |
| 6k±1 Optimization | O(√n/3)    | Check only 1/3 of candidates    |

### Space Complexity

* All approaches: O(1)

### Special Cases

* n ≤ 1: Not prime by definition
* n = 2: Only even prime
* n = 3: Prime
* Even numbers > 2: Not prime

### Applications

* Cryptography (RSA, key generation)
* Hash table sizing
* Random number generation
* Number theory

---

## Prime Factorization

**📁 Implementation:** [08. Prime Factorization.py](./08.%20Prime%20Factorization.py)

### Problem

Find all prime factors of a number with their powers.

Example: 60 = 2² × 3 × 5

### Approach 1: Division by Primes (Efficient)

```python
def prime_factorization(n):
    factors = []
    
    # Check for 2s
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    
    # Check odd numbers from 3
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 2
    
    # If n is prime > 2
    if n > 2:
        factors.append(n)
    
    return factors
```

### How It Works

For n = 60:

```
60 ÷ 2 = 30  → factor: 2
30 ÷ 2 = 15  → factor: 2
15 ÷ 3 = 5   → factor: 3
5 is prime   → factor: 5
Result: [2, 2, 3, 5] = 2² × 3 × 5
```

### Time Complexity

| Approach       | Complexity | Calculation                                      |
| -------------- | ---------- | ------------------------------------------------ |
| Trial Division | O(√n)      | Check divisors up to √n, each division reduces n |

**Why O(√n)?**

* We only check up to √n
* Each successful division reduces n
* Worst case: n is prime (check all up to √n)

### Space Complexity

* O(log n) - Maximum number of prime factors (when n = 2^k)

### Optimizations

1. **Check 2 separately**, then only odd numbers
2. **Stop at √n** for remaining checks
3. **Early termination** when n becomes 1

### With Powers (Compressed Format)

```python
def prime_factorization_with_powers(n):
    factors = {}
    
    # Check for 2s
    while n % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        n //= 2
    
    # Check odd numbers
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors[i] = factors.get(i, 0) + 1
            n //= i
        i += 2
    
    if n > 2:
        factors[n] = 1
    
    return factors
```

Example: 60 → {2: 2, 3: 1, 5: 1}

### Applications

* Finding divisors of a number
* GCD/LCM calculations
* Cryptography
* Number theory problems
* Simplifying fractions

---

## All Divisors

**📁 Implementation:** [09. All Divisors of a Number.py](./09.%20All%20Divisors%20of%20a%20Number.py)

### Problem

Find all positive divisors of a number.

Example: 36 → [1, 2, 3, 4, 6, 9, 12, 18, 36]

### Approach 1: Check Up to √n (Efficient)

```python
def all_divisors(n):
    divisors = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            divisors.append(i)
            if i != n // i:  # Avoid duplicates for perfect squares
                divisors.append(n // i)
        i += 1
    return sorted(divisors)
```

### How It Works

For n = 36:

```
i = 1: 36 % 1 = 0 → divisors: 1, 36
i = 2: 36 % 2 = 0 → divisors: 2, 18
i = 3: 36 % 3 = 0 → divisors: 3, 12
i = 4: 36 % 4 = 0 → divisors: 4, 9
i = 5: 36 % 5 ≠ 0
i = 6: 36 % 6 = 0 → divisor: 6 (6 = 36/6, don't add twice)
Stop at √36 = 6
Result: [1, 2, 3, 4, 6, 9, 12, 18, 36]
```

### Approach 2: Naive

```python
def all_divisors_naive(n):
    divisors = []
    for i in range(1, n + 1):
        if n % i == 0:
            divisors.append(i)
    return divisors
```

### Time Complexity

| Approach  | Complexity | Calculation                     |
| --------- | ---------- | ------------------------------- |
| Naive     | O(n)       | Check every number from 1 to n  |
| Efficient | O(√n)      | Check only up to √n, find pairs |

### Space Complexity

* O(d) where d is the number of divisors
* For most numbers, d = O(log n) on average
* Worst case: d = O(√n) for highly composite numbers

### Why Check Only √n?

If i divides n, then n/i also divides n.

* If i < √n, then n/i > √n (larger pair)
* If i = √n, then i = n/i (perfect square case)

### Count of Divisors Formula

If n = p₁^a₁ × p₂^a₂ × ... × pₖ^aₖ (prime factorization):

```
Number of divisors = (a₁ + 1) × (a₂ + 1) × ... × (aₖ + 1)
```

Example: 36 = 2² × 3²

* Count = (2+1) × (2+1) = 3 × 3 = 9 divisors ✓

### Sum of Divisors Formula

```
Sum = [(p₁^(a₁+1) - 1)/(p₁ - 1)] × [(p₂^(a₂+1) - 1)/(p₂ - 1)] × ...
```

### Applications

* Perfect numbers (sum of divisors = 2n)
* Abundant/deficient numbers
* Number theory
* Algorithm optimizations

---

## Sieve of Eratosthenes

**📁 Implementation:** [10. Sieve of Eratosthenes.py](./10.%20Sieve%20of%20Eratosthenes.py)

### Problem

Find all prime numbers up to a given number N.

Example: N = 20 → [2, 3, 5, 7, 11, 13, 17, 19]

### Algorithm

Ancient algorithm for finding all primes up to N by iteratively marking multiples of each prime.

### How It Works

```python
def sieve_of_eratosthenes(n):
    if n < 2:
        return []
    
    # Create boolean array, initially all True
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    
    # Start with 2
    p = 2
    while p * p <= n:
        if is_prime[p]:
            # Mark all multiples of p as not prime
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
        p += 1
    
    # Collect all primes
    return [i for i in range(n + 1) if is_prime[i]]
```

### Visual Example (N = 20)

```
Initial: [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

p=2: Mark 4,6,8,10,12,14,16,18,20
     [2,3,_,5,_,7,_,9,__,11,__,13,__,15,__,17,__,19,__]

p=3: Mark 9,15 (6,12,18 already marked)
     [2,3,_,5,_,7,_,_,__,11,__,13,__,__,__,17,__,19,__]

p=5: p²=25 > 20, stop

Result: [2,3,5,7,11,13,17,19]
```

### Why Start at p²?

All composite numbers less than p² have already been marked by smaller primes.

Example: For p=5, multiples 10,15,20 already marked by 2 or 3. Start at 25.

### Time Complexity

| Operation | Complexity     | Calculation                                   |
| --------- | -------------- | --------------------------------------------- |
| Sieve     | O(n log log n) | Sum of n/2 + n/3 + n/5 + ... (for each prime) |

**Why O(n log log n)?**

* Mark multiples of each prime p: O(n/p) operations
* Sum over all primes: n×(1/2 + 1/3 + 1/5 + 1/7 + ...) ≈ n log log n

### Space Complexity

* O(n) - Boolean array of size n+1

### Optimizations

#### 1. Only Odd Numbers

```python
# Skip even numbers except 2
# Use half the space
```

#### 2. Segmented Sieve

For very large n, process in segments to fit in cache.

### Comparison with Other Methods

| Method                | Single Prime Check | All Primes up to N |
| --------------------- | ------------------ | ------------------ |
| Trial Division        | O(√n)              | O(n√n)             |
| Sieve of Eratosthenes | N/A                | O(n log log n)     |

### When to Use

* Finding all primes in a range (use sieve)
* Checking if single number is prime (use trial division)
* Preprocessing for multiple queries (use sieve)

### Applications

* Prime number generation
* Cryptography (finding large primes)
* Number theory research
* Competitive programming

---

## Computing Power

**📁 Implementation:** [11. Computing Power.py](./11.%20Computing%20Power.py)

### Problem

Compute x^n (x raised to power n) efficiently.

Example: 2^10 = 1024

### Approach 1: Exponentiation by Squaring (Best)

**Binary Exponentiation** - Most efficient recursive method

```python
def power(x, n):
    if n == 0:
        return 1
    if n < 0:
        return 1 / power(x, -n)
    
    if n % 2 == 0:
        half = power(x, n // 2)
        return half * half
    else:
        return x * power(x, n - 1)
```

**Time**: O(log n), **Space**: O(log n) - recursion stack

### How It Works

Key insight: x^n = (x^(n/2))² when n is even

Example: 2^10

```
2^10 = (2^5)²
2^5 = 2 × (2^2)²
2^2 = (2^1)²
2^1 = 2 × 2^0
2^0 = 1

Unwinding:
2^1 = 2 × 1 = 2
2^2 = 2 × 2 = 4
2^5 = 2 × 16 = 32
2^10 = 32 × 32 = 1024
```

### Approach 2: Naive Loop

```python
def power_naive(x, n):
    result = 1
    for _ in range(n):
        result *= x
    return result
```

**Time**: O(n), **Space**: O(1)

### Time Complexity

| Approach               | Complexity | Calculation          |
| ---------------------- | ---------- | -------------------- |
| Naive Loop             | O(n)       | Multiply x, n times  |
| Binary Exp (Recursive) | O(log n)   | Halve n each time    |
| Binary Exp (Iterative) | O(log n)   | Same logic, no stack |

**Why O(log n)?**
We divide n by 2 in each recursive call → log₂(n) calls.

### Space Complexity

* **Recursive**: O(log n) - Call stack depth
* **Iterative**: O(1) - No recursion

### Binary Representation Method

Power can be computed using binary representation of exponent:

Example: 2^13

```
13 in binary = 1101 = 2³ + 2² + 2⁰
2^13 = 2^8 × 2^4 × 2^1 = 256 × 16 × 2 = 8192
```

### Applications

* Fast modular exponentiation (cryptography)
* Large number computations
* Scientific calculations
* Graphics transformations (matrix powers)

---

## Iterative Power

**📁 Implementation:** [12. Iterative Power.py](./12.%20Iterative%20Power.py)

### Problem

Compute x^n using iteration instead of recursion (avoids stack overflow for large n).

### Approach: Binary Exponentiation (Iterative)

```python
def power_iterative(x, n):
    if n == 0:
        return 1
    if n < 0:
        x = 1 / x
        n = -n
    
    result = 1
    current_power = x
    
    while n > 0:
        if n % 2 == 1:  # If current bit is 1
            result *= current_power
        current_power *= current_power  # Square the base
        n //= 2  # Move to next bit
    
    return result
```

### How It Works (Bit by Bit)

Example: 3^13 where 13 = 1101₂

```
n = 13 (1101₂), x = 3, result = 1

Iteration 1: n = 13 (1101₂), bit = 1
  result = 1 × 3¹ = 3
  current_power = 3² = 9
  n = 6 (110₂)

Iteration 2: n = 6 (110₂), bit = 0
  result = 3 (unchanged)
  current_power = 9² = 81
  n = 3 (11₂)

Iteration 3: n = 3 (11₂), bit = 1
  result = 3 × 81 = 243
  current_power = 81² = 6561
  n = 1 (1₂)

Iteration 4: n = 1 (1₂), bit = 1
  result = 243 × 6561 = 1,594,323
  n = 0 → Stop

3^13 = 1,594,323 ✓
```

### Time Complexity

| Case         | Complexity | Calculation              |
| ------------ | ---------- | ------------------------ |
| Best Case    | O(1)       | When n = 0 or 1          |
| Average Case | O(log n)   | Process each bit of n    |
| Worst Case   | O(log n)   | Process all log₂(n) bits |

### Space Complexity

* **Auxiliary Space**: O(1) - Only uses variables, no recursion

### Comparison: Recursive vs Iterative

| Aspect              | Recursive            | Iterative          |
| ------------------- | -------------------- | ------------------ |
| Time                | O(log n)             | O(log n)           |
| Space               | O(log n)             | O(1)               |
| Stack Overflow Risk | Yes (deep recursion) | No                 |
| Readability         | More intuitive       | Slightly complex   |
| Production Use      | Good for small n     | Better for large n |

### When to Use

* Large exponents (avoid stack overflow)
* Production systems (better space efficiency)
* Embedded systems (limited stack)
* When O(1) space is critical

### Applications

* Modular exponentiation in cryptography
* Fast Fibonacci (matrix exponentiation)
* Computing large powers efficiently

---

## Modular Multiplicative Inverse

**📁 Implementation:** [13. Modular Multiplicative Inverse.py](./13.%20Modular%20Multiplicative%20Inverse.py)

### Problem

Find the modular multiplicative inverse of a number 'a' under modulo 'm'.

**Definition**: Find x such that (a × x) % m = 1

Example: Inverse of 3 under mod 11 is 4 because (3 × 4) % 11 = 12 % 11 = 1

### Prerequisites

Modular inverse exists **only if** GCD(a, m) = 1 (a and m are coprime).

### Approach 1: Extended Euclidean Algorithm (Best)

```python
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    
    if gcd != 1:
        return None  # Inverse doesn't exist
    
    return (x % m + m) % m  # Ensure positive result
```

**Time**: O(log min(a,m)), **Space**: O(log min(a,m))

### How Extended Euclidean Works

Extended Euclidean finds integers x and y such that:

```
a × x + m × y = GCD(a, m)
```

If GCD(a, m) = 1:

```
a × x + m × y = 1
a × x = 1 - m × y
a × x ≡ 1 (mod m)  [since m×y vanishes under mod m]
Therefore, x is the modular inverse of a
```

### Example: Find inverse of 3 under mod 11

```
extended_gcd(3, 11):
  gcd(11, 3)
    gcd(3, 2)
      gcd(2, 1)
        gcd(1, 0) → return (1, 1, 0)
      ← x = 0, y = 1 - 2×0 = 1
    ← x = 1, y = 0 - 1×1 = -1
  ← x = -1, y = 1 - 3×(-1) = 4

3 × 4 + 11 × (-1) = 12 - 11 = 1 ✓
x = 4 (taking positive modulo)

Verification: (3 × 4) % 11 = 12 % 11 = 1 ✓
```

### Approach 2: Fermat's Little Theorem (When m is prime)

If m is prime:

```
a^(m-1) ≡ 1 (mod m)
a × a^(m-2) ≡ 1 (mod m)
Therefore: inverse(a) = a^(m-2) mod m
```

```python
def mod_inverse_fermat(a, m):
    # Only works when m is prime
    if gcd(a, m) != 1:
        return None
    return power(a, m - 2, m)  # Using modular exponentiation
```

**Time**: O(log m), **Space**: O(1) with iterative power

### Approach 3: Naive (Brute Force)

```python
def mod_inverse_naive(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None
```

**Time**: O(m), **Space**: O(1)

### Time Complexity Comparison

| Approach           | Complexity      | Notes                      |
| ------------------ | --------------- | -------------------------- |
| Extended Euclidean | O(log min(a,m)) | Works for any coprime a, m |
| Fermat's Theorem   | O(log m)        | Only when m is prime       |
| Naive              | O(m)            | Too slow for large m       |

### Space Complexity

* **Extended Euclidean**: O(log min(a,m)) - recursion depth
* **Fermat's Theorem**: O(1) with iterative power
* **Naive**: O(1)

### Why It Matters

Modular inverse is crucial for:

1. **Division in modular arithmetic**: (a/b) mod m = (a × b⁻¹) mod m
2. **Cryptography**: RSA encryption/decryption
3. **Solving linear congruences**: ax ≡ b (mod m)
4. **Computer algebra systems**

### Properties

* Inverse of (a mod m) = inverse of a (mod m)
* If a has inverse x: (a × x) % m = 1 and (x × a) % m = 1
* Inverse of 1 is always 1
* If m is prime, all numbers 1 to m-1 have inverses

### Example Applications

#### Modular Division

```python
# Compute (a / b) mod m
def mod_divide(a, b, m):
    b_inv = mod_inverse(b, m)
    if b_inv is None:
        return None
    return (a * b_inv) % m
```

#### Solving Linear Congruence

```python
# Solve: ax ≡ b (mod m)
def solve_congruence(a, b, m):
    a_inv = mod_inverse(a, m)
    if a_inv is None:
        return None
    return (b * a_inv) % m
```

### When to Use Each Method

* **Extended Euclidean**: General case, works for any coprime numbers
* **Fermat's Theorem**: When modulus is prime and you have fast modular exponentiation
* **Naive**: Only for very small m (< 1000) or educational purposes

---

## Comparison Summary

### Time Complexity Table

| Problem               | Best Approach         | Time            | Space          | Notes                    |
| --------------------- | --------------------- | --------------- | -------------- | ------------------------ |
| Sum of N Numbers      | Formula               | O(1)            | O(1)           | Always use formula       |
| Count Digits          | Logarithm             | O(1)            | O(1)           | Or iterative O(log n)    |
| Palindrome Number     | Reverse               | O(log n)        | O(1)           | Check digit by digit     |
| Factorial             | Iterative             | O(n)            | O(1)           | Avoid recursion          |
| GCD                   | Euclidean             | O(log min(a,b)) | O(1)           | Very efficient           |
| LCM                   | GCD Formula           | O(log min(a,b)) | O(1)           | Use: a×b/GCD(a,b)        |
| Prime Check           | √n with 6k±1          | O(√n)           | O(1)           | Optimal for single check |
| Prime Factorization   | Trial Division        | O(√n)           | O(log n)       | Check up to √n           |
| All Divisors          | Check up to √n        | O(√n)           | O(d)           | Find pairs               |
| Sieve of Eratosthenes | Sieve                 | O(n log log n)  | O(n)           | Best for multiple primes |
| Power                 | Binary Exponentiation | O(log n)        | O(1) iterative | Much faster than O(n)    |
| Modular Inverse       | Extended Euclidean    | O(log m)        | O(log m)       | Or Fermat if m prime     |

---

## Important Mathematical Concepts

### Prime Numbers

* **Definition**: Numbers > 1 with exactly two divisors (1 and itself)
* **Fundamental Theorem**: Every integer > 1 is either prime or can be uniquely factored into primes
* **Distribution**: Approximately n/ln(n) primes up to n

### Modular Arithmetic

* **(a + b) mod m = ((a mod m) + (b mod m)) mod m**
* **(a × b) mod m = ((a mod m) × (b mod m)) mod m**
* **(a^b) mod m**: Use binary exponentiation with mod at each step
* **Division**: Use modular inverse: (a/b) mod m = (a × b⁻¹) mod m

### GCD Properties

* **GCD(a, b) = GCD(b, a mod b)** - Euclidean algorithm
* **GCD(a, 0) = a**
* **LCM(a, b) × GCD(a, b) = a × b**
* **Bézout's Identity**: GCD(a, b) = a×x + b×y for some integers x, y

### Divisibility Rules

* **By 2**: Last digit is even
* **By 3**: Sum of digits divisible by 3
* **By 5**: Last digit is 0 or 5
* **By 9**: Sum of digits divisible by 9
* **By 11**: Alternating sum of digits divisible by 11

---

## Optimization Tips

### 1. Use Mathematical Formulas

Prefer O(1) formulas over O(n) loops when available:

* Sum of n numbers: n(n+1)/2
* Sum of squares: n(n+1)(2n+1)/6
* Sum of cubes: [n(n+1)/2]²

### 2. Check Up to √n

For divisibility, factorization, primality - only check up to √n.

### 3. Avoid Repeated Calculations

* Memoize GCD/LCM if computing multiple times
* Precompute factorials for combinations
* Use sieve for multiple prime queries

### 4. Binary Exponentiation

Always use O(log n) exponentiation, never O(n) loop for powers.

### 5. Modular Arithmetic

When dealing with large numbers:

* Apply mod at each step to prevent overflow
* Use modular inverse for division
* Use fast modular exponentiation

---

## Common Patterns

### Pattern 1: Digit Manipulation

```python
# Extract digits right to left
while n > 0:
    digit = n % 10
    n //= 10

# Count digits: O(log n)
# Reverse number: O(log n)
# Sum digits: O(log n)
```

### Pattern 2: Prime-Related

```python
# Check prime: O(√n)
for i in range(2, int(n**0.5) + 1):
    if n % i == 0:
        return False

# Find all primes up to n: O(n log log n)
# Use Sieve of Eratosthenes
```

### Pattern 3: Factor Pairs

```python
# Find divisors in pairs
for i in range(1, int(n**0.5) + 1):
    if n % i == 0:
        # Found pair: i and n//i
```

### Pattern 4: Binary Exponentiation

```python
result = 1
while n > 0:
    if n % 2 == 1:
        result *= base
    base *= base
    n //= 2
```

---

## Edge Cases to Remember

### Always Consider

1. **n = 0**: Special case for many problems
2. **n = 1**: Often base case
3. **Negative numbers**: Handle sign separately
4. **Very large n**: Watch for overflow (less issue in Python)
5. **GCD(a, 0) = a**: Don't divide by zero
6. **Prime checks**: 2 is the only even prime
7. **Modular inverse**: Exists only if GCD(a, m) = 1

---
