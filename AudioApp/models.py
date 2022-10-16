import os

from django.contrib.auth.models import User
from django.db import models
from django.http import FileResponse
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
    audio_name = models.CharField(max_length=100, verbose_name='Имя трека')
    original_format = models.CharField(max_length=100, verbose_name='Формат оригинала')
    original_path = models.CharField(max_length=100, verbose_name='Оригинальный трек')
    convert_path = models.CharField(max_length=100, verbose_name='Сконвертированный трек')
    convert_format = models.CharField(max_length=100, verbose_name='Формат сконвертированного трека')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата конвертации')
    original_audio_size_b = models.IntegerField(verbose_name="Оригинальный трек. B")
    original_audio_size_mb = models.FloatField(verbose_name="Оригинальный трек. Mb")
    convert_audio_size_b = models.IntegerField(verbose_name="Сконвертированный трек. b")
    convert_audio_size_mb = models.FloatField(verbose_name="Сконвертированный трек Mb")
    deleted = models.BooleanField(default=False, verbose_name="Удален")



    def __str__(self):
        return str(self.login)

    def get_absolute_url(self):
        """Возвращает url пользователя"""
        return reverse('user_page', kwargs={'slug': self.login})

    class Meta:
        """Настройки модели"""
        verbose_name = 'Трек пользователя'
        verbose_name_plural = 'Треки пользователя'
        ordering = ['date',]

    def audiofile_name(self)->str:
        """Возвращает имя аудиофайла."""
        if self.audio_name:
            return str(self.audio_name)

    def orig_audio_format(self)->str:
        """Возвращает формат оригинального аудиофайла."""
        if self.original_format:
            return str(self.original_format)

    def orig_audio_fullname(self)->str:
        """Возвращает имя и формат оригинального аудиофайла."""
        if self.original_path:
            return f"{self.audio_name}.{self.original_format}"

    def convert_audio_format(self)->str:
        """Возвращает имя конвертированного аудиофайла."""
        if self.convert_format:
            return str(self.convert_format)

    def convert_audio_fullname(self)->str:
        """Возвращает имя и формат конвертированного аудиофайла."""
        if self.convert_path:
            return f"{self.audio_name}.{self.convert_format}"

    def orig_audio_path(self)->str:
        """Возвращает абсолютный путь к оригинальному аудиофайлу."""
        if self.original_path:
            return os.path.normpath(str(self.original_path))

    def convert_audio_path(self)->str:
        """Возвращает абсолютный путь к конвертированному аудиофайлу."""
        if self.convert_path:
            return os.path.normpath(str(self.convert_path))

    def orig_aduio_relpath(self) -> str:
        """Возвращает относительную ссылку на оригинальный аудиофайл."""
        # Возвращает путь относительно media\original_tracks. <<< Guest\testsong1.mp3
        if self.original_path:
            audio_path :str = self.orig_audio_path()
            audio_path :str = audio_path[audio_path.rfind('original_tracks'): ]
            return audio_path

    def convert_aduio_relpath(self) -> str:
        """Возвращает относительную ссылку на конвертированный аудиофайл."""
        # Возвращает путь относительно media\convertible_tracks. <<< Guest\testsong1.ac3
        if self.original_path:
            audio_path :str = self.convert_audio_path()
            audio_path :str = audio_path[audio_path.rfind('convertible_tracks'): ]
            return audio_path

    def orig_size_mb(self)->float:
        """Возвращает размер оригинального аудифоайла в мегабайтах."""
        if self.original_audio_size_mb:
            return float(str(self.original_audio_size_mb))

    def convert_size_mb(self)->float:
        """Возвращает размер конвертированного аудиофайла в мегабайтах."""
        if self.convert_audio_size_mb:
            return float(str(self.convert_audio_size_mb))

    def convert_date(self):
        """Возвращает дату и время конвертации."""
        # return self.date
        return str(self.date)

