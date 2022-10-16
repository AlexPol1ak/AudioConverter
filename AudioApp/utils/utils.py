import os

from django.http import FileResponse


def error_messages(form) ->dict:
    """ Возвращает список ошибок для пользователя, при загрузке не валидных данных"""

    errors = {}
    for field in form.errors:
        errors[field] = form.errors[field].as_text().replace('* ', '')

    return errors

def download_audio(audio_path :str) -> FileResponse:
    """ Возвращает объект-аудиофайл в двоичном формате готовый для скачивания пользвателем. """

    response = FileResponse(open(audio_path, 'rb'))
    response['content_type'] = "application/octet-stream"
    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(audio_path)

    return response


