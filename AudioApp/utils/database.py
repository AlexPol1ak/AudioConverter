from ..models import AudioData
import os

def write_database(data_dict : dict) ->bool :
    """Сохраняет данные о треке в базу данных"""

    login :str = data_dict.get('user_name', '')
    trek_name :str = data_dict.get('trek_name', '')
    original_format  :str = data_dict.get('original_format', '')
    original_track :str = os.path.relpath(data_dict.get('path_original', ''), 'AudioApp\static')
    convertable_track :str = os.path.relpath(data_dict.get('path_convert', ''), 'AudioApp\static')
    convertable_format :str= data_dict.get('format', '')
    # Дата и время конвретации формируется в модели автоматически.
    # date = data_dict.get('date', '')

    try:
        database :AudioData = AudioData(login=login, trek_name=trek_name, original_format=original_format,
                          original_track=original_track, convertable_track=convertable_track,
                          convertable_format=convertable_format ) #date=date
        database.save()
    except:
        raise Exception('Error writing to database')
    return True