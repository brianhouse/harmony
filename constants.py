
# PITCHES

KEYS = 'C', 'G', 'D', 'A', 'E', 'B', 'F♯', 'D♭', 'A♭', 'E♭', 'B♭', 'F'

PITCHES_FLAT  = 'C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B'
PITCHES_SHARP = 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B'


# MODES

def rot(scale, steps):
    scale = scale[steps:] + scale[:steps]
    scale = [degree - scale[0] for degree in scale]
    return [(degree + 12) if degree < 0 else degree for degree in scale]


ION = MAJ = 0, 2, 4, 5, 7, 9, 11
DOR = rot(ION, 1)
PHR = rot(ION, 2)
LYD = rot(ION, 3)
MYX = rot(ION, 4)
AOL = MIN = rot(ION, 5)
LOC = rot(ION, 6)
IOMODES = ION, DOR, PHR, LYD, MYX, AOL, LOC

JAZ = 0, 2, 3, 5, 7, 9, 11
HAR = 0, 2, 3, 5, 7, 8, 11
ULT = rot(HAR, 6)  # Ultralocrian

# https://en.wikipedia.org/wiki/Jazz_minor_scale
# https://en.wikipedia.org/wiki/Acoustic_scale


# SCALES / CHORDS

FUNCTIONS = 'I', '', 'II', '♭III', 'III', 'IV', '♯IV', 'V', '♭VI', 'VI', '♭VII', 'VII'


# functional (not exhaustive) notes in chord types
# 1, ([2, 3, 4], 5, [6, 7])  # as named
# 0, ([1, 2, 3], 4, [5, 6])  # 0-indexed
CHORDS = [(0, 2, 4, 6),   # 7th
          (0, 2, 4, 5),   # 6th
          (0, 3, 4, 6),   # 7sus4
          (0, 3, 4, 5),   # 6sus4
          (0, 1, 4, 6),   # 7sus2
          (0, 1, 4, 5),   # 6sus2
          ]

LABELS = [{0: ''},
          {1: ('♭2', '♭2'), 2: ('s2', '9')},                      # 2nds
          {3: ('-', '♭2'), 4: ('', '13')},                        # 3rds
          {4: ('♭4', '♭11'), 5: ('s4', '11'), 6: ('♯4', '♯11')},  # 4ths
          {6: '♭5', 7: '', 8: '+'},                               # 5ths
          {8: ('♭6', '♭13'), 9: ('6', '13')},                     # 6ths
          {9: 'o7', 10: '7', 11: '∆7'}                            # 7ths
          ]


# TRANSITIONS

CIRCLE = 0
DOM = 1
PULL = 2
MORPH = 3

