# Day 1: Array Fundamentals & Hash Maps Intro

## Topics Covered
- Basic array operations
- Hash maps for counting
- Linear search patterns
- Duplicate detection

## Problems to Solve

### Easy - Foundations

1. **Two Sum**
   - Link: https://leetcode.com/problems/two-sum/
   - Difficulty: Easy
   - Pattern: Hash Map
   - Companies: Google, Meta, Amazon, Apple
   - **Hint**: Store each number in a hash map and check if the complement exists

2. **Remove Element**
   - Link: https://leetcode.com/problems/remove-element/
   - Difficulty: Easy
   - Pattern: Two Pointers
   - Companies: Amazon, Microsoft
   - **Hint**: Use two pointers - one for iteration, one for placement position

3. **Remove Duplicates from Sorted Array**
   - Link: https://leetcode.com/problems/remove-duplicates-from-sorted-array/
   - Difficulty: Easy
   - Pattern: Two Pointers
   - Companies: Microsoft, Google
   - **Hint**: Two pointers with index tracking for in-place removal

4. **Contains Duplicate**
   - Link: https://leetcode.com/problems/contains-duplicate/
   - Difficulty: Easy
   - Pattern: Hash Map
   - Companies: Amazon, Google
   - **Hint**: Use a set to track seen elements, return true on first duplicate

5. **Merge Sorted Array**
   - Link: https://leetcode.com/problems/merge-sorted-array/
   - Difficulty: Easy
   - Pattern: Two Pointers
   - Companies: Amazon, Microsoft
   - **Hint**: Work backwards to avoid overwriting elements in the first array

6. **Best Time to Buy and Sell Stock**
   - Link: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
   - Difficulty: Easy
   - Pattern: One Pass
   - Companies: Google, Meta, Apple
   - **Hint**: Track minimum price seen and maximum profit simultaneously in one pass

7. **Majority Element**
   - Link: https://leetcode.com/problems/majority-element/
   - Difficulty: Easy
   - Pattern: Boyer-Moore Voting
   - Companies: Meta, Amazon
   - **Hint**: Boyer-Moore voting algorithm: track candidate and count

## Key Concepts Learned Today

✅ **Hash Maps for O(1) lookup**
- Perfect for "find complement" problems
- Use when you need fast lookups or counting

✅ **Two Pointer Technique**
- Efficient for sorted arrays and in-place modifications
- Space complexity: O(1) vs O(n) with extra space

✅ **Single Pass Solutions**
- Track state variables as you iterate
- Minimize time complexity to O(n)

✅ **Boyer-Moore Voting**
- Find majority element in linear time
- Track candidate and count pair

## Review & Reflection

- Did you understand why hash map solutions are O(n)?
- Can you explain when two pointers work vs when you need sorting?
- What's the time/space tradeoff in majority element?

