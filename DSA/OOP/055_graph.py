"""
Problem 055: Building a Graph Class

Difficulty: Advanced
Topic: Data Structure Implementation

=== PROBLEM DESCRIPTION ===

A graph consists of vertices (nodes) and edges connecting them. Graphs can be:
- Directed or Undirected
- Weighted or Unweighted
- Represented as adjacency list or adjacency matrix

Your Task:
-----------
1. Create a `Graph` class using adjacency list:
   - `__init__(directed=False)` - default undirected
   - `add_vertex(vertex)` - add a vertex
   - `add_edge(v1, v2, weight=1)` - add edge between v1 and v2
   - `remove_edge(v1, v2)` - remove edge
   - `get_neighbors(vertex)` - return list of adjacent vertices
   - `has_edge(v1, v2)` - check if edge exists

2. Implement graph traversals:
   - `bfs(start)` - Breadth-First Search, returns list of vertices
   - `dfs(start)` - Depth-First Search, returns list of vertices

3. Implement useful algorithms:
   - `has_path(start, end)` - check if path exists
   - `find_path(start, end)` - return one path if exists
   - `is_connected()` - check if all vertices are reachable

4. Print the graph nicely:
   - `__str__` shows adjacency list

Expected Output:
----------------
Graph:
A -> [(B, 1), (C, 1)]
B -> [(A, 1), (C, 1), (D, 1)]
C -> [(A, 1), (B, 1), (D, 1)]
D -> [(B, 1), (C, 1)]

BFS from A: ['A', 'B', 'C', 'D']
DFS from A: ['A', 'B', 'C', 'D']
Path A to D: ['A', 'B', 'D']
Is connected: True

=== CONCEPTS TO LEARN ===
- Adjacency list: dict of vertex -> list of neighbors
- BFS uses queue, DFS uses stack (or recursion)
- Graph traversal is foundation for many algorithms
- Essential for interviews (shortest path, cycle detection, etc.)

=== STARTER CODE ===
"""

from collections import deque

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# g = Graph()
# for v in ['A', 'B', 'C', 'D']:
#     g.add_vertex(v)
#
# g.add_edge('A', 'B')
# g.add_edge('A', 'C')
# g.add_edge('B', 'C')
# g.add_edge('B', 'D')
# g.add_edge('C', 'D')
#
# print(f"Graph:\n{g}")
# print(f"BFS from A: {g.bfs('A')}")
# print(f"DFS from A: {g.dfs('A')}")
# print(f"Path A to D: {g.find_path('A', 'D')}")
# print(f"Is connected: {g.is_connected()}")
