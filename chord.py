from constants import *
from display import display


class Key():

    def __init__(self, tonic_string, name, mode):
        key_index = KEYS.index(tonic_string.upper().strip())
        signature_offset = MODES[0][MODES.index(mode)]
        key_index = (key_index + signature_offset) % len(KEYS)
        self.pitch_names = PITCHES_FLAT if key_index > 6 else PITCHES_SHARP
        self.tonic = self.pitch_names.index(tonic_string)
        self.scales = []
        self.tonic_scale = Scale(self, self.tonic, name, mode)
        self.scales.append(self.tonic_scale)

    def add_scale(self, step, name, mode):
        scale = Scale(self, self.tonic + step, name, mode)
        self.scales.append(scale)
        scale.accidentals = [pitch not in self.tonic_scale.pitches for pitch in scale.pitches]
        for scale in self.scales:
            scale.find_transitions()

    def __str__(self):
        return "\n".join([display(self, scale) for scale in self.scales[::-1]])


class Scale():

    def __init__(self, key, root, name, mode):
        self.key = key
        self.name = name
        self.root = root % 12
        self.mode = mode
        self.pitches = [(self.root + semitones) % 12 for semitones in self.mode]
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

    def find_transitions(self):

        # colors should be in display
        # transitions should be in categories, maybe

        self.transitions = [[] for i in range(len(self.mode))]

        # the circle: resolve down a fifth / up a fourth
        for scale in self.key.scales:
            if (self.root + 5) % 12 == scale.root:
                self.transitions[0].append({scale: (self.root, CIRCLE)})  # purple

        # dominant <-> sub-dominant
        for scale in self.key.scales:
            if self.root == (self.key.tonic + 5) % 12 and scale.root == (self.key.tonic + 7) % 12 or \
               self.root == (self.key.tonic + 7) % 12 and scale.root == (self.key.tonic + 5) % 12:
                self.transitions[0].append({scale: (scale.root, DOM)})

        # semitone pulls from scale tone to scale tone
        for start_degree in [0, 2, 4, 6]:  # including 7th in start, but not in target
            if self.pitches[start_degree] == self.key.tonic:  # tonic doesn't go anywhere
                continue
            for scale in self.key.scales:
                if scale == self:
                    continue
                for target_degree in [0, 2, 4]:
                    # print(scale.name, start_degree + 1, target_degree + 1, (scale.pitches[target_degree] - self.pitches[start_degree]) % 12, (scale.pitches[target_degree] - self.pitches[start_degree]) % 12 == 1)
                    if (scale.pitches[target_degree] - self.pitches[start_degree]) % 12 in (1, 11):
                        self.transitions[start_degree].append({scale: (scale.pitches[target_degree], PULL)})

        # morphs (shared root/3rd, a bit controversial)
        for scale in self.key.scales:
            if scale.root == self.key.tonic:  # don't morph to tonic
                continue
            if self.root == scale.pitches[2]:
                self.transitions[0].append({scale: (self.root, MORPH)})
            if self.pitches[2] == scale.root:
                self.transitions[2].append({scale: (scale.root, MORPH)})
