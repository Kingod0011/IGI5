from django.contrib import admin
from .models import Client, ProductType, ProductModel, Product, Employee, PromoCode, PickupPoint, Order, Factory, Reviews

admin.site.register(Client)
admin.site.register(ProductType)
admin.site.register(ProductModel)
admin.site.register(Product)
admin.site.register(Employee)
admin.site.register(PromoCode)
admin.site.register(PickupPoint)
admin.site.register(Order)
admin.site.register(Factory)
admin.site.register(Reviews)