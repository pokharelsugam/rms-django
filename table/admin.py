from django.contrib import admin
from .models import Table,Reservation,Seating

# Register your models here.

admin.site.register(Table)
admin.site.register(Reservation)
admin.site.register(Seating)