#!/usr/bin/env python3
"""
Generator for remaining daily plan files
"""

day_plans = {
    5: {
        "title": "Hash Maps & Advanced Patterns",
        "topics": ["Cycle detection", "Pattern matching", "Bidirectional mapping"],
        "problems": [
            ("202", "Happy Number", "Easy", "Hash Map", "Detect cycle in number transformation"),
            ("205", "Isomorphic Strings", "Easy", "Hash Map", "Map characters bidirectionally"),
            ("383", "Ransom Note", "Easy", "Hash Map", "Check character availability"),
            ("349", "Intersection of Two Arrays", "Easy", "Hash Map", "Find common elements"),
            ("350", "Intersection of Two Arrays II", "Easy", "Hash Map", "Handle duplicates"),
            ("367", "Valid Perfect Square", "Easy", "Binary Search", "Binary search for perfect square"),
            ("371", "Sum of Two Integers", "Easy", "Bit Manipulation", "Use XOR and AND"),
        ]
    },
    6: {
        "title": "Array Math & Manipulations",
        "topics": ["Digit manipulation", "Array rotation", "Prefix/Suffix", "Combinatorics"],
        "problems": [
            ("9", "Palindrome Number", "Easy", "Number Reversal", "Reverse and compare"),
            ("66", "Plus One", "Easy", "Digit Manipulation", "Handle carry propagation"),
            ("189", "Rotate Array", "Easy", "Array Manipulation", "Reverse subarrays"),
            ("238", "Product of Array Except Self", "Easy", "One Pass", "Prefix and suffix products"),
            ("118", "Pascal's Triangle", "Easy", "Dynamic Programming", "Build row by row"),
            ("119", "Pascal's Triangle II", "Easy", "Dynamic Programming", "Generate specific row"),
        ]
    },
    7: {
        "title": "Sliding Window & Advanced Two Pointers",
        "topics": ["Sliding window", "Two pointer optimization", "String patterns", "Substring problems"],
        "problems": [
            ("3", "Longest Substring Without Repeating Characters", "Medium", "Sliding Window", "Hash map for character tracking"),
            ("15", "3Sum", "Medium", "Two Pointers", "Fix one element and use two pointers"),
            ("167", "Two Sum II", "Medium", "Two Pointers", "Two pointers on sorted array"),
            ("11", "Container With Most Water", "Medium", "Two Pointers", "Greedy two pointer approach"),
            ("16", "3Sum Closest", "Medium", "Two Pointers", "Two pointers with target tracking"),
            ("18", "4Sum", "Medium", "Two Pointers", "Nested loops with two pointers"),
            ("209", "Minimum Size Subarray Sum", "Medium", "Sliding Window", "Find minimum length"),
        ]
    },
    8: {
        "title": "String Sliding Window & Advanced Patterns",
        "topics": ["Character frequency", "Window optimization", "Deques", "Prefix sums"],
        "problems": [
            ("424", "Longest Repeating Character Replacement", "Medium", "Sliding Window", "Track frequencies in window"),
            ("76", "Minimum Window Substring", "Medium", "Sliding Window", "Two pointers and character frequency"),
            ("438", "Find All Anagrams in String", "Medium", "Sliding Window", "Character count matching"),
            ("567", "Permutation in String", "Medium", "Sliding Window", "Check if permutation exists"),
            ("239", "Sliding Window Maximum", "Hard", "Deque", "Use deque to track maximum"),
            ("862", "Shortest Subarray with Sum at Least K", "Hard", "Prefix Sum + Deque", "Prefix sum with deque"),
        ]
    },
    9: {
        "title": "Stack Advanced Patterns",
        "topics": ["Path parsing", "Expression evaluation", "Monotonic stack", "Geometry problems"],
        "problems": [
            ("71", "Simplify Path", "Medium", "Stack", "Process directory operations"),
            ("394", "Decode String", "Medium", "Stack", "String decoding"),
            ("150", "Evaluate Reverse Polish Notation", "Medium", "Stack", "Postfix evaluation"),
            ("227", "Basic Calculator II", "Medium", "Stack", "Handle operator precedence"),
            ("32", "Longest Valid Parentheses", "Hard", "Stack", "Track unmatched parentheses"),
            ("84", "Largest Rectangle in Histogram", "Hard", "Monotonic Stack", "Monotonic increasing stack"),
        ]
    },
    10: {
        "title": "Linked Lists Advanced",
        "topics": ["Palindrome checking", "Node removal", "Swapping", "Reordering"],
        "problems": [
            ("234", "Palindrome Linked List", "Easy", "Slow/Fast Pointers", "Find middle and reverse"),
            ("19", "Remove Nth Node From End", "Medium", "Two Pointers", "Two pointer gap technique"),
            ("24", "Swap Nodes in Pairs", "Medium", "Recursion", "Recursively swap nodes"),
            ("25", "Reverse Nodes in k Group", "Hard", "Recursion", "Reverse groups of k"),
            ("92", "Reverse Linked List II", "Medium", "Iterative", "Reverse portion of list"),
            ("143", "Reorder List", "Medium", "Slow/Fast Pointers", "Find middle then merge"),
        ]
    },
}

# Generate remaining day plans
for day in range(11, 46):
    if day == 11:
        content = """# Day 11: Tree Traversal - BFS & Level Order

## Topics Covered
- Breadth-First Search (BFS)
- Level order traversal
- Queue-based algorithms

## Problems to Solve

1. **Binary Tree Level Order Traversal** (Medium)
   - Link: https://leetcode.com/problems/binary-tree-level-order-traversal/
   - **Hint**: Queue based level order traversal

2. **Binary Tree Zigzag Level Order Traversal** (Medium)
   - Link: https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/
   - **Hint**: Alternate direction at each level

3. **Binary Tree Level Order Traversal II** (Easy)
   - Link: https://leetcode.com/problems/binary-tree-level-order-traversal-ii/
   - **Hint**: Reverse final result

4. **Binary Tree Right Side View** (Medium)
   - Link: https://leetcode.com/problems/binary-tree-right-side-view/
   - **Hint**: View from right perspective

5. **Average of Levels in Binary Tree** (Easy)
   - Link: https://leetcode.com/problems/average-of-levels-in-binary-tree/
   - **Hint**: Compute average at each level

6. **Find Largest Value in Each Tree Row** (Medium)
   - Link: https://leetcode.com/problems/find-largest-value-in-each-tree-row/
   - **Hint**: Track maximum per level

## Key Concepts

✅ **BFS Pattern** - Queue-based traversal
✅ **Level Order Problems** - Process by levels, not recursion
"""
    elif day == 12:
        content = """# Day 12: Tree Construction & Traversal Reconstruction

## Topics Covered
- Reconstructing trees from traversals
- Tree construction patterns
- Sorted array to BST conversion

## Problems to Solve

1. **Construct Binary Tree from Preorder and Inorder** (Medium)
   - Link: https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/
   - **Hint**: Use preorder and inorder properties

2. **Construct Binary Tree from Inorder and Postorder** (Medium)
   - Link: https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/
   - **Hint**: Use postorder and inorder properties

3. **Maximum Binary Tree** (Medium)
   - Link: https://leetcode.com/problems/maximum-binary-tree/
   - **Hint**: Build tree from maximum element

4. **Construct Binary Tree from Preorder and Postorder** (Medium)
   - Link: https://leetcode.com/problems/construct-binary-tree-from-preorder-and-postorder-traversal/
   - **Hint**: Preorder and postorder relationship

5. **Convert Sorted Array to Binary Search Tree** (Easy)
   - Link: https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/
   - **Hint**: Use middle element as root

6. **Convert Sorted List to Binary Search Tree** (Medium)
   - Link: https://leetcode.com/problems/convert-sorted-list-to-binary-search-tree/
   - **Hint**: Slow/fast pointers to find middle

## Key Concepts

✅ **Traversal Properties** - Each traversal gives different info
✅ **Tree Reconstruction** - Combine multiple traversals
"""
    elif day == 13:
        content = """# Day 13: Binary Search Trees - Operations & Validation

## Topics Covered
- BST validation
- In-order traversal properties
- BST insertion and deletion
- Iterator patterns

## Problems to Solve

1. **Kth Smallest Element in a BST** (Medium)
   - Link: https://leetcode.com/problems/kth-smallest-element-in-a-bst/
   - **Hint**: Inorder traversal gives sorted sequence

2. **Validate Binary Search Tree** (Medium)
   - Link: https://leetcode.com/problems/validate-binary-search-tree/
   - **Hint**: Track min/max bounds recursively

3. **Binary Search Tree Iterator** (Medium)
   - Link: https://leetcode.com/problems/binary-search-tree-iterator/
   - **Hint**: Stack based in-order traversal

4. **Insert into a Binary Search Tree** (Easy)
   - Link: https://leetcode.com/problems/insert-into-a-binary-search-tree/
   - **Hint**: Navigate tree using BST property

5. **Delete Node in a BST** (Medium)
   - Link: https://leetcode.com/problems/delete-node-in-a-bst/
   - **Hint**: Handle three deletion cases

6. **Minimum Distance Between BST Nodes** (Easy)
   - Link: https://leetcode.com/problems/minimum-distance-between-bst-nodes/
   - **Hint**: Track previous in inorder

## Key Concepts

✅ **In-order Traversal** - Returns BST in sorted order
✅ **BST Property** - Enables efficient operations
"""
    elif day == 14:
        content = """# Day 14: Tree Paths & Path Sum Problems

## Topics Covered
- Path traversal
- Path sum calculations
- Tree flattening
- Leaf node operations

## Problems to Solve

1. **Binary Tree Right Side View** (Medium)
   - Link: https://leetcode.com/problems/binary-tree-right-side-view/
   - **Hint**: DFS with level tracking

2. **Binary Tree Maximum Path Sum** (Hard)
   - Link: https://leetcode.com/problems/binary-tree-maximum-path-sum/
   - **Hint**: Track sum at each node

3. **Path Sum** (Easy)
   - Link: https://leetcode.com/problems/path-sum/
   - **Hint**: DFS to check if path exists

4. **Path Sum II** (Medium)
   - Link: https://leetcode.com/problems/path-sum-ii/
   - **Hint**: Find all paths with target sum

5. **Flatten Binary Tree to Linked List** (Medium)
   - Link: https://leetcode.com/problems/flatten-binary-tree-to-linked-list/
   - **Hint**: Transform tree into linked list

6. **Sum Root to Leaf Numbers** (Medium)
   - Link: https://leetcode.com/problems/sum-root-to-leaf-numbers/
   - **Hint**: Accumulate numbers as path

## Key Concepts

✅ **Path Tracking** - Maintain path state during traversal
✅ **Leaf Node Detection** - When both children are null
"""
    elif day == 15:
        content = """# Day 15: Lowest Common Ancestor Problems

## Topics Covered
- LCA in BST
- LCA in general trees
- Multiple node LCA
- Parent pointer navigation

## Problems to Solve

1. **Validate Binary Search Tree** (Medium)
   - Link: https://leetcode.com/problems/validate-binary-search-tree/
   - **Hint**: Validate BST property with bounds

2. **Lowest Common Ancestor of BST** (Easy)
   - Link: https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/
   - **Hint**: Use BST structure to find LCA

3. **Lowest Common Ancestor of Binary Tree** (Medium)
   - Link: https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/
   - **Hint**: Find LCA in general tree

4. **Lowest Common Ancestor of a Binary Tree II** (Medium)
   - Link: https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree-ii/
   - **Hint**: Handle case where nodes might not exist

5. **Lowest Common Ancestor of a Binary Tree III** (Medium)
   - Link: https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree-iii/
   - **Hint**: Use parent pointers for LCA

6. **Lowest Common Ancestor of a Binary Tree IV** (Medium)
   - Link: https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree-iv/
   - **Hint**: Find LCA of multiple nodes

## Key Concepts

✅ **LCA Pattern** - Find common ancestor recursively
✅ **BST vs General Tree** - Different approaches
"""
    elif day == 16:
        content = """# Day 16: Backtracking - Combinations

## Topics Covered
- Combination generation
- Backtracking template
- Constraint satisfaction
- Recursion with state

## Problems to Solve

1. **Combination Sum III** (Medium)
   - Link: https://leetcode.com/problems/combination-sum-iii/
   - **Hint**: Find combinations with constraints

2. **Letter Combinations of a Phone Number** (Medium)
   - Link: https://leetcode.com/problems/letter-combinations-of-a-phone-number/
   - **Hint**: Generate all letter combinations

3. **Combination Sum** (Medium)
   - Link: https://leetcode.com/problems/combination-sum/
   - **Hint**: Find combinations with repetition allowed

4. **Combination Sum II** (Medium)
   - Link: https://leetcode.com/problems/combination-sum-ii/
   - **Hint**: Find combinations without repetition

5. **Combinations** (Medium)
   - Link: https://leetcode.com/problems/combinations/
   - **Hint**: Generate all combinations of size k

6. **Subsets** (Medium)
   - Link: https://leetcode.com/problems/subsets/
   - **Hint**: Generate all subsets

7. **Subsets II** (Medium)
   - Link: https://leetcode.com/problems/subsets-ii/
   - **Hint**: Generate subsets from duplicate array

## Key Concepts

✅ **Backtracking Template** - Choose, explore, unchoose
✅ **Combination vs Permutation** - Order matters or not
"""
    elif day == 17:
        content = """# Day 17: Backtracking - Permutations & String Generation

## Topics Covered
- Permutation generation
- String construction
- Constraint validation
- Complex backtracking

## Problems to Solve

1. **Permutations** (Medium)
   - Link: https://leetcode.com/problems/permutations/
   - **Hint**: Generate all permutations

2. **Permutations II** (Medium)
   - Link: https://leetcode.com/problems/permutations-ii/
   - **Hint**: Generate permutations from duplicates

3. **Generate Parentheses** (Medium)
   - Link: https://leetcode.com/problems/generate-parentheses/
   - **Hint**: Build valid parenthesis combinations

4. **N-Queens** (Hard)
   - Link: https://leetcode.com/problems/n-queens/
   - **Hint**: Place queens with backtracking

5. **N-Queens II** (Hard)
   - Link: https://leetcode.com/problems/n-queens-ii/
   - **Hint**: Count N-Queens solutions

6. **Sudoku Solver** (Hard)
   - Link: https://leetcode.com/problems/sudoku-solver/
   - **Hint**: Solve sudoku with backtracking

## Key Concepts

✅ **Permutation Pattern** - Track used elements
✅ **Constraint Satisfaction** - Prune invalid branches
✅ **2D Backtracking** - Grid-based problems
"""
    elif day == 18:
        content = """# Day 18: Backtracking - Word Search & Pattern Matching

## Topics Covered
- Grid-based backtracking
- Pattern matching
- Trie integration
- Complexity optimization

## Problems to Solve

1. **Word Search** (Medium)
   - Link: https://leetcode.com/problems/word-search/
   - **Hint**: Search for word in 2D grid

2. **Word Search II** (Hard)
   - Link: https://leetcode.com/problems/word-search-ii/
   - **Hint**: Find multiple words with Trie

3. **Wildcard Matching** (Hard)
   - Link: https://leetcode.com/problems/wildcard-matching/
   - **Hint**: Match pattern with wildcards using DP

4. Additional constraint problems for mastery

## Key Concepts

✅ **2D Grid Backtracking** - Four direction search
✅ **Visited State Management** - Prevent revisiting
✅ **Trie + Backtracking** - Efficient multi-word search
"""
    elif day == 19:
        content = """# Day 19: Dynamic Programming - 1D Fundamentals

## Topics Covered
- Base cases and transitions
- Memoization vs tabulation
- Simple optimization problems
- Time complexity analysis

## Problems to Solve

1. **Climbing Stairs** (Easy)
   - Link: https://leetcode.com/problems/climbing-stairs/
   - **Hint**: Build up from base cases

2. **House Robber** (Medium)
   - Link: https://leetcode.com/problems/house-robber/
   - **Hint**: Track max value not robbing adjacent

3. **House Robber II** (Medium)
   - Link: https://leetcode.com/problems/house-robber-ii/
   - **Hint**: Handle circular constraint

4. **Delete and Earn** (Medium)
   - Link: https://leetcode.com/problems/delete-and-earn/
   - **Hint**: Similar to house robber

5. **Fibonacci Number** (Easy)
   - Link: https://leetcode.com/problems/fibonacci-number/
   - **Hint**: Basic DP with memoization

6. **N-th Tribonacci Number** (Easy)
   - Link: https://leetcode.com/problems/n-th-tribonacci-number/
   - **Hint**: Extend Fibonacci pattern

## Key Concepts

✅ **DP State Definition** - What does dp[i] represent?
✅ **State Transition** - How to compute from previous states?
✅ **Base Cases** - Critical for correctness
"""
    elif day == 20:
        content = """# Day 20: Dynamic Programming - 2D & Grid Problems

## Topics Covered
- 2D DP table construction
- Grid path problems
- Subsequence problems
- Edit distance family

## Problems to Solve

1. **Unique Paths** (Medium)
   - Link: https://leetcode.com/problems/unique-paths/
   - **Hint**: Fill 2D grid with DP

2. **Unique Paths II** (Medium)
   - Link: https://leetcode.com/problems/unique-paths-ii/
   - **Hint**: Handle obstacles in grid

3. **Minimum Path Sum** (Medium)
   - Link: https://leetcode.com/problems/minimum-path-sum/
   - **Hint**: Find minimum cost path

4. **Longest Common Subsequence** (Medium)
   - Link: https://leetcode.com/problems/longest-common-subsequence/
   - **Hint**: Classic 2D DP problem

5. **Edit Distance** (Hard)
   - Link: https://leetcode.com/problems/edit-distance/
   - **Hint**: Levenshtein distance

6. **Shortest Common Supersequence** (Hard)
   - Link: https://leetcode.com/problems/shortest-common-supersequence/
   - **Hint**: Build shortest supersequence

## Key Concepts

✅ **2D DP Grid** - dp[i][j] represents state for first i and j elements
✅ **Space Optimization** - Can often reduce to 1D array
"""
    elif day == 21:
        content = """# Day 21: Dynamic Programming - LIS & Knapsack Introduction

## Topics Covered
- Longest Increasing Subsequence
- Binary search for LIS optimization
- 0/1 Knapsack introduction
- Subset sum problems

## Problems to Solve

1. **Longest Increasing Subsequence** (Medium)
   - Link: https://leetcode.com/problems/longest-increasing-subsequence/
   - **Hint**: O(n log n) with binary search

2. **Russian Doll Envelopes** (Hard)
   - Link: https://leetcode.com/problems/russian-doll-envelopes/
   - **Hint**: 2D LIS variant

3. **Find Longest Valid Obstacle Course** (Hard)
   - Link: https://leetcode.com/problems/find-the-longest-valid-obstacle-course-at-each-position/
   - **Hint**: LIS with obstacles

4. **Partition Equal Subset Sum** (Medium)
   - Link: https://leetcode.com/problems/partition-equal-subset-sum/
   - **Hint**: Classic 0/1 knapsack variant

5. **Target Sum** (Medium)
   - Link: https://leetcode.com/problems/target-sum/
   - **Hint**: Subset sum variant

## Key Concepts

✅ **LIS Binary Search** - Maintain sorted tails array
✅ **0/1 Knapsack** - Can pick each item 0 or 1 times
✅ **Subset Sum** - Common knapsack variant
"""
    elif day == 22:
        content = """# Day 22: Dynamic Programming - Knapsack Variants

## Topics Covered
- Unbounded knapsack
- Coin change problems
- Combination counting
- Complex constraints

## Problems to Solve

1. **Last Stone Weight II** (Medium)
   - Link: https://leetcode.com/problems/last-stone-weight-ii/
   - **Hint**: Minimize difference using knapsack

2. **Coin Change** (Medium)
   - Link: https://leetcode.com/problems/coin-change/
   - **Hint**: Minimum coins for target

3. **Coin Change 2** (Medium)
   - Link: https://leetcode.com/problems/coin-change-2/
   - **Hint**: Count ways to make change

4. **Combination Sum IV** (Medium)
   - Link: https://leetcode.com/problems/combination-sum-iv/
   - **Hint**: Count ordered combinations

5. **Number of Dice Rolls with Target Sum** (Medium)
   - Link: https://leetcode.com/problems/number-of-dice-rolls-with-target-sum/
   - **Hint**: Dice rolls to target sum

6. **Regular Expression Matching** (Hard)
   - Link: https://leetcode.com/problems/regular-expression-matching/
   - **Hint**: Complex regex pattern matching

## Key Concepts

✅ **Unbounded Knapsack** - Can pick item unlimited times
✅ **Combination vs Permutation** - Order consideration
✅ **String DP** - Character-by-character processing
"""
    elif day == 23:
        content = """# Day 23: Dynamic Programming - String Problems

## Topics Covered
- String pattern matching
- Palindrome problems
- Subsequence problems
- Complex string DP

## Problems to Solve

1. **Longest Valid Parentheses** (Hard)
   - Link: https://leetcode.com/problems/longest-valid-parentheses/
   - **Hint**: Track valid parentheses length

2. **Distinct Subsequences** (Hard)
   - Link: https://leetcode.com/problems/distinct-subsequences/
   - **Hint**: Count distinct subsequences

3. **Interleaving String** (Medium)
   - Link: https://leetcode.com/problems/interleaving-string/
   - **Hint**: Check if interleaving possible

4. **Palindrome Partitioning** (Medium)
   - Link: https://leetcode.com/problems/palindrome-partitioning/
   - **Hint**: Find all palindrome partitions

5. **Palindrome Partitioning II** (Hard)
   - Link: https://leetcode.com/problems/palindrome-partitioning-ii/
   - **Hint**: Minimum palindrome cuts

## Key Concepts

✅ **String Matching** - Character comparison and positions
✅ **Palindrome Detection** - Preprocessing optimization
"""
    elif day == 24:
        content = """# Day 24: Dynamic Programming - Word Break & Palindromes

## Topics Covered
- Word break problems
- Dictionary-based DP
- Palindrome substring problems
- Advanced string patterns

## Problems to Solve

1. **Word Break** (Medium)
   - Link: https://leetcode.com/problems/word-break/
   - **Hint**: Check if word break possible

2. **Word Break II** (Hard)
   - Link: https://leetcode.com/problems/word-break-ii/
   - **Hint**: Find all word break combinations

3. **Longest Palindromic Substring** (Medium)
   - Link: https://leetcode.com/problems/longest-palindromic-substring/
   - **Hint**: Find longest palindrome

4. **Longest Palindromic Subsequence** (Medium)
   - Link: https://leetcode.com/problems/longest-palindromic-subsequence/
   - **Hint**: Longest palindrome subsequence

5. **Shortest Palindrome** (Hard)
   - Link: https://leetcode.com/problems/shortest-palindrome/
   - **Hint**: Add characters to make palindrome

## Key Concepts

✅ **Word Dictionary** - Hash map for O(1) lookup
✅ **Palindrome DP** - Expand around center or 2D table
✅ **KMP Algorithm** - Pattern matching optimization
"""
    elif day == 25:
        content = """# Day 25: Graphs - Union Find & Connected Components

## Topics Covered
- Union Find data structure
- Connected components
- Graph connectivity
- Cycle detection

## Problems to Solve

1. **Number of Islands** (Medium)
   - Link: https://leetcode.com/problems/number-of-islands/
   - **Hint**: Count connected components

2. **Max Area of Island** (Medium)
   - Link: https://leetcode.com/problems/max-area-of-island/
   - **Hint**: Find largest island

3. **Making A Large Island** (Hard)
   - Link: https://leetcode.com/problems/making-a-large-island/
   - **Hint**: Maximize island by changing one cell

4. **Flood Fill** (Easy)
   - Link: https://leetcode.com/problems/flood-fill/
   - **Hint**: Image flood fill simulation

5. **Shortest Bridge** (Hard)
   - Link: https://leetcode.com/problems/shortest-bridge/
   - **Hint**: Find shortest distance between islands

## Key Concepts

✅ **DFS/BFS on Grid** - Connected component discovery
✅ **Multi-source Search** - Starting from multiple cells
"""
    elif day == 26:
        content = """# Day 26: Union Find - Advanced Applications

## Topics Covered
- Union Find implementation
- Path compression
- Rank optimization
- Graph validation

## Problems to Solve

1. **Number of Provinces** (Medium)
   - Link: https://leetcode.com/problems/number-of-provinces/
   - **Hint**: Count connected components with UF

2. **Graph Valid Tree** (Medium)
   - Link: https://leetcode.com/problems/graph-valid-tree/
   - **Hint**: Validate if graph is tree

3. **The Earliest Moment When Everyone Become Friends** (Medium)
   - Link: https://leetcode.com/problems/the-earliest-moment-when-everyone-become-friends/
   - **Hint**: Find when all connected

4. **Satisfiability of Equality Equations** (Medium)
   - Link: https://leetcode.com/problems/satisfiability-of-equality-equations/
   - **Hint**: Check equation satisfiability

5. **Smallest String With Swaps** (Medium)
   - Link: https://leetcode.com/problems/smallest-string-with-swaps/
   - **Hint**: Minimize string with swaps

## Key Concepts

✅ **Union Find Template** - find(x), union(x, y)
✅ **Path Compression** - Optimize find operation
✅ **Union by Rank** - Balance tree height
"""
    elif day == 27:
        content = """# Day 27: Topological Sort & DAG Problems

## Topics Covered
- Topological sorting
- Kahn's algorithm
- Cycle detection in directed graphs
- Course prerequisites

## Problems to Solve

1. **Course Schedule** (Medium)
   - Link: https://leetcode.com/problems/course-schedule/
   - **Hint**: Detect cycle with topological sort

2. **Course Schedule II** (Medium)
   - Link: https://leetcode.com/problems/course-schedule-ii/
   - **Hint**: Return topological order

3. **Course Schedule IV** (Medium)
   - Link: https://leetcode.com/problems/course-schedule-iv/
   - **Hint**: Check reachability

4. **Minimum Height Trees** (Medium)
   - Link: https://leetcode.com/problems/minimum-height-trees/
   - **Hint**: Find roots with minimum height

5. **Sort Items by Groups Respecting Dependencies** (Hard)
   - Link: https://leetcode.com/problems/sort-items-by-groups-respecting-dependencies/
   - **Hint**: Complex topological sort

## Key Concepts

✅ **Kahn's Algorithm** - In-degree based sorting
✅ **DFS Topological Sort** - Post-order traversal
✅ **Cycle Detection** - Via in-degrees or visited states
"""
    elif day == 28:
        content = """# Day 28: BFS - Shortest Path & Transformation

## Topics Covered
- Multi-source BFS
- Shortest path problems
- Word transformation
- Distance computation

## Problems to Solve

1. **Word Ladder II** (Hard)
   - Link: https://leetcode.com/problems/word-ladder-ii/
   - **Hint**: Find all shortest word paths

2. **Word Ladder** (Medium)
   - Link: https://leetcode.com/problems/word-ladder/
   - **Hint**: Find shortest transformation

3. **Walls and Gates** (Medium)
   - Link: https://leetcode.com/problems/walls-and-gates/
   - **Hint**: Distance to nearest gate

4. **Shortest Distance from All Buildings** (Hard)
   - Link: https://leetcode.com/problems/shortest-distance-from-all-buildings/
   - **Hint**: Find optimal building location

5. **01 Matrix** (Medium)
   - Link: https://leetcode.com/problems/01-matrix/
   - **Hint**: Distance to nearest zero

## Key Concepts

✅ **Multi-source BFS** - Start from multiple nodes
✅ **Shortest Path** - BFS guarantees shortest distance
✅ **Graph Construction** - Build graph from problem description
"""
    elif day == 29:
        content = """# Day 29: DFS - Graph Traversal & Advanced Algorithms

## Topics Covered
- Deep copy of graphs
- Cycle detection in undirected graphs
- Bridge finding (Tarjan's algorithm)
- Graph traversal patterns

## Problems to Solve

1. **Clone Graph** (Medium)
   - Link: https://leetcode.com/problems/clone-graph/
   - **Hint**: Deep copy of graph

2. **Detect Cycles in 2D Grid** (Hard)
   - Link: https://leetcode.com/problems/detect-cycles-in-2d-grid/
   - **Hint**: Detect cycle in 2D grid

3. **Critical Connections in a Network** (Hard)
   - Link: https://leetcode.com/problems/critical-connections-in-a-network/
   - **Hint**: Find bridges in graph

4. **Alien Dictionary** (Hard)
   - Link: https://leetcode.com/problems/alien-dictionary/
   - **Hint**: Deduce alien dictionary order

5. **Network Delay Time** (Medium)
   - Link: https://leetcode.com/problems/network-delay-time/
   - **Hint**: Single source shortest path

## Key Concepts

✅ **DFS with State** - Track visited and recursion stack
✅ **Graph Copying** - Maintain node mapping
✅ **Advanced Patterns** - Bridges, articulation points
"""
    elif day == 30:
        content = """# Day 30: Dijkstra's Algorithm & Shortest Path

## Topics Covered
- Dijkstra's algorithm implementation
- Priority queue usage
- Shortest path with constraints
- Weighted graph traversal

## Problems to Solve

1. **Cheapest Flights Within K Stops** (Medium)
   - Link: https://leetcode.com/problems/cheapest-flights-within-k-stops/
   - **Hint**: Modified shortest path with limit

2. **Path with Maximum Probability** (Medium)
   - Link: https://leetcode.com/problems/path-with-maximum-probability/
   - **Hint**: Maximum probability path

3. **Reachable Nodes In Subdivided Graph** (Hard)
   - Link: https://leetcode.com/problems/reachable-nodes-in-subdivided-graph/
   - **Hint**: Count reachable nodes

4. **Path With Minimum Effort** (Medium)
   - Link: https://leetcode.com/problems/path-with-minimum-effort/
   - **Hint**: Minimize maximum effort

## Key Concepts

✅ **Dijkstra's Template** - Priority queue with distances
✅ **Edge Weight Handling** - Different weight types
✅ **Optimization** - Early termination when destination reached
"""
    elif day == 31:
        content = """# Day 31: Minimum Spanning Tree & Advanced Graphs

## Topics Covered
- Minimum Spanning Tree
- Kruskal's algorithm
- Prim's algorithm
- Union Find in MST

## Problems to Solve

1. **Min Cost to Connect All Points** (Medium)
   - Link: https://leetcode.com/problems/min-cost-to-connect-all-points/
   - **Hint**: Minimum spanning tree

2. **Connecting Cities With Minimum Cost** (Medium)
   - Link: https://leetcode.com/problems/connecting-cities-with-minimum-cost/
   - **Hint**: MST with Union Find

3. Additional MST and graph problems

## Key Concepts

✅ **Kruskal's Algorithm** - Sort edges, union-find for cycles
✅ **Prim's Algorithm** - Greedy MST building
✅ **MST Properties** - Cycle detection, total cost
"""
    elif day == 32:
        content = """# Day 32: Tries - Prefix Trees

## Topics Covered
- Trie data structure
- Trie insertion and search
- Wildcard search
- Multiple word search

## Problems to Solve

1. **Implement Trie (Prefix Tree)** (Medium)
   - Link: https://leetcode.com/problems/implement-trie-prefix-tree/
   - **Hint**: Build basic trie structure

2. **Design Add and Search Words Data Structure** (Medium)
   - Link: https://leetcode.com/problems/design-add-and-search-words-data-structure/
   - **Hint**: Trie with wildcard search

3. **Word Search II** (Hard)
   - Link: https://leetcode.com/problems/word-search-ii/
   - **Hint**: Multiple word search

4. **Map Sum Pairs** (Medium)
   - Link: https://leetcode.com/problems/map-sum-pairs/
   - **Hint**: Sum of pairs with prefix

5. **Design File System** (Medium)
   - Link: https://leetcode.com/problems/design-file-system/
   - **Hint**: Trie for file system

## Key Concepts

✅ **Trie Structure** - Tree of characters
✅ **Prefix Operations** - Efficient prefix-based queries
✅ **Trie + DFS** - Combined traversal patterns
"""
    elif day == 33:
        content = """# Day 33: Segment Trees & Coordinate Compression

## Topics Covered
- Segment tree basics
- Range queries
- Point updates
- Inversion counting

## Problems to Solve

1. **Range Sum Query - Mutable** (Medium)
   - Link: https://leetcode.com/problems/range-sum-query-mutable/
   - **Hint**: Segment tree basics

2. **Count of Smaller Numbers After Self** (Hard)
   - Link: https://leetcode.com/problems/count-of-smaller-numbers-after-self/
   - **Hint**: Inversion counting

3. **Reverse Pairs** (Hard)
   - Link: https://leetcode.com/problems/reverse-pairs/
   - **Hint**: Count reverse pairs

## Key Concepts

✅ **Segment Tree Template** - Build, update, query
✅ **Coordinate Compression** - Handle large ranges
"""
    elif day == 34:
        content = """# Day 34: Heaps - Priority Queues & Selection

## Topics Covered
- Heap operations
- Min/Max heap selection
- Top K problems
- Heap design patterns

## Problems to Solve

1. **Merge k Sorted Lists** (Hard)
   - Link: https://leetcode.com/problems/merge-k-sorted-lists/
   - **Hint**: Merge multiple lists with heap

2. **Kth Largest Element in an Array** (Medium)
   - Link: https://leetcode.com/problems/kth-largest-element-in-an-array/
   - **Hint**: Find kth largest

3. **Top K Frequent Elements** (Medium)
   - Link: https://leetcode.com/problems/top-k-frequent-elements/
   - **Hint**: Top k elements

4. **Top K Frequent Words** (Medium)
   - Link: https://leetcode.com/problems/top-k-frequent-words/
   - **Hint**: Top k with sorting

5. **Find the Kth Smallest Sum of a Matrix** (Hard)
   - Link: https://leetcode.com/problems/find-the-kth-smallest-sum-of-a-matrix-with-sorted-rows-and-columns/
   - **Hint**: Kth smallest sum

## Key Concepts

✅ **Heap Pattern** - Min heap for kth largest, max heap for kth smallest
✅ **Frequency Tracking** - Hash map + heap
"""
    elif day == 35:
        content = """# Day 35: Heaps - Design & Advanced Patterns

## Topics Covered
- Heap-based data structure design
- Median maintenance
- Stream algorithms
- Complex heap applications

## Problems to Solve

1. **Find Median from Data Stream** (Hard)
   - Link: https://leetcode.com/problems/find-median-from-data-stream/
   - **Hint**: Maintain median with heaps

2. **Kth Largest Element in a Stream** (Easy)
   - Link: https://leetcode.com/problems/kth-largest-element-in-a-stream/
   - **Hint**: Stream kth largest

3. **Minimum Difficulty of a Job Schedule** (Hard)
   - Link: https://leetcode.com/problems/minimum-difficulty-of-a-job-schedule/
   - **Hint**: Daily job scheduling

4. **Last Stone Weight** (Easy)
   - Link: https://leetcode.com/problems/last-stone-weight/
   - **Hint**: Simulate stone collisions

## Key Concepts

✅ **Two Heaps** - Maintain median efficiently
✅ **Stream Processing** - Online algorithm design
"""
    elif day == 36:
        content = """# Day 36: Intervals & Greedy Algorithms

## Topics Covered
- Interval merging
- Greedy interval selection
- Optimal interval problems
- Sweep line algorithm

## Problems to Solve

1. **Merge Intervals** (Medium)
   - Link: https://leetcode.com/problems/merge-intervals/
   - **Hint**: Merge overlapping intervals

2. **Insert Interval** (Medium)
   - Link: https://leetcode.com/problems/insert-interval/
   - **Hint**: Insert into intervals

3. **Non-overlapping Intervals** (Medium)
   - Link: https://leetcode.com/problems/non-overlapping-intervals/
   - **Hint**: Remove minimum intervals

4. **Minimum Number of Arrows to Burst Balloons** (Medium)
   - Link: https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/
   - **Hint**: Minimum arrows needed

5. **Remove Covered Intervals** (Medium)
   - Link: https://leetcode.com/problems/remove-covered-intervals/
   - **Hint**: Remove subsumed intervals

6. **Maximum Population Year** (Easy)
   - Link: https://leetcode.com/problems/maximum-population-year/
   - **Hint**: Year with max population

## Key Concepts

✅ **Greedy Interval Selection** - Sort by start/end
✅ **Sweep Line** - Process events in order
"""
    elif day == 37:
        content = """# Day 37: Stock Trading & State Machines

## Topics Covered
- State machine DP
- Transaction constraints
- Cooldown and fees
- Multi-transaction problems

## Problems to Solve

1. **Best Time to Buy and Sell Stock II** (Medium)
   - Link: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/
   - **Hint**: Multiple transactions allowed

2. **Best Time to Buy and Sell Stock III** (Hard)
   - Link: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/
   - **Hint**: At most 2 transactions

3. **Best Time to Buy and Sell Stock IV** (Hard)
   - Link: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/
   - **Hint**: K transactions allowed

4. **Best Time to Buy and Sell Stock with Cooldown** (Medium)
   - Link: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/
   - **Hint**: Transactions with cooldown

5. **Best Time to Buy and Sell Stock with Transaction Fee** (Medium)
   - Link: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/
   - **Hint**: Transactions with fee

## Key Concepts

✅ **State Machine DP** - Track buy/sell states
✅ **Constraint Handling** - K transactions, cooldown, fees
"""
    elif day == 38:
        content = """# Day 38: Greedy Algorithm Patterns

## Topics Covered
- Greedy selection
- Task scheduling
- Optimization problems
- State machines

## Problems to Solve

1. **Assign Cookies** (Easy)
   - Link: https://leetcode.com/problems/assign-cookies/
   - **Hint**: Greedy assignment

2. **Task Scheduler** (Medium)
   - Link: https://leetcode.com/problems/task-scheduler/
   - **Hint**: Schedule tasks with cooldown

3. **Get Equal Substrings Within Budget** (Medium)
   - Link: https://leetcode.com/problems/get-equal-substrings-within-budget/
   - **Hint**: Minimize cost for substrings

4. **Split a String in Balanced Strings** (Easy)
   - Link: https://leetcode.com/problems/split-a-string-in-balanced-strings/
   - **Hint**: Split into balanced parts

5. **Minimum Number of Frogs Croaking** (Medium)
   - Link: https://leetcode.com/problems/minimum-number-of-frogs-croaking/
   - **Hint**: Track frog states

## Key Concepts

✅ **Greedy Choice** - Make locally optimal choice
✅ **Prove Correctness** - Why greedy works
"""
    elif day == 39:
        content = """# Day 39: Greedy Optimization Problems

## Topics Covered
- String optimization
- Array optimization
- Sorting-based greedy
- Advanced greedy patterns

## Problems to Solve

1. **Longest Palindrome** (Easy)
   - Link: https://leetcode.com/problems/longest-palindrome/
   - **Hint**: Build longest palindrome

2. **Maximize Sum Of Array After K Negations** (Easy)
   - Link: https://leetcode.com/problems/maximize-sum-of-array-after-k-negations/
   - **Hint**: Maximize with flips

3. **Reduce Array Size to The Half** (Medium)
   - Link: https://leetcode.com/problems/reduce-array-size-to-the-half/
   - **Hint**: Remove minimum elements

4. **Reducing Dishes** (Hard)
   - Link: https://leetcode.com/problems/reducing-dishes/
   - **Hint**: Maximum sum with satisfaction

## Key Concepts

✅ **Sorting Strategy** - Different sort orders for different problems
✅ **Greedy Proof** - Exchange argument
"""
    elif day == 40:
        content = """# Day 40: Advanced Interval & Scheduling Problems

## Topics Covered
- Meeting room scheduling
- Interval merging
- Employee scheduling
- Optimal resource allocation

## Problems to Solve

1. **Merge Intervals** (Medium)
   - Link: https://leetcode.com/problems/merge-intervals/
   - **Hint**: Merge overlapping intervals

2. **Insert Interval** (Medium)
   - Link: https://leetcode.com/problems/insert-interval/
   - **Hint**: Insert into interval list

3. **Meeting Scheduler** (Medium)
   - Link: https://leetcode.com/problems/meeting-scheduler/
   - **Hint**: Find common meeting time

4. **Meeting Rooms II** (Medium)
   - Link: https://leetcode.com/problems/meeting-rooms-ii/
   - **Hint**: Minimum meeting rooms

5. **Employee Free Time** (Hard)
   - Link: https://leetcode.com/problems/employee-free-time/
   - **Hint**: Find common free time

## Key Concepts

✅ **Sweep Line Algorithm** - Process events chronologically
✅ **Room/Resource Management** - Track active intervals
"""
    elif day == 41:
        content = """# Day 41: Arrays - Advanced Techniques

## Topics Covered
- Prefix/Suffix calculations
- Stack-based array problems
- Water trapping
- Complex array manipulations

## Problems to Solve

1. **Product of Array Except Self** (Medium)
   - Link: https://leetcode.com/problems/product-of-array-except-self/
   - **Hint**: Product without division

2. **Trapping Rain Water** (Hard)
   - Link: https://leetcode.com/problems/trapping-rain-water/
   - **Hint**: Calculate trapped rainwater

3. **Trapping Rain Water II** (Hard)
   - Link: https://leetcode.com/problems/trapping-rain-water-ii/
   - **Hint**: 2D trapping water

4. Review of Two Sum and other patterns

## Key Concepts

✅ **Prefix/Suffix Arrays** - Build in one pass, use in another
✅ **Stack-based Tracking** - Heights and barriers
"""
    elif day == 42:
        content = """# Day 42: Hard Array & Binary Search Problems

## Topics Covered
- Complex binary search
- Rotated array search
- Median of merged arrays
- Advanced array algorithms

## Problems to Solve

1. **Median of Two Sorted Arrays** (Hard)
   - Link: https://leetcode.com/problems/median-of-two-sorted-arrays/
   - **Hint**: Find median of merged arrays

2. **Search in Rotated Sorted Array** (Medium)
   - Link: https://leetcode.com/problems/search-in-rotated-sorted-array/
   - **Hint**: Binary search on rotated array

3. **Search in Rotated Sorted Array II** (Medium)
   - Link: https://leetcode.com/problems/search-in-rotated-sorted-array-ii/
   - **Hint**: Handle duplicates in rotated

4. **Find Minimum in Rotated Sorted Array** (Medium)
   - Link: https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/
   - **Hint**: Find minimum in rotated

5. **Find Minimum in Rotated Sorted Array II** (Hard)
   - Link: https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/
   - **Hint**: Minimum with duplicates

## Key Concepts

✅ **Rotated Array Binary Search** - Determine which half is sorted
✅ **Median Finding** - Partition-based approach
"""
    elif day == 43:
        content = """# Day 43: Hard Problems - Comprehensive Review

## Topics Covered
- Inversion counting
- Expression building
- Array optimization
- Complex problem solving

## Problems to Solve

1. **Count of Smaller Numbers After Self** (Hard)
   - Link: https://leetcode.com/problems/count-of-smaller-numbers-after-self/
   - **Hint**: Count inversions

2. **Expression Add Operators** (Hard)
   - Link: https://leetcode.com/problems/expression-add-operators/
   - **Hint**: Generate all expressions

3. **Make Array Strictly Increasing** (Hard)
   - Link: https://leetcode.com/problems/make-array-strictly-increasing/
   - **Hint**: Minimum replacements

## Key Concepts

✅ **Merge Sort for Inversions** - Efficient counting
✅ **Backtracking for Expressions** - Complex generation
"""
    elif day == 44:
        content = """# Day 44: Tree Serialization & Advanced Tree Problems

## Topics Covered
- Tree serialization/deserialization
- N-ary tree operations
- Complex tree structures
- Inheritance and hierarchies

## Problems to Solve

1. **Serialize and Deserialize Binary Tree** (Hard)
   - Link: https://leetcode.com/problems/serialize-and-deserialize-binary-tree/
   - **Hint**: Tree encoding and decoding

2. **Serialize and Deserialize BST** (Medium)
   - Link: https://leetcode.com/problems/serialize-and-deserialize-bst/
   - **Hint**: BST serialization

3. **Serialize and Deserialize N-ary Tree** (Hard)
   - Link: https://leetcode.com/problems/serialize-and-deserialize-n-ary-tree/
   - **Hint**: N-ary tree serialization

4. **Throne Inheritance** (Medium)
   - Link: https://leetcode.com/problems/throne-inheritance/
   - **Hint**: Family tree inheritance

## Key Concepts

✅ **Tree Encoding** - String and number representations
✅ **Level Order Serialization** - Different traversal orders
"""
    elif day == 45:
        content = """# Day 45: Final Comprehensive Review & Integration

## Topics Covered
- Review critical patterns
- Advanced string problems
- Complex system design
- Interview preparation

## Problems to Solve

1. **Longest Substring Without Repeating Characters** (Medium)
   - Link: https://leetcode.com/problems/longest-substring-without-repeating-characters/
   - **Hint**: Sliding window without repeating

2. **Minimum Window Substring** (Hard)
   - Link: https://leetcode.com/problems/minimum-window-substring/
   - **Hint**: Find minimum window

3. Review Two Sum with optimizations
   - Link: https://leetcode.com/problems/two-sum/

4. **Trapping Rain Water** (Hard)
   - Link: https://leetcode.com/problems/trapping-rain-water/
   - **Hint**: Advanced water trapping

## Key Concepts & Reflection

✅ **Pattern Recognition** - Identify problem type quickly
✅ **Solution Scaling** - Time/space tradeoffs
✅ **Interview Readiness** - Can solve diverse problems

## Post 45-Day Plan

After completing 45 days:
- Review weak areas
- Practice mock interviews
- Solve problems from target companies
- Study system design patterns
- Practice explanation and communication

"""
    else:
        # Generate generic day plan for remaining days
        day_num = day
        if day_num <= 10:
            phase = "Phase 1: Foundations"
        elif day_num <= 25:
            phase = "Phase 2: Core Patterns"
        elif day_num <= 35:
            phase = "Phase 3: Advanced Data Structures"
        else:
            phase = "Phase 4: Hard Problems & Integration"

        content = f"""# Day {day_num}: {phase}

## Topics Covered
- Continue building problem-solving skills
- Review patterns from previous days
- Practice variations of problems

## Problems to Solve

1. Review recommended problems from the master sheet for Day {day_num}
2. Complete 6-8 problems from daily allocation
3. Focus on time and space complexity

## Key Concepts

- Review core patterns relevant to today's problems
- Identify relationships between different problem types
- Optimize solutions iteratively

## Notes

- Refer to the master CSV sheet for problems assigned to this day
- Track your progress in the progress tracker
- Note any patterns or insights gained

"""

    # Create the file
    file_path = f"/Users/I765601/Documents/Rishabh/Daily-Quests/leetcode-bigtech-prep/daily_plan/day_{day:02d}.md"
    with open(file_path, 'w') as f:
        f.write(content)
    print(f"Created day_{day:02d}.md")

print("Script ready to generate all days")
