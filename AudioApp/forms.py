import os

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from captcha.fields import CaptchaField

from AudioApp.models import UserSong
from .audiohandler.audio import AudioConverter


class UploadFileForm(forms.ModelForm, forms.Form):
    """Форма загрузки файла"""

    converter_formats: list = AudioConverter.available_formats()
    formats_tuple: tuple = tuple(zip(tuple(converter_formats), tuple(converter_formats)))

    format: forms.Form = forms.ChoiceField(choices=formats_tuple)

    captcha = CaptchaField()

    def clean_audio_file(self):
        """Проверка файла"""

        file = self.cleaned_data.get('audio_file', False)

        if file:
            if file.size > 50 * 1024 * 1024:
                raise ValidationError("Аудиофайл слишком большой ( > 50mb )")

            if not os.path.splitext(file.name)[1] in ['.'+i for i in UploadFileForm.converter_formats]:
                raise ValidationError("Недопустимое расширение.")

            return file
        else:
            raise ValidationError("Не удалось прочитать загруженный файл.")

    class Meta:
        model = UserSong
        fields = ['audio_file']


    def show_formats(self):
        """Возвращает строку доступных форматов."""
        formats =", ".join(UploadFileForm.converter_formats)
        formats += "."

        return formats



class RegisterUserForm(UserCreationForm):
    """Форма регистрации пользователя."""

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Ваше имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']


class LoginUserForm(AuthenticationForm):
    """Форма авторизации пользователя."""

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class InputPasswordForm(forms.Form):
    """Представление для ввода пароля при подтверждений действий."""

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, user= None, data=None):
        self.user = user
        super().__init__(data=data)

    def clean_password(self):
        """Проверка пароля"""

        valid = self.user.check_password(self.cleaned_data['password'])
        if not valid:
            raise forms.ValidationError("Password Incorrect")
        return valid





