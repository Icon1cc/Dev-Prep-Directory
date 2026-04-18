"""
Problem 058: Building a Trie (Prefix Tree)

Difficulty: Advanced
Topic: Data Structure Implementation

=== PROBLEM DESCRIPTION ===

A Trie is a tree-like data structure used to store strings. It's efficient
for prefix-based operations like autocomplete. Each node represents a character.

Your Task:
-----------
1. Create a `TrieNode` class:
   - `children` - dict mapping char to TrieNode
   - `is_end_of_word` - boolean marking end of a complete word

2. Create a `Trie` class:
   - `__init__()` - initialize with root node
   - `insert(word)` - insert a word into the trie
   - `search(word)` - return True if exact word exists
   - `starts_with(prefix)` - return True if any word starts with prefix
   - `delete(word)` - remove word from trie

3. Advanced methods:
   - `autocomplete(prefix)` - return all words starting with prefix
   - `count_words()` - return total number of words
   - `get_all_words()` - return list of all words

Expected Output:
----------------
Insert: apple, app, application, apply, banana
Search 'apple': True
Search 'app': True
Search 'appl': False
Starts with 'app': True
Autocomplete 'app': ['app', 'apple', 'application', 'apply']
All words: ['app', 'apple', 'application', 'apply', 'banana']
Delete 'apple', search 'apple': False
Search 'app': True  (still exists)

=== CONCEPTS TO LEARN ===
- Each path from root represents a prefix
- O(m) for insert/search where m = word length
- Space efficient for common prefixes
- Used for: autocomplete, spell checkers, IP routing

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# trie = Trie()
# words = ['apple', 'app', 'application', 'apply', 'banana']
# for word in words:
#     trie.insert(word)
#
# print(f"Insert: {', '.join(words)}")
# print(f"Search 'apple': {trie.search('apple')}")
# print(f"Search 'app': {trie.search('app')}")
# print(f"Search 'appl': {trie.search('appl')}")
# print(f"Starts with 'app': {trie.starts_with('app')}")
# print(f"Autocomplete 'app': {trie.autocomplete('app')}")
# print(f"All words: {trie.get_all_words()}")
#
# trie.delete('apple')
# print(f"Delete 'apple', search 'apple': {trie.search('apple')}")
# print(f"Search 'app': {trie.search('app')}  (still exists)")
