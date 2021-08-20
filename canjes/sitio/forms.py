from django import forms
from django.core.exceptions import ValidationError
from django.forms import models
from django.forms.fields import DateField, DateTimeField
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.widgets import Widget

class FormCreateUser(forms.Form): #Lista de datos que se necesitan al crear un usuario nuevo
    nombre = forms.CharField(label="", max_length=125, widget=forms.TextInput(attrs={'placeholder':'Nombre'}))
    apellido = forms.CharField(label="", max_length=125, widget=forms.TextInput(attrs={'placeholder':'Apellido'}))
    usuario = forms.CharField(label="", max_length=50, widget=forms.TextInput(attrs={'placeholder':'Nombre de Usuario'}))
    email = forms.EmailField(label="", max_length=125, widget=forms.TextInput(attrs={'placeholder':'E-Mail'}))
    direccion = forms.CharField(label="", max_length=125, widget=forms.TextInput(attrs={'placeholder':'Direccion'}))
    cp = forms.CharField(label="", max_length=4, widget=forms.TextInput(attrs={'placeholder':'Codigo Postal'}))
    fecha_nacimiento = forms.DateField(label="", widget=forms.DateInput(attrs={'type':'date'}))
    cuil_cuit = forms.CharField(label="", max_length=10, widget=forms.TextInput(attrs={'placeholder':'CUIT/CUIL'}))
    contraseña = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder':'Nueva Contraseña'}))
    contraseña2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder':'Repetir Contraseña'}))

    def clean_nombre(self): #Controla que no se ingrtesen malas palabras
        malas_palabras = ['maldito', 'puto', 'idiota', 'imbecil']
        texto_ingresado =self.cleaned_data['nombre']
        for i in malas_palabras:
            if texto_ingresado in malas_palabras:
                raise ValidationError("No se puede ingresar malas palabras")
            break
        return texto_ingresado

    def clean_contraseña2(self):
        pass1 = self.cleaned_data['contraseña']
        pass2 = self.cleaned_data['contraseña2']
        if pass1 != pass2:
            raise forms.ValidationError ('Las contraseñas NO se repiten')
        return pass2

class FormLogin(forms.Form):
    usuario = forms.CharField(label="", max_length=50, widget=forms.TextInput(attrs={'placeholder':'Usuario'}))
    contraseña = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder':'Contraseña'}))