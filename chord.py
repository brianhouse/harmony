from constants import *
from display import display


class Key():

    def __init__(self, tonic_name, maj_min):
        tonic_name = tonic_name.upper().strip()
        key_index = KEYS.index(tonic_name) + (5 if maj_min == 'MINOR' else 0)
        self.pitch_names = PITCHES_FLAT if key_index > 6 else PITCHES_SHARP
        self.tonic = self.pitch_names.index(tonic_name)
        self.scales = []
        self.add_scale(0, 'AOL' if maj_min == 'MINOR' else 'ION')

    def add_scale(self, step, mode_name):
        scale = Scale(self, self.tonic + step, mode_name)
        self.scales.append(scale)
        for scale in self.scales:
            for chord in scale.chords:
                chord.find_transitions()

    def __str__(self):
        return "\n".join([display(self, scale) for scale in self.scales[::-1]])


class Scale():

    def __init__(self, key, root, mode_name):
        self.key = key
        self.root = root
        self.mode_name = mode_name
        self.mode = globals()[mode_name]
        self.pitches = [(self.root + semitones) % 12 for semitones in self.mode]
        self.accidentals = [pitch not in self.key.scales[0].pitches if len(self.key.scales) else False for pitch in self.pitches]
        self.chords = [Chord(self, kind) for kind in CHORDS]
        self.set_role()

    def set_role(self):
        self.function = FUNCTIONS[(self.root - self.key.tonic) % 12]
        self.labels = []
        for step in range(len(self.mode)):
            try:
                self.labels.append(LABELS[step][self.mode[step]])
            except KeyError as e:
                print('mode', self.mode)
                print('step number', step)
                print('label', LABELS[step])
                print('step', self.mode[step])
                raise e


class Chord():

    def __init__(self, scale, functional_degrees):
        self.scale = scale
        self.functional_degrees = functional_degrees
        self.avoid_degrees = []
        self.find_avoids()
        self.transitions = {}
        self.find_transitions()

    def find_avoids(self):

        for degree in range(1, len(self.scale.mode)):
            pdegree = degree - 1

            # no half-steps above functional degrees
            if self.scale.mode[degree] - self.scale.mode[pdegree] == 1:
                if pdegree in self.functional_degrees:
                    self.avoid_degrees.append(degree)

            # # no tritones above functional degrees other than root, unless it's a 3rd in dom7
            # if self.scale.mode[degree] - self.scale.mode[pdegree] == 6 and degree != 0:
            #     if not (pdegree == 2 and self.scale.mode[degree] == 10):
            #         self.avoid_degrees.append(degree)

        self.avoid_degrees = list(set(self.avoid_degrees))

    def find_transitions(self):

        for degree in range(7):  # 0-indexed, natch

            pitch = self.scale.pitches[degree]
            target_scales = [scale for scale in self.scale.key.scales if scale != self.scale]

            transitions = []

            # the circle: resolve down a fifth or up a fourth
            if degree == 0:
                for scale in target_scales:
                    if pitch + 5 % 12 == scale.root:
                        transitions.append((scale, CIRCLE))

            # dominant <-> sub-dominant
            for scale in target_scales:
                if degree == 4 and pitch == scale.pitches[3] or \
                   degree == 3 and pitch == scale.pitches[4]:
                    transitions.append((scale, CIRCLE))

            # semitone pulls from scale tone to triad scale tone
            if degree != 0:  # tonic doesn't move
                for scale in target_scales:
                    for target_degree in (0, 2, 4):
                        if scale.pitches[target_degree] - pitch % 12 in (1, 11):
                            transitions.append((scale, PULL))

            # morphs (shared root/3rd)
            for scale in target_scales:
                if degree == 0 and pitch == scale.pitches[2] or \
                   degree == 2 and pitch == scale.pitches[0]:
                    transitions.append((scale, MORPH))

            self.transitions[degree] = transitions


## fuck, wait, this is treating sus4s as the third degree. is that good???
## also have to verify that the dominant and sub-dominant is actually the 3rd and 4th degrees

## if pitch == self.scale.dominant  --- and the other pitch? fuck


