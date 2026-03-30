from constants import *
from display import display
import json


class Key():

    def __init__(self, tonic_name, maj_min):
        tonic_name = tonic_name.upper().strip()
        key_index = KEYS.index(tonic_name) + (5 if maj_min == 'MINOR' else 0)
        self.pitch_names = PITCHES_FLAT if key_index > 6 else PITCHES_SHARP
        self.tonic = self.pitch_names.index(tonic_name)
        self.scales = []
        self.add_scale(0, 'AOL' if maj_min == 'MINOR' else 'ION')

    def add_scale(self, step, mode_name, parent=None):
        scale = Scale(self, self.tonic + step, mode_name, parent=parent)
        self.scales.append(scale)

    def __str__(self):
        for scale in self.scales:
            for chord in scale.chords:
                chord.find_transitions()
            scale.find_strengths()
        return "\n".join([display(self, scale) for scale in self.scales[::-1]])


class Scale():

    def __init__(self, key, root, mode_name, parent=None):
        self.key = key
        self.root = root
        self.mode_name = mode_name
        self.mode = globals()[mode_name]
        if parent is not None:
            parent_mode = globals()[parent]
            if parent_mode[2] == 3:  # minor; go up to relative major
                relative_major = (key.tonic + 3) % 12
            else:
                relative_major = key.tonic
            if PITCHES_FLAT[relative_major] in KEYS:
                key_index = KEYS.index(PITCHES_FLAT[relative_major])
                self.pitch_names = PITCHES_FLAT if key_index > 6 else PITCHES_SHARP
        else:
            self.pitch_names = key.pitch_names
        self.pitches = [(self.root + semitones) % 12 for semitones in self.mode]
        self.accidentals = [pitch not in self.key.scales[0].pitches if len(self.key.scales) else False for pitch in self.pitches]
        self.chords = []
        for kind in CHORDS:
            chord = Chord(self, kind)
            if not chord.conflict:
                self.chords.append(chord)
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

    def find_strengths(self):
        self.transitions = {}
        for chord in self.chords:
            for degree, transitions in chord.transitions.items():
                if not len(transitions):
                    continue
                for transition in transitions:
                    if degree not in self.transitions:
                        self.transitions[degree] = []
                    scale, target, kind = transition
                    self.transitions[degree].append(transition)
        for degree, tally in self.transitions.items():
            self.transitions[degree] = list(dict.fromkeys(tally))
        self.strengths = {}
        for degee, tally in self.transitions.items():
            for transition in tally:
                scale, target, kind = transition
                if scale not in self.strengths:
                    self.strengths[scale] = 0
                self.strengths[scale] += 1


class Chord():

    def __init__(self, scale, functional_degrees):
        self.scale = scale
        self.functional_degrees = functional_degrees
        self.hide_dominant = 2 in self.functional_degrees and 4 in self.functional_degrees and self.scale.mode[4] == 7
        self.find_avoids()
        self.flag_conflict()
        self.find_transitions()

    def find_avoids(self):

        self.avoid_degrees = []

        for degree in range(1, len(self.scale.mode)):
            pdegree = degree - 1

            # in general, tensions resolve to a lower partial

            # no half-steps _above_ functional degrees (so it's not bi-directional like pulls)
            if self.scale.mode[degree] - self.scale.mode[pdegree] == 1:
                if pdegree in self.functional_degrees:
                    self.avoid_degrees.append(degree)

            # no tritones above functional degrees other than root
            # ...unless it's a dominant (maj 3rd + dom7)
            # ...or fully diminished
            # both of which are special cases that are used very directly in functional harmony
            for functional_degree in self.functional_degrees:
                if functional_degree != 0:
                    if self.scale.mode[degree] - self.scale.mode[functional_degree] == 6:  # tritone
                        if not (self.scale.mode[functional_degree] == 4 and self.scale.mode[degree] == 10):  # maj3 and dom7
                            if not (self.scale.mode[functional_degree] == 3 and self.scale.mode[4] == 6 and self.scale.mode[degree] == 9):  # fully diminished
                                self.avoid_degrees.append(degree)

            # sus disallow third
            if degree == 2 and (1 in self.functional_degrees or 3 in self.functional_degrees):
                self.avoid_degrees.append(degree)

        self.avoid_degrees = list(dict.fromkeys(self.avoid_degrees))

    def flag_conflict(self):
        self.conflict = False
        for functional_degree in self.functional_degrees:
            if functional_degree in self.avoid_degrees:
                self.conflict = True
        if 3 in self.functional_degrees and self.scale.mode[3] != 5:  # no imperfect sus4 (imperfect sus2 implicitly avoided)
            self.conflict = True

    def find_transitions(self):

        self.transitions = {}

        for degree in range(7):

            pitch = self.scale.pitches[degree]
            target_scales = self.scale.key.scales

            transitions = []

            # tonic doesn't move
            if pitch == self.scale.key.tonic:
                continue

            # the circle: resolve up a fourth /down a fifth
            if degree == 0:
                for scale in target_scales:
                    if (pitch - 7) % 12 == scale.root:
                        transitions.append((scale, scale.root, CIRCLE))

            # dominant <-> sub-dominant
            if degree == 0:
                for scale in target_scales:
                    if pitch == (self.scale.key.tonic + 5) % 12 and scale.root == (self.scale.key.tonic + 7) % 12 or \
                       pitch == (self.scale.key.tonic + 7) % 12 and scale.root == (self.scale.key.tonic + 5) % 12:
                        transitions.append((scale, scale.root, DOM))

            # semitone between a chord tone (excluding dominant) and a scale triad (this is bi-directional)
            if degree in self.functional_degrees and pitch != self.scale.root + 7:
                for scale in target_scales:
                    for target_degree in (0, 2, 4):
                        target_pitch = scale.pitches[target_degree]
                        if (target_pitch - pitch) % 12 in (1, 11):
                            transitions.append((scale, target_pitch, PULL))

            # morphs (shared root or 3rd) (a bit controversial)
            for scale in target_scales:
                if scale.root == self.scale.key.tonic:  # don't morph to tonic
                    continue
                if degree == 0 and pitch == scale.pitches[2]:
                    transitions.append((scale, scale.pitches[2], MORPH))
                if degree == 2 and pitch == scale.pitches[0] and degree in self.functional_degrees:
                    transitions.append((scale, scale.pitches[0], MORPH))

            # # # morphs (from root or second functional degree to root or third) (more controversial)
            # # [but then why not let the second degree be a target too? ... because I don't have that with scales]
            # for scale in target_scales:
            #     if scale.root == self.scale.key.tonic:  # don't morph to tonic
            #         continue
            #     if degree == 0 and pitch == scale.pitches[2]:
            #         transitions.append((scale, scale.pitches[2], MORPH))
            #     if degree == self.functional_degrees[1] and pitch == scale.pitches[0]:
            #         transitions.append((scale, scale.pitches[0], MORPH))

            self.transitions[degree] = transitions


