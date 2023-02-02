from django.contrib import admin
from rango.models import Category, Page

# Register your models here.
admin.site.register(Category) # to register the Category and the Page model to be viewed in the admin page 
admin.site.register(Page)
