from django.contrib import admin
from .models import UserSong, AudioData

class AudioDataAdmin(admin.ModelAdmin):
    """Класс настроек для отображения модели TrackData в админке"""
    # prepopulated_fields = {'slug': ('login',)}
    list_display = ('login', 'trek_name', 'original_format', 'date')
    search_fields = ('login', 'date')
    list_filter = ('login', 'original_format', 'convertable_format', 'date')


admin.site.register(UserSong)
admin.site.register(AudioData, AudioDataAdmin)

# Register your models here.
