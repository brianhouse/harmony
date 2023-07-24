
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
        
            # no half-steps above chord tones         
            if pdegree in (0, 2, 4, 6) and self.mode[degree] - self.mode[pdegree] == 1:
                self.avoid_degrees.append(degree)

            # no tritones with chord tones other than root, unless it's dom7
            for pdegree in (2, 4, 6):
                if degree != 6 and self.mode[degree] - self.mode[pdegree] == 6:
                    self.avoid_degrees.append(degree)



    def set_role(self, key):
        self.key = key
        self.labels = []
        self.labels.append(LABELS[0][(self.root - self.key) % 12])
        for degree in range(1, len(self.mode)):      
            self.labels.append(LABELS[degree][self.mode[degree]])



    def relate(self, chords):

        ### LEADS ###

        # circle of fourths
        for chord in chords:
            if chord.pitches[4] == self.root:
                self.leads[0].append({chord: (self.root, 'light_blue')})

        # dominant / sub-dominant symmetry
        for chord in chords:            
            if  self.root == (self.key + 5) % 12 and chord.root == (self.key + 7) % 12 or \
                self.root == (self.key + 7) % 12 and chord.root == (self.key + 5) % 12:                    
                    self.leads[0].append({chord: (chord.root, 'light_cyan')})

        # semitone pulls
        transitions = ( ((self.key - 1) % 12, self.key),            # leading tone to tonic
                        ((self.key + 4) % 12, (self.key + 5) % 12), # major third to perfect fourth
                        ((self.key + 5) % 12, (self.key + 4) % 12), # perfect fourth to major third
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





