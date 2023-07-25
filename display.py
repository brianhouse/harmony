from termcolor import colored


def display(key, chord):
    s = []
    s.append(f"{chord.name.rjust(8)}\n")        
    for degree in (5, 3, 1, 6, 4, 2, 0):

        # analysis labels
        if degree == 0:
            c = chord.labels[degree]
            s.append(f"{c.rjust(8)}")
        else:
            s.append(f"{chord.labels[degree].rjust(8)}")

        # pitches
        pitch_name = key.pitch_names[chord.pitches[degree]]
        if degree in chord.avoid_degrees:
            # s.append(f"<{pitch_name}>".ljust(4))
            s.append(f" {colored(pitch_name, 'red')}".ljust(2))
        elif degree % 2:
            s.append(f" {colored(pitch_name, 'yellow')}".ljust(2))
        elif degree == 0:
            s.append(f" {colored(pitch_name, 'cyan', attrs=['reverse', 'bold']).ljust(2)}")
        else:
            s.append(f" {colored(pitch_name, 'cyan').ljust(2)}")

        # if chord.pitches[degree] not in chords[0].pitches:
        #     s.append("*")

        # transitions
        if len(chord.leads[degree]):
            s.append(f" → ")
            for lead in chord.leads[degree]:
                for ch, (pitch, color) in lead.items():
                    target = '(' + key.pitch_names[pitch] + ')' if pitch != ch.root else ""
                    # s.append(f"{colored(ch.labels[0] + ch.labels[2] + ch.labels[6] + target, color)} ")
                    s.append(f"{colored(ch.labels[0] + ':' + key.pitch_names[ch.root] + ch.labels[2] + ch.labels[6] + target, color)} ")
        s.append("\n")
    return "".join(s)


