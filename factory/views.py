from django.views import View
from django.shortcuts import render, redirect
from .forms import RegistrationForm,ClientForm, EmployeeForm
from django.contrib.auth.models import User, Group
from .models import Product, ProductType, Client, Employee 

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
