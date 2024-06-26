from django.core.validators import RegexValidator,MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date

phone_regex = RegexValidator(
    regex=r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$',
    message="Phone number must be entered in the format: '+375 (XX) XXX-XX-XX'. Up to 9 digits allowed."
)

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(validators=[phone_regex], max_length=20)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    company = models.CharField(max_length=100,blank=True, null=True)
    date_of_birth = models.DateField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} {'' if self.company is None else self.company}"

    def get_absolute_url(self):
        return reverse('client_detail', args=[str(self.id)])

    class Meta:
        ordering = ['name']

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

class ProductType(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('producttype_detail', args=[str(self.name)])

    class Meta:
        ordering = ['name']

class ProductModel(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('model_detail', args=[str(self.name)])

    class Meta:
        ordering = ['name']

class Product(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, editable=False)
    product_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True)
    product_model = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    production_time = models.DurationField()
    is_producing = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} {self.product_type} {self.product_model} {self.price}"

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])

    class Meta:
        ordering = ['name']

    def delete(self, *args, **kwargs):
        self.is_producing = False
        self.save()

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='main/images',  null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    phone = models.CharField(validators=[phone_regex], max_length=20) 
    email = models.EmailField()
    date_of_birth = models.DateField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('employee_detail', args=[str(self.id)])

    class Meta:
        ordering = ['name']

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.photo = None
        self.save()

class PromoCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    discount = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    times_used = models.PositiveIntegerField(default=0)
    usage_limit = models.PositiveIntegerField()
    valid_until = models.DateField()
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} {self.discount}% {"expired" if self.valid_until<=date.today() else "is valid until " + self.valid_until.strftime('%d-%m-%Y')} {self.usage_limit - self.times_used} times" 

    def get_absolute_url(self):
        return reverse('promocode_detail', args=[str(self.id)])

    class Meta:
        ordering = ['code']

    def delete(self, *args, **kwargs):
        self.is_valid = False
        self.save()

class PickupPoint(models.Model):
    address = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address}"

    def get_absolute_url(self):
        return reverse('pickuppoint_detail', args=[str(self.id)])

    class Meta:
        ordering = ['address']

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField()
    client_name = models.CharField(max_length=100, null=True)
    product_name = models.CharField(max_length=100, null=True)    
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    quantity = models.IntegerField()
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL,blank=True, null=True)

    def __str__(self):
        return f"{self.product_name} {self.client_name} {self.order_date.strftime('%d-%m-%Y')} {self.completion_date.strftime('%d-%m-%Y')} {self.pickup_point}"

        #order_date_utc = self.order_date.astimezone(timezone('UTC'))
        #completion_date_user_tz = localtime(self.completion_date, timezone=self.client.timezone)
        #return f"{self.product_name} {self.client_name} {order_date_utc} {completion_date_user_tz} {self.pickup_point}"

    def get_absolute_url(self):
        return reverse('order_detail', args=[str(self.id)])

    class Meta:
        ordering = ['completion_date']

class Factory(models.Model):
    busy_until = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.busy_until}"

class Reviews(models.Model):
    client_name = models.CharField(max_length=50, default="default")
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review from {self.client.name}'