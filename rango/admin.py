from django.contrib import admin
from rango.models import Category, Page
from rango.models import UserProfile

# Register your models here.
# admin.site.register(Category) # to register the Category and the Page model to be viewed in the admin page 


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')


admin.site.register(Page, PageAdmin)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)

#adding the userprofile model
admin.site.register(UserProfile)