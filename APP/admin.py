# admin.py

from django.contrib import admin
from .models import Product, Slider, Profile, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # Number of extra forms to display

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email', 'phone', 'address', 'total_amount')
    inlines = [OrderItemInline]

# Register your models here.
admin.site.register(Product)
admin.site.register(Slider)
admin.site.register(Profile)
