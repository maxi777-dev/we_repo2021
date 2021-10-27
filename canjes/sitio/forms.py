from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import User, UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from .models import *

class FormCreateUser(UserCreationForm):

    email = forms.EmailField(max_length=100)       
    password1 = forms.CharField(
        label='Contraseña',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    def clean_first_name(self): #Controla que no se ingrtesen malas palabras en el nombre
        malas_palabras = ['maldito', 'maldita', 'puto', 'puta', 'idiota', 'imbecil', 'nazi', 'pelotudo', 'pelotuda', 'boludo', 'boluda']
        texto_ingresado = self.cleaned_data['first_name']
        for i in malas_palabras:
            if texto_ingresado in malas_palabras:
                raise forms.ValidationError("No se puede ingresar malas palabras")
            break
        
        return texto_ingresado
    
    def clean_last_name(self): #Controla que no se ingrtesen malas palabras en el nombre
        malas_palabras = ['maldito', 'maldita', 'puto', 'puta', 'idiota', 'imbecil', 'nazi', 'pelotudo', 'pelotuda', 'boludo', 'boluda']
        texto_ingresado = self.cleaned_data['last_name']
        for i in malas_palabras:
            if texto_ingresado in malas_palabras:
                raise forms.ValidationError("No se puede ingresar malas palabras")
            break
        
        return texto_ingresado
    
    def clean_username(self): #Controla que no se ingrtesen malas palabras en el nombre
        malas_palabras = ['maldito', 'maldita', 'puto', 'puta', 'idiota', 'imbecil', 'nazi', 'pelotudo', 'pelotuda', 'boludo', 'boluda']
        texto_ingresado = self.cleaned_data['username']
        for i in malas_palabras:
            if texto_ingresado in malas_palabras:
                raise forms.ValidationError("No se puede ingresar malas palabras")
            break
        
        return texto_ingresado


    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        if len(password1) < 8:
            raise forms.ValidationError('Las contraseñas no pueden tener menos de 8 caracteres.')

        return password2

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude().filter(username=username).exists():
            raise forms.ValidationError('El Nombre elegido ya existe.')
        
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude().filter(email=email).exists():
            raise forms.ValidationError('El Email elegido ya esta en uso.')
        return email

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email','password1', 'password2']
        help_texts = {
            'first_name': None,
            'last_name': None,
            'email': None,
            'username': None,
        }
    
    def __init__(self,*args,**kwargs):
        super(FormCreateUser, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = "Nombre de usuario"
        self.fields['first_name'].widget.attrs['placeholder'] = "Nombre"
        self.fields['last_name'].widget.attrs['placeholder'] = "Apellido"
        self.fields['email'].widget.attrs['placeholder'] = "E-Mail"
        self.fields['password1'].widget.attrs['placeholder'] = "Contraseña"
        self.fields['password1'].label = ''      
        self.fields['password1'].help_text = ''        

        self.fields['password2'].widget.attrs['placeholder'] = "Confirmar contraseña"
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = ''
    
class FormLogin(AuthenticationForm):
    def confirm_login_allowed(self, user): # Bypass login without is_active() 
        pass

    def __init__(self,*args,**kwargs):
        super(FormLogin, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = "Usuario"
        self.fields['username'].label = ''

        self.fields['password'].widget.attrs['placeholder'] = "Contraseña"
        self.fields['password'].label = ''  

class FormCreateArticle(ModelForm):
    description = forms.CharField(widget=forms.Textarea, max_length= 250)
    title = forms.CharField(max_length=20)
    class Meta:
        model = Article
        fields = ['title', 'category', 'description', 'image_one', 'image_two', 'image_three', 'image_four', 'image_five']

class FormCreateComment(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class FormCreateCanje(ModelForm):
    class Meta:
        model = Canje
        fields = ['articles_creator', 'articles_assignee', 'comment']