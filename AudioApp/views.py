
# from django.contrib.auth.models import User
from django.shortcuts import redirect, render, reverse
# from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UploadFileForm, SelectFormatForm, RegisterUserForm
from .audiohandler.audio import AudioConverter
from .utils.database import write_database
from AudioConverter.settings import STATIC_URL # файлы статики

#Converter setiings
settings = {
        'move': True, # Перемещать (не копировать) файлы в папку конвертированных
        'write_db': False, # Использовать стандартную базу данных конвертора
        'db_path': '', # Путь к стандартной базе данных конвертора
        'storage_path': f'AudioApp{STATIC_URL}', # Путь, где будут храниться конвертированные файлы
        }
#object converter
converter = AudioConverter(setting_dict=settings)


def upload_file(request):
    """Загрузка аудио и его конвретирвоание."""

    select = SelectFormatForm()

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()
            text :str= str(form.files['audio_file']).replace(' ', '_')
            frmt = request.POST.get('format')

            # Конвертирование аудиофайла и сохранение информации о нем в базу данных
            trek_dict : dict = converter.convert(f'AudioApp/media/audio_files/{text}', frmt=frmt, name='Guest')
            flag: bool = write_database(trek_dict)

            # Инфа о файле в home.html
            trek_name :str= trek_dict['trek_name']
            trek_format :str = trek_dict['format']
            audio :str= trek_dict['path_convert'].replace('AudioApp/static/', '')

            context :dict = {'form': form,
                       'trek_name': trek_name,
                       'format': trek_format,
                       'audio':audio,
                       'select': select,
                       }

            return render(request,  'AudioApp/home.html', context=context)
            # return redirect('home')
    else:
        form = UploadFileForm()
        context :dict = {'form': form,
                        'select': select,
                         }

        return render(request, 'AudioApp/home.html',context=context)



def user_account(request):
    return render(request, 'AudioApp/user.html')

class RegisterUser(CreateView):
    """Регистрация пользователя."""
    form_class = RegisterUserForm
    template_name = 'AudioApp/registration.html'
    success_url = reverse_lazy('user_page')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        print(context)
        return context



def about(request):
    return render(request, 'AudioApp/about.html')

def deletion_page(request):
    return render(request, 'AudioApp/deletion.html')

def login(request):
    return render(request, 'AudioApp/authorization.html')

def user_page(request):
    return render(request, 'AudioApp/userpage.html')



