#!venv/bin/python

import sys
from chord import *


key = Key('C', 'ION', ION)
key.add_chord(2, 'DOR', DOR)
key.add_chord(3, 'PHR', PHR)
key.add_chord(4, 'LYD', LYD)
key.add_chord(5, 'MYX', MYX)
key.add_chord(6, 'AOL', AOL)
key.add_chord(7, 'LOC', LOC)

# interchange. how to label as such?
# auto detect and label the whole chord as non-diatonic?
key.add_chord(5, 'XDR', DOR)   # IV- borrowed from AOLIAN
key.add_chord(10,'XMX', MYX)  # bVII borrowed from AOLIAN

# secondary dominant
key.add_chord(9, 'MX2', MYX) 
key.add_chord(11,'MX3', MYX) 
key.add_chord(0, 'MX4', MYX) 
key.add_chord(2, 'MX5', MYX) 
key.add_chord(4, 'MX6', MYX) 


for chord in key.chords[::-1]:
    print(key.display(chord))


## but see, the point here is you don't use every one all the time


# diatonic = [
#             Chord("ION", key,     (0, 2, 4, 5, 7, 9, 11)),
#             Chord("DOR", key + 2, (0, 2, 3, 5, 7, 9, 10)),
#             Chord("PHR", key + 4, (0, 1, 3, 5, 7, 8, 10)),
#             Chord("LYD", key + 5, (0, 2, 4, 6, 7, 9, 11)),
#             Chord("MYX", key + 7, (0, 2, 4, 5, 7, 9, 10)),
#             Chord("AOL", key + 9, (0, 2, 3, 5, 7, 8, 10)),
#             Chord("LOC", key + 11,(0, 1, 3, 5, 6, 8, 10)),
#             ]

# interchange = [
#             Chord("DOR", key + 5,  (0, 2, 3, 5, 7, 9, 10)),  
#             Chord("MYX", key + 10, (0, 2, 4, 5, 7, 9, 10)), 
#             ]

# secondary_dominants = [
#             Chord("MX2", key + 9, (0, 2, 4, 5, 7, 9, 10)),  # V7/II
#             Chord("MX3", key + 11,(0, 2, 4, 5, 7, 9, 10)),  # V7/III
#             Chord("MX4", key + 0, (0, 2, 4, 5, 7, 9, 10)),  # V7/IV
#             Chord("MX5", key + 2, (0, 2, 4, 5, 7, 9, 10)),  # V7/V
#             Chord("MX6", key + 4, (0, 2, 4, 5, 7, 9, 10)),  # V7/VI
#             ]

# blues = [
#             Chord("MYX", key,     (0, 2, 4, 5, 7, 9, 10)),
#             Chord("MYX", key + 5, (0, 2, 4, 5, 7, 9, 10)),
#             ]


# chords = diatonic + interchange + secondary_dominants + blues

 
## change this to happen inside Key instead

# # how to handle enharmonic
# for chord in chords:
#     chord.set_role(key)
#     chord.relate(chords)

# print("/ SECONDARY DOMINANTS\n")
# for chord in secondary_dominants[::-1]:  
#     print(display(chord))

# print("/ INTERCHANGE\n")
# for chord in interchange[::-1]:  
#     print(display(chord))

# print("/ DIATONIC\n")
# for chord in diatonic[::-1]:  
#     print(display(chord))




