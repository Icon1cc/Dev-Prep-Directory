"""
Problem 042: Adapter Design Pattern

Difficulty: Intermediate
Topic: Design Patterns

=== PROBLEM DESCRIPTION ===

The Adapter pattern converts the interface of a class into another interface
that clients expect. It allows classes with incompatible interfaces to work
together. Think: power adapters for different countries.

Your Task:
-----------
1. Create an existing `OldPrinter` class (legacy system):
   - Method `print_text(text)` - prints text

2. Create a new interface `ModernPrinter` (ABC):
   - Method `print_document(document)` - expected method name

3. Create `PrinterAdapter` that:
   - Takes an OldPrinter in __init__
   - Implements ModernPrinter interface
   - `print_document()` internally calls `print_text()`

4. Real-world example - JSON to XML adapter:
   - `JsonApi` returns data in JSON format
   - `XmlProcessor` expects XML format
   - Create an adapter to convert between them

Expected Output:
----------------
Using legacy printer via adapter:
Printing: Hello from modern interface!

Converting JSON to XML:
JSON: {"name": "Alice", "age": 30}
XML: <data><name>Alice</name><age>30</age></data>

=== CONCEPTS TO LEARN ===
- Adapter wraps an incompatible class
- Makes old code work with new interfaces
- No need to modify original classes
- Useful for integrating third-party libraries

=== STARTER CODE ===
"""

from abc import ABC, abstractmethod
import json

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# # Printer adapter example
# old_printer = OldPrinter()
# adapter = PrinterAdapter(old_printer)
#
# print("Using legacy printer via adapter:")
# adapter.print_document("Hello from modern interface!")
#
# print("\nConverting JSON to XML:")
# json_api = JsonApi()
# xml_adapter = JsonToXmlAdapter(json_api)
# data = json_api.get_data()
# print(f"JSON: {data}")
# print(f"XML: {xml_adapter.get_xml_data()}")
