import os
import re
from .scales import scales


def get_folder_path(intrument_type):
    """
    Get the folder path for the given instrument type.

    Args:
        intrument_type (str): The type of instrument.

    Returns:
        str: The folder path.
    """
    return f"./swar_saadhna/instrument_sounds/{intrument_type}"


def notes_audio_mapping(instrument):
    mapping = {
        1: f"./swar_saadhna/instrument_sounds/{instrument}/1.m4a",
        2: f"./swar_saadhna/instrument_sounds/{instrument}/2.m4a",
        3: f"./swar_saadhna/instrument_sounds/{instrument}/3.m4a",
        4: f"./swar_saadhna/instrument_sounds/{instrument}/4.m4a",
        5: f"./swar_saadhna/instrument_sounds/{instrument}/5.m4a",
        6: f"./swar_saadhna/instrument_sounds/{instrument}/6.m4a",
        7: f"./swar_saadhna/instrument_sounds/{instrument}/7.m4a",
        8: f"./swar_saadhna/instrument_sounds/{instrument}/8.m4a",
        9: f"./swar_saadhna/instrument_sounds/{instrument}/9.m4a",
        10: f"./swar_saadhna/instrument_sounds/{instrument}/10.m4a",
        11: f"./swar_saadhna/instrument_sounds/{instrument}/11.m4a",
        12: f"./swar_saadhna/instrument_sounds/{instrument}/12.m4a",
        13: f"./swar_saadhna/instrument_sounds/{instrument}/13.m4a",
        14: f"./swar_saadhna/instrument_sounds/{instrument}/14.m4a",
        15: f"./swar_saadhna/instrument_sounds/{instrument}/15.m4a",
        16: f"./swar_saadhna/instrument_sounds/{instrument}/16.m4a",
        17: f"./swar_saadhna/instrument_sounds/{instrument}/17.m4a",
        18: f"./swar_saadhna/instrument_sounds/{instrument}/18.m4a",
        19: f"./swar_saadhna/instrument_sounds/{instrument}/19.m4a",
        20: f"./swar_saadhna/instrument_sounds/{instrument}/20.m4a",
        21: f"./swar_saadhna/instrument_sounds/{instrument}/21.m4a",
        22: f"./swar_saadhna/instrument_sounds/{instrument}/22.m4a",
        23: f"./swar_saadhna/instrument_sounds/{instrument}/23.m4a",
        24: f"./swar_saadhna/instrument_sounds/{instrument}/24.m4a",
        25: f"./swar_saadhna/instrument_sounds/{instrument}/25.m4a",
        26: f"./swar_saadhna/instrument_sounds/{instrument}/26.m4a",
        27: f"./swar_saadhna/instrument_sounds/{instrument}/27.m4a",
        28: f"./swar_saadhna/instrument_sounds/{instrument}/28.m4a",
        29: f"./swar_saadhna/instrument_sounds/{instrument}/29.m4a",
        30: f"./swar_saadhna/instrument_sounds/{instrument}/30.m4a",
        31: f"./swar_saadhna/instrument_sounds/{instrument}/31.m4a",
        32: f"./swar_saadhna/instrument_sounds/{instrument}/32.m4a",
        33: f"./swar_saadhna/instrument_sounds/{instrument}/33.m4a",
        34: f"./swar_saadhna/instrument_sounds/{instrument}/34.m4a",
        35: f"./swar_saadhna/instrument_sounds/{instrument}/35.m4a",
        36: f"./swar_saadhna/instrument_sounds/{instrument}/36.m4a",
    }
    return mapping


notes = [
    "l_sa_s",
    "l_re_k",
    "l_re_s",
    "l_ga_k",
    "l_ga_s",
    "l_ma_s",
    "l_ma_t",
    "l_pa_s",
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
    "h_da_k",
    "h_da_s",
    "h_ni_k",
    "h_ni_s",
]


def get_audios_for_intruments(intrument, scale):
    mapping = {}
    print(scales)
    notes_mapping = notes_audio_mapping(intrument)
    for note in notes:
        if scales[scale][note] is not None:
            mapping[note] = notes_mapping[scales[scale][note]]
        else:
            mapping[note] = None

    return mapping


def get_audios_for_rhythm(rhythm):
    mapping = {}
    folder_path = get_folder_path(rhythm)
    files = sorted(os.listdir(folder_path), key=lambda x: int(re.findall(r"\d+", x)[0]))
    for filename in files:
        mapping[filename.split("/")[-1].split(".")[0]] = (
            f"./swar_saadhna/instrument_sounds/{rhythm}/{filename}"
        )
    return mapping
