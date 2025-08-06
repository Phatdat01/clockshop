from django.contrib import admin
from .models import Product, Order, OrderItem, ShipingAddress, Category

# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShipingAddress)
admin.site.register(Category)
