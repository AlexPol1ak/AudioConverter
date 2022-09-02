from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse
# from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView
from rest_framework.generics import get_object_or_404

from .forms import UploadFileForm, RegisterUserForm, LoginUserForm, InputPasswordForm
from .models import AudioData
from .utils.database import write_database
from .utils.converter import converter



def home_page(request):
    """Представление для домашней страницы."""

    if request.method !='POST':
        form = UploadFileForm()
        context = {'form': form}

    else:
        # Если пользватель зарегистирован ,получаем его имя и логин
        if request.user.is_authenticated:
            login :str = request.user.username
            name :str = request.user.first_name
        # Если нет, инициализируем его как гостя
        else:
            login = 'Guest'
            name = None
        # Получаем данные из формы
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

        # Получаем имя файла и выбраный пользвателем формат конвертации
        text :str = str(form.files['audio_file']).replace(' ', '_')
        frmt :str = request.POST.get('format')

        # Конвертирование аудиофайла и сохранение информации о нем в базу данных
        try:
            trek_dict: dict = converter.convert(f'AudioApp/media/audio_files/{text}', frmt=frmt, name=login)
            flag: bool = write_database(trek_dict)
        except:
            return render(request, 'AudioApp/conversion_error.html')

        # Информация о конвертированном файле для контекста
        trek_name: str = trek_dict['trek_name']
        trek_format: str = trek_dict['format']
        audio: str = trek_dict['path_convert'].replace('AudioApp/static/', '')

        # формируем контекст для представления
        context = {'form': form, # форма загрузки файла
                    'trek_name': trek_name, # имя сконвертированного файла
                    'format': trek_format, # формат сконвертированного файла
                    'audio': audio, # путь к сконвертированному файлу
                    'name': name # имя пользователя
                    }

    return render(request, 'AudioApp/home.html',context=context)



def user_account(request):
    """Представление для личного кабинета пользователя"""

    if request.user.is_authenticated:
        return redirect(reverse('user_page',kwargs={'slug': request.user.username.lower()}))
        # return redirect('user_page')
    else:
        return render(request, 'AudioApp/guest.html')



class RegisterUser(CreateView):
    """Представление для регистрации пользователя."""
    form_class = RegisterUserForm
    template_name = 'AudioApp/registration.html'
    success_url = reverse_lazy('user_account')
    raise_exception = True


    def get_context_data(self, *, object_list=None, **kwargs):
        """Формирует динамический контекст"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        """Авторизовывает при успешной регистрации."""
        user = form.save()
        login(self.request, user)
        return redirect('user_account')



def about(request):
    return render(request, 'AudioApp/about.html',context={'title': 'О нас'})

class Login(LoginView):
    """Представление для авторизации пользователя."""
    form_class= LoginUserForm
    template_name = 'AudioApp/login.html'
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        """Формирует динамический контекст."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'

        return context

    def get_success_url(self):
        """Перенаправление пользователя на страницу профиля."""
        return reverse('user_account')


def logout_user(request):
    """Осуществляет выход пользователя из своей учетной записи"""
    logout(request)
    return redirect('home')



class UserPage(LoginRequiredMixin, ListView,):
    """Представление для страницы пользователя"""

    model = AudioData
    # paginate_by = 5
    template_name = 'AudioApp/userpage.html'
    context_object_name = 'userdata'
    allow_empty = True

    def get_queryset(self):
        self.kwargs['slug'] = self.request.user.username
        return AudioData.objects.filter(login=self.request.user.username)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']= "Личный кабинет"

        return context


def user_settings(request):
    context = {'title': 'Настройки',}
    return render(request, 'AudioApp/settings.html', context=context)




class PasswordChange(PasswordChangeView):
    """Представление для изменения пароля."""
    template_name = 'AudioApp/password_change.html'
    success_url = reverse_lazy('password_change_ok')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']= "Изменение пароля"

        return context

class PasswordChangeOk(PasswordChangeDoneView):
    """Предсталвение успешной смены пороля"""

    template_name = 'AudioApp/password_change_ok.html'
    title = 'Пароль изменен'

class EmailChange(UpdateView):
    model = User
    fields = ['email']
    template_name = 'AudioApp/email_change.html'
    # success_url = reverse_lazy('user_account')

    def get_queryset(self):
        print(EmailChange.__dir__(self))
        self.kwargs['pk'] = self.request.user.id
        return User.objects.filter(pk=self.request.user.id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Сменить пороль',})

        return context

    def form_valid(self, form):
        """Авторизовывает при успешной регистрации."""
        user = form.save()
        return redirect('email_change_ok')

@login_required
def del_page(request):
    """Представление для удаления деактивации аккаутна."""

    context = {'title': 'Удаление аккаунта'}

    if request.method !='POST':
        form = InputPasswordForm()
        context.update({'form': form})

    else:
        form = InputPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            # Деактивировать аккаунт и разлогинить пользвателя
            request.user.is_active = False
            request.user.save()
            return logout_user(request)

        else:
            form = InputPasswordForm()
            context.update({'form': form, 'error': 'Неверный пароль !'})


    return render(request, 'AudioApp/del_page.html', context)

@login_required
def email_change_done(request):
    """Передстовление для отображения успешной смены email."""

    context = {
        'title': 'Изменить email',
        'message': 'Email изменен!',
        'email': request.user.email
    }
    return render(request,'AudioApp/email_change_ok.html', context)