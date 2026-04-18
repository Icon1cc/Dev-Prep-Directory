# Day 2: Binary Search & Strings

## Topics Covered
- Binary search fundamentals
- String comparison techniques
- Hash map applications for strings
- Character frequency analysis

## Problems to Solve

### Easy - Binary Search Basics

1. **Search Insert Position**
   - Link: https://leetcode.com/problems/search-insert-position/
   - Difficulty: Easy
   - Pattern: Binary Search
   - Companies: Google, Microsoft
   - **Hint**: Standard binary search with edge case for insertion position

2. **Guess Number Higher or Lower**
   - Link: https://leetcode.com/problems/guess-number-higher-or-lower/
   - Difficulty: Easy
   - Pattern: Binary Search
   - Companies: Meta, Amazon
   - **Hint**: Classic binary search game - eliminate half the range each time

3. **Binary Search**
   - Link: https://leetcode.com/problems/binary-search/
   - Difficulty: Easy
   - Pattern: Binary Search
   - Companies: Google, Apple
   - **Hint**: Standard template - mid = left + (right - left) / 2

4. **First Bad Version**
   - Link: https://leetcode.com/problems/first-bad-version/
   - Difficulty: Easy
   - Pattern: Binary Search
   - Companies: Apple, Amazon
   - **Hint**: Find first occurrence - use binary search with boundary tracking

### Easy - Strings & Hash Maps

5. **First Unique Character in a String**
   - Link: https://leetcode.com/problems/first-unique-character-in-a-string/
   - Difficulty: Easy
   - Pattern: Hash Map
   - Companies: Amazon, Google
   - **Hint**: Use hash map to count frequencies, then iterate to find first unique

6. **Reverse String**
   - Link: https://leetcode.com/problems/reverse-string/
   - Difficulty: Easy
   - Pattern: Two Pointers
   - Companies: Microsoft, Apple
   - **Hint**: Two pointer reversal from both ends

7. **Valid Anagram**
   - Link: https://leetcode.com/problems/valid-anagram/
   - Difficulty: Easy
   - Pattern: Hash Map
   - Companies: Amazon, Google
   - **Hint**: Check if character frequencies match between strings

8. **Valid Palindrome**
   - Link: https://leetcode.com/problems/valid-palindrome/
   - Difficulty: Easy
   - Pattern: Two Pointers
   - Companies: Meta, Microsoft
   - **Hint**: Two pointers from both ends, skip non-alphanumeric characters

## Key Concepts Learned Today

✅ **Binary Search Template**
- Time: O(log n), Space: O(1)
- Must avoid infinite loops: mid = left + (right - left) / 2
- Apply to sorted arrays and monotonic properties

✅ **String Problems with Hash Maps**
- Frequency counting is fundamental
- Two pass approach: count first, then verify

✅ **Character Set Operations**
- Anagrams: same characters with same frequencies
- Palindromes: symmetric property

## Next Steps

- Practice binary search variations
- Understand when to use hash map vs sorting for string problems
- Recognize string validation patterns

