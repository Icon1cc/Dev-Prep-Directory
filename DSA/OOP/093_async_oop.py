"""
Problem 093: Asynchronous OOP with asyncio

Difficulty: Advanced
Topic: Async Programming

=== PROBLEM DESCRIPTION ===

Learn how to write asynchronous object-oriented code using Python's asyncio.
This is essential for modern Python applications.

Your Task:
-----------
1. Create an async `HTTPClient` class:
   - `__init__` with base_url
   - `async get(path)` - simulates HTTP GET
   - `async post(path, data)` - simulates HTTP POST
   - Use `async with` for connection context manager

2. Create an async `DataProcessor`:
   - `async process(data)` - process data asynchronously
   - `async process_batch(items)` - process multiple items concurrently

3. Create an async `Cache`:
   - `async get(key)` - get with simulated delay
   - `async set(key, value)` - set with simulated delay
   - Use asyncio.Lock for thread safety

4. Create an async `Pipeline`:
   - Chain multiple async operations
   - `add_stage(async_func)`
   - `async run(data)` - execute all stages

5. Demonstrate async context managers:
   - `__aenter__` and `__aexit__`
   - Async iterators: `__aiter__` and `__anext__`

Expected Output:
----------------
Async HTTP Client:
GET /users: [{"id": 1, "name": "Alice"}]
POST /users: Created user Bob

Batch processing 5 items...
Processing took 0.5s (parallel) vs 2.5s (sequential)

Async Pipeline:
Data: hello
  Stage 1 (uppercase): HELLO
  Stage 2 (reverse): OLLEH
  Stage 3 (add prefix): PREFIX_OLLEH
Final result: PREFIX_OLLEH

Async iteration:
async for item in DataStream():
  Received: item_0
  Received: item_1
  Received: item_2

=== CONCEPTS TO LEARN ===
- async def defines coroutines
- await calls coroutines
- asyncio.gather for concurrent execution
- Async context managers and iterators
- asyncio.Lock for synchronization

=== STARTER CODE ===
"""

import asyncio
from typing import Any, List

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# async def main():
#     # Test async classes
#     pass
#
# asyncio.run(main())
