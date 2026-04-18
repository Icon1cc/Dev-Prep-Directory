"""
Problem 089: Interview Problem - Design a Chess Game

Difficulty: Advanced
Topic: System Design Interview Question

=== PROBLEM DESCRIPTION ===

Design a chess game with proper OOP modeling. This tests your ability to
model complex game rules and piece movements.

Requirements:
- 8x8 board with all standard pieces
- Each piece type has unique movement rules
- Detect check, checkmate, stalemate
- Track game history (moves)
- Support castling, en passant, pawn promotion

Your Task:
-----------
1. Create `Color` enum: WHITE, BLACK

2. Create `Position`:
   - `row` (1-8), `col` ('a'-'h')
   - `__eq__`, `__hash__` for comparison

3. Create `Piece` ABC:
   - `color`, `position`
   - `get_valid_moves(board)` - returns list of valid positions
   - Subclasses: King, Queen, Rook, Bishop, Knight, Pawn

4. Create `Board`:
   - 8x8 grid of Pieces or None
   - `get_piece(position)`
   - `move_piece(from_pos, to_pos)`
   - `is_valid_move(piece, to_pos)`

5. Create `Game`:
   - `board`, `current_turn`, `move_history`
   - `make_move(from_pos, to_pos)`
   - `is_check(color)` - is this color in check?
   - `is_checkmate(color)` - is this color checkmated?
   - `get_game_status()` - ongoing, check, checkmate, draw

Expected Output:
----------------
Game started!
  a b c d e f g h
8 r n b q k b n r
7 p p p p p p p p
6 . . . . . . . .
5 . . . . . . . .
4 . . . . . . . .
3 . . . . . . . .
2 P P P P P P P P
1 R N B Q K B N R

White's turn: e2 -> e4
  a b c d e f g h
8 r n b q k b n r
7 p p p p p p p p
6 . . . . . . . .
5 . . . . . . . .
4 . . . . P . . .
3 . . . . . . . .
2 P P P P . P P P
1 R N B Q K B N R

Black's turn: e7 -> e5
...

=== STARTER CODE ===
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional, Tuple

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Play a few moves of chess
