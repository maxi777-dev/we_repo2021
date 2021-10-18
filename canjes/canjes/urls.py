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
from os import name

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from sitio import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.logear, name='login'), 
    path('logout/', views.logout, name='logout'),    
    path('createuser/', views.crear_usuario, name='register'),
    path('articulos/', views.mis_articulos, name='mis_articulos'),
    path('createarticulo/', views.cargar_articulo, name='cargar_articulo'),
    path('miscanjes/',views.mis_canjes, name='mis_canjes'),
    path('canjes/<id>', views.ver_canje, name='ver_canje'),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name='homepage'), # HOMEPAGE,
    path('articulo/<id>', views.article, name='detalle_articulo'),
    path('articulo/delete/<id>', views.delete_article, name='delete_article'),
    path('articulo/edit/<id>', views.edit_article, name='edit_article'),
    path('activate/<uidb64>/<token>', views.verificationview.as_view(), name='activate'),
    path('article_categories/<id>', views.get_category, name='get_category'),
    path('get_articles_by_category/<id>', views.get_articles_by_category, name='get_articles_by_category'),
    path('categorias', views.categories, name='categories'),
    path('comment/<id>', views.comment, name='comment'),
    path('notifications/<id>', views.notifications, name='notifications'),
    path('iniciar_canje/<id_article>', views.iniciar_canje, name='iniciar_canje'),
    path('notifications/', views.mis_notifications, name='mis_notifications'),
    path('search/', include('haystack.urls')),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
