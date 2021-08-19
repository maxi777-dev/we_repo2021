from django.forms.forms import Form
from django.http import HttpResponse, request
import datetime
from django.template import Template, Context
from django.shortcuts import render, redirect
from sitio.forms import FormCreateUser, FormLogin


#----------------------------------------------------------------
#Falta el is valid y guardar datos en la BDD
def logear(request):

    if request.method == 'POST':

        form = FormLogin(request.POST)
        
    
    else:

        form = FormLogin()

    return render(request,"Login.html", {'form': form})        

#----------------------------------------------------------------

#Guardar en la BDD

def crear_usuario(request):

    if request.method == "POST":

        form = FormCreateUser(request.POST)
        
        if form.is_valid():
            
            form.cleaned_data['nombre']
            
        
        return redirect("Login")
    
    else:

        form = FormCreateUser()
    
    return render(request, 'CrearUsuario.html', {'form': form})

#----------------------------------------------------------------

def home(request):
    return render(request, 'Home.html')

#----------------------------------------------------------------