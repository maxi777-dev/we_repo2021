
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, null = True, default = None, on_delete = models.CASCADE)
    location = models.CharField(max_length = 1250, null= True, blank = True)
    cp = models.CharField(max_length = 4, null= True, blank = True)
    birthdate = models.DateField(null= True, blank = True)
    cuil_cuit = models.CharField(max_length = 10, null= True, blank = True)

    def __str__(self):
        return self.nombre + ' ' + self.apellido

#class CategoriasArt(models.Model):
    
class Article(models.Model):
    user = models.ForeignKey(User, null = True, default = None, on_delete = models.CASCADE)
    title = models.CharField(max_length = 255, null = False)
    date_created = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length = 2055, null = False)
    state = models.IntegerField(default = 0, null = False)
    image_one = models.ImageField(upload_to = "articles/images/", null= True, blank = True)
    image_two = models.ImageField(upload_to = "articles/images/", null= True, blank = True)
    image_three = models.ImageField(upload_to = "articles/images/", null= True, blank = True)
    image_four = models.ImageField(upload_to = "articles/images/", null= True, blank = True)
    image_five = models.ImageField(upload_to = "articles/images/", null= True, blank = True)
    #caregory = Class CategoriasArt() para podes buscar y ubicar el art


#class Canje(models.Model):



# AGgregar para que una persona pueda canjear mpas d eun art en un mismo canje