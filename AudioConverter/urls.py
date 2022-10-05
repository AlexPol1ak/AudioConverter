from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from AudioConverter import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha', include('captcha.urls')),
    path('', include('AudioApp.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)  # Загрузка файлов на локальном сервере

handler404 = "AudioApp.views.error404"

# Загрузка медиа файлов на локальном сервере .
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns



