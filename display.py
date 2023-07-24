from termcolor import colored
from chord import KEYS, PITCHES_FLAT, PITCHES_SHARP


def get_key(key_string):
    global pitch_names
    pitch_names = PITCHES_FLAT if KEYS.index(key_string) > 6 else PITCHES_SHARP
    key = pitch_names.index(key_string)    
    return key


def display(chord):
    s = []
    # s.append(f"{chord.name.rjust(3)}\n")        
    for degree in (5, 3, 1, 6, 4, 2, 0):

        # analysis labels
        if degree == 0:
            c = chord.name + "-" + chord.labels[degree]
            s.append(f"{c.rjust(8)}")
        else:
            s.append(f"{chord.labels[degree].rjust(8)}")

        # pitches
        pitch_name = pitch_names[chord.pitches[degree]]
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
            s.append(f" -> ")
            for lead in chord.leads[degree]:
                for ch, (pitch, color) in lead.items():
                    # if chords.index(ch) < 8:
                    #     s.append(f"{colored(ch.name + '-' + ch.labels[0] + '(' + pitch_names[pitch] + ')', color, attrs=['underline'])}<{chords.index(ch)}> ")
                    # else:
                    s.append(f"{colored(ch.name + '-' + ch.labels[0] + '(' + pitch_names[pitch] + ')', color)} ")

        s.append("\n")
    return "".join(s)