from sitio.models import Profile
from django import template
from django.forms.forms import Form
from django.http import HttpResponse, request
import datetime
from django.template import Template, Context, context
from django.shortcuts import render, redirect
from sitio.forms import FormCreateUser, FormLogin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages

def home(request): #Pagina principal
    return render(request, 'home.html')

def logear(request): #Logeo de usuarios ya creados
    if request.method == 'POST':
        form = FormLogin(request.POST)
        authenticate(form.username, form.password) #Autentica al usuario, me falta agregar algo aca
    else:
        form = FormLogin()
    return render(request,"login.html", {'form': form})        

def crear_usuario(request): #Registro de nuevo usuario
    mensajes = []
    if request.method == "POST":
        form = FormCreateUser(request.POST)        
        if form.is_valid():
            validar_mail = request.POST['email']
            lista_usuarios = Profile.objects.all() #Se trae todos los usuarios que haya para validar mail existente
            email_valido = True
            for u in lista_usuarios:
                if u.mail == validar_mail:
                    email_valido = False
                    break
            if email_valido:
                form.cleaned_data['name']
                form.cleaned_data['lastname']
                form.cleaned_data['location']
                form.cleaned_data['cp']
                form.cleaned_data['cuil_cuit']
                form.cleaned_data['password_checks']
                nuevo = Profile()
                nuevo.name = request.POST['name']
                nuevo.lastname = request.POST['lastname']
                nuevo.birthdate = request.POST['fecha_nacimiento']
                nuevo.password = request.POST['password']
                nuevo.cp = request.POST['cp']
                nuevo.cuil_cuit = request.POST['cuil_cuit']
                nuevo.mail = request.POST['email']
                nuevo.location = request.POST['location']
                #nuevo.save()
                return redirect("login")
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



@login_required(login_url='login') #Pide el logeo de un usuario para poder ingresar a una pagina en espesifico
def mis_canjes(request):
    return render(request, 'mis_canjes.html')
