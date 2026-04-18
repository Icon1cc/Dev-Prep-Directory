"""
Problem 074: Command Design Pattern

Difficulty: Intermediate-Advanced
Topic: Behavioral Design Pattern

=== PROBLEM DESCRIPTION ===

The Command pattern encapsulates a request as an object, allowing:
- Parameterization of clients with different requests
- Queueing of requests
- Logging of requests
- Undo/redo operations

Your Task:
-----------
1. Create a `Command` ABC:
   - `execute()` - perform the action
   - `undo()` - reverse the action

2. Create a `TextEditor` (Receiver):
   - `text` - current text content
   - `write(content)` - append text
   - `delete(n)` - delete last n characters
   - `get_text()` - return current text

3. Create concrete commands:
   - `WriteCommand(editor, text)` - adds text
   - `DeleteCommand(editor, n)` - deletes characters
   - `CopyCommand(editor)` - copies text to clipboard
   - `PasteCommand(editor)` - pastes from clipboard

4. Create `CommandInvoker`:
   - `execute(command)` - runs command and stores for undo
   - `undo()` - undoes last command
   - `redo()` - redoes last undone command
   - `history` - list of executed commands

Expected Output:
----------------
Write "Hello ": Hello
Write "World!": Hello World!
Undo: Hello
Redo: Hello World!
Delete 6: Hello
Undo: Hello World!

Command history: ['Write', 'Write', 'Delete']

=== CONCEPTS TO LEARN ===
- Commands are objects that represent actions
- Decouples invoker from receiver
- Enables undo/redo, macro commands, logging
- Can queue and schedule commands

=== STARTER CODE ===
"""

from abc import ABC, abstractmethod

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Demonstrate command pattern with undo/redo
