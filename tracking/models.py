from django.db import models
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import datetime
from dateutil.relativedelta import relativedelta
#from django.utils import timezone
from django import forms

from django.contrib.auth.models import User

# Модели отображают информацию о данных, с которыми вы работаете.
# Они содержат поля и поведение ваших данных.
# Обычно одна модель представляет одну таблицу в базе данных.
# Каждая модель это класс унаследованный от django.db.models.Model.
# Атрибут модели представляет поле в базе данных.
# Django предоставляет автоматически созданное API для доступа к данным

# choices (список выбора). Итератор (например, список или кортеж) 2-х элементных кортежей,
# определяющих варианты значений для поля.
# При определении, виджет формы использует select вместо стандартного текстового поля
# и ограничит значение поля указанными значениями.

# Читабельное имя поля (метка, label). Каждое поле, кроме ForeignKey, ManyToManyField и OneToOneField,
# первым аргументом принимает необязательное читабельное название.
# Если оно не указано, Django самостоятельно создаст его, используя название поля, заменяя подчеркивание на пробел.
# null - Если True, Django сохранит пустое значение как NULL в базе данных. По умолчанию - False.
# blank - Если True, поле не обязательно и может быть пустым. По умолчанию - False.
# Это не то же что и null. null относится к базе данных, blank - к проверке данных.
# Если поле содержит blank=True, форма позволит передать пустое значение.
# При blank=False - поле обязательно.

# Пользователь клиент
class Customer(models.Model):
    telegram_id = models.IntegerField(_('telegram_id'))     # id пользователя Telegram
    phone_number = models.CharField(_('phone_number'), max_length=20)
    email = models.CharField(_('email'), max_length=128, blank=True, null=True)
    first_name = models.CharField(_('first_name'), max_length=64)
    last_name = models.CharField(_('last_name'), blank=True, null=True, max_length=64)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'customer'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['telegram_id']),
            models.Index(fields=['phone_number']),
        ]
        # Сортировка по умолчанию
        ordering = ['first_name', 'last_name', 'phone_number']        
    def __str__(self):
        # Вывод в тег Select
        return "{} ({})".format(self.phone_number, self.first_name)    

# Страна
class Country(models.Model):
    title = models.CharField(_('title_country'), unique=True, max_length=196)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'country'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['title']),
        ]
        # Сортировка по умолчанию
        ordering = ['title']
    def __str__(self):
        # Вывод Название в тег SELECT 
        return self.title

# Статус
class Status(models.Model):
    title = models.CharField(_('title_status'), unique=True, max_length=196)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'status'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['title']),
        ]
        # Сортировка по умолчанию
        ordering = ['title']
    def __str__(self):
        # Вывод Название в тег SELECT 
        return self.title

# Посылка (почтовое отправление)
class Package(models.Model):    
    #track_number = models.CharField(_('track_number'), unique=True, max_length=13)
    track_number = models.CharField(_('track_number'), max_length=13)
    dates = models.DateTimeField(_('datep'))
    sender_country = models.ForeignKey(Country, related_name='package_sender_country', on_delete=models.CASCADE)
    sender_address = models.CharField(_('sender_address'), max_length=192)
    sender_name = models.CharField(_('sender_name'), max_length=192)
    recipient_country = models.ForeignKey(Country, related_name='package_recipient_country', on_delete=models.CASCADE)
    recipient_address = models.CharField(_('recipient_address'), max_length=192)
    recipient_name = models.CharField(_('recipient_name'), max_length=192)
    recipient_phone = models.CharField(_('recipient_phone'), max_length=64, blank=True, null=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'package'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['track_number']),
            models.Index(fields=['sender_country']),
            models.Index(fields=['recipient_country']),            
        ]
        # Сортировка по умолчанию
        ordering = ['track_number']        
    def __str__(self):
        # Вывод в тег Select
        return "{}".format(self.track_number)

# Перемещение посылки
class Movement(models.Model):    
    package = models.ForeignKey(Package, related_name='movement_package', on_delete=models.CASCADE)
    datem = models.DateTimeField(_('dates'))
    status = models.ForeignKey(Status, related_name='movement_status', on_delete=models.CASCADE)
    details = models.TextField(_('details_movement'), blank=True, null=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'movement'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['package']),
            models.Index(fields=['datem']),
            models.Index(fields=['status']),            
        ]
        # Сортировка по умолчанию
        ordering = ['datem']        
    def __str__(self):
        # Вывод в тег Select
        return "{} ({}): {}".format(self.datem, self.package.track_number, self.details)

# Посылка (почтовое отправление) 
class ViewPackage(models.Model):
    """
    REATE VIEW view_package AS
        SELECT package.id, track_number, dates, sender_country_id, cs.title AS sender_country, sender_address,  sender_name, recipient_country_id, cr.title AS recipient_country, recipient_address, recipient_name, recipient_phone,
        (SELECT strftime('%d.%m.%Y %H:%M', datem) || " " || title FROM movement LEFT JOIN status ON movement.status_id =  status.id WHERE datem=(SELECT Max(datem) FROM movement m WHERE m.package_id=package.id)) AS final
        FROM package LEFT JOIN country cs ON package.sender_country_id = cs.id
        LEFT JOIN country cr ON package.recipient_country_id = cr.id
    """
    track_number = models.CharField(_('track_number'), unique=True, max_length=13)
    dates = models.DateTimeField(_('dates'))
    sender_country_id = models.IntegerField() 
    sender_country = models.CharField(_('title_country'), max_length=196)
    sender_address = models.CharField(_('sender_address'), max_length=192)
    sender_name = models.CharField(_('sender_name'), max_length=192)
    recipient_country_id = models.IntegerField()
    recipient_country = models.CharField(_('title_country'), max_length=196)
    recipient_address = models.CharField(_('recipient_address'), max_length=192)
    recipient_name = models.CharField(_('recipient_name'), max_length=192)
    recipient_phone = models.CharField(_('recipient_phone'), max_length=64, blank=True, null=True)
    final = models.CharField(_('final'), max_length=192)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'view_package'
        # Сортировка по умолчанию
        ordering = ['track_number']
        # Таблицу не надо не добавлять не удалять
        managed = False
