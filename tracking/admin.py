from django.contrib import admin

from .models import Customer, Country, Status, Package, Movement

# Добавление модели на главную страницу интерфейса администратора
admin.site.register(Customer)
admin.site.register(Country)
admin.site.register(Status)
admin.site.register(Package)
admin.site.register(Movement)
