from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import datetime
from authentication.models import Address

# Create your models here.

class Product(models.Model):
    class Brand(models.TextChoices):
        BenAndJerrys = 'Ben & Jerry\'s', 'Ben & Jerry\'s'
        Magnum = 'Magnum', 'Magnum'
        DairyQueen = 'Dairy Queen', 'Dairy Queen'

    BRAND_CHOICES = [
        ('BenAndJerrys', 'Ben & Jerry\'s'),
        ('Magnum', 'Magnum'),
        ('DairyQueen', 'Dairy Queen'),
    ]

    class Category(models.TextChoices):
        IceCream = 'Ice Cream', 'Ice Cream'
        Gelato = 'Gelato', 'Gelato'
        IceCreamBars = 'Ice Cream Bars', 'Ice Cream Bars'

    CATEGORY_CHOICES = [
        ('IceCream', 'Ice Cream'),
        ('Gelato', 'Gelato'),
        ('IceCreamBars', 'Ice Cream Bars'),
    ]

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', default="vinod")
    description = models.TextField()
    price = models.FloatField()
    image_url = models.ImageField(upload_to='products/images/')
    # brand = models.CharField(max_length=50, choices=Brand.choices, default=Brand.Magnum)
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES, default=Brand.Magnum)
    # category = models.CharField(max_length=50, choices=Category.choices, default=Category.IceCream)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=Category.IceCream)
    created_at = models.DateTimeField(auto_now_add=True)

    # Automatically populate the slug field based on the name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
        ('refunded', 'Refunded'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='orders', null=True)
    currency = models.CharField(max_length=10, default='INR')
    receipt = models.CharField(max_length=128, unique=True, editable=False, null=True, blank=True)
    total = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, default='pending')
    order_id = models.CharField(max_length=128, unique=True, editable=False, null=False)
    razorpay_order_id = models.CharField(max_length=128, editable=False, null=False, blank=True, default="")
    amount_paid = models.FloatField(default=0.0, blank=True, null=False)
    amount_due = models.FloatField(default=0.0, blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            today = datetime.today().strftime('%d%m%y')  # Get today's date as DDMMYYYY
            order_count = Order.objects.filter(created_at__date=datetime.today().date()).count() + 1
            sequence_number = f"{order_count:03}"  # Format sequence as a 3-digit number
            self.order_id = f"ICE_CREAM_{today}_{sequence_number}"
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} - {self.status}"


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_items')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.FloatField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"OrderItem {self.id}: {self.product.name} x {self.quantity} = {self.price * self.quantity}"
    

# class Transaction(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('completed', 'Completed'),
#         ('failed', 'Failed'),
#         ('refunded', 'Refunded'),
#     ]

#     PAYMENT_METHOD_CHOICES = [
#         ('credit_card', 'Credit Card'),
#         ('debit_card', 'Debit Card'),
#         ('paypal', 'PayPal'),
#         ('bank_transfer', 'Bank Transfer'),
#         ('cash_on_delivery', 'Cash on Delivery'),
#     ]

#     id = models.AutoField(primary_key=True)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transactions')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
#     amount = models.FloatField()
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
#     payment_id = models.CharField(max_length=100, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Transaction details {self.payment_id} - {self.status} - Amount paid: {self.amount}"
    

class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CartItem {self.id}: {self.product.name} - {self.price} x {self.quantity} = {self.price * self.quantity}"
    
class Enquiry(models.Model):
    class Meta:
        verbose_name_plural = "Enquiries"
        
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enquiries', default=None, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile = models.CharField(max_length=10)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='enquiries')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Enquiry from: {self.first_name} {self.last_name} on {self.product.name}"