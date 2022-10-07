from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.views.static import serve as mediaserve
# from django.conf.urls import url
from django.urls import re_path as url

from AudioConverter import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha', include('captcha.urls')),
    path('', include('AudioApp.urls'))
]

handler404 = "AudioApp.views.error404"


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATICFILES_DIRS)  # Загрузка файлов на локальном сервере

else:
    urlpatterns += [
        url(f'^{settings.MEDIA_URL.lstrip("/")}(?P<path>.*)$',
            mediaserve, {'document_root': settings.MEDIA_ROOT}),
        url(f'^{settings.STATIC_URL.lstrip("/")}(?P<path>.*)$',
            mediaserve, {'document_root': settings.STATIC_ROOT})
    ]



