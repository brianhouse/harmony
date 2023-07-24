#!venv/bin/python

import sys
from chord import *
from display import *

try:
    key = get_key(sys.argv[1].lower().capitalize())
except IndexError:
    print("[key]")
    exit()
except ValueError:
    print("Bad key")
    exit()



diatonic = [
            Chord("ION", key,     (0, 2, 4, 5, 7, 9, 11)),
            Chord("DOR", key + 2, (0, 2, 3, 5, 7, 9, 10)),
            Chord("PHR", key + 4, (0, 1, 3, 5, 7, 8, 10)),
            Chord("LYD", key + 5, (0, 2, 4, 6, 7, 9, 11)),
            Chord("MYX", key + 7, (0, 2, 4, 5, 7, 9, 10)),
            Chord("AOL", key + 9, (0, 2, 3, 5, 7, 8, 10)),
            Chord("LOC", key + 11,(0, 1, 3, 5, 6, 8, 10)),
            ]

interchange = [
            Chord("DOR", key + 5,  (0, 2, 3, 5, 7, 9, 10)),  # IV- borrowed from AOLIAN
            Chord("MYX", key + 10, (0, 2, 4, 5, 7, 9, 10)), # bVII borrowed from AOLIAN
            ]

secondary_dominants = [
            Chord("MX2", key + 9, (0, 2, 4, 5, 7, 9, 10)),  # V7/II
            Chord("MX3", key + 11,(0, 2, 4, 5, 7, 9, 10)),  # V7/III
            Chord("MX4", key + 0, (0, 2, 4, 5, 7, 9, 10)),  # V7/IV
            Chord("MX5", key + 2, (0, 2, 4, 5, 7, 9, 10)),  # V7/V
            Chord("MX6", key + 4, (0, 2, 4, 5, 7, 9, 10)),  # V7/VI
            ]

blues = [
            Chord("MYX", key,     (0, 2, 4, 5, 7, 9, 10)),
            Chord("MYX", key + 5, (0, 2, 4, 5, 7, 9, 10)),
            ]


chords = diatonic + interchange + secondary_dominants + blues

 
# how to handle enharmonic
for chord in chords:
    chord.set_role(key)
    chord.relate(chords)

print("/ SECONDARY DOMINANTS\n")
for chord in secondary_dominants[::-1]:  
    print(display(chord))

print("/ INTERCHANGE\n")
for chord in interchange[::-1]:  
    print(display(chord))

print("/ DIATONIC\n")
for chord in diatonic[::-1]:  
    print(display(chord))




