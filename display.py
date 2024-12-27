from termcolor import colored


def display(key, chord):
    s = []
    s.append(f"{colored(chord.name.rjust(8), 'white', attrs=['bold'])}\n")
    for degree in (5, 3, 1, 6, 4, 2, 0):

        # analysis labels
        if degree == 0:
            c = chord.labels[degree]
            s.append(f"{c.rjust(8)}")
        else:
            s.append(f"{chord.labels[degree]}".rjust(8))

        # pitches
        pitch_name = key.pitch_names[chord.pitches[degree]]
        attrs = []
        if chord.accidentals[degree]:
            attrs.append('underline')
            if len(pitch_name) < 2:
                pitch_name += '♮'
        if degree in chord.avoid_degrees:
            s.append(f" {colored(pitch_name.ljust(2), 'red', attrs=attrs)}")
        elif degree % 2:
            s.append(f" {colored(pitch_name.ljust(2), 'yellow', attrs=attrs)}")
        elif degree == 0:
            attrs.append('bold')
            s.append(f" {colored(pitch_name.ljust(2), 'cyan', attrs=attrs)}")
        else:
            s.append(f" {colored(pitch_name.ljust(2), 'cyan', attrs=attrs)}")

        # transitions
        if len(chord.leads[degree]):
            s.append("→ ")
            for lead in chord.leads[degree]:
                for ch, (pitch, color) in lead.items():
                    target = '(' + key.pitch_names[pitch] + ')' if pitch != ch.root else ""
                    # s.append(f"{colored(ch.labels[0] + ch.labels[2] + ch.labels[6] + target, color)} ")
                    s.append(f"{colored(ch.labels[0] + ':' + key.pitch_names[ch.root] + ch.labels[2] + ch.labels[4] + ch.labels[6] + target, color, attrs=[])} ")
        s.append("\n")
    return "".join(s)
