from django.contrib import auth
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from sitio.forms import FormCreateUser, FormLogin, FormCreateArticle, FormCreateComment
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.views.generic import View
from django.http import JsonResponse
from datetime import date
from haystack.generic_views import SearchView

## TOKEN AUTH USER
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site 
from django.urls import reverse
from .tokenizer import token_generator

def home(request): #Pagina principal
    articles = Article.objects.order_by("-date_created")[:10]
    content = {}
    sender = []
    for article in articles:
        content = {
            'title': article.title,
            'date_created': article.date_created,
            'link': '/articulo/' + str(article.id),
            'user': article.user,
            'image': article.image_one.url,
        }
        sender.append(content)
    return render(request, 'home.html', {'articles': sender})

def logear(request): #Logeo de usuarios ya creados
    if not request.user.is_authenticated: # Check if its ok
        form = FormLogin()
        no_activo = False
        mensajes = []
        if request.method == "POST":
            form = FormLogin(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user = authenticate(username=username, password=password)

                if user is not None:
                    if user.is_active:
                        auth.login(request, user)
                        next = request.POST.get('next')
                        if next:
                            return redirect(request.POST.get('next'))
                        return redirect('homepage')
            else:
                username = form.cleaned_data['username']     
                usuarios_comunes = User.objects.all()
                usuario_encontrado = False
                for usr in usuarios_comunes:
                    if (usr.username == username): 
                        usuario_encontrado = True
                        break
                if (usuario_encontrado):
                    if (not usr.is_active):
                        mensajes.append('El usuario no está activo, verifique su email')
                    else:
                        mensajes.append('La contraseña ingresada es incorrecta') 
                else:
                    msj = 'El usuario "' + username + '" no existe'
                    mensajes.append(msj)        
        context = {'form': form, 'messages': mensajes}
        return render(request, "login.html", context)
    else:
        return redirect('homepage')

def crear_usuario(request): #Registro de nuevo usuario
    if not request.user.is_authenticated: # Check if its ok
        mensajes = []
        if request.method == "POST":
            form = FormCreateUser(data=request.POST)
            if form.is_valid():
                validar_mail = request.POST['email']
                lista_usuarios = User.objects.all() #Se trae todos los usuarios que haya para validar mail existente
                email_valido = True
                for u in lista_usuarios:
                    if u.email == validar_mail:
                        email_valido = False
                        break
                if email_valido:
                    user = form.save()
                    user.is_active = False
                    grupo = Group.objects.get(name = 'comun')
                    user.groups.add(grupo)
                    Profile.objects.create(
                        user = user
                    )

                    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                    domain = get_current_site(request).domain
                    link = reverse('activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})
                    
                    activate_url = 'http://'+domain+link
                    user.save()
                    email = EmailMessage(
                        'Hola ' +user.username+ '! Gracias por registrarte!',
                        'Activa tu cuenta mediante este link: '+ activate_url,
                        'validate.canjea@gmail.com',
                        [user.email]
                    )
                    email.send(fail_silently=False)

                    return redirect('login')
                else:
                    mensajes.append('El mail ingresado ya existe')
                    form = FormCreateUser(data=request.POST)
            else:
                form = FormCreateUser(data=request.POST)
        else:
            form = FormCreateUser()
        context = {'form': form, 'messages': mensajes}   
        return render(request, 'register.html', context)
    else:
        return redirect('homepage')

@login_required(login_url='login')
def mis_notifications(request):
    notifications = Notification.objects.all().filter(user = request.user)
    content = {}
    sender = []
    for notification in notifications:
        content = {
            'notif': notification.context,
            'notif_id': notification.id,
            'is_readed': notification.is_readed,
            'link': notification.link
        }
        sender.append(content)
    return render(request, 'notifications.html', {'notifications': sender})

@login_required(login_url='login') #Pide el logeo de un usuario para poder ingresar a una pagina en espesifico
def mis_articulos(request):
    articles = Article.objects.all().filter(user = request.user)
    content = {}
    sender = []
    for article in articles:
        content = {
            'title': article.title,
            'date_created': article.date_created,
            'link': '/articulo/' + str(article.id),
            'edit_article': '/articulo/edit/' + str(article.id),
            'image': article.image_one.url,
        }
        sender.append(content)
    return render(request, 'mis_articulos.html', {'articles': sender})

@login_required(login_url='login')
def edit_article(request, id):
    article = get_object_or_404(Article, id=id)
    form = FormCreateArticle(request.POST or None, instance=article)
    if request.user == article.user:
        if form.is_valid():
            form.save()
            return redirect('mis_articulos')
        return render(request, 'edit_articulo.html', {'article': article})
    else:
        return redirect('homepage')

@login_required(login_url='login')
def delete_article(request, id):
    article = get_object_or_404(Article, id = id)
    article.delete()
    return redirect('homepage')

@login_required()
def cargar_articulo(request):
    mensajes = []
    if request.method == "POST":
        form = FormCreateArticle(request.POST, request.FILES)
        if form.is_valid():
            new_article = form.save(commit=False)
            new_article.user = request.user
            new_article.save()
            return redirect('mis_articulos')
    else:
        form = FormCreateArticle()
    context = {'form': form, 'messages': mensajes} 
    return render(request, 'cargar_articulo.html', context)

@login_required(login_url='homepage') #Pide el logeo de un usuario para poder ingresar a una pagina en espesifico
def logout(request):
    auth.logout(request)
    return redirect("homepage")

def article(request, id):
    article = Article.objects.get(pk=id)
    comments = Comment.objects.filter(article=article.id)
    if article:
        return render(request, 'single-product.html', {'article': article, 'comments': comments})
    else:
        pass

def get_category(request, id):
    if request.method == "GET":
        categories = Category.objects.all()
        if id == '0':
            categories = categories.filter(parent=None).values()
        else:
            categories = categories.filter(parent=id).values()
        categories_list = list(categories)
        return JsonResponse(categories_list, safe=False)
    pass

def get_articles_by_category(request, id):
    if request.method == "GET":
        articles = Article.objects.filter(category=id)
        content = {}
        sender = []
        for article in articles:
            content = {
                'title': article.title,
                'date_created': article.date_created,
                'link': '/articulo/' + str(article.id),
                'edit_article': '/articulo/edit/' + str(article.id),
                'image': article.image_one.url,
                'category': article.category.title,
                'user': str(article.user),
            }
            sender.append(content)
        return JsonResponse(sender, safe=False)
    pass

@login_required(login_url='login')
def comment(request, id):
    if request.method == 'POST':
        article = Article.objects.get(pk=id)
        comment = request.POST['comment']
        if len(comment) < 254:
            Comment.objects.create(
                comment=comment, 
                user=request.user,
                article=article,
            )
    return redirect('detalle_articulo', id)


@login_required(login_url='login') #Pide el logeo de un usuario para poder ingresar a una pagina en espesifico
def iniciar_canje(request, id_article):
    if request.method == 'POST':
        articles = request.POST.getlist('articles')
        own_articles = request.POST.getlist('own_articles')
        comment =  request.POST['comment']
        if len(comment) < 254:
            new_canje = Canje()
            new_canje.save()
            article_id = 0
            for article in articles:
                article_id = article.split(' - ')[0]
                new_canje.articles_assignee.add(article_id)
            user_assignee = Article.objects.get(pk=article_id).user
            for article in own_articles:
                article_id = article.split(' - ')[0]
                new_canje.articles_creator.add(article_id)
            new_canje.comment = comment
            new_canje.user_creator = request.user
            new_canje.user_assignee = user_assignee
            new_canje.save()
            Notification.objects.create(
                user = user_assignee,
                is_readed = False,
                context = f"Tienes un canje pendiente de {request.user}. ¿Deseas aceptarlo?",
                link = f'/canjes/{new_canje.id}'
            )
    else:
        if id_article == '0':
            return render('mis_canjes')
        else:
            article_user = Article.objects.get(pk=id_article).user
            articles = Article.objects.filter(user=article_user)
            own_articles = Article.objects.filter(user=request.user)
            return render(request, 'iniciar_canje.html', {'articles': articles, 'own_articles': own_articles, 'user': article_user})
    return mis_canjes(request)

@login_required(login_url='login')
def ver_canje(request, id):
    if request.method == "GET":
        canje = Canje.objects.get(pk=id)
        user_creator = canje.user_creator
        user_assignee = canje.user_assignee
        if request.user != user_creator and request.user != user_assignee:
            return redirect('homepage')
        else:
            art_creator = []
            context = {}
            for articles_creator in canje.articles_creator.all():
                context = {
                    'title': articles_creator.title,
                    'link': '/articulo/' + str(articles_creator.id),
                    'category': articles_creator.category.title
                }
                art_creator.append(context)
            context = {}
            art_assignee = []
            for articles_assignee in canje.articles_assignee.all():
                context = {
                    'title': articles_assignee.title,
                    'link': '/articulo/' + str(articles_assignee.id),
                    'category': articles_assignee.category.title
                }
                art_assignee.append(context)
            return render(request, 'canjes.html', {'art_creator': art_creator, 'art_assignee': art_assignee, 'user_creator': user_creator, 'user_assignee': user_assignee, 'id': id})
    elif request.method == "POST":
        canje = Canje.objects.get(pk=id)
        if request.POST.get('acept_button'):
            canje.update(state=1)
        else:
            canje.update(state=2)
            notif = Notification.objects.get(pk=id)
            notif.is_readed = True
            notif.save()
        return redirect('homepage')

@login_required(login_url='login') #Pide el logeo de un usuario para poder ingresar a una pagina en especifico
def mis_canjes(request):
    canjes = Canje.objects.all().filter(user_creator = request.user)
    content = {}
    sender = []
    for canje in canjes:
        content = {
            'title1': canje.state,
            'title2': canje.user_assignee,
            'title3': canje.date_created,
            'title4': canje.id
        }
        sender.append(content)
    return render(request, 'mis_canjes.html', {'canjes': sender})

def categories(request):
    categories = Category.objects.exclude(parent=None)
    articles = Article.objects.order_by("-date_created")[:9]
    content = {}
    sender = []
    for article in articles:
        content = {
            'title': article.title,
            'date_created': article.date_created,
            'link': '/articulo/' + str(article.id),
            'edit_article': '/articulo/edit/' + str(article.id),
            'image': article.image_one.url,
            'category': article.category.title,
            'user': str(article.user),
        }
        sender.append(content)
    return render(request, 'categories.html', {'categories': categories, 'articles': sender})

def notifications(request, id):
    if request.method == "GET" and request.user.is_authenticated == True:
        if id == '0':
            notifications = Notification.objects.filter(user=request.user).filter(is_readed=False)
            notifications_list = []
            content = {}
            for notification in notifications:
                content = {
                    'notif': notification.context,
                    'notif_id': notification.id,
                }
                notifications_list.append(content)
            return JsonResponse({'notifications': notifications_list, 'count': len(notifications_list)}, safe=False)
        else:
            Notification.objects.filter(pk=id).update(is_readed=True)
    return JsonResponse({'notifications': list([]), 'count': 0}, safe=False)

def get_images(request, id):
    photos = []
    if request.method == "GET":
        article = Article.objects.get(pk=id)
        if article.image_one:
            photos.append(article.image_one.url)
        if article.image_two:
            photos.append(article.image_two.url)
        if article.image_three:
            photos.append(article.image_three.url)
        if article.image_four:
            photos.append(article.image_four.url)
        if article.image_five:
            photos.append(article.image_five.url)
    return JsonResponse({'photos': photos}, safe=False)

class verificationview(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('login')

            if user.is_active:
                return redirect('homepage')
            user.is_active = True
            user.save()

            messages.success(request, 'Usuario activado con Éxito')
            return redirect('login')
        except Exception as ex:
            pass
            return redirect('login')

def robots_txt(request): #El robot.txt
    return render(request, "robots.txt", {})