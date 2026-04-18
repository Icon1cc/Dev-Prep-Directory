"""
Check if a string is subsequence of other
Given two strings s and t, check if s is subsequence of t.
"""
def is_subsequence(s: str, t: str) -> bool:
    s_len = len(s)
    t_len = len(t)
    s_index = 0
    t_index = 0
    while s_index < s_len and t_index < t_len:
        if s[s_index] == t[t_index]:
            s_index += 1
        t_index += 1
    return s_index == s_len

try:
    s = input("Enter the first string (s): ")
    t = input("Enter the second string (t): ")
    if is_subsequence(s, t):
        print(f'"{s}" is a subsequence of "{t}".')
    else:
        print(f'"{s}" is not a subsequence of "{t}".')
except Exception as e:
    print(f"An error occurred: {e}")