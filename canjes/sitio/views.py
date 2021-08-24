from django.contrib import auth
from sitio.models import Profile
from django import template
from django.forms.forms import Form
from django.http import HttpResponse, request
import datetime
from django.template import Template, Context, context
from django.shortcuts import render, redirect
from sitio.forms import FormCreateUser, FormLogin, FormRecuperarContraseña
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages

def home(request): #Pagina principal
    return render(request, 'home.html')


def logear(request): #Logeo de usuarios ya creados
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

    return render(request, "login.html", {'form': form})

def crear_usuario(request): #Registro de nuevo usuario
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
                user.is_active = True # Then return it to False
                grupo = Group.objects.get(name = 'comun')
                user.groups.add(grupo)
                Profile.objects.create(
                    user = user
                )

                user.save()

                return redirect('login')
            else:
                mensajes.append('El mail ingresado ya existe')    
    else:
        form = FormCreateUser()
    context = {'form': form, 'messages': mensajes}   
    return render(request, 'crear_usuario.html', context)

def contact(request): #Esto envia un mail al correo para verificar
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        template = render_to_string('email_template.html', {
            'name': name,
            'email': email,
            'message': message})
        email =EmailMessage(
            subject,
            template,
            settings.EMAIL_HOST_USER,
            email)
        email.fail_silently = False
        email.send()
        messages.success(request, 'Se a enviado un correo de verificacion')

def recuperarcontraseña(request): #Esto se usa para recuperar la contraseña
    if request.method == "POST":
        form = FormRecuperarContraseña(request.POST)
        return redirect("login")
    return render(request,"recuperarcontraseña.html") 

@login_required(login_url='login') #Pide el logeo de un usuario para poder ingresar a una pagina en espesifico
def mis_canjes(request):
    return render(request, 'mis_canjes.html')
