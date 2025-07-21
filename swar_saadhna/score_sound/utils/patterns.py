import music21
from music21 import converter, instrument, note, chord, stream


notes = [
    "m_sa",
    "m_re",
    "m_ga",
    "m_ma",
    "m_pa",
    "m_dha",
    "m_ni",
    "h_sa",
]


def generate_sequential_patterns(n):
    pattern = []
    length = len(notes) - 1
    for index, note in enumerate(notes):
        for i in range(n):
            if index + i <= length:
                pattern.append(notes[index + i])
            if index + i == length:
                return pattern + pattern[::-1]


def get_alankaar_composition(ashud_notes, length, input):
    pattern = generate_sequential_patterns(length)
    output = []
    for note in pattern:
        if ashud_notes != []:
            if "re" in ashud_notes and "re" in note:
                output.append(note + "_k")
            elif "ga" in ashud_notes and "ga" in note:
                output.append(note + "_k")
            elif "ma" in ashud_notes and "ma" in note:
                output.append(note + "_t")
            elif "da" in ashud_notes and "da" in note:
                output.append(note + "_k")
            elif "ni" in ashud_notes and "ni" in note:
                output.append(note + "_k")
            else:
                output.append(note + "_s")
        else:
            output.append(note + "_s")

    req_input = {
        "scale": input["scale"],
        "tempo": input["tempo"],
        "rhythm": input["rhythm"],
        "instrument": input["instrument"],
        "sheet_composition": [],
    }

    for note in output:
        req_input["sheet_composition"].append({"notes": [note]})

    return req_input, output


n1 = note.Note("C4")
n2 = note.Note("C3")
n1.quarterLength = 2
# n1.show()

s = stream.Stream()
s.append([n1, n2])
s.write("midi", fp="test.midi")
