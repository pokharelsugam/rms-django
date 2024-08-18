from django.db import models
from django.utils import timezone
from menu.models import MenuItem, Customization
from user.models import User
from table.models import Table, Reservation, Seating

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('CR', 'Created'),
        ('RC', 'Received'),
        ('IP', 'In Preparation'),
        ('RP', 'Ready for Pickup'),
        ('SR', 'Served'),
        ('RJ', 'Rejected'),
    ]

    ORDER_TYPE_CHOICES = [
        ('DI', 'Dine-In'),
        ('TO', 'Takeout'),
        ('DV', 'Delivery'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('PN', 'Pending'),
        ('UP', 'Unpaid'),
        ('PD', 'Paid'),
        ('RF', 'Refunded'),
    ]


    order_number = models.CharField(max_length=20, unique=True, blank=True)
    customer_name = models.CharField(max_length=100, blank=True)
    order_type = models.CharField(max_length=2, choices=ORDER_TYPE_CHOICES)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    order_status = models.CharField(max_length=2, choices=ORDER_STATUS_CHOICES, default='CR')
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    seating = models.ForeignKey(Seating, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    payment_status = models.CharField(max_length=2, choices=PAYMENT_STATUS_CHOICES, default='PN')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_orders')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_orders', blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        if not self.order_number:
            self.order_number = self.generate_order_number()
        if self.reservation:
            self.customer_name = self.reservation.guest_name
        elif self.seating:
            self.customer_name = self.seating.guest_name
        super().save(*args, **kwargs)

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.orders.all())

    def __str__(self):
        return f"{self.order_number} - {self.customer_name} ({self.get_order_status_display()})"

    def generate_order_number(self):
        last_order = Order.objects.all().order_by('created_at').last()
        if not last_order:
            return 'ORD0001'
        last_number = int(last_order.order_number[3:])
        new_number = last_number + 1
        return f'ORD{new_number:04}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    customizations = models.ManyToManyField(Customization, blank=True, related_name='order_customizations')
    preparation_instructions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.menu_item.name} (x{self.quantity})"
    
    def get_customized_order_price(self):
        base_price = self.menu_item.price
        for customization in self.customizations.all():
            base_price += customization.price
        return base_price

    def get_total_price(self):
        return self.get_customized_order_price() * self.quantity

    @property
    def total_price(self):
        return self.get_total_price()

class SpecialOrder(models.Model):
    ORDER_STATUS_CHOICES = [
        ('CR', 'Created'),
        ('RC', 'Received'),
        ('IP', 'In Preparation'),
        ('RP', 'Ready for Pickup'),
        ('SR', 'Served'),
        ('RJ', 'Rejected'),
    ]

    ORDER_TYPE_CHOICES = [
        ('DI', 'Dine-In'),
        ('TO', 'Takeout'),
        ('DV', 'Delivery'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('PN', 'Pending'),
        ('UP', 'Unpaid'),
        ('PD', 'Paid'),
        ('RF', 'Refunded'),
    ]

    order_number = models.CharField(max_length=20, unique=True, blank=True)
    customer_name = models.CharField(max_length=100, blank=True)
    order_type = models.CharField(max_length=2, choices=ORDER_TYPE_CHOICES)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True, related_name='special_orders')
    order_status = models.CharField(max_length=2, choices=ORDER_STATUS_CHOICES, default='CR')
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, blank=True, related_name='special_orders')
    seating = models.ForeignKey(Seating, on_delete=models.SET_NULL, null=True, blank=True, related_name='special_orders')
    order_item = models.CharField(max_length=255)
    preparation_instructions = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=2, choices=PAYMENT_STATUS_CHOICES, default='PN')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_special_orders')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_special_orders', blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        if not self.order_number:
            self.order_number = self.generate_order_number()
        if self.reservation:
            self.customer_name = self.reservation.guest_name
        elif self.seating:
            self.customer_name = self.seating.guest_name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_number} - {self.customer_name} ({self.get_order_status_display()})"
    
    @property
    def total_price(self):
        return self.price * self.quantity

    def generate_order_number(self):
        last_order = SpecialOrder.objects.all().order_by('created_at').last()
        if not last_order:
            return 'SORD0001'
        last_number = int(last_order.order_number[4:])
        new_number = last_number + 1
        return f'SORD{new_number:04}'