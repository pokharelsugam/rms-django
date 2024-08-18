from django import forms
from .models import Ingredient, IngredientUsage

class IngredientForm(forms.ModelForm):
    expiration_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Ingredient
        fields = ['name', 'description', 'stock_level', 'unit', 'expiration_date']

class IngredientUsageForm(forms.ModelForm):
    class Meta:
        model = IngredientUsage
        fields = ['ingredient', 'menu_item', 'quantity']
