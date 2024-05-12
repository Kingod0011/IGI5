from django.contrib import admin
from .models import Client, ProductType, ProductModel, Product, Employee, PromoCode, PickupPoint, Order, Factory, Reviews

class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'city', 'address', 'company', 'date_of_birth', 'is_deleted']
    list_filter = ['city', 'company', 'is_deleted']
    search_fields = ['name', 'phone']

class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'product_type', 'product_model', 'price', 'production_time', 'is_producing']
    list_filter = ['product_type', 'product_model', 'is_producing']
    search_fields = ['name', 'code']

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'date_of_birth', 'is_deleted']
    list_filter = ['is_deleted']
    search_fields = ['name', 'phone', 'email']

class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'times_used', 'usage_limit', 'valid_until', 'is_valid']
    list_filter = ['is_valid']
    search_fields = ['code']

class PickupPointAdmin(admin.ModelAdmin):
    list_display = ['address', 'is_deleted']
    list_filter = ['is_deleted']
    search_fields = ['address']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_date', 'completion_date', 'client_name', 'product_name', 'client', 'product', 'pickup_point', 'price', 'quantity', 'promo_code']
    list_filter = ['client', 'product', 'pickup_point', 'promo_code']
    search_fields = ['client_name', 'product_name']

class FactoryAdmin(admin.ModelAdmin):
    list_display = ['busy_until']

class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client', 'text', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['client_name', 'text']

admin.site.register(Client, ClientAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(ProductModel, ProductModelAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(PromoCode, PromoCodeAdmin)
admin.site.register(PickupPoint, PickupPointAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Factory, FactoryAdmin)
admin.site.register(Reviews, ReviewsAdmin)
