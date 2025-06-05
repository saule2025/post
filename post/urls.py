"""
URL configuration for post project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path, include

from django.conf import settings 
from django.conf.urls.static import static 
from django.conf.urls import include

from tracking import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('', views.index),
    path('index/', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('report/', views.report, name='report'),        
    path('contact/', views.contact, name='contact'),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),

    path('country/index/', views.country_index, name='country_index'),
    path('country/create/', views.country_create, name='country_create'),
    path('country/edit/<int:id>/', views.country_edit, name='country_edit'),
    path('country/delete/<int:id>/', views.country_delete, name='country_delete'),
    path('country/read/<int:id>/', views.country_read, name='country_read'),

    path('status/index/', views.status_index, name='status_index'),
    path('status/create/', views.status_create, name='status_create'),
    path('status/edit/<int:id>/', views.status_edit, name='status_edit'),
    path('status/delete/<int:id>/', views.status_delete, name='status_delete'),
    path('status/read/<int:id>/', views.status_read, name='status_read'),

    path('package/index/', views.package_index, name='package_index'),
    path('package/create/', views.package_create, name='package_create'),
    path('package/edit/<int:id>/', views.package_edit, name='package_edit'),
    path('package/delete/<int:id>/', views.package_delete, name='package_delete'),
    path('package/read/<int:id>/', views.package_read, name='package_read'),

    path('movement/index/<int:package_id>\d+)/', views.movement_index, name='movement_index'),
    path('movement/create/<int:package_id>\d+)/', views.movement_create, name='movement_create'),
    path('movement/edit/<int:id>/<int:package_id>\d+)/', views.movement_edit, name='movement_edit'),
    path('movement/delete/<int:id>/<int:package_id>\d+)/', views.movement_delete, name='movement_delete'),
    path('movement/read/<int:id>/<int:package_id>\d+)/', views.movement_read, name='movement_read'),

    path('customer/list/', views.customer_list, name='customer_list'),

    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', views.logoutUser, name="logout"),
    path('settings/account/', views.UserUpdateView.as_view(), name='my_account'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



