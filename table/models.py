from django.db import models
from django.utils import timezone
from user.models import User
from django.core.exceptions import ValidationError

# Create your models here.

class Table(models.Model):
    TABLE_STATUS_CHOICES = [
        ('A', 'Available'),
        ('O', 'Occupied'),
        ('R', 'Reserved'),
    ]

    table_number = models.CharField(max_length=10, unique=True)
    capacity = models.PositiveIntegerField()
    table_status = models.CharField(max_length=1, choices=TABLE_STATUS_CHOICES, default='A')

    def __str__(self):
        return f"Table {self.table_number} ({self.get_table_status_display()})"
    
    def update_table_status(self):
        now = timezone.localtime()
        current_reservations = self.reservations.filter(
            reservation_date=now.date(),
            start_time__lte=now.time(),
            end_time__gte=now.time()
        )
        current_seatings = self.seatings.filter(
            start_time__lte=now.time(),
            end_time__isnull=True
        ) | self.seatings.filter(
            start_time__lte=now.time(),
            end_time__gte=now.time()
        )

        if current_seatings.exists():
            self.table_status = 'O'
        elif current_reservations.exists():
            self.table_status = 'R'
        else:
            self.table_status = 'A'
        self.save()

class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations')
    guest_name = models.CharField(max_length=100)
    guest_count = models.PositiveIntegerField()
    reservation_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    reserved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='handled_reservations')

    def __str__(self):
        return f"Guest: {self.guest_name} ({self.table.table_number}, {self.reservation_date} - {self.start_time})"
    
    def clean(self):
        # Check for overlapping reservations
        overlapping_reservations = Reservation.objects.filter(
            table=self.table,
            reservation_date=self.reservation_date,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(pk=self.pk)
        if overlapping_reservations.exists():
            raise ValidationError("This table is already reserved for the specified time period.")
        
        # Check if guest count exceeds table capacity
        if self.guest_count > self.table.capacity:
            raise ValidationError("Guest count exceeds the table capacity.")

    def save(self, *args, **kwargs):
        self.clean()  # Ensure validation is checked before saving
        super().save(*args, **kwargs)
        self.table.update_table_status()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.table.update_table_status()

class Seating(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='seatings')
    guest_name = models.CharField(max_length=100)
    guest_count = models.PositiveIntegerField()
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(blank=True, null=True)
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='handled_seatings')

    def __str__(self):
        return f"Guest: {self.guest_name} ({self.table.table_number}, {self.guest_count}, {self.start_time})"

    @property
    def is_occupied(self):
        return self.end_time is None
    
    def clean(self):
        # Check for overlapping seatings
        overlapping_seatings = Seating.objects.filter(
            table=self.table,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(pk=self.pk)
        if overlapping_seatings.exists():
            raise ValidationError("This table is already occupied for the specified time period.")
        
        # Check if guest count exceeds table capacity
        if self.guest_count > self.table.capacity:
            raise ValidationError("Guest count exceeds the table capacity.")

    def save(self, *args, **kwargs):
        self.clean()  # Ensure validation is checked before saving
        super().save(*args, **kwargs)
        self.table.update_table_status()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.table.update_table_status()