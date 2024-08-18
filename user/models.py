from django.db import models
from django.contrib.auth.models import AbstractUser,Group
from phonenumber_field.modelfields import PhoneNumberField
import os

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique = True)
    phone_no = PhoneNumberField(unique = True)
    is_admin = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_waiter = models.BooleanField(default=False)
    is_chef = models.BooleanField(default=False)
    is_cashier = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['email','phone_no', 'first_name', 'last_name']

    # Override save method to set admin flag for superuser and assign groups
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_admin = True
        super().save(*args, **kwargs)

        # Assign user to the appropriate group
        
        if self.is_admin:
            group, created = Group.objects.get_or_create(name='Admin')
            self.groups.add(group)
        elif self.is_manager:
            group, created = Group.objects.get_or_create(name='Manager')
            self.groups.add(group)
        elif self.is_waiter:
            group, created = Group.objects.get_or_create(name='Waiter')
            self.groups.add(group)
        elif self.is_chef:
            group, created = Group.objects.get_or_create(name='Chef')
            self.groups.add(group)
        elif self.is_cashier:
            group, created = Group.objects.get_or_create(name='Cashier')
            self.groups.add(group)

    def __str__(self):
        full_name = f'{self.first_name} {self.last_name}'
        return f'{self.username} ({full_name})'        