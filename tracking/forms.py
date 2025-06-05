from django import forms
from django.forms import ModelForm, TextInput, Textarea, DateInput, NumberInput
from .models import Customer, Country, Status, Package, Movement
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# При разработке приложения, использующего базу данных, чаще всего необходимо работать с формами, которые аналогичны моделям.
# В этом случае явное определение полей формы будет дублировать код, так как все поля уже описаны в модели.
# По этой причине Django предоставляет вспомогательный класс, который позволит вам создать класс Form по имеющейся модели
# атрибут fields - указание списка используемых полей, при fields = '__all__' - все поля
# атрибут widgets для указания собственный виджет для поля. Его значением должен быть словарь, ключами которого являются имена полей, а значениями — классы или экземпляры виджетов.

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ('title',)
        widgets = {
            'title': TextInput(attrs={"size":"100"}),            
        }

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ('title',)
        widgets = {
            'title': TextInput(attrs={"size":"100"}),            
        }

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ('track_number', 'dates', 'sender_country', 'sender_address', 'sender_name', 'recipient_country', 'recipient_address', 'recipient_name', 'recipient_phone')
        widgets = {
            'track_number': TextInput(attrs={"size":"80"}),
            'dates': DateInput(attrs={"type":"date"}),
            'sender_country': forms.Select(attrs={'class': 'chosen'}),
            'sender_address': TextInput(attrs={"size":"100"}),
            'sender_name': TextInput(attrs={"size":"100"}),
            'recipient_country': forms.Select(attrs={'class': 'chosen'}),
            'recipient_address': TextInput(attrs={"size":"100"}),
            'recipient_name': TextInput(attrs={"size":"100"}),
            'recipient_phone': TextInput(attrs={"size":"100"}),
        }
        labels = {
            'sender_country': _('sender_country'),
            'recipient_country': _('recipient_country'),
        }

class MovementForm(forms.ModelForm):
    class Meta:
        model = Movement
        fields = ('datem', 'status', 'details')
        widgets = {
            'datem': DateInput(attrs={"type":"date"}),
            'status': forms.Select(attrs={'class': 'chosen'}),
            'details': Textarea(attrs={'cols': 80, 'rows': 10}),            
        }
        labels = {
            'status': _('status'),            
        }

# Форма регистрации
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

