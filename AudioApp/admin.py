from django.contrib import admin
from .models import UserSong, AudioData

class AudioDataAdmin(admin.ModelAdmin):
    """Класс настроек для отображения модели TrackData в админке"""
    # prepopulated_fields = {'slug': ('login',)}
    list_display = ('login', 'audio_name', 'original_format','original_audio_size_mb', 'convert_audio_size_mb', 'deleted' ,'date', )
    list_editable = ('deleted',)
    search_fields = ('login', 'date')
    list_filter = ('login', 'deleted', 'original_format', 'convert_format', 'date',)
    readonly_fields = ('convert_audio_size_b', 'original_audio_size_b', 'original_audio_size_mb', 'convert_audio_size_mb')


admin.site.register(UserSong)
admin.site.register(AudioData, AudioDataAdmin)

# Register your models here.
