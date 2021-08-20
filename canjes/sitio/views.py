from django.forms.forms import Form
from django.http import HttpResponse, request
import datetime
from django.template import Template, Context
from django.shortcuts import render, redirect
from sitio.forms import FormCreateUser, FormLogin
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')


def logear(request):
    if request.method == 'POST':
        form = FormLogin(request.POST)
    else:
        form = FormLogin()
    return render(request,"login.html", {'form': form})        


def crear_usuario(request):
    if request.method == "POST":
        form = FormCreateUser(request.POST)        
        if form.is_valid():            
            form.cleaned_data['nombre']
            form.cleaned_data['contraseña2']
            return redirect("login")    
    else:
        form = FormCreateUser()    
    return render(request, 'crear_usuario.html', {'form': form})


@login_required(login_url='login')
def mis_canjes(request):  
    return render(request, 'mis_canjes.html')
