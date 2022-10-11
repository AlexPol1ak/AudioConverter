from django.views.decorators.cache import cache_page
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home'), # Домашняя страница
    path('about/', views.about, name='about'), # О нас. Кэш предст. 1 суток.
    path('user/', views.user_account, name='user_account'), # Кабинет пользователя
    path('login/',views.Login.as_view(), name='login'), # Авторизация
    path('registration/', views.RegisterUser.as_view(), name='user_reg'), # Регистрация
    path('userpage/<slug:slug>/', views.UserPage.as_view(),name='user_page'), # Страница пользователя
    path('logout/', views.logout_user, name='logout_user'), # Выход из аккаунта
    path('settings/', views.user_settings, name='settings'), # Страница настроек
    path('password-change/', views.PasswordChange.as_view(), name='password_change'), # Страница изменения пароля
    path('password-change/done/', views.PasswordChangeOk.as_view(), name='password_change_ok'),  # Страница успешного изм пароля. Кеш html 60 сек.
    path('email-change/', views.EmailChange.as_view(), name='email_change'), #  Страница изменения email
    path('email-change/done/', views.email_change_done, name='email_change_ok'), # Страница успш. из. email. Кэш html 60 сек.
    path('delete-page/', views.del_page, name='del_page'), # Удаление данных
    path('page-not-found/', views.error404, name='error404'), # Несуществующая страница. Кэш предст. 1 суток.
    path('footer/', views.footer, name='footer'), # футер. Кэш предст. 1 суток.
    path('audio-delete/', views.del_audio, name='audio_delete') #Удаление трека

]



