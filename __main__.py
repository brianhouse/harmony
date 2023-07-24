#!venv/bin/python

import sys
from termcolor import colored

KEYS = 'C', 'G', 'D', 'A', 'E', 'B', 'F#', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F'
PITCHES_FLAT  = 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B'
PITCHES_SHARP = 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'
LABELS = [  ('I', '', 'II', 'bIII', 'III', 'IV', '#IV', 'V', 'bVI', 'VI', 'bVII', 'VII'), 
            {1: 'b9', 2: '9'}, 
            {3: '-', 4: ''}, 
            {5: '11', 6: '#11'}, 
            {6: 'b5', 7: ''}, 
            {8: 'b13', 9: '13'}, 
            {9: 'dim7', 10: '7', 11: 'ma7'}
            ]


class Chord():


    def __init__(self, name, root, mode):
        self.name = name        
        self.root = root % 12
        self.mode = mode
        self.pitches = [(self.root + semitones) % 12 for semitones in self.mode] 
        self.leads = [[] for i in range(len(self.mode))]

        ### AVOIDS ###
        self.avoid_degrees = []
        for degree in range(1, len(self.mode)):
            pdegree = degree - 1
        
            # no half-degrees above chord tones         
            if pdegree in (0, 2, 4, 6) and self.mode[degree] - self.mode[pdegree] == 1:
                self.avoid_degrees.append(degree)

            # no tritones with chord tones other than root, unless it's dom7
            for pdegree in (2, 4, 6):
                if degree != 6 and self.mode[degree] - self.mode[pdegree] == 6:
                    self.avoid_degrees.append(degree)

        self.set_labels()


    def relate(self, chords):

        ### LEADS ###

        # circle of fourths
        for chord in chords:
            if chord.pitches[4] == self.root:
                self.leads[0].append({chord: (self.root, 'light_blue')})

        # dominant / sub-dominant symmetry
        for chord in chords:            
            if  self.root == (key + 5) % 12 and chord.root == (key + 7) % 12 or \
                self.root == (key + 7) % 12 and chord.root == (key + 5) % 12:                    
                    self.leads[0].append({chord: (chord.root, 'light_cyan')})

        # semitone pulls
        transitions = ( ((key - 1) % 12, key),            # leading tone to tonic
                        ((key + 4) % 12, (key + 5) % 12), # major third to perfect fourth
                        ((key + 5) % 12, (key + 4) % 12), # perfect fourth to major third
                        )
        for transition in transitions:
            start, target = transition
            if start in self.pitches[0:7:2]: # including leading tone in start, but not target
                for chord in chords:
                    if chord == self:
                        continue
                    if target in chord.pitches[0:5:2]:
                        self.leads[self.pitches.index(start)].append({chord: (target, 'light_green')})

        # morphs (a bit controversial)
        for chord in chords:
            if chord.root == 0: # don't morph to tonic
                continue
            if self.root == chord.pitches[2]:
                self.leads[0].append({chord: (self.root, 'magenta')})
            if self.pitches[2] == chord.root:
                self.leads[2].append({chord: (chord.root, 'magenta')})                


        self.set_labels()


    def set_labels(self):
        self.labels = []
        self.labels.append(LABELS[0][(self.root - key) % 12])
        for degree in range(1, len(self.mode)):      
            self.labels.append(LABELS[degree][self.mode[degree]])


    def __str__(self):
        s = []
        # s.append(f"{self.name.rjust(3)}\n")        
        for degree in (5, 3, 1, 6, 4, 2, 0):

            # analysis labels
            if degree == 0:
                c = self.name + "-" + self.labels[degree]
                s.append(f"{c.rjust(8)}")
            else:
                s.append(f"{self.labels[degree].rjust(8)}")

            # pitches
            pitch_name = pitch_names[self.pitches[degree]]
            if degree in self.avoid_degrees:
                # s.append(f"<{pitch_name}>".ljust(4))
                s.append(f" {colored(pitch_name, 'red')}".ljust(2))
            elif degree % 2:
                s.append(f" {colored(pitch_name, 'yellow')}".ljust(2))
            elif degree == 0:
                s.append(f" {colored(pitch_name, 'cyan', attrs=['reverse', 'bold']).ljust(2)}")
            else:
                s.append(f" {colored(pitch_name, 'cyan').ljust(2)}")

            if self.pitches[degree] not in chords[0].pitches:
                s.append("*")

            # transitions
            if len(self.leads[degree]):
                s.append(f" -> ")
                for lead in self.leads[degree]:
                    for chord, (pitch, color) in lead.items():
                        # if chords.index(chord) < 8:
                        #     s.append(f"{colored(chord.name + '-' + chord.labels[0] + '(' + pitch_names[pitch] + ')', color, attrs=['underline'])}<{chords.index(chord)}> ")
                        # else:
                        s.append(f"{colored(chord.name + '-' + chord.labels[0] + '(' + pitch_names[pitch] + ')', color)} ")

            s.append("\n")
        return "".join(s)


try:
    key = sys.argv[1].lower().capitalize()
    key_i = KEYS.index(key)       
    pitch_names = PITCHES_FLAT if key_i > 6 else PITCHES_SHARP
    key = pitch_names.index(key)
except IndexError:
    print("[key]")
    exit()
except ValueError:
    print("Bad key")
    exit()


# maybe this labeling is bad, could have a category field
chords = [  # diatonic
            Chord("ION", key,     (0, 2, 4, 5, 7, 9, 11)),
            Chord("DOR", key + 2, (0, 2, 3, 5, 7, 9, 10)),
            Chord("PHR", key + 4, (0, 1, 3, 5, 7, 8, 10)),
            Chord("LYD", key + 5, (0, 2, 4, 6, 7, 9, 11)),
            Chord("MYX", key + 7, (0, 2, 4, 5, 7, 9, 10)),
            Chord("AOL", key + 9, (0, 2, 3, 5, 7, 8, 10)),
            Chord("LOC", key + 11,(0, 1, 3, 5, 6, 8, 10)),

            # interchange
            Chord("XDR", key + 5, (0, 2, 3, 5, 7, 9, 10)),  # IV- borrowed from AOLIAN
            Chord("XMX", key + 10, (0, 2, 4, 5, 7, 9, 10)), # bVII borrowed from AOLIAN

            # secondary dominants
            Chord("MX2", key + 9, (0, 2, 4, 5, 7, 9, 10)),  # V7/II
            Chord("MX3", key + 11, (0, 2, 4, 5, 7, 9, 10)), # V7/III
            Chord("MX4", key + 0, (0, 2, 4, 5, 7, 9, 10)),  # V7/IV
            Chord("MX5", key + 2, (0, 2, 4, 5, 7, 9, 10)),  # V7/V
            Chord("MX6", key + 4, (0, 2, 4, 5, 7, 9, 10)),  # V7/VI

            # Blues: I7 and IV7
            ]

# how to handle enharmonic
for chord in chords:
    chord.relate(chords)

for chord in chords[::-1]:  
    print(chord)

