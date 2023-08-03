#!venv/bin/python

import sys
from chord import *

## MAJOR

# key = Key('C', 'ION', ION)
# key.add_chord(2, 'DOR', DOR)
# key.add_chord(4, 'PHR', PHR)
# key.add_chord(5, 'LYD', LYD)
# key.add_chord(7, 'MYX', MYX)
# key.add_chord(9, 'AOL', AOL)
# key.add_chord(11,'LOC', LOC)

# # interchange. how to label as such?
# # auto detect and label the whole chord as non-diatonic?
# # maybe list the actual analysis symbol?
# key.add_chord(5, 'X DOR', DOR)   # IV- borrowed from AOLIAN
# key.add_chord(10,'X MYX', MYX)  # bVII borrowed from AOLIAN

# # secondary dominant
# key.add_chord(9, 'V7/II', MYX) 
# key.add_chord(11,'V7/III', MYX) 
# key.add_chord(0, 'V7/IV', MYX) 
# key.add_chord(2, 'V7/V', MYX) 
# key.add_chord(4, 'V7/VI', MYX) 

# # blues
# key.add_chord(0, 'BLUES MYX', MYX)
# key.add_chord(5, 'BLUES MYX', MYX)


## COMPOSITE MINOR

key = Key('A', 'AOL', AOL)
key.add_chord(0, 'JAZ', JAZ)  # I-ma7  
key.add_chord(2, 'LOC', LOC)
key.add_chord(2, 'DOR', DOR)  # borrow from Dorian
key.add_chord(3, 'ION', ION)
key.add_chord(3, 'JZ2', rot(JAZ, 2))  # wait, is this a Jaz mode?

# left off here
# https://bocce.online.berklee.edu/#/15768/OCOMP-111.01/15847/5/composite-minor-chords-narrowed-down
key.add_chord(5, 'DOR', DOR)
key.add_chord(7, 'MYX', MYX)  # substitute V7 for V-7
key.add_chord(8, 'LYD', LYD)
key.add_chord(10,'MYX', MYX)
key.add_chord(11,'LOC', LOC)  # include VII-

# # secondary dominants
# key.add_chord(10, 'V7/♭III', MYX)  # same as MYX7
# key.add_chord(0, 'V7/IV', MYX) 
# key.add_chord(2, 'V7/V', MYX) 


print(key)

