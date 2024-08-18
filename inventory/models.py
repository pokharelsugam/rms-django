from django.db import models
from django.utils import timezone

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    stock_level = models.PositiveIntegerField()
    unit = models.CharField(max_length=50)
    expiration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def is_expired(self):
        return self.expiration_date and self.expiration_date < timezone.now().date()

class IngredientUsage(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    menu_item = models.ForeignKey('menu.MenuItem', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} {self.ingredient.unit} of {self.ingredient.name} for {self.menu_item.name}"
    
    def save(self, *args, **kwargs):
        # Check if the instance already exists in the database
        if self.pk:
            original = IngredientUsage.objects.get(pk=self.pk)
            quantity_difference = self.quantity - original.quantity
        else:
            quantity_difference = self.quantity

        self.ingredient.stock_level -= quantity_difference
        self.ingredient.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.ingredient.stock_level += self.quantity
        self.ingredient.save()
        super().delete(*args, **kwargs)
