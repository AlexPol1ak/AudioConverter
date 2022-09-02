from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class UserSong(models.Model):
    """Модель для загрузки трека"""
    title = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='audio_files/')

    def __str__(self):
        return str(self.audio_file) + str(self.title)


class AudioData(models.Model):
    """База данных для хранения данных о треках"""
    login = models.CharField(max_length=100, verbose_name='Имя пользователя')
    # slug = models.SlugField(max_length=100, db_index=True, verbose_name='URL')
    trek_name = models.CharField(max_length=100, verbose_name='Имя трека')
    original_format = models.CharField(max_length=100, verbose_name='Формат оригинала')
    original_track = models.CharField(max_length=100, verbose_name='Оригинальный трек')
    convertable_track = models.CharField(max_length=100, verbose_name='Сконвертированный трек')
    convertable_format = models.CharField(max_length=100, verbose_name='Формат сконвертированного трека')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата конвертации')

    def __str__(self):
        return str(self.login)

    def get_absolute_url(self):
        """Возвращает url пользователя"""
        return reverse('user_page', kwargs={'slug': self.login})

    class Meta:
        """Настройки модели"""
        verbose_name = 'Трек пользователя'
        verbose_name_plural = 'Треки пользователя'
        ordering = ['date']

    def get_convertable(self):
        """Возвращет относительный путь к сконвертированному треку."""

        # Для отображения путей к трекам в личном кабинете с тегом static
        if self.convertable_track:
            audio = str(self.convertable_track) # << AudioApp/static//convertible_tracks/____.___
            path = audio[audio.rfind('convertible_tracks'):] # << convertible_tracks/_____.___

            return path
        else:
            return None

    def get_trek_name(self):
        """Возвращает имя сконвертированного трека."""

        if self.trek_name and self.convertable_format:
            name :str = f"{str(self.trek_name)}.{str(self.convertable_format)}"
            return name

        else:
            return None

    def get_trek_format(self):
        """возвращает формат трека."""
        if self.convertable_format:
            frmt = str(self.convertable_format).lower()
            return frmt

        else:
            return None