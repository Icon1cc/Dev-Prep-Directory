"""
Problem 080: Implementing a File System (Composite Pattern)

Difficulty: Intermediate-Advanced
Topic: Real-world Application + Design Pattern

=== PROBLEM DESCRIPTION ===

Build a file system using the Composite pattern. Files and directories
should be treated uniformly where possible.

Your Task:
-----------
1. Create `FileSystemItem` ABC:
   - Properties: name, size, parent
   - Methods: get_path(), get_size()

2. Create `File` class:
   - Extends FileSystemItem
   - Has content or size attribute

3. Create `Directory` class:
   - Extends FileSystemItem
   - Contains list of FileSystemItems (files or directories)
   - `add(item)`, `remove(item)`, `get_children()`
   - `get_size()` returns sum of all contained items

4. Add operations:
   - `find(name)` - search recursively for items by name
   - `tree()` - display hierarchical structure
   - `copy()`, `move()` operations

5. Implement iterator to traverse the file system

Expected Output:
----------------
/home
├── documents
│   ├── report.pdf (1024 KB)
│   └── notes.txt (256 KB)
├── pictures
│   ├── vacation
│   │   └── beach.jpg (2048 KB)
│   └── profile.png (512 KB)
└── music
    └── song.mp3 (4096 KB)

Total size of /home: 7936 KB
Find 'beach.jpg': /home/pictures/vacation/beach.jpg

=== CONCEPTS TO LEARN ===
- Composite pattern: treat individual objects and compositions uniformly
- Recursive structures (directory contains directories)
- Tree traversal algorithms
- Iterator pattern for hierarchical data

=== STARTER CODE ===
"""

from abc import ABC, abstractmethod

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Build and navigate a file system
