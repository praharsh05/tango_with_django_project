from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

#adding Category model which will create Category table as well as Page table
class Category(models.Model):
    name= models.CharField(max_length=128, unique=True)
    views= models.IntegerField(default=0)
    likes= models.IntegerField(default=0)
    slug= models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug= slugify(self.name)
        if self.views<0:
            self.views=0
        super(Category, self).save(*args, **kwargs)


    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    last_visit = models.DateTimeField(default=timezone.now())
    
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    #this line links UserProfile with a User model instance
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    #these are the additional fields we wish to include
    website= models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

