from django.forms.forms import Form
from django.http import HttpResponse, request
import datetime
from django.template import Template, Context
from django.shortcuts import render, redirect
from sitio.Forms import FormCreateUser, FormLogin


#----------------------------------------------------------------
def Logear(request):

    if request.method == 'POST':

        form = FormLogin(request.POST)
        #Falta el is valid y guardar datos en la BDD
    
    else:

        form = FormLogin()

    return render(request,"Login.html", {'form': form})        
#----------------------------------------------------------------
def CrearUsuario(request):

    if request.method == "POST":

        form = FormCreateUser(request.POST)
        
        if form.is_valid():
            
            form.cleaned_data['nombre']
            #Guardar en la BDD
        
        return redirect("Login")
    
    else:

        form = FormCreateUser()
    
    return render(request, 'CrearUsuario.html', {'form': form})
#----------------------------------------------------------------
