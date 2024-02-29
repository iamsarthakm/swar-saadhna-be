from pydub import AudioSegment
from swar_saadhna.utils.instrument_scale import (
    get_audios_for_intruments,
    get_audios_for_rhythm,
)


def generate_audios(params):
    intrument = params["intrument"]
    scale = params["scale"]
    rhythm = params["rhythm"]
    tempo = params["tempo"]
    composition = params["sheet_composition"]

    intrument_audio = get_audios_for_intruments(intrument, scale)
    rhythm_audios = get_audios_for_rhythm(rhythm)

    composition_audio = get_audio_composition(
        tempo, intrument_audio, rhythm_audios, composition
    )
    composition_audio.export("composition.wav", format="wav")
    return "audio"


# considering file is 2 sec long
def get_audio_composition(tempo, intrument_audios, rhythm_audios, composition):
    output_composition = None
    for sounds in composition:
        rhythm_audio = None
        if "rhythm" in sounds:
            rhythm_audio = get_formatted_audio_note(
                rhythm_audios[sounds["rhythm"]], tempo, "mp3"
            )

        note_audio = None
        if "notes" in sounds:
            bpm = tempo * len(sounds["notes"])
            for note in sounds["notes"]:
                if note == "":
                    note_audio_file = None
                else:
                    note_audio_file = intrument_audios[note]
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
    print(audio_file)
    audio = AudioSegment.from_file(audio_file, format=format)

    bps = 60 / bpm
    duration = int(bps * 1000)
    audio = audio[0:duration]

    duration_difference = target_duration - len(audio)
    audio = audio + AudioSegment.silent(duration=duration_difference)
    audio = audio.fade_in(fade_duration).fade_out(fade_duration)

    return audio
