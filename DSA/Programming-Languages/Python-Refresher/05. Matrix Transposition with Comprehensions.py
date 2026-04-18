"""
5. Matrix Transposition with Comprehensions
Description: Write a function transpose(matrix) that takes a 2D list (a list of lists) representing a matrix. The function must return the transpose of the matrix. You are required to implement the core logic using a single nested list comprehension.
Example:
Input: matrix = [[1, 2, 3], [4, 5, 6]]
Output: [[1, 4], [2, 5], [3, 6]]
Constraints:
You can assume the input matrix is non-empty and rectangular (all rows have the same length).
"""

def transpose(matrix):
    row = len(matrix) 
    col = len(matrix[0])
    transposed = []
    
    for i in range(col):
        new_row = []
        for j in range(row):
            element = matrix[j][i]
            new_row.append(element)
        transposed.append(new_row)
    
    return transposed

rows = int(input("Enter number of rows: "))

matrix = []
for i in range(rows):
    row = list(map(int, input(f"Enter row {i+1} (space separated): ").split()))
    matrix.append(row)
    
# transposed = [[matrix[j][i] for j in range(row)] for i in range(col)]
# transposed = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

print("Matrix =", matrix)
transposed_matrix = transpose(matrix)
print("Transposed Matrix =", transposed_matrix)