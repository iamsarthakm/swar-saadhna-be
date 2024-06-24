import random

# split the array so that higher notes doesn't get combined with the lower ones
notes = [
    "l_da_k",
    "l_da_s",
    "l_ni_k",
    "l_ni_s",
    "m_sa_s",
    "m_re_k",
    "m_re_s",
    "m_ga_k",
    "m_ga_s",
    "m_ma_s",
    "m_ma_t",
    "m_pa_s",
    "m_da_k",
    "m_da_s",
    "m_ni_k",
    "m_ni_s",
    "h_sa_s",
    "h_re_k",
    "h_re_s",
    "h_ga_k",
    "h_ga_s",
    "h_ma_s",
    "h_ma_t",
    "h_pa_s",
]

freq_patterns = [
    ["m_re_k", "m_sa_s", "m_re_k", "m_re_k", "m_sa_s"],
    ["m_ga_s", "m_ma_s", "m_da_k"],
    ["l_ni_s", "m_re_k", "m_sa_s"],
    ["m_ga_s", "m_ma_s", "m_re_k", "m_sa_s"],
    ["m_ma_s", "m_ga_s", "m_re_k", "m_sa_s"],
    ["m_ga_s", "m_ma_s", "m_pa_s", "m_ma_s"],
    ["m_ga_s", "m_ma_s", "m_re_k", "m_sa_s", "m_ga_s", "m_ma_s", "m_pa_s", "m_ma_s"],
    ["m_ma_s", "m_ga_s", "m_re_k", "m_sa_s", "m_ga_s", "m_ma_s", "m_pa_s", "m_ma_s"],
]

most_frequent = ["m_da_k", "l_da_k"]
second_most_frequent = ["m_re_k"]
prohibited = [
    "m_re_s",
    "h_re_s",
    "m_da_s",
    "l_da_s",
    "h_ma_t",
    "h_ga_k",
    "m_ga_k",
    "m_ma_t",
    "l_ni_k",
    "m_ni_k",
]


def create_random_composition(input):
    raag_notes = list(set(notes) - set(prohibited))
    frequent_strings = [",".join(subarray) for subarray in freq_patterns]

    notes_weight = {}

    for fs in frequent_strings:
        notes_weight[fs] = 0.5 / len(frequent_strings)

    for fs in most_frequent:
        notes_weight[fs] = 0.15 / len(most_frequent)

    for fs in second_most_frequent:
        notes_weight[fs] = 0.05 / len(second_most_frequent)

    raag_notes_left = list(
        set(raag_notes) - set(most_frequent) - set(second_most_frequent)
    )
    for note in raag_notes_left:
        notes_weight[note] = 0.3 / len(raag_notes_left)

    choices = list(notes_weight.keys())
    weights = list(notes_weight.values())

    pattern = random.choices(choices, weights, k=30)
    output_composition = []
    out_of_place = []
    for note_pat in pattern:
        if "," in note_pat:
            output_composition.extend(note_pat.split(","))
        else:
            if abs(notes.index(note_pat) - notes.index(output_composition[-1])) > 4:
                out_of_place.append(notes.index(note_pat))
                continue
            output_composition.append(note_pat)

    req_input = {
        "scale": input["scale"],
        "tempo": input["tempo"],
        "rhythm": input["rhythm"],
        "instrument": input["instrument"],
        "sheet_composition": [],
    }

    for note in output_composition:
        req_input["sheet_composition"].append({"notes": [note]})

    return req_input, output_composition
