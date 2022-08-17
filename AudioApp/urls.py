from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='home'),
    path('user/', views.user_account, name='user_account'),
    path('login/',views.login, name='login'),
    path('registration', views.RegisterUser.as_view(), name='user_reg'),
    path('about/', views.about, name='about'),
    path('deletion/', views.deletion_page, name='deletion_page'),
    path('userpage/', views.user_page, name='user_page'),
]
