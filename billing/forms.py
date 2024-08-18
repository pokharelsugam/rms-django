from django import forms
from .models import BillItem
from order.models import Order, SpecialOrder

class BillItemForm(forms.ModelForm):
    class Meta:
        model = BillItem
        fields = ['item_type', 'order_item', 'special_order_item', 'quantity', 'price', 'subtotal']
        widgets = {
            'order_item': forms.HiddenInput(),
            'special_order_item': forms.HiddenInput(),
        }

class BillGenerationForm(forms.Form):
    BILL_TYPE_CHOICES = [
        ('order', 'Order'),
        ('special', 'Special Order'),
    ]

    bill_type = forms.ChoiceField(choices=BILL_TYPE_CHOICES)
    order_number = forms.CharField(max_length=20, label='Order Number')

    def clean(self):
        cleaned_data = super().clean()
        bill_type = cleaned_data.get('bill_type')
        order_number = cleaned_data.get('order_number')

        if bill_type == 'order':
            if not Order.objects.filter(order_number=order_number).exists():
                raise forms.ValidationError("Order with this number does not exist.")
        elif bill_type == 'special':
            if not SpecialOrder.objects.filter(order_number=order_number).exists():
                raise forms.ValidationError("Special Order with this number does not exist.")

        return cleaned_data