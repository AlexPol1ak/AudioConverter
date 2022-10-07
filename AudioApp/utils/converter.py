from AudioConverter.settings import STATICFILES_DIRS, MEDIA_ROOT
from ..audiohandler.audio import AudioConverter

# Создаем объект конвертора, который будет отвечать за конвертацию аудиофайлов. Передаем настройки

settings = {
        'move': True, # Перемещать (не копировать) файлы в папку конвертированных
        'write_db': False, # Использовать стандартную базу данных конвертора
        'db_path': '', # Путь к стандартной базе данных конвертора
        'storage_path': f'{MEDIA_ROOT}', # Путь, где будут храниться конвертированные файлы
        }

#object converter
converter = AudioConverter(setting_dict=settings)






