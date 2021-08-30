"""canjes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from sitio import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.logear, name="login"), 
    path('logout/', views.logout, name="logout"),    
    path('createuser/', views.crear_usuario, name='register'),
    path('canjes/', views.mis_canjes, name='mis_canjes'),
    path('createcanjes/', views.cargar_canje, name='cargar_canje'),
    path('recuperarcontraseña/', views.recuperarcontraseña, name='recuperarcontraseña'),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name='homepage'), # HOMEPAGE,
    path('activate/<uidb64>/<token>', views.verificationview.as_view(), name="activate"),
]

