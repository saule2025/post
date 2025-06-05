from django.shortcuts import render, redirect

# Класс HttpResponse из пакета django.http, который позволяет отправить текстовое содержимое.
from django.http import HttpResponse, HttpResponseNotFound
# Конструктор принимает один обязательный аргумент – путь для перенаправления. Это может быть полный URL (например, 'https://www.yahoo.com/search/') или абсолютный путь без домена (например, '/search/').
from django.http import HttpResponseRedirect

from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from django.db.models import Max
from django.db.models import Q

from datetime import datetime, timedelta

# Отправка почты
from django.core.mail import send_mail

# Подключение моделей
from .models import Customer, Country, Status, Package, Movement, ViewPackage
# Подключение форм
from .forms import CountryForm, StatusForm, PackageForm, MovementForm, SignUpForm

from django.db.models import Sum

from django.db import models

import sys

import math


#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _

from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.contrib.auth import login as auth_login

from django.db.models.query import QuerySet

import csv
import xlwt
from io import BytesIO

# Create your views here.
# Групповые ограничения
def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='403')

###################################################################################################

# Стартовая страница
#@login_required 
def index(request):
    return render(request, "index.html")

# Страница Контакты
def contact(request):
    return render(request, "contact.html")

# Страница Отчеты
@login_required
@group_required("Managers")
def report(request):
    package = ViewPackage.objects.all().order_by('dates')
    return render(request, "report.html", {"package": package})

# Список 
@login_required
@group_required("Managers")
def customer_list(request):
    customer = Customer.objects.all().order_by('first_name')
    return render(request, "customer/list.html", {"customer": customer})

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def country_index(request):
    try:
        country = Country.objects.all().order_by('title')
        return render(request, "country/index.html", {"country": country})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def country_create(request):
    try:
        if request.method == "POST":
            country = Country()        
            country.title = request.POST.get("title")
            countryform = CountryForm(request.POST)
            if countryform.is_valid():
                country.save()
                return HttpResponseRedirect(reverse('country_index'))
            else:
                print(countryform.errors)
                return render(request, "country/create.html", {"form": countryform})
        else:        
            countryform = CountryForm()
            return render(request, "country/create.html", {"form": countryform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def country_edit(request, id):
    try:
        country = Country.objects.get(id=id) 
        if request.method == "POST":
            country.title = request.POST.get("title")
            countryform = CountryForm(request.POST)
            if countryform.is_valid():
                country.save()
                return HttpResponseRedirect(reverse('country_index'))
            else:
                print(countryform.errors)
                return render(request, "country/edit.html", {"form": countryform})
        else:
            # Загрузка начальных данных
            countryform = CountryForm(initial={'title': country.title, })
            return render(request, "country/edit.html", {"form": countryform})
    except Country.DoesNotExist:
        return HttpResponseNotFound("<h2>Country not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def country_delete(request, id):
    try:
        country = Country.objects.get(id=id)
        country.delete()
        return HttpResponseRedirect(reverse('country_index'))
    except Country.DoesNotExist:
        return HttpResponseNotFound("<h2>Country not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def country_read(request, id):
    try:
        country = Country.objects.get(id=id) 
        return render(request, "country/read.html", {"country": country})
    except Country.DoesNotExist:
        return HttpResponseNotFound("<h2>Country not found</h2>")    
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def status_index(request):
    try:
        status = Status.objects.all().order_by('title')
        return render(request, "status/index.html", {"status": status})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def status_create(request):
    try:
        if request.method == "POST":
            status = Status()        
            status.title = request.POST.get("title")
            statusform = StatusForm(request.POST)
            if statusform.is_valid():
                status.save()
                return HttpResponseRedirect(reverse('status_index'))
            else:
                print(statusform.errors)
                return render(request, "status/create.html", {"form": statusform})
        else:        
            statusform = StatusForm()
            return render(request, "status/create.html", {"form": statusform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def status_edit(request, id):
    try:
        status = Status.objects.get(id=id) 
        if request.method == "POST":
            status.title = request.POST.get("title")
            statusform = StatusForm(request.POST)
            if statusform.is_valid():
                status.save()
                return HttpResponseRedirect(reverse('status_index'))
            else:
                print(statusform.errors)
                return render(request, "status/edit.html", {"form": statusform})
        else:
            # Загрузка начальных данных
            statusform = StatusForm(initial={'title': status.title, })
            return render(request, "status/edit.html", {"form": statusform})
    except Status.DoesNotExist:
        return HttpResponseNotFound("<h2>Status not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def status_delete(request, id):
    try:
        status = Status.objects.get(id=id)
        status.delete()
        return HttpResponseRedirect(reverse('status_index'))
    except Status.DoesNotExist:
        return HttpResponseNotFound("<h2>Status not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def status_read(request, id):
    try:
        status = Status.objects.get(id=id) 
        return render(request, "status/read.html", {"status": status})
    except Status.DoesNotExist:
        return HttpResponseNotFound("<h2>Status not found</h2>")    
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def package_index(request):
    try:
        package = ViewPackage.objects.all().order_by('dates')
        return render(request, "package/index.html", {"package": package})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def package_create(request):
    try:
       if request.method == "POST":
           package = Package()                   
           package.track_number = request.POST.get("track_number")
           #package.dates = request.POST.get("dates")
           package.dates = datetime.now()
           package.sender_country = Country.objects.filter(id=request.POST.get("sender_country")).first()
           package.sender_address = request.POST.get("sender_address")
           package.sender_name = request.POST.get("sender_name")
           package.recipient_country = Country.objects.filter(id=request.POST.get("recipient_country")).first()
           package.recipient_address = request.POST.get("recipient_address")
           package.recipient_name = request.POST.get("recipient_name")
           package.recipient_phone = request.POST.get("recipient_phone")
           packageform = PackageForm(request.POST)
           if packageform.is_valid():               
               try:
                    package.save()
               except:
                   max_id = Package.objects.aggregate(Max('id'))['id__max']
                   package.id = max_id + 1
                   package.save()
               return HttpResponseRedirect(reverse('package_index'))
           else:
               print(packageform.errors)
               return render(request, "package/create.html", {"form": packageform})
       else:        
           packageform = PackageForm(initial={'dates': datetime.now().strftime('%Y-%m-%d') })
           return render(request, "package/create.html", {"form": packageform})
    except Exception as exception:
       print(exception)
       return HttpResponse(exception)
    
# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def package_edit(request, id):
    try:
        package = Package.objects.get(id=id) 
        if request.method == "POST":
            package.track_number = request.POST.get("track_number")
            package.dates = request.POST.get("dates")
            package.sender_country = Country.objects.filter(id=request.POST.get("sender_country")).first()
            package.sender_address = request.POST.get("sender_address")
            package.sender_name = request.POST.get("sender_name")
            package.recipient_country = Country.objects.filter(id=request.POST.get("recipient_country")).first()
            package.recipient_address = request.POST.get("recipient_address")
            package.recipient_name = request.POST.get("recipient_name")
            package.recipient_phone = request.POST.get("recipient_phone")
            packageform = PackageForm(request.POST)
            if packageform.is_valid():
                package.save()
                return HttpResponseRedirect(reverse('package_index'))
            else:
                print(packageform.errors)
                return render(request, "package/edit.html", {"form": packageform})
        else:
            # Загрузка начальных данных
            packageform = PackageForm(initial={'track_number': package.track_number, 'dates': package.dates.strftime('%Y-%m-%d'), 'sender_country': package.sender_country, 'sender_address': package.sender_address, 'sender_name': package.sender_name, 'recipient_country': package.recipient_country, 'recipient_address': package.recipient_address, 'recipient_name': package.recipient_name, 'recipient_phone': package.recipient_phone, })
            return render(request, "package/edit.html", {"form": packageform})
    except Package.DoesNotExist:
        return HttpResponseNotFound("<h2>Package not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def package_delete(request, id):
    try:
        package = Package.objects.get(id=id)
        package.delete()
        return HttpResponseRedirect(reverse('package_index'))
    except Package.DoesNotExist:
        return HttpResponseNotFound("<h2>Package not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def package_read(request, id):
    try:
        package = ViewPackage.objects.get(id=id) 
        return render(request, "package/read.html", {"package": package})
    except Package.DoesNotExist:
        return HttpResponseNotFound("<h2>Package not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################
    
# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers", "Receivers", "Masters")
def movement_index(request, package_id):
    try:
        movement = Movement.objects.filter(package_id=package_id).order_by('-datem')
        pack = Package.objects.get(id=package_id)
        #movement = Movement.objects.all().order_by('-orders', '-datem')
        return render(request, "movement/index.html", {"movement": movement, "package_id": package_id, "pack": pack})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers", "Masters")
def movement_create(request, package_id):
    try:
        pack = Package.objects.get(id=package_id)
        track_number = pack.track_number
        if request.method == "POST":
            movement = Movement()
            #movement.package = Package.objects.filter(id=request.POST.get("package")).first()
            movement.package_id = package_id
            #movement.datem = request.POST.get("datem")
            movement.datem = datetime.now()
            movement.status = Status.objects.filter(id=request.POST.get("status")).first()
            movement.details = request.POST.get("details")
            movementform = MovementForm(request.POST)
            if movementform.is_valid():
                movement.save()
                return HttpResponseRedirect(reverse('movement_index', args=(package_id,)))
            else:
                print(movementform.errors)
                return render(request, "movement/create.html", {"form": movementform})        
        else:
            print(track_number)
            movementform = MovementForm(initial={ 'datem': datetime.now().strftime('%Y-%m-%d'), "track_number": track_number})
            return render(request, "movement/create.html", {"form": movementform, "package_id": package_id})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers", "Masters")
def movement_edit(request, id, package_id):
    pack = Package.objects.get(id=package_id)
    track_number = pack.track_number    
    try:
        movement = Movement.objects.get(id=id) 
        if request.method == "POST":
            #movement.package = Package.objects.filter(id=request.POST.get("package")).first()
            movement.package_id = package_id
            #movement.datem = request.POST.get("datem")
            movement.datem = datetime.now()
            movement.status = Status.objects.filter(id=request.POST.get("status")).first()
            movement.details = request.POST.get("details")
            movementform = MovementForm(request.POST)
            if movementform.is_valid():
                movement.save()
                return HttpResponseRedirect(reverse('movement_index', args=(package_id,)))
            else:
                print(movementform.errors)
                return render(request, "movement/edit.html", {"form": movementform})                     
        else:
            # Загрузка начальных данных
            movementform = MovementForm(initial={"track_number": track_number, 'package': movement.package, 'datem': movement.datem.strftime('%Y-%m-%d'), 'status': movement.status, 'details': movement.details, })
            return render(request, "movement/edit.html", {"form": movementform, "package_id": package_id})
    except Movement.DoesNotExist:
        return HttpResponseNotFound("<h2>Movement not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers", "Masters")
def movement_delete(request, id, package_id):
    try:
        movement = Movement.objects.get(id=id)
        movement.delete()
        return HttpResponseRedirect(reverse('movement_index', args=(package_id,)))
    except Movement.DoesNotExist:
        return HttpResponseNotFound("<h2>Movement not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def movement_read(request, id, package_id):
    try:
        movement = Movement.objects.get(id=id) 
        return render(request, "movement/read.html", {"movement": movement, "package_id": package_id})
    except Movement.DoesNotExist:
        return HttpResponseNotFound("<h2>Movement not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Регистрационная форма 
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
            #return render(request, 'registration/register_done.html', {'new_user': user})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    #fields = ('first_name', 'last_name', 'email',)
    fields = ('email',)
    template_name = 'registration/my_account.html'
    success_url = reverse_lazy('index')
    #success_url = reverse_lazy('my_account')
    def get_object(self):
        return self.request.user

# Выход
from django.contrib.auth import logout
def logoutUser(request):
    logout(request)
    return render(request, "index.html")


