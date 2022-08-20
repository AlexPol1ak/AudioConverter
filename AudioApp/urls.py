from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='home'), # Домашняя страница
    path('user/', views.user_account, name='user_account'), # Кабинет пользователя
    path('login/',views.Login.as_view(), name='login'), # Авторизация
    path('registration', views.RegisterUser.as_view(), name='user_reg'), # Регистрация
    path('about/', views.about, name='about'), # О нас
    path('deletion/', views.deletion_page, name='deletion_page'), # Страница удаления аккаунта
    path('userpage/', views.user_page, name='user_page'), # Страница пользователя
    path('logout/', views.logout_user, name='logout_user'), # Выход из аккаунта
]
