def error_messages(form) ->dict:
    """ Возвращает список ошибок для пользователя, при загрузке не валидных данных"""

    errors = {}
    for field in form.errors:
        errors[field] = form.errors[field].as_text().replace('* ', '')

    return errors


