"""
Problem 079: Implementing a Card Game (Practical OOP)

Difficulty: Intermediate
Topic: Real-world Application

=== PROBLEM DESCRIPTION ===

Build a card game system demonstrating multiple OOP concepts together.
This is similar to what you might be asked in an interview.

Your Task:
-----------
1. Create `Card` class:
   - Attributes: suit (hearts, diamonds, clubs, spades), rank (2-10, J, Q, K, A)
   - Comparison methods based on rank
   - `__str__` shows "Rank of Suit" (e.g., "Ace of Spades")

2. Create `Deck` class:
   - Contains 52 cards
   - `shuffle()` - randomize card order
   - `deal()` - return and remove top card
   - `__len__` - cards remaining
   - Use iterator protocol to iterate over cards

3. Create `Hand` class:
   - Holds cards dealt to a player
   - `add_card(card)` - add to hand
   - `play_card(index)` - remove and return card
   - `value` property - total value (for Blackjack)

4. Create `Player` class:
   - Attributes: name, hand, chips/score
   - `bet(amount)`, `win(amount)`, `lose(amount)`

5. Create a simple `BlackjackGame` class:
   - Deal cards, calculate scores, determine winner

Expected Output:
----------------
Deck created with 52 cards
Shuffling...
Dealing to Alice: Jack of Hearts, 5 of Diamonds (value: 15)
Dealing to Dealer: Ace of Spades, hidden

Alice hits: 3 of Clubs (total: 18)
Alice stands

Dealer reveals: Ace of Spades, 7 of Hearts (total: 18)
Push! (Tie)

=== STARTER CODE ===
"""

import random
from enum import Enum

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Play a simple game of Blackjack
