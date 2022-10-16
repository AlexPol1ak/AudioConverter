from ..models import AudioData
import os


def write_database(data_dict : dict) ->bool :
    """Сохраняет данные о треке в базу данных"""

    login :str = data_dict.get('user_name', '')
    audio_name :str = data_dict.get('audio_name', '')
    original_format  :str = data_dict.get('original_format', '')
    original_path :str = data_dict.get('path_original', '')
    convert_path :str = data_dict.get('path_convert', '')
    convert_format :str= data_dict.get('format', '')
    original_audio_size_b :int = data_dict.get('original_size_b', 0)
    original_audio_size_mb :int = data_dict.get('original_size_mb', 0)
    convert_audio_size_b :int = data_dict.get('convert_size_b', 0)
    convert_audio_size_mb :int = data_dict.get('convert_size_mb', 0)
    # Дата и время конвретации формируется в модели автоматически.
    # date = data_dict.get('date', '')

    try:
        database :AudioData = AudioData(login=login, audio_name=audio_name, original_format=original_format,
                                        original_path=original_path, convert_path=convert_path,
                                        convert_format=convert_format, original_audio_size_b=original_audio_size_b,
                                        original_audio_size_mb=original_audio_size_mb,
                                        convert_audio_size_b=convert_audio_size_b,
                                        convert_audio_size_mb=convert_audio_size_mb)
        #date=date
        database.save()
    except:
        raise Exception('Error writing to database')
    return True