from django.db import models
from order.models import Order, OrderItem, SpecialOrder
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

class Bill(models.Model):
    BILL_TYPE_CHOICES = [
        ('order', 'Order'),
        ('special', 'Special Order'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('UP', 'Unpaid'),
        ('PD', 'Paid'),
        ('RF', 'Refunded'),
    ]

    bill_number = models.CharField(max_length=20, unique=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    special_order = models.ForeignKey(SpecialOrder, on_delete=models.CASCADE, null=True, blank=True)
    customer_name = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=2, choices=PAYMENT_STATUS_CHOICES, default='UP')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only generate bill_number if the object is new
            if not self.bill_number:
                self.bill_number = self.generate_bill_number()
        super().save(*args, **kwargs)


    def generate_bill_number(self):
        # Generate a unique bill number in the format YYYYMMDDNNN.
        today = datetime.now()
        date_prefix = today.strftime('%Y%m%d')
        
        # Find the highest number used for today's date
        last_bill = Bill.objects.filter(bill_number__startswith=date_prefix).order_by('-bill_number').first()
        if last_bill:
            last_number = int(last_bill.bill_number[-4:])
        else:
            last_number = 0
        
        # Increment and pad the number
        new_number = str(last_number + 1).zfill(4)
        
        return f"{date_prefix}{new_number}"

    def __str__(self):
        if self.order:
            return f"Bill {self.bill_number} for Order {self.order.order_number}"
        if self.special_order:
            return f"Bill {self.bill_number} for Special Order {self.special_order.order_number}"
        return f"Bill {self.bill_number}"

class BillItem(models.Model):
    BILL_ITEM_TYPE_CHOICES = [
        ('order', 'Order Item'),
        ('special', 'Special Order Item'),
    ]

    bill = models.ForeignKey(Bill, related_name='bill_items', on_delete=models.CASCADE)
    item_type = models.CharField(max_length=10, choices=BILL_ITEM_TYPE_CHOICES)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, null=True, blank=True)
    special_order_item = models.ForeignKey(SpecialOrder, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.item_type == 'order' and self.order_item:
            self.price = self.order_item.get_customized_order_price()
            self.subtotal = self.price * self.quantity
        elif self.item_type == 'special' and self.special_order_item:
            self.price = self.special_order_item.price
            self.subtotal = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        if self.order_item:
            return f"BillItem for {self.order_item.menu_item.name}"
        if self.special_order_item:
            return f"BillItem for {self.special_order_item.order_item}"
        return "BillItem"
