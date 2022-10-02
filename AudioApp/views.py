import os

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.shortcuts import redirect, render, reverse
from django.urls import reverse_lazy
from django.utils.decorators import classonlymethod
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, ListView, UpdateView

from .forms import UploadFileForm, RegisterUserForm, LoginUserForm, InputPasswordForm
from .models import AudioData
from .utils.database import write_database
from .utils.converter import converter
from .utils.utils import error_messages


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
                # Открыть страницу при ошибке конвертирования
                return render(request, 'AudioApp/conversion_error.html')

            # Информация о конвертированном файле для контекста
            trek_name: str = trek_dict['trek_name']
            trek_format: str = trek_dict['format']
            # audio: str = trek_dict['path_convert']
            audio :str = os.path.relpath(trek_dict['path_convert'], 'AudioApp\static')

            # формируем контекст для представления
            context = {'form': form, # форма загрузки файла
                        'trek_name': trek_name, # имя сконвертированного файла
                        'format': trek_format, # формат сконвертированного файла
                        'audio': audio, # путь к сконвертированному файлу
                        'name': name # имя пользователя
                      }

        else:
            # получить ошибки в случае невалидных данных.
            errors = error_messages(form)
            context = {'form':UploadFileForm(),
                       'errors': errors}

    return render(request, 'AudioApp/home.html',context=context)


def user_account(request):
    """Представление для личного кабинета пользователя"""

    if request.user.is_authenticated:
        return redirect(reverse('user_page', kwargs={'slug': request.user.username}))
    else:
        return render(request, 'AudioApp/guest.html')


class RegisterUser(CreateView):
    """Представление для регистрации пользователя."""

    form_class = RegisterUserForm
    template_name = 'AudioApp/registration.html'
    success_url = reverse_lazy('user_account')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        """Формирует динамический контекст."""

        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'

        return context

    def form_valid(self, form):
        """Авторизовывает при успешной регистрации."""
        user = form.save()
        login(self.request, user)

        return redirect('user_account')


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
    paginate_by = 5
    paginate_orphans = 2
    template_name = 'AudioApp/userpage.html'
    context_object_name = 'userdata'
    allow_empty = True

    def get_queryset(self):
        # Url пользователя формируется по его логину. Проверяем совпадение url пользователя с его логином.
        # Возвращаем список аудио пользователя если он авторизован, url совпадет с логином
        if self.check_url() == True:
            return AudioData.objects.filter(login=self.kwargs['slug'])
        else:
            return ['error404']

    def get_context_data(self, *, object_list=None, **kwargs):
        """Формирует контекст"""

        context = super().get_context_data(**kwargs)
        context['title']= "Личный кабинет"

        return context

    def check_url(self):
        """Проверяет наличие совпадение слага с адресом веб-страницы, именем пользвателя."""

        # Провеярет подмену url пользвателя в адресе веб-страницы
        if self.kwargs['slug'] == self.request.user.username:
            return True
        else:
            return False

    def paginator_objects_count(self):
        pass


@login_required
def user_settings(request):
    """Представление для страницы настроек."""

    context = {'title': 'Настройки',}
    return render(request, 'AudioApp/settings.html', context=context)


class PasswordChange(PasswordChangeView):
    """Представление для изменения пароля."""

    template_name = 'AudioApp/password_change.html'
    success_url = reverse_lazy('password_change_ok')

    def get_context_data(self, *, object_list=None, **kwargs):
        """Формирует контекст."""
        context = super().get_context_data(**kwargs)
        context['title']= "Изменение пароля"

        return context


class PasswordChangeOk(PasswordChangeDoneView):
    """Предсталвение для отображения успешного изменения пароля"""

    template_name = 'AudioApp/password_change_ok.html'
    title = 'Пароль изменен'


class EmailChange(UpdateView):
    """Представление для изменения email."""

    model = User
    fields = ['email']
    template_name = 'AudioApp/email_change.html'
    # success_url = reverse_lazy('user_account')

    def get_queryset(self):
        """Выбор нужного пользователя."""

        self.kwargs['pk'] = self.request.user.id

        return User.objects.filter(pk=self.request.user.id)

    def get_context_data(self, *, object_list=None, **kwargs):
        """Формирует контекст."""
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Изменить email',})

        return context

    def form_valid(self, form):
        """Сохранения пароля."""

        user = form.save()
        return redirect('email_change_ok')


@login_required
def email_change_done(request):
    """Передстовление для отображения успешного изменения email."""

    context = {
        'title': 'Изменить email',
        'message': 'Email изменен!',
        'email': request.user.email
    }
    return render(request,'AudioApp/email_change_ok.html', context)

@login_required
def del_page(request):
    """Представление для удаления (деактивации) аккаутна."""

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


@cache_page(60 * 60 * 24)
def about(request):
    """Представление для страницы 'О нас'."""
    return render(request, 'AudioApp/about.html',context={'title': 'О нас'})


@cache_page(60 * 60 * 24)
def error404(request,exception=''):
    """Представление для несуществующих страниц.  """
    context = {
        'message' : 'Упс, ошибка',
        'title': 'Ошибка 404',
    }
    return render(request, 'AudioApp/error404.html', context, status=404)


@cache_page(60 * 60 * 24)
def footer(request):
    """Представление для footer."""

    context = {'title': 'Cправочная информация'}
    return render(request, 'AudioApp/footer.html', context)