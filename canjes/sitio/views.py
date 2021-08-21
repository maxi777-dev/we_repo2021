from django import template
from django.forms.forms import Form
from django.http import HttpResponse, request
import datetime
from django.template import Template, Context
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
    if request.method == "POST":
        form = FormCreateUser(request.POST)        
        if form.is_valid():    
            #form.save()         no se porque pero en un video lo pone para guardar los datos pero aca me tira que no existe
            form.cleaned_data['name']
            form.cleaned_data['password_checks']
            return redirect("login")    
    else:
        form = FormCreateUser()    
    return render(request, 'crear_usuario.html', {'form': form})

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
