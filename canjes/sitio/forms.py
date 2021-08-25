from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

class FormCreateUser(UserCreationForm):
    first_name = forms.CharField(label="", max_length=40, widget=forms.TextInput(attrs={'placeholder':'Nombre'}))
    last_name = forms.CharField(label="", max_length=40, widget=forms.TextInput(attrs={'placeholder':'Apellido'}))
    email = forms.EmailField(label="", max_length=125, widget=forms.TextInput(attrs={'placeholder':'E-Mail'}))
    username = forms.CharField(label="", max_length=40, widget=forms.TextInput(attrs={'placeholder':'Nombre de Usuario'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username','password1', 'password2']
        help_texts = {
            'first_name': None,
            'last_name': None,
            'email': None,
            'username': None,
        }
    
    def __init__(self,*args,**kwargs):
        super(FormCreateUser, self).__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs['placeholder'] = "Contraseña"
        self.fields['password1'].label = ''      
        self.fields['password1'].help_text = ''        

        self.fields['password2'].widget.attrs['placeholder'] = "Confirmar contraseña"
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = ''
    
    def clean_first_name(self): #Controla que no se ingrtesen malas palabras en el nombre
        malas_palabras = ['maldito', 'maldita', 'puto', 'puta', 'idiota', 'imbecil', 'nazi', 'pelotudo', 'pelotuda', 'boludo', 'boluda']
        texto_ingresado = self.cleaned_data['first_name']
        for i in malas_palabras:
            if texto_ingresado in malas_palabras:
                raise ValidationError("No se puede ingresar malas palabras")
            break
        return texto_ingresado
    
    def clean_last_name(self): #Controla que no se ingrtesen malas palabras en el nombre
        malas_palabras = ['maldito', 'maldita', 'puto', 'puta', 'idiota', 'imbecil', 'nazi', 'pelotudo', 'pelotuda', 'boludo', 'boluda']
        texto_ingresado = self.cleaned_data['last_name']
        for i in malas_palabras:
            if texto_ingresado in malas_palabras:
                raise ValidationError("No se puede ingresar malas palabras")
            break
        return texto_ingresado
    
    def clean_username(self): #Controla que no se ingrtesen malas palabras en el nombre
        malas_palabras = ['maldito', 'maldita', 'puto', 'puta', 'idiota', 'imbecil', 'nazi', 'pelotudo', 'pelotuda', 'boludo', 'boluda']
        texto_ingresado = self.cleaned_data['username']
        for i in malas_palabras:
            if texto_ingresado in malas_palabras:
                raise ValidationError("No se puede ingresar malas palabras")
            break
        return texto_ingresado

class FormLogin(AuthenticationForm):
    def confirm_login_allowed(self, user): # Bypass login without is_active() 
        pass

    def __init__(self,*args,**kwargs):
        super(FormLogin, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = "Usuario"
        self.fields['username'].label = ''

        self.fields['password'].widget.attrs['placeholder'] = "Contraseña"
        self.fields['password'].label = ''  

class FormRecuperarContraseña(forms.Form): #Lista de datos pararecuperar contraseña
    email = forms.EmailField(label="", max_length=125, widget=forms.TextInput(attrs={'placeholder':'E-Mail'}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder':'Nueva Contraseña'}))
    password_checks = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder':'Repetir Contraseña'}))

