from constants import *
from display import *


class Key():

    def __init__(self, tonic_string, name, mode):
        self.key_index = KEYS.index(tonic_string.upper().strip())
        signature_offset = MODES[0][MODES.index(mode)]
        self.key_index = (self.key_index + signature_offset) % len(KEYS)
        self.pitch_names = PITCHES_FLAT if self.key_index > 6 else PITCHES_SHARP
        self.tonic = self.pitch_names.index(tonic_string)
        self.chords = []
        self.tonic_chord = Chord(self, self.tonic, name, mode)
        self.chords.append(self.tonic_chord)

    def add_chord(self, step, name, mode):
        chord = Chord(self, self.tonic + step, name, mode)
        self.chords.append(chord) 
        chord.accidentals = [pitch not in self.tonic_chord.pitches for pitch in chord.pitches]
        for chord in self.chords:
            chord.find_leads()

    def __str__(self):
        return "\n".join([display(self, chord) for chord in self.chords[::-1]])


class Chord():

    def __init__(self, key, root, name, mode):
        self.key = key
        self.name = name
        self.root = root % 12
        self.mode = mode
        self.pitches = [(self.root + semitones) % 12 for semitones in self.mode]
        # diatonic?
        # self.pitch_names = self.key.pitch_names
        # self.pitch_names = PITCHES_FLAT if self.key_index > 6 else PITCHES_SHARP
        self.accidentals = [False] * len(self.pitches)
        self.set_role()
        self.find_avoids()

    def set_role(self):
        self.labels = []
        self.labels.append(LABELS[0][(self.root - self.key.tonic) % 12])
        for degree in range(1, len(self.mode)):
            try:
                self.labels.append(LABELS[degree][self.mode[degree]])
            except KeyError as e:
                print(self.mode)
                print('degree', degree)
                print('label', LABELS[degree])
                print('step', self.mode[degree])
                raise e

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

        # the circle: resolve down a fifth / up a fourth
        for chord in self.key.chords:
            if (self.root + 5) % 12 == chord.root:
                self.leads[0].append({chord: (self.root, 'light_blue')}) # looks purple

        # dominant / sub-dominant symmetry
        for chord in self.key.chords:
            if self.root == (self.key.tonic + 5) % 12 and chord.root == (self.key.tonic + 7) % 12 or \
               self.root == (self.key.tonic + 7) % 12 and chord.root == (self.key.tonic + 5) % 12:
                self.leads[0].append({chord: (chord.root, 'light_cyan')})

        # semitone pulls from chord tone to chord tone
        for start_degree in [0, 2, 4, 6]:  # including 7th in start, but not in target
            if self.pitches[start_degree] == self.key.tonic: # tonic doesn't go anywhere
                continue
            for chord in self.key.chords:
                if chord == self:
                    continue
                for target_degree in [0, 2, 4]:
                    # print(chord.name, start_degree + 1, target_degree + 1, (chord.pitches[target_degree] - self.pitches[start_degree]) % 12, (chord.pitches[target_degree] - self.pitches[start_degree]) % 12 == 1)
                    if (chord.pitches[target_degree] - self.pitches[start_degree]) % 12 in (1, 11):
                        self.leads[start_degree].append({chord: (chord.pitches[target_degree], 'light_green')})

        # morphs (shared root/3rd, a bit controversial)
        for chord in self.key.chords:
            if chord.root == self.key.tonic:  # don't morph to tonic
                continue
            if self.root == chord.pitches[2]:
                self.leads[0].append({chord: (self.root, 'magenta')})
            if self.pitches[2] == chord.root:
                self.leads[2].append({chord: (chord.root, 'magenta')})


