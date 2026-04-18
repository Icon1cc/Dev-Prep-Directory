# Stack - Complete Reference Guide

## Table of Contents

1. [Stack Operations](#stack-operations) - [Code: 01. Operations in stack.py](./01.%20Operations%20in%20stack.py)
2. [List Implementation](#list-implementation-of-stack) - [Code: 02. List Implementation of stack.py](./02.%20List%20Implementation%20of%20stack.py)
3. [Deque Implementation](#deque-implementation-of-stack) - [Code: 03. Deque implementation of stack.py](./03.%20Deque%20implementation%20of%20stack.py)
4. [Linked List Implementation](#linked-list-implementation-of-stack) - [Code: 04. Linked List implementation of stack.py](./04.%20Linked%20List%20implementation%20of%20stack.py)
5. [Balanced Parentheses](#check-for-balanced-parentheses) - [Code: 05. Check for balanced paranthesis.py](./05.%20Check%20for%20balanced%20paranthesis.py)
6. [Infix to Postfix](#infix-to-postfix-conversion) - [Code: 06. Infix to Postfix.py](./06.%20Infix%20to%20Postfix.py)
7. [Prefix to Infix](#prefix-to-infix-conversion) - [Code: 07. Prefix to Infix.py](./07.%20Prefix%20to%20Infix.py)
8. [Postfix to Infix](#postfix-to-infix-conversion) - [Code: 08. Postfix to Infix.py](./08.%20Postfix%20to%20Infix.py)
9. [Parenthesis Checker](#parenthesis-checker) - [Code: 09. Paranthesis checker.py](./09.%20Paranthesis%20checker.py)

---

## Understanding Stacks

### What is a Stack?

A **Stack** is a linear data structure that follows the **LIFO** (Last In, First Out) principle. The last element added is the first one to be removed.

### Visual Representation

```
    ┌───────┐
    │   30  │  ← Top (Last In, First Out)
    ├───────┤
    │   20  │
    ├───────┤
    │   10  │  ← Bottom
    └───────┘

Push 40:        Pop:
    ┌───────┐       ┌───────┐
    │   40  │ ← Top │       │
    ├───────┤       ├───────┤
    │   30  │       │   30  │ ← Top (40 removed)
    ├───────┤       ├───────┤
    │   20  │       │   20  │
    ├───────┤       ├───────┤
    │   10  │       │   10  │
    └───────┘       └───────┘
```

### Core Operations

| Operation | Description | Time Complexity |
|-----------|-------------|-----------------|
| **Push** | Add element to top | O(1) |
| **Pop** | Remove and return top element | O(1) |
| **Peek/Top** | View top element without removing | O(1) |
| **isEmpty** | Check if stack is empty | O(1) |
| **Size** | Return number of elements | O(1) |

### Real-World Analogies

1. **Stack of plates**: Take from top, add to top
2. **Browser back button**: Most recent page first
3. **Undo operation**: Most recent action first
4. **Function call stack**: Last called, first to return

---

## Stack Operations
**📁 Implementation:** [01. Operations in stack.py](./01.%20Operations%20in%20stack.py)

### Basic Stack Class

```python
class Stack:
    def __init__(self):
        self.stack = []

    def push(self, data):
        """Add element to top"""
        self.stack.append(data)

    def pop(self):
        """Remove and return top element"""
        if not self.is_empty():
            return self.stack.pop()
        raise IndexError("Stack Underflow")

    def peek(self):
        """View top element without removing"""
        if not self.is_empty():
            return self.stack[-1]
        raise IndexError("Stack is empty")

    def is_empty(self):
        """Check if stack is empty"""
        return len(self.stack) == 0

    def size(self):
        """Return number of elements"""
        return len(self.stack)
```

### Usage Example

```python
s = Stack()
s.push(10)
s.push(20)
s.push(30)

print(s.peek())    # 30
print(s.pop())     # 30
print(s.size())    # 2
print(s.is_empty())# False
```

---

## List Implementation of Stack
**📁 Implementation:** [02. List Implementation of stack.py](./02.%20List%20Implementation%20of%20stack.py)

### Python List as Stack

Python's built-in list provides efficient stack operations.

```python
# Using list as stack
stack = []

# Push
stack.append(10)
stack.append(20)
stack.append(30)

# Pop
top = stack.pop()  # Returns 30

# Peek
top = stack[-1]    # 20 (without removing)

# Check empty
is_empty = len(stack) == 0
```

### Time Complexity

| Operation | List | Notes |
|-----------|------|-------|
| Push (append) | O(1)* | Amortized |
| Pop | O(1) | From end |
| Peek | O(1) | Index -1 |

*Amortized O(1) due to dynamic array resizing

### Advantages
- Simple, built-in
- No external imports needed
- Dynamic sizing

### Disadvantages
- Occasional O(n) for resizing
- Uses more memory than linked list for small stacks

---

## Deque Implementation of Stack
**📁 Implementation:** [03. Deque implementation of stack.py](./03.%20Deque%20implementation%20of%20stack.py)

### Using collections.deque

```python
from collections import deque

class StackDeque:
    def __init__(self):
        self.stack = deque()

    def push(self, data):
        self.stack.append(data)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        raise IndexError("Stack Underflow")

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        raise IndexError("Stack is empty")

    def is_empty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)
```

### Why deque?

| Feature | List | Deque |
|---------|------|-------|
| Append/Pop from end | O(1)* | O(1) |
| Append/Pop from start | O(n) | O(1) |
| Thread-safe operations | No | Yes |
| Memory efficiency | Good | Better |

*Amortized for list

### Best Practice
Use `deque` when you need guaranteed O(1) operations or thread-safety.

---

## Linked List Implementation of Stack
**📁 Implementation:** [04. Linked List implementation of stack.py](./04.%20Linked%20List%20implementation%20of%20stack.py)

### Implementation

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedListStack:
    def __init__(self):
        self.top = None
        self._size = 0

    def push(self, data):
        """Add element at top (beginning of list)"""
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node
        self._size += 1

    def pop(self):
        """Remove and return top element"""
        if self.is_empty():
            raise IndexError("Stack Underflow")

        data = self.top.data
        self.top = self.top.next
        self._size -= 1
        return data

    def peek(self):
        """View top element"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.top.data

    def is_empty(self):
        return self.top is None

    def size(self):
        return self._size
```

### Visual Example

```
Push 10, 20, 30:

Step 1: Push 10
top → [10|None]

Step 2: Push 20
top → [20|•] → [10|None]

Step 3: Push 30
top → [30|•] → [20|•] → [10|None]

Pop:
top → [20|•] → [10|None]
(30 removed)
```

### Comparison with Array-Based

| Aspect | Array/List | Linked List |
|--------|------------|-------------|
| Memory | Contiguous | Scattered |
| Extra space | None | Pointer per node |
| Resize needed | Yes | No |
| Cache performance | Better | Worse |
| Fixed size | Optional | No |

---

## Check for Balanced Parentheses
**📁 Implementation:** [05. Check for balanced paranthesis.py](./05.%20Check%20for%20balanced%20paranthesis.py)

### Problem
Check if an expression has balanced parentheses: `()`, `{}`, `[]`

### Algorithm

1. Scan expression left to right
2. Push opening brackets onto stack
3. For closing brackets, check if top matches
4. At end, stack should be empty

### Implementation

```python
def is_balanced(expression):
    stack = []
    matching = {')': '(', '}': '{', ']': '['}

    for char in expression:
        # Opening bracket: push to stack
        if char in matching.values():
            stack.append(char)

        # Closing bracket: check match
        elif char in matching:
            if not stack or stack[-1] != matching[char]:
                return False
            stack.pop()

    return len(stack) == 0
```

### Examples

```
"{[()()]}"  → True
"(()))"     → False (extra closing)
"([)]"      → False (wrong nesting)
"((())"     → False (missing closing)
```

### Visual Trace

```
Input: "{[(]}"

char | stack     | action
-----|-----------|--------
{    | ['{']     | push
[    | ['{','['] | push
(    | ['{','[','('] | push
]    | Error!    | ] doesn't match ( at top

Result: False
```

### Time & Space Complexity
- **Time**: O(n) - single pass
- **Space**: O(n) - worst case all opening brackets

### Applications
- Compiler syntax checking
- JSON/XML validation
- Math expression validation
- Code editors

---

## Infix to Postfix Conversion
**📁 Implementation:** [06. Infix to Postfix.py](./06.%20Infix%20to%20Postfix.py)

### Expression Notations

| Type | Format | Example |
|------|--------|---------|
| **Infix** | a op b | `a + b * c` |
| **Postfix** | a b op | `a b c * +` |
| **Prefix** | op a b | `+ a * b c` |

### Why Postfix?
- No parentheses needed
- Easy for computers to evaluate
- No operator precedence ambiguity

### Algorithm

```python
def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    stack = []
    postfix = []

    for char in expression:
        # Operand: add to output
        if char.isalnum():
            postfix.append(char)

        # Opening parenthesis: push
        elif char == '(':
            stack.append(char)

        # Closing parenthesis: pop until '('
        elif char == ')':
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
            stack.pop()  # Remove '('

        # Operator
        elif char in precedence:
            while (stack and stack[-1] != '(' and
                   stack[-1] in precedence and
                   precedence[stack[-1]] >= precedence[char]):
                postfix.append(stack.pop())
            stack.append(char)

    # Pop remaining operators
    while stack:
        postfix.append(stack.pop())

    return ''.join(postfix)
```

### Example

```
Infix: a+b*(c^d-e)
Postfix: abcd^e-*+

Step-by-step:
char | stack       | output
-----|-------------|--------
a    | []          | a
+    | ['+']       | a
b    | ['+']       | ab
*    | ['+','*']   | ab
(    | ['+','*','(']| ab
c    | ['+','*','(']| abc
^    | ['+','*','(','^']| abc
d    | ['+','*','(','^']| abcd
-    | ['+','*','(','-']| abcd^
e    | ['+','*','(','-']| abcd^e
)    | ['+','*']   | abcd^e-
     | []          | abcd^e-*+
```

### Time & Space Complexity
- **Time**: O(n)
- **Space**: O(n)

---

## Prefix to Infix Conversion
**📁 Implementation:** [07. Prefix to Infix.py](./07.%20Prefix%20to%20Infix.py)

### Algorithm

1. Scan prefix expression **right to left**
2. If operand, push to stack
3. If operator, pop two operands, form `(op1 operator op2)`, push result

### Implementation

```python
def prefix_to_infix(expression):
    stack = []

    # Scan right to left
    for char in reversed(expression):
        if char.isalnum():
            stack.append(char)
        else:
            # Pop two operands
            op1 = stack.pop()
            op2 = stack.pop()
            # Form infix and push
            result = f"({op1}{char}{op2})"
            stack.append(result)

    return stack.pop()
```

### Example

```
Prefix: *+AB-CD
Infix: ((A+B)*(C-D))

Scan: D C - B A + *
char | stack
-----|--------
D    | ['D']
C    | ['D','C']
-    | ['D','(C-D)']  → Wait, reversed!

Correct scan (right to left of *+AB-CD):
D    | ['D']
C    | ['C','D']
-    | ['(C-D)']
B    | ['B','(C-D)']
A    | ['A','B','(C-D)']
+    | ['(A+B)','(C-D)']
*    | ['((A+B)*(C-D))']
```

---

## Postfix to Infix Conversion
**📁 Implementation:** [08. Postfix to Infix.py](./08.%20Postfix%20to%20Infix.py)

### Algorithm

1. Scan postfix expression **left to right**
2. If operand, push to stack
3. If operator, pop two operands, form `(op2 operator op1)`, push result

### Implementation

```python
def postfix_to_infix(expression):
    stack = []

    for char in expression:
        if char.isalnum():
            stack.append(char)
        else:
            # Pop two operands (order matters!)
            op2 = stack.pop()
            op1 = stack.pop()
            # Form infix and push
            result = f"({op1}{char}{op2})"
            stack.append(result)

    return stack.pop()
```

### Example

```
Postfix: AB+CD-*
Infix: ((A+B)*(C-D))

char | stack
-----|--------
A    | ['A']
B    | ['A','B']
+    | ['(A+B)']
C    | ['(A+B)','C']
D    | ['(A+B)','C','D']
-    | ['(A+B)','(C-D)']
*    | ['((A+B)*(C-D))']
```

---

## Parenthesis Checker
**📁 Implementation:** [09. Paranthesis checker.py](./09.%20Paranthesis%20checker.py)

### Problem
Validate that parentheses in an expression are properly matched and nested.

### Implementation

```python
def check_parentheses(expression):
    stack = []

    for char in expression:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()

    return len(stack) == 0
```

### Extended Version (Multiple Types)

```python
def check_all_brackets(expression):
    stack = []
    brackets = {'(': ')', '{': '}', '[': ']'}

    for char in expression:
        if char in brackets:  # Opening
            stack.append(char)
        elif char in brackets.values():  # Closing
            if not stack:
                return False
            if brackets[stack.pop()] != char:
                return False

    return len(stack) == 0
```

---

## Comparison Summary

### Stack Implementation Comparison

| Implementation | Push | Pop | Pros | Cons |
|----------------|------|-----|------|------|
| Python List | O(1)* | O(1) | Simple, built-in | Resize overhead |
| Deque | O(1) | O(1) | Thread-safe, guaranteed O(1) | Import needed |
| Linked List | O(1) | O(1) | No resize, dynamic | Memory overhead |

*Amortized

### Expression Conversion Summary

| Conversion | Scan Direction | Algorithm |
|------------|----------------|-----------|
| Infix → Postfix | Left to Right | Use precedence, handle parentheses |
| Prefix → Infix | Right to Left | Pop 2, form (op1 operator op2) |
| Postfix → Infix | Left to Right | Pop 2, form (op1 operator op2) |

---

## Applications of Stack

### 1. Function Call Management
```
main() calls foo()
foo() calls bar()
bar() returns to foo()
foo() returns to main()

Stack: [main] → [main, foo] → [main, foo, bar] → [main, foo] → [main]
```

### 2. Undo/Redo Operations
```python
class Editor:
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def perform_action(self, action):
        self.undo_stack.append(action)
        self.redo_stack.clear()

    def undo(self):
        if self.undo_stack:
            action = self.undo_stack.pop()
            self.redo_stack.append(action)

    def redo(self):
        if self.redo_stack:
            action = self.redo_stack.pop()
            self.undo_stack.append(action)
```

### 3. Browser History
```python
class BrowserHistory:
    def __init__(self):
        self.back_stack = []
        self.forward_stack = []
        self.current = None

    def visit(self, url):
        if self.current:
            self.back_stack.append(self.current)
        self.current = url
        self.forward_stack.clear()

    def back(self):
        if self.back_stack:
            self.forward_stack.append(self.current)
            self.current = self.back_stack.pop()

    def forward(self):
        if self.forward_stack:
            self.back_stack.append(self.current)
            self.current = self.forward_stack.pop()
```

### 4. Syntax Parsing
- Compiler design
- HTML/XML validation
- Mathematical expressions

### 5. Depth-First Search (DFS)
```python
def dfs(graph, start):
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            stack.extend(graph[node] - visited)
```

---

## Common Patterns

### Pattern 1: Monotonic Stack
Find next greater/smaller element.

```python
def next_greater_element(arr):
    result = [-1] * len(arr)
    stack = []

    for i in range(len(arr)):
        while stack and arr[i] > arr[stack[-1]]:
            result[stack.pop()] = arr[i]
        stack.append(i)

    return result
```

### Pattern 2: Stock Span Problem
Days since price was higher.

```python
def stock_span(prices):
    span = []
    stack = []

    for i, price in enumerate(prices):
        while stack and prices[stack[-1]] <= price:
            stack.pop()

        span.append(i - stack[-1] if stack else i + 1)
        stack.append(i)

    return span
```

### Pattern 3: Evaluate Postfix Expression

```python
def evaluate_postfix(expression):
    stack = []

    for token in expression.split():
        if token.isdigit():
            stack.append(int(token))
        else:
            b, a = stack.pop(), stack.pop()
            if token == '+': stack.append(a + b)
            elif token == '-': stack.append(a - b)
            elif token == '*': stack.append(a * b)
            elif token == '/': stack.append(a // b)

    return stack.pop()
```

---

## Edge Cases to Test

1. **Empty stack**: Pop/peek on empty
2. **Single element**: Push one, pop one
3. **Overflow**: If using fixed-size stack
4. **Unbalanced brackets**: Extra open/close
5. **Wrong nesting**: `([)]`
6. **Empty expression**: `""`
7. **Only operators/operands**: Edge in expression conversion

---

## Interview Tips

### Common Questions
1. Implement stack using queues
2. Implement min stack (O(1) getMin)
3. Valid parentheses
4. Evaluate reverse polish notation
5. Daily temperatures (next greater element)
6. Largest rectangle in histogram

### Key Points
- LIFO principle
- O(1) for all basic operations
- Useful for matching problems
- Expression evaluation
- DFS and backtracking

---
