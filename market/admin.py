from django.contrib import admin
from .models import Product,orders,OrderUpdate

# Register your models here.
admin.site.register(Product)
admin.site.register(orders)
admin.site.register(OrderUpdate)

