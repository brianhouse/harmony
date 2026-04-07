#!venv/bin/python

import sys
from harmony import *

# MAJOR

key = Key('C', 'MAJ')
# key.add_scale(2, 'DOR')
key.add_scale(2, 'MYX')
key.add_scale(4, 'PHR')
# key.add_scale(4, 'DOR')
# key.add_scale(5, 'LYD')
key.add_scale(5, 'DOR', 'MIN')   # IV-7 borrowed from AOLIAN
key.add_scale(7, 'MYX')
key.add_scale(9, 'AOL')
# key.add_scale(11,'LOC')
key.add_scale(11,'ULT', 'MIN')

print(key)


# Avoid Notes in Major Scale Modes (Diatonic)
# Ionian (I): 4th degree
# Dorian (ii): None (or 6th in some contexts)
# Phrygian (iii): 2nd and 6th degrees
# Lydian (IV): None
# Mixolydian (V): 4th degree
# Aeolian (vi): 6th degree
# Locrian (vii°): 2nd degree

# this is all covered by semitones


# # interchange. how to label as such?
# # auto detect and label the whole chord as non-diatonic?
# # maybe list the actual analysis symbol?
# key.add_scale(0, 'X DOR', DOR)   # I-7 borrowed from DORIAN
# key.add_scale(0, 'X JAZ', JAZ)   # I-ma7 jazz
# key.add_scale(1, 'X LYD', LYD)	 # bIIma7 borrowed from PHRYGIAN
# key.add_scale(2, 'X LOC', LOC)	 # II-7b5 borrowed from AOLIAN
# key.add_scale(3, 'X ION', ION)   # bIIIma7 borrowed from DORIAN
# key.add_scale(5, 'X DOR', DOR)   # IV-7 borrowed from AOLIAN
# key.add_scale(5, 'X JAZ4', rot(JAZ, 3)) # IV7 borrowed from jazz
# key.add_scale(7, 'X DOR', DOR)   # V-7 borrowed from MYXOLYDIAN
# key.add_scale(7, 'X HAR', rot(HAR, 4)) # V7 from harmonic minor
# key.add_scale(8, 'X LYD', LYD)   # bVIma7 borrowed from AOLIAN
# key.add_scale(10,'X MYX', MYX)   # bVII7 borrowed from AOLIAN
# key.add_scale(10,'X LYD', LYD)   # bVIIma7 borrowed from MYXOLYDIAN


# # secondary dominant
# key.add_scale(9, 'V7/II', MYX)
# key.add_scale(11,'V7/III', MYX)
# key.add_scale(0, 'V7/IV', MYX)
# key.add_scale(2, 'V7/V', MYX)
# key.add_scale(4, 'V7/VI', MYX)

# # blues
# key.add_scale(0, 'BLUES MYX', MYX)
# key.add_scale(5, 'BLUES MYX', MYX)


# COMPOSITE MINOR
# https://bocce.online.berklee.edu/#/15768/OCOMP-111.01/15847/5/composite-minor-chords-narrowed-down

# key = Key('D', 'MINOR')
# # key.add_scale(0, 'DOR')  # I-ma7, a jazz minor mode
# # key.add_scale(0, 'JAZ')  # I-ma7, a jazz minor mode
# key.add_scale(2, 'LOC')
# # key.add_scale(2, 'PHR')  # dorian mode2 (aka PHR)
# key.add_scale(3, 'ION')
# # key.add_scale(3, 'JZ2', rot(JAZ, 2))  # a jazz minor mode
# # key.add_scale(5, 'MYX')  # a dorian mode4 (aka MYX), also JAZ4
# key.add_scale(5, 'DOR')
# key.add_scale(7, 'PHR')  # natural (aeolian) V-7
# # key.add_scale(7, 'MYX')  # substitute V7 for V-7
# key.add_scale(8, 'LYD')
# # key.add_scale(9, 'LOC')  # dorian mode6, also JAZ6
# key.add_scale(10, 'MYX')  # natural (aeolian) bVII7
# # key.add_scale(11,'HR7', rot(HAR, 6))  # VIIdim from harmonic minor

# # secondary dominants
# key.add_scale(9, 'V7/II', MYX)  # same as MYX6
# key.add_scale(10,'V7/♭III', MYX)  # same as MYX7
# key.add_scale(0, 'V7/IV', MYX)
# key.add_scale(2, 'V7/V', MYX)

# neapolitan chord?


# print(key)
