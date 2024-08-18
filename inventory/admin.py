from django.contrib import admin
from .models import Ingredient,IngredientUsage

# Register your models here.
admin.site.register(Ingredient)
admin.site.register(IngredientUsage)