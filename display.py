from termcolor import colored
from constants import *


def display(key, scale):
    s = []
    s.append(f"{colored(scale.function + " " + scale.mode_name.rjust(0), 'white', attrs=['bold'])}\n")

    for degree in (6, 5, 4, 3, 2, 1, 0):
        for ct, chord_type in enumerate(CHORDS):
            chord = scale.chords[ct]
            if chord.conflict:
                continue

            # analysis labels]
            label = scale.labels[degree]
            if isinstance(label, tuple):
                label = label[0 if degree in chord_type else 1]
            if degree in chord_type:
                s.append(f"{label}".rjust(4))
            else:
                s.append(f"".rjust(4))

            # pitches
            pitch_name = key.pitch_names[scale.pitches[degree]]
            attrs = []
            if scale.accidentals[degree]:
                attrs.append('underline')
                if len(pitch_name) < 2:
                    pitch_name += '♮'
            if degree in chord.avoid_degrees:
                s.append(f" {colored(pitch_name.ljust(2), 'red', attrs=attrs)}")
            elif degree not in chord_type or degree == 4 and not len(label):  # special case for dominant
                s.append(f" {colored(pitch_name.ljust(2), 'yellow', attrs=attrs)}")
            elif degree == 0:
                attrs.append('bold')
                s.append(f" {colored(pitch_name.ljust(2), 'cyan', attrs=attrs)}")
            else:
                s.append(f" {colored(pitch_name.ljust(2), 'cyan', attrs=attrs)}")

            # # transitions
            # if len(chord.transitions[degree]):
            #     s.append("→ ")
            #     for transition in chord.transitions[degree]:
            #         for ch, (pitch, kind) in transition.items():
            #             if kind == CIRCLE:
            #                 color = 'light_blue'  # looks purple
            #             elif kind == DOM:
            #                 color = 'light_cyan'
            #             elif kind == PULL:
            #                 color = 'green'
            #             elif kind == MORPH:
            #                 color = 'magenta'
            #             target = '(' + key.pitch_names[pitch] + ')' if pitch != ch.root else ""
            #             # s.append(f"{colored(ch.labels[0] + ch.labels[2] + ch.labels[6] + target, color)} ")
            #             # s.append(f"{colored(ch.labels[0] + ':' + key.pitch_names[ch.root] + ch.labels[2] + ch.labels[4] + ch.labels[6] + target, color, attrs=[])} ")
            #             s.append(f"{colored(ch.labels[0] + ':' + key.pitch_names[ch.root] + target, color, attrs=[])} ")
        s.append("\n")
    return "".join(s)
