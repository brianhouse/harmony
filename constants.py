
KEYS = 'C', 'G', 'D', 'A', 'E', 'B', 'F♯', 'D♭', 'A♭', 'E♭', 'B♭', 'F'

PITCHES_FLAT  = 'C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B'
PITCHES_SHARP = 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B'

LABELS = [  ('I', '', 'II', '♭III', 'III', 'IV', '♯IV', 'V', '♭VI', 'VI', '♭VII', 'VII'),
            {1: '♭9', 2: '9'},              # 2nds
            {3: '-', 4: ''},                # 3rds
            {4: '♭11', 5: '11', 6: '♯11'},  # 4ths
            {6: '♭5', 7: '', 8: '+'},       # 5ths
            {8: '♭13', 9: '13'},            # 6ths
            {9: 'o7', 10: '7', 11: '∆7'}    # 7ths
            ]


def rot(scale, steps):
    scale = scale[steps:] + scale[:steps]
    scale = [degree - scale[0] for degree in scale]
    return [(degree + 12) if degree < 0 else degree for degree in scale]


ION = 0, 2, 4, 5, 7, 9, 11
DOR = rot(ION, 1)
PHR = rot(ION, 2)
LYD = rot(ION, 3)
MYX = rot(ION, 4)
AOL = rot(ION, 5)
LOC = rot(ION, 6)
MODES = ION, DOR, PHR, LYD, MYX, AOL, LOC

JAZ = 0, 2, 3, 5, 7, 9, 11
HAR = 0, 2, 3, 5, 7, 8, 11


# https://en.wikipedia.org/wiki/Jazz_minor_scale
# https://en.wikipedia.org/wiki/Acoustic_scale
