from django import forms
from django.core.exceptions import ValidationError
from .models import Client, Employee, Order, PromoCode
from django.contrib.auth.models import User
from datetime import date, timedelta

class OrderForm(forms.ModelForm):    
    promo = forms.CharField(required=False,widget=forms.TextInput(attrs={'required': False}))  
    class Meta:
        model = Order
        fields = ['quantity', 'pickup_point']

    def clean_promo(self):
        promo = self.cleaned_data.get('promo')
        if promo:
            promo_code_obj = PromoCode.objects.filter(code=promo).first()
            if not promo_code_obj:
                raise ValidationError('There is no such promo code')
            else:
                if not promo_code_obj.is_valid:
                    raise ValidationError('Promo code is not valid')
                if promo_code_obj.valid_until  < date.today():
                    promo_code_obj.is_valid=False
                    raise ValidationError('Promo code has expired')
        return promo
                

class RegistrationForm(forms.ModelForm):
    login = forms.CharField(widget=forms.TextInput(attrs={'required': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': True}))

    class Meta:
        model = Client
        fields = ['name', 'phone', 'city', 'address', 'company', 'date_of_birth']
        widgets = {
            'login': forms.TextInput(attrs={'required': True}),
            'password': forms.TextInput(attrs={'required': True}),
            'name': forms.TextInput(attrs={'required': True}),
            'phone': forms.TextInput(attrs={'required': True, 'pattern': r'\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}'}),
            'city': forms.TextInput(attrs={'required': True}),
            'address': forms.TextInput(attrs={'required': True}),
            'company': forms.TextInput(),
            'date_of_birth': forms.DateInput(attrs={'required': True, 'type': 'date'}),
        }

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob > date.today():
            raise ValidationError('Date of birth cannot be in the future')
        if dob > date.today() - timedelta(days=18*365):
            raise ValidationError('Client must be at least 18 years old')
        return dob

    def clean_login(self):
        login = self.cleaned_data.get('login')
        if User.objects.filter(username=login).exists():
            raise ValidationError('Пользователь с таким именем уже существует')
        else:
            return login

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone', 'city', 'address', 'company', 'date_of_birth']

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('date_of_birth'):
            raise ValidationError("Incorrect input")
        if not cleaned_data.get('name') or not cleaned_data.get('phone') or not cleaned_data.get('city') or not cleaned_data.get('address') or not cleaned_data.get('date_of_birth'):
            raise ValidationError("All fields except 'company' must be filled.")
        if cleaned_data.get('date_of_birth') > date.today() - timedelta(days=18*365):
            raise ValidationError("User must be over 18 years old.")

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'photo', 'description', 'phone', 'email', 'date_of_birth']

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('name') or not cleaned_data.get('phone') or not cleaned_data.get('email') or not cleaned_data.get('date_of_birth'):
            raise ValidationError("All fields except 'photo' and 'description' must be filled.")
        if cleaned_data.get('date_of_birth') > date.today() - timedelta(days=18*365):
            raise ValidationError("User must be over 18 years old.")


