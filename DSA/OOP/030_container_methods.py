"""
Problem 030: Container Magic Methods (__len__, __getitem__, __setitem__)

Difficulty: Intermediate
Topic: Making Custom Containers

=== PROBLEM DESCRIPTION ===

You can make your objects behave like lists or dictionaries by implementing
container magic methods:
- __len__: len(obj)
- __getitem__: obj[key]
- __setitem__: obj[key] = value
- __delitem__: del obj[key]
- __contains__: item in obj

Your Task:
-----------
1. Create a class `Playlist`:
   - `__init__(name)` - initializes with name and empty songs list
   - `add_song(song)` - adds a song to the playlist

2. Implement container methods:
   - `__len__` - returns number of songs
   - `__getitem__(index)` - get song by index (support negative indices)
   - `__setitem__(index, song)` - replace song at index
   - `__delitem__(index)` - remove song at index
   - `__contains__(song)` - check if song is in playlist

3. Also implement `__iter__` so the playlist can be iterated

Expected Output:
----------------
Playlist 'Road Trip' has 3 songs
First song: Bohemian Rhapsody
Last song: Stairway to Heaven
'Hotel California' in playlist: True
Songs:
- Bohemian Rhapsody
- Hotel California
- Stairway to Heaven

=== CONCEPTS TO LEARN ===
- These methods make your object usable with Python's built-in syntax
- __iter__ returns an iterator (can just return iter(self.songs))
- Support negative indices for Pythonic behavior

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# playlist = Playlist("Road Trip")
# playlist.add_song("Bohemian Rhapsody")
# playlist.add_song("Hotel California")
# playlist.add_song("Stairway to Heaven")
#
# print(f"Playlist '{playlist.name}' has {len(playlist)} songs")
# print(f"First song: {playlist[0]}")
# print(f"Last song: {playlist[-1]}")
# print(f"'Hotel California' in playlist: {'Hotel California' in playlist}")
#
# print("Songs:")
# for song in playlist:
#     print(f"- {song}")
