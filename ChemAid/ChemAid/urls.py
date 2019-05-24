"""ChemAid URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path, include
from Users import views as user_views
from Items import views as it_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ChemAid/home/', include('Users.urls')),
    path('ChemAid/', user_views.welcome, name='welcome'),
    path('ChemAid/register/', user_views.register, name='register'),
    path('ChemAid/profile/', user_views.profile, name='profile'),
    path('ChemAid/home/credentials', user_views.credentials, name='credentials'),
    path('ChemAid/profile/update/', user_views.updateProfile, name='updateProfile'),
    path('ChemAid/login/', user_views.log_in, name='log_in'),
    path('ChemAid/logout/', user_views.log_out, name='log_out'),
    path('ChemAid/admin/home/',user_views.adminhome, name='adminhome'),
    path('ChemAid/admin/profile/', user_views.adminprofile, name='adminprofile'),
    path('ChemAid/admin/profile/update/', user_views.updateAdmin, name='updateAdmin'),
    url(r'^', include('Items.urls')),
]
