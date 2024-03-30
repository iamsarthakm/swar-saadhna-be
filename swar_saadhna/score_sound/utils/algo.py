from .static import scales, notes
import os
import re
from pydub import AudioSegment


def get_scale_note_number_mapping(scale):
    out = {}
    skip = 8 - scales.index(scale)

    counter = 1
    length = len(notes)
    c_length = 0
    for index, note in enumerate(notes):
        if skip >= 0:
            if index < skip:
                out[note] = None

            else:
                out[note] = counter
                counter += 1
        else:
            if index <= length and c_length < length:
                c_length = counter - skip
                out[note] = counter - skip
                counter += 1
            else:
                out[note] = None

    return out


def notes_audio_mapping(instrument):
    out = {}
    for i in range(1, 37):
        out[i] = f"./score_sound/media/{instrument}/{i}.m4a"
    return out


def get_audios_for_rhythm(beat):
    mapping = {}
    folder_path = f"./score_sound/media/{beat}/"
    files = sorted(os.listdir(folder_path), key=lambda x: int(re.findall(r"\d+", x)[0]))
    for filename in files:
        mapping[filename.split("/")[-1].split(".")[0]] = (
            f"./score_sound/media/{beat}/{filename}"
        )
    return mapping


def get_scale_audios_for_instruments(instrument, scale):
    mapping = {}
    notes_no = get_scale_note_number_mapping(scale)
    no_audios = notes_audio_mapping(instrument)
    for note in notes:
        if notes_no[note] is not None:
            mapping[note] = no_audios[notes_no[note]]
        else:
            mapping[note] = None

    return mapping


# considering file is 2 sec long
def get_audio_composition(tempo, instrument_audios, rhythm_audios, composition):
    output_composition = None
    for sounds in composition:
        rhythm_audio = None
        if "beat_name" in sounds:
            if rhythm_audios.get(sounds["beat_name"], None):
                rhythm_audio = get_formatted_audio_note(
                    rhythm_audios.get(sounds["beat_name"], None), tempo, "mp3"
                )

        note_audio = None
        if "notes" in sounds:
            bpm = tempo * len(sounds["notes"])
            for note in sounds["notes"]:
                if note == "":
                    note_audio_file = None
                else:
                    note_audio_file = instrument_audios.get(note, None)
                if note_audio is None:
                    note_audio = get_formatted_audio_note(note_audio_file, bpm)
                else:
                    note_audio += get_formatted_audio_note(note_audio_file, bpm)

        if not note_audio:
            continue

        if rhythm_audio is None and note_audio:
            final_audio = note_audio

        if rhythm_audio and note_audio:
            final_audio = note_audio.overlay(rhythm_audio, position=0)

        if output_composition is None:
            output_composition = final_audio
        else:
            output_composition += final_audio

    return output_composition


def get_formatted_audio_note(audio_file, bpm, format="m4a"):

    target_duration = (60 / bpm) * 1000
    fade_duration = int((1 / 100) * target_duration)

    if audio_file is None:
        return AudioSegment.silent(duration=target_duration)
    audio = AudioSegment.from_file(audio_file, format=format)

    bps = 60 / bpm
    duration = int(bps * 1000)
    audio = audio[0:duration]

    duration_difference = target_duration - len(audio)
    audio = audio + AudioSegment.silent(duration=duration_difference)
    audio = audio.fade_in(fade_duration).fade_out(fade_duration)

    return audio


def generate_audios_algo(scale, tempo, instrument, rhythm, composition):

    instrument_audio = get_scale_audios_for_instruments(instrument, scale)
    rhythm_audios = get_audios_for_rhythm(rhythm)

    composition_audio = get_audio_composition(
        tempo, instrument_audio, rhythm_audios, composition
    )
    composition_audio.export("composition.wav", format="wav")
    return "audio"
