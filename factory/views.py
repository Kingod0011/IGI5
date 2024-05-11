from django.views import View
from django.views.generic import ListView, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm,ClientForm, EmployeeForm, OrderForm
from django.contrib.auth.models import User, Group
from .models import Product, ProductType, Client, Employee, Order, PromoCode, Factory
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from functools import wraps
from django.http import HttpResponse, HttpResponseBadRequest
from datetime import date, timedelta




def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            if bool(request.user.groups.filter(name__in=group_names)) or request.user.is_superuser:
                return view_func(self, request, *args, **kwargs)
            else:
                raise PermissionDenied
        return _wrapped_view
    return decorator

employee_required = group_required('Employees')
client_required = group_required('Clients')


#@method_decorator(client_required, name='dispatch')
@login_required
def order_create(request, product_id):
    
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Clients').exists():
            if request.method == 'POST':
                form = OrderForm(request.POST)
                if form.is_valid():
                    order = form.save(commit=False)
                    promo = form.cleaned_data['promo']
                    promo_code = PromoCode.objects.filter(code=promo).first()
                    order.promo_code = promo_code
                    if order.promo_code:
                        promo_code.times_used+=1
                        if(promo_code.usage_limit == promo_code.times_used):
                            promo_code.is_valid = False
                        promo_code.save()
                    factory = Factory.objects.first()
                    form.instance.client = request.user.client
                    order.client = request.user.client
                    order.product = get_object_or_404(Product, id=product_id)
                    order.client_name = request.user.client.company if request.user.client.company is not None else request.user.client.name
                    order.product_name = order.product.name
                    factory.busy_until += timedelta(seconds=int(order.quantity * order.product.production_time.total_seconds() * (1 if not order.promo_code else (order.promo_code.discount/100.))))
                    order.completion_date = factory.busy_until
                    order.save()
                    factory.save()
                    return HttpResponse(f'Ваш заказ будет готов: {factory.busy_until}')
            else:
                form = OrderForm()
            return render(request, 'order_create.html', {'form': form})
        else:
            return redirect('login')
    else:
        return redirect('login')
    
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