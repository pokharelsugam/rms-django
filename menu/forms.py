from django import forms
from .models import Category, Customization,MenuItem
from django.utils.safestring import mark_safe
from django.urls import reverse 


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class CustomizationForm(forms.ModelForm):
    class Meta:
        model = Customization
        fields = ['category','name', 'description', 'price','is_available']        


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'category', 'description', 'price', 'customization', 'is_available']
        widgets = {
            'customization': forms.CheckboxSelectMultiple(),
        }
       
    def __init__(self, *args, **kwargs):
        super(MenuItemForm, self).__init__(*args, **kwargs)
        
        # Help text with the dynamic URL for adding a new category
        self.fields['category'].help_text = mark_safe(
            f'Need a new category? <a href="{reverse("category_add")}">Click Here</a>'
        )
        
        # Adjust the queryset for the customization field based on the instance's category
        if self.instance.pk:
            self.fields['customization'].queryset = Customization.objects.filter(category=self.instance.category)
        else:
            self.fields['customization'].queryset = Customization.objects.none() 


