from termcolor import colored
from constants import *


def display(key, scale):

    s = []
    s.append(f"{colored(scale.function + " " + scale.mode_name.rjust(0), 'white', attrs=['bold'])}")
    s.append(f" (V/{scale.dominant.function})" if scale.dominant is not None else "")
    s.append(f" (II/{scale.related_ii.function})" if scale.related_ii is not None else "")
    s.append("\n")
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
            pitch_name = scale.pitch_names[scale.pitches[degree]]
            attrs = []
            if scale.accidentals[degree]:
                attrs.append('underline')
                if len(pitch_name) < 2:
                    pitch_name += '♮'
            if degree in chord.avoid_degrees:
                s.append(f" {colored(pitch_name.ljust(2), 'red', attrs=attrs)}")
                # s.append(f" {colored("  ", 'red', attrs=attrs)}")
            elif degree not in chord_type or degree == 4 and chord.hide_dominant:
                s.append(f" {colored(pitch_name.ljust(2), 'light_yellow', attrs=attrs)}")
            elif degree == 0:
                attrs.append('bold')
                s.append(f" {colored(pitch_name.ljust(2), 'light_cyan', attrs=attrs)}")
            else:
                s.append(f" {colored(pitch_name.ljust(2), 'light_cyan', attrs=attrs)}")

        # transitions
        if degree in scale.transitions:
            if len(scale.transitions[degree]):
                s.append(f" {colored("  → ", 'grey', attrs=attrs)}")
            for transition in scale.transitions[degree]:
                target_scale, target_pitch, kind = transition
                strength = scale.strengths[target_scale]
                if kind == CIRCLE:
                    color = 'magenta'
                elif kind == DOM:
                    color = 'green'
                elif kind == PULL:
                    color = 'cyan'
                elif kind == MORPH:
                    color = 'light_blue'   # looks purple
                target = '(' + scale.pitch_names[target_pitch] + ')' if target_pitch != target_scale.root else ""
                # print("scale", scale.root, "target_scale.root", target_scale.root)
                s.append(f"{colored(target_scale.function + ':' + target_scale.mode_name + ':' + scale.pitch_names[target_scale.root] + target + ((strength - 1) * "*"), color, attrs=[])} ")

        s.append("\n")
    return "".join(s)
