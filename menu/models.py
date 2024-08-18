from django.db import models
from inventory.models import Ingredient, IngredientUsage

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Customization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='customizations')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} ({self.price})'

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null= True, related_name='items')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    customization = models.ManyToManyField(Customization, blank=True)
    is_available = models.BooleanField(default=True)
    ingredients = models.ManyToManyField(Ingredient, through= IngredientUsage, related_name='menu_items')

    def __str__(self):
        return self.name
    
    def get_customized_price(self):
        customized_price = self.price
        for customization in self.customization.all():
            customized_price += customization.price
        return customized_price

