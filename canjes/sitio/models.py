
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

class Category(models.Model):
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length = 255, null = False)
    subtitle = models.CharField(max_length = 255, null = False)

    def __unicode__(self):
        if self.subtitle:
            return "%s - %s" % (self.title, self.subtitle)
        else:
            return self.title

    __str__ = __unicode__

    class Meta:
        ordering = ("title",)
        verbose_name = "category"
        verbose_name_plural = "categories"

    def save(self, *args, **kwargs):
        # Raise on circular reference
        parent = self.parent
        while parent is not None:
            if parent == self:
                raise RuntimeError("Circular references not allowed")
            parent = parent.parent

        super(Category, self).save(*args, **kwargs)

    @property
    def children(self):
        return self.category_set.all().order_by("title")

    @property
    def tags(self):
        return Tag.objects.filter(categories__in=[self]).order_by("title")

    def get_absolute_url(self):
        return reverse("category_object_list", kwargs={"category_slug": self.slug})
    
class Article(models.Model):
    user = models.ForeignKey(User, null = True, default = None, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, null = True, default = None, on_delete = models.CASCADE)
    title = models.CharField(max_length = 255, null = False)
    date_created = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length = 2055, null = False)
    state = models.IntegerField(default = 0, null = False)
    image_one = models.ImageField(upload_to = "articles/images/", null= True, blank = True)
    image_two = models.ImageField(upload_to = "articles/images/", null= True, blank = True)
    image_three = models.ImageField(upload_to = "articles/images/", null= True, blank = True)
    image_four = models.ImageField(upload_to = "articles/images/", null= True, blank = True)
    image_five = models.ImageField(upload_to = "articles/images/", null= True, blank = True)

    def __unicode__(self):
        return "%s - %s" % (self.title, self.description)

    __str__ = __unicode__

    class Meta:
        ordering = ("title",)
        verbose_name = "article"
        verbose_name_plural = "articles"

class Comment(models.Model):
    article = models.ForeignKey(Article, null = True, default = None, on_delete = models.CASCADE)
    user = models.ForeignKey(User, null = True, default = None, on_delete = models.CASCADE)
    comment = models.CharField(max_length = 255, null = False)
    date_created = models.DateTimeField(default=timezone.now)

class Canje(models.Model):
    articles_creator = models.ManyToManyField(Article, related_name='creator')
    articles_assignee = models.ManyToManyField(Article, related_name='assignee')
    comment = models.CharField(max_length = 255, null = False)
    date_created = models.DateTimeField(default=timezone.now)
    user_creator = models.ForeignKey(User, null = True, default = None, on_delete = models.CASCADE, related_name='creator')
    user_assignee = models.ForeignKey(User, null = True, default = None, on_delete = models.CASCADE, related_name='assignee')
    state = models.IntegerField(default = 0, null = False)

class Notification(models.Model):
    user = models.ForeignKey(User, null = True, default = None, on_delete = models.CASCADE)
    is_readed = models.BooleanField()
    context = models.CharField(max_length = 255, null = False)
    link = models.CharField(max_length = 255, null = False)