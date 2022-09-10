from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from AudioConverter import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha', include('captcha.urls')),
    path('', include('AudioApp.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)  # Загрузка файлов на локальном сервере

# Загрузка медиа файлов на локальном сервере .
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
