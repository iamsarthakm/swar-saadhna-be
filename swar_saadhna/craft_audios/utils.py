from swar_saadhna.utils.instrument_scale import create_audio_dict
import os
from pydub import AudioSegment
import pydub.effects as effects

AudioSegment.converter = "/Users/sarthakmaheshwari/opt/anaconda3/condabin/ffmpeg"
AudioSegment.ffmpeg = "/Users/sarthakmaheshwari/opt/anaconda3/condabin/ffmpeg"
AudioSegment.ffprobe ="/Users/sarthakmaheshwari/opt/anaconda3/condabin/ffprobe"


def create_audio_using_notations(notes, intrument="harmonium", scale="C#"):
    """
    Create an audio file using the provided notations for a specific instrument and scale.
    
    Args:
        intrument (str): The type of instrument.
        scale (str): The desired scale.
    """
    audio_mappings = create_audio_dict(intrument,scale)
    notes = ['m_ga_s','m_ma_s', 'm_da_k', 'm_da_k', 'm_pa_s', '', 'm_da_k' ,'m_ma_s', 'm_pa_s', 'm_pa_s', 'm_pa_s', 'm_da_k','m_ma_s','m_da_k','m_ma_s','m_ga_s']

    combined = None
    for note in notes:
        if note in audio_mappings:
            audio_file = audio_mappings[note]
        else:
            audio_file = None
        audio = get_formatted_audio(audio_file, 120)
        if combined is None:
            combined = audio
        else:
            combined += audio
    combined.export("louder_and_quieter.wav", format="wav")


def get_formatted_audio(audio_file, bpm=60):
    """
    Get the formatted audio based on the provided audio file and BPM (beats per minute).

    Args:
        audio_file (str): The path to the audio file.
        bpm (int): The desired BPM.
        
    Returns:
        pydub.AudioSegment: The formatted audio segment.
    """
    target_duration = (60/bpm) * 1000
    fade_duration = int((40/100) * target_duration)

    if audio_file == None:
        return AudioSegment.silent(duration=target_duration)

    audio = AudioSegment.from_file(audio_file, format="m4a") 

    # in here we can get a 5 sec audio clip and trim it down for audios, to be done later
    if bpm == 15:
        audio = (audio.fade_in(400).fade_out(200))*4
    elif bpm == 30:
        audio = (audio.fade_in(200).fade_out(100))*2
    elif bpm == 60:
        audio = audio
    elif bpm == 120:
        audio = audio[0:500]
    elif bpm == 180:
        audio = audio[0:333]
    elif bpm == 240:
        audio = audio[0:250]
    # this part to be redone
        
    duration_difference = target_duration - len(audio)
    audio = audio + AudioSegment.silent(duration=duration_difference)
    audio = audio.fade_in(fade_duration).fade_out(fade_duration)
    # audio = effects.normalize(audio)
    # audio = match_target_amplitude(audio, -20.0)
    return audio


def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)