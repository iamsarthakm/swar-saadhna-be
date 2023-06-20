import os
import re


# first there is ocatve, then note, then its variable such as shudh, komal or teevra
# if lower-l , middle-m, higher-h
# sa , re, ga, ma, pa, dha, ni , sa
# shudh-> -s, komal -k, teevra-t
path = "./swar_saadhna/instrument_sounds/harmonium/"
reference_mapping = {
    1: 'l_sa_s',
    2: 'l_re_k',
    3: 'l_re_s', 
    4: 'l_ga_k', 
    5: 'l_ga_s', 
    6: 'l_ma_s', 
    7: 'l_ma_t', 
    8: 'l_pa_s', 
    9: 'l_da_k', 
    10: 'l_da_s', 
    11: 'l_ni_k', 
    12: 'l_ni_s', 
    13: 'm_sa_s', 
    14: 'm_re_k', 
    15: 'm_re_s', 
    16: 'm_ga_k', 
    17: 'm_ga_s', 
    18: 'm_ma_s', 
    19: 'm_ma_t', 
    20: 'm_pa_s', 
    21: 'm_da_k', 
    22: 'm_da_s', 
    23: 'm_ni_k', 
    24: 'm_ni_s', 
    25: 'h_sa_s', 
    26: 'h_re_k', 
    27: 'h_re_s', 
    28: 'h_ga_k', 
    29: 'h_ga_s', 
    30: 'h_ma_s', 
    31: 'h_ma_t', 
    32: 'h_pa_s', 
    33: 'h_da_k', 
    34: 'h_da_s', 
    35: 'h_ni_k', 
    36: 'h_ni_s'
    }
notes_array = ['m_ga_s','m_ma_s', 'm_da_k', '', 'm_pa_s', '', 'm_da_k' ,'m_ma_s', 'm_pa_s', '', '', 'm_da_k','m_ma_s','m_da_k','m_ma_s','m_ga_s']


def create_audio_dict(intrument_type, scale):
    """
    Create a dictionary mapping note names to audio file paths based on the given instrument type and scale.
    Args:
        intrument_type (str): The type of instrument.
        scale (str): The desired scale.
    Returns:
        dict: A dictionary mapping note names to audio file paths.
    """
    audio_dict = {}
    folder_path = get_folder_path(intrument_type)
    files = sorted(os.listdir(folder_path), key=lambda x: int(re.findall(r'\d+', x)[0]))
    for filename in files:
        name = int(os.path.splitext(filename)[0])
        audio_file = os.path.join(folder_path, filename)
        adjust_scale = get_scale_adjusting_value(scale)
        if name + adjust_scale>=1 and name+adjust_scale <=36:
            audio_dict[reference_mapping[name+adjust_scale]] = audio_file

    return audio_dict

def get_scale_adjusting_value(scale):
    """
    Get the scale adjusting value based on the given scale.
    
    Args:
        scale (str): The desired scale.
        
    Returns:
        int: The scale adjusting value.
    """
    if scale == "D#":
        return -2
    elif scale == "D":
        return -1
    elif scale == 'C#':
        return 0
    elif scale == "C":
        return 1
    elif scale == "B":
        return 2
    elif scale == "A#":
        return 3
    elif scale == "A":
        return 4
    elif scale == "G#":
        return 5
    elif scale == "G":
        return 6
    elif scale == "F#":
        return 7

def get_folder_path(intrument_type):
    """
    Get the folder path for the given instrument type.
    
    Args:
        intrument_type (str): The type of instrument.
        
    Returns:
        str: The folder path.
    """
    return f"./swar_saadhna/instrument_sounds/{intrument_type}"