"""
Problem 078: Flyweight Design Pattern

Difficulty: Advanced
Topic: Structural Design Pattern

=== PROBLEM DESCRIPTION ===

The Flyweight pattern minimizes memory usage by sharing common data between
multiple objects. It separates intrinsic (shared) state from extrinsic
(unique) state.

Your Task:
-----------
1. Create a text editor scenario:
   - Millions of characters on screen
   - Each character has: char, font, size, color, position
   - Font, size, color can be shared (intrinsic)
   - Position is unique (extrinsic)

2. Create `CharacterStyle` (Flyweight):
   - Stores font, size, color (intrinsic state)

3. Create `CharacterStyleFactory`:
   - Returns existing style if available
   - Creates new one only if needed
   - Caches all created styles

4. Create `Character`:
   - References a CharacterStyle (shared)
   - Stores position (unique per character)

5. Demonstrate memory savings:
   - Without flyweight: each character stores all data
   - With flyweight: characters share style objects

Expected Output:
----------------
Without Flyweight:
Created 10000 characters, each with own style object
Memory: ~10000 style objects

With Flyweight:
Created 10000 characters
Unique styles created: 5 (Arial-12-black, Arial-14-red, etc.)
Characters share style objects, massive memory savings!

Style cache:
- 'Arial-12-black': used by 3500 characters
- 'Arial-14-red': used by 2000 characters
- ...

=== CONCEPTS TO LEARN ===
- Intrinsic state: shared, immutable, context-independent
- Extrinsic state: unique, varies with context
- Factory ensures sharing of flyweights
- Huge memory savings for many similar objects

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Demonstrate memory savings with flyweight pattern
