from django.db import models
from django.contrib.auth.models import User

# Define your models here without importing each other

from django.shortcuts import render, redirect

from django.shortcuts import get_object_or_404, redirect


def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        # Perform cancellation logic (e.g., delete the order)
        order.delete()
        # Redirect to a success page or reload the my_orders page
        return redirect('my_orders')
    
    # Handle GET request (usually to confirm cancellation)
    context = {
        'order': order
    }
    return render(request, 'cancel_order.html', context)


def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    context = {
        'orders': orders
    }
    return render(request, 'my_orders.html', context)


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('VEG', 'Vegetables'),
        ('ICE', 'Ice creams'),
        ('FRU', 'Fruits'),
        ('GRO', 'Groceries'),
    ]
    
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300, default='')
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ImageField(upload_to='images/', null=True)
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES, default='VEG')
    in_stock = models.BooleanField(default=True)  # New field for stock availability

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    email = models.EmailField(default='your_email@example.com')
    phone = models.CharField(max_length=15, default='1234567890')
    address = models.TextField(default='Default Address')

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

class Slider(models.Model):
    image = models.ImageField(upload_to='slider_images/')
    description = models.TextField()

    def __str__(self):
        return self.description
