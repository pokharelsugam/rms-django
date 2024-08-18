from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from staff.models import Staff

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_no = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    employee_id = forms.CharField(required=True)
    address = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no', 'password1', 'password2', 'first_name', 'last_name', 'is_manager', 'is_waiter', 'is_chef', 'is_cashier']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Staff.objects.create(user=user, employee_id=self.cleaned_data['employee_id'], address=self.cleaned_data['address'])
        return user
