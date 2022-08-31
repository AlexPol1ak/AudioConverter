from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home'), # Домашняя страница
    path('user/', views.user_account, name='user_account'), # Кабинет пользователя
    path('login/',views.Login.as_view(), name='login'), # Авторизация
    path('registration', views.RegisterUser.as_view(), name='user_reg'), # Регистрация
    path('about/', views.about, name='about'), # О нас
    path('settings/', views.user_settings, name='settings'), # Страница удаления аккаунта
    path('userpage/<slug:slug>/', views.UserPage.as_view(),name='user_page'), # Страница пользователя
    path('logout/', views.logout_user, name='logout_user'), # Выход из аккаунта
    path('password-change/', views.PasswordChange.as_view(), name='password_change'),
    path('password-change/done/', views.PasswordChangeOk.as_view(), name='password_change_ok'),

]

