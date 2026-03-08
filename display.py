from termcolor import colored
from constants import *


def display(key, scale):
    s = []
    s.append(f"{colored(scale.function + " " + scale.mode_name.rjust(0), 'white', attrs=['bold'])}\n")

    for degree in (6, 5, 4, 3, 2, 1, 0):
        s.append("".rjust(6))
        for ct, chord_type in enumerate(CHORDS):

            # find the chord type
            found = False
            for chord in scale.chords:
                if chord.functional_degrees == chord_type:
                    found = True
                    break
            if not found:
                s.append("".rjust(6))
                continue

            # analysis labels]
            label = scale.labels[degree]
            if isinstance(label, tuple):
                label = label[0 if degree in chord_type else 1]
            if degree in chord_type:
                s.append(f"{label}".rjust(3))
            else:
                s.append("".rjust(3))

            # pitches
            pitch_name = key.pitch_names[scale.pitches[degree]]
            attrs = []
            if scale.accidentals[degree]:
                attrs.append('underline')
                if len(pitch_name) < 2:
                    pitch_name += '♮'
            if degree in chord.avoid_degrees:
                s.append(f" {colored(pitch_name.ljust(2), 'red', attrs=attrs)}")
            elif degree not in chord_type or degree == 4 and chord.hide_dominant:
                s.append(f" {colored(pitch_name.ljust(2), 'yellow', attrs=attrs)}")
            elif degree == 0:
                attrs.append('bold')
                s.append(f" {colored(pitch_name.ljust(2), 'cyan', attrs=attrs)}")
            else:
                s.append(f" {colored(pitch_name.ljust(2), 'cyan', attrs=attrs)}")

            # transitions
            if degree in chord.transitions:
                s.append("→ ")
                for transition in chord.transitions[degree]:
                    target_scale, target_pitch, kind = transition
                    if kind == CIRCLE:
                        color = 'light_blue'  # looks purple
                    elif kind == DOM:
                        color = 'light_cyan'
                    elif kind == PULL:
                        color = 'green'
                    elif kind == MORPH:
                        color = 'magenta'
                    target = '(' + key.pitch_names[target_pitch] + ')' if target_pitch != target_scale.root else ""
                    s.append(f"{colored(target_scale.function + ':' + key.pitch_names[target_scale.root] + target, color, attrs=[])} ")

        s.append("\n")
    return "".join(s)
