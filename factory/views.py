from django.views import View
from django.views.generic import ListView
from django.shortcuts import render, redirect
from .forms import RegistrationForm,ClientForm, EmployeeForm
from django.contrib.auth.models import User, Group
from .models import Product, ProductType, Client, Employee, Order 
from django.db.models import Q

class RegistrationView(View):
    def handle_request(self, request):
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = User.objects.create_user(username=form.cleaned_data['login'], password=form.cleaned_data['password'])
                client = form.save(commit=False)            
                group = Group.objects.get(name='Clients')  
                user.groups.add(group)
                client.user = user
                client.save()
                return redirect('/')
            else:
                print(form.errors)
        else:
            form = RegistrationForm()

        return render(request, 'register.html', {'form': form})

    get = handle_request
    post = handle_request


class HomePageView(View):
    def get(self, request):
        products = Product.objects.all()
        producttypes = ProductType.objects.all()
        is_employee = request.user.groups.filter(name='Employees').exists() if request.user.is_authenticated else False
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')
        product_type = request.GET.get('producttype')
        search = request.GET.get('search')

        
        if search:
            products = products.filter(Q(name__icontains=search))
        else:
            if price_min and price_min.isdigit():
                products = products.filter(price__gte=price_min)
            if price_max and price_max.isdigit():
                products = products.filter(price__lte=price_max)
            if product_type:
                products = products.filter(product_type=product_type)
        context = {
            'products': products,
            'producttypes': producttypes,
            'is_employee': is_employee,
        }
        return render(request, 'home.html', context)


class ProfileView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.groups.filter(name='Clients').exists():
                form = ClientForm(instance=request.user.client)
                template_name = 'client_view.html'
            elif request.user.groups.filter(name='Employees').exists():
                form = EmployeeForm(instance=request.user.employee)
                template_name = 'employee_view.html'
            else:
                return redirect('login')
            return render(request, template_name, {'form': form})
        else:
            return redirect('login')

class EditProfileView(View):
    def handle_request(self, request):
        if request.user.is_authenticated:
            if request.user.groups.filter(name='Clients').exists():
                instance = request.user.client
                FormClass = ClientForm
                template_name = 'client_edit.html'
            elif request.user.groups.filter(name='Employees').exists():
                instance = request.user.employee
                FormClass = EmployeeForm
                template_name = 'employee_edit.html'
            else:
                return redirect('login')

            if request.method == 'POST':
                form = FormClass(request.POST, request.FILES, instance=instance)
                if form.is_valid():
                    form.save()
                    return redirect('profile')
            else:
                form = FormClass(instance=instance)

            return render(request, template_name, {'form': form})
        else:
            return redirect('login')

    get = handle_request
    post = handle_request

class ClientListView(ListView):
    model = Client
    template_name = 'clients.html'  
    context_object_name = 'clients'
    ordering = ['name']

class OrderListView(ListView):
    model = Order
    template_name = 'orders.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'orders'