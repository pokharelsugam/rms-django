from django.contrib import admin
from .models import Category, MenuItem, Customization

# Register your models here.

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Customization)

