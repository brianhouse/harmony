from constants import *
from display import *


class Key():


    def __init__(self, tonic_string, name, mode):
        self.tonic = KEYS.index(tonic_string.upper().strip())
        self.pitch_names = PITCHES_FLAT if self.tonic > 6 else PITCHES_SHARP        
        self.chords = []
        self.tonic_chord = Chord(self, self.tonic, name, mode)
        self.chords.append(self.tonic_chord)


    def add_chord(self, step, name, mode):        
        self.chords.append(Chord(self, self.tonic + step, name, mode))  
        for chord in self.chords:
            chord.find_leads()
        ## star pitches here somehow that arent diatonic


    def __str__(self):
        return "\n".join([display(self, chord) for chord in self.chords[::-1]])


class Chord():


    def __init__(self, key, root, name, mode):
        self.key = key
        self.name = name
        self.root = root % 12
        self.mode = mode
        self.pitches = [(self.root + semitones) % 12 for semitones in self.mode] 
        self.set_role()
        self.find_avoids()
        

    def set_role(self):
        self.labels = []
        self.labels.append(LABELS[0][(self.root - self.key.tonic) % 12])
        for degree in range(1, len(self.mode)):      
            self.labels.append(LABELS[degree][self.mode[degree]])


    def find_avoids(self):
        
        self.avoid_degrees = []
        for degree in range(1, len(self.mode)):
            pdegree = degree - 1
        
            # no half-steps above chord tones         
            if pdegree in (0, 2, 4, 6) and self.mode[degree] - self.mode[pdegree] == 1:
                self.avoid_degrees.append(degree)

            # no tritones with chord tones other than root, unless it's dom7
            for pdegree in (2, 4, 6):
                if degree != 6 and self.mode[degree] - self.mode[pdegree] == 6:
                    self.avoid_degrees.append(degree)


    def find_leads(self):

        ## colors should be in display
        ## leads should be in categories, maybe

        self.leads = [[] for i in range(len(self.mode))]

        # circle of fourths
        for chord in self.key.chords:
            if chord.pitches[4] == self.root:
                self.leads[0].append({chord: (self.root, 'light_blue')}) # looks purple

        # dominant / sub-dominant symmetry
        for chord in self.key.chords:            
            if  self.root == (self.key.tonic + 5) % 12 and chord.root == (self.key.tonic + 7) % 12 or \
                self.root == (self.key.tonic + 7) % 12 and chord.root == (self.key.tonic + 5) % 12:                    
                    self.leads[0].append({chord: (chord.root, 'light_cyan')})

        # semitone pulls
        transitions = ( ((self.key.tonic - 1) % 12, self.key.tonic),            # leading tone to tonic
                        ((self.key.tonic + 4) % 12, (self.key.tonic + 5) % 12), # major third to perfect fourth
                        ((self.key.tonic + 5) % 12, (self.key.tonic + 4) % 12), # perfect fourth to major third
                        )
        for transition in transitions:
            start, target = transition
            if start in self.pitches[0:7:2]: # including leading tone in start, but not target
                for chord in self.key.chords:
                    if chord == self:
                        continue
                    if target in chord.pitches[0:5:2]:
                        self.leads[self.pitches.index(start)].append({chord: (target, 'light_green')})

        # morphs (a bit controversial)
        for chord in self.key.chords:
            if chord.root == 0: # don't morph to tonic
                continue
            if self.root == chord.pitches[2]:
                self.leads[0].append({chord: (self.root, 'magenta')})
            if self.pitches[2] == chord.root:
                self.leads[2].append({chord: (chord.root, 'magenta')})





