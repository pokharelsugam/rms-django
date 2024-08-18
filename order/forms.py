from django import forms
from .models import Order, OrderItem, SpecialOrder
from menu.models import Customization, MenuItem

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_type','table','customer_name', 'reservation', 'seating']
        widgets = {
            'customer_name': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity', 'customizations','preparation_instructions']
        help_texts = {
            'customizations': 'Save Order Item and go edit to add customizations.',
        }

        widgets= {
            'customizations': forms.CheckboxSelectMultiple,
        }
        
    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        if 'menu_item' in self.data:
            try:
                menu_item_id = int(self.data.get('menu_item'))
                menu_item = MenuItem.objects.get(id=menu_item_id)
                self.fields['customizations'].queryset = Customization.objects.filter(category=menu_item.category, is_available=True)
            except (ValueError, TypeError, MenuItem.DoesNotExist):
                self.fields['customizations'].queryset = Customization.objects.none()
        elif self.instance.pk:
            menu_item = self.instance.menu_item
            self.fields['customizations'].queryset = Customization.objects.filter(category=menu_item.category, is_available=True)
        else:
            self.fields['customizations'].queryset = Customization.objects.none()
    


class SpecialOrderForm(forms.ModelForm):
    class Meta:
        model = SpecialOrder
        fields = ['order_type','order_item','table', 'customer_name','preparation_instructions', 'quantity', 'price', 'reservation', 'seating']
        widgets = {
            'customer_name': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
