"""metrics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views
from meter_readings.views import UserRegisterView, CustomPasswordChangeView, password_change_done, user_register_done

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('register/done', user_register_done, name='user_register_done'),
    path('password/change/', CustomPasswordChangeView.as_view(), name='change'),
    path('password/change/done', password_change_done, name='password_done'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', include('meter_readings.urls')),
    path('admin/', admin.site.urls),
]
