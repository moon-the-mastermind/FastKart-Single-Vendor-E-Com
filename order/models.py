from django.db import models
from django.conf import settings
from product.models import Product
import uuid

def generate_order_num():
    return f"ORD-{uuid.uuid4.hex[:8].upper()}"


class Order(models.Model):
    PAYMENT_METHOD_CHOICE = [
        ("bkash", "Bkash"),
        ("nogod", "Nogod"),
        ("rocket", "Rocket"),
        ("upay", "Upay"),
        ("skrill", "Skril"),
        ("paypal", "Paypal"),
        ("bank", "Bank")
    ]
    PAYMENT_STATUS_CHOICE = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("canceled", "Canceled")
    ]
    ORDER_STATUS_CHOICE = [
        ("pending", "Pending"),
        ("received", "Received"),
        ("returned", "Returned"),
        ("canceled", "Canceled")
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="order")
    order_num = models.CharField(max_length=100, unique=True, editable=False, default = generate_order_num)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    customer_mobile = models.CharField(max_length=20, null=True, blank=True)
    shipping_address = models.TextField(null=True, blank=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICE, default="bkash")
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICE, default="pending" )
    order_status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICE, default="pending" )
    note = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.order_num} - {self.user.username}"

    # def save(self, *args, **kwargs):
    #     items = Order.order_items.all()
        

    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="ordered_product")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.PositiveIntegerField(default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount= models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    note = models.TextField(null=True, blank= True)

    def __str__(self):
        return f"{self.product.name}x{self.quantity}"
    
    def save(self, *args, **kwargs):
        product = self.product
        price = self.price
        if product.discount_percent and product.discount_percent > 0:
            discounted_price = price - (price * product.discount_percent/100)
            total = discounted_price * self.quantity
            discount = price * product.discount_percent/100
        else:
            total = price * self.quantity
            discount = 0
        
        self.price = price
        self.discount = discount
        self.total_amount = total

        super().save(*args, **kwargs)
    

        

