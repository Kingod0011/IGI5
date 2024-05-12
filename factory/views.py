from django.views import View
from django.views.generic import ListView, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm,ClientForm, EmployeeForm, OrderForm
from django.contrib.auth.models import User, Group
from .models import Product, ProductType, Client, Employee, Order, PromoCode, Factory, ProductModel, Reviews
from django.db.models import Q, Count, Sum
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.utils.decorators import method_decorator
from functools import wraps
from django.http import HttpResponse, HttpResponseBadRequest
from datetime import date, timedelta
from itertools import groupby
from django.utils.timezone import now
from collections import Counter
from statistics import mean, mode, median, StatisticsError

def reviews_list(request):
    reviews = Reviews.objects.all()
    return render(request, 'reviews.html', {'reviews': reviews})

def promocode_list(request):
    promocodes = PromoCode.objects.filter()
    return render(request, 'promocodes.html', {'promocodes': promocodes})

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees.html', {'employees': employees})

def all_modes(data):
    counts = Counter(data)
    max_count = max(counts.values())
    modes = [number for number, count in counts.items() if count == max_count]
    return modes  

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


class StatisticView(View):
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('login')
        
        sales_values = list(Order.objects.values_list('price', flat=True))
        total_sales = sum(sales_values)
        sales_avg = mean(sales_values)
        sales_modes = all_modes(sales_values)
        sales_median = median(sales_values)

        date_values = list(Client.objects.values_list('date_of_birth', flat=True))
        age_values = [calculate_age(birth_date) for birth_date in date_values]
        age_avg = mean(age_values)
        age_median = median(age_values)

        popular_product_type = Product.objects.values('product_type').annotate(total=Count('product_type')).order_by('-total').first()
        most_profitable_product_type = Product.objects.values('product_type').annotate(total_profit=Sum('order__price')).order_by('-total_profit').first()
        products_by_orders = Product.objects.annotate(total_orders=Count('order')).order_by('-total_orders')
        monthly_sales = Order.objects.filter(order_date__gte=now()-timedelta(days=30)).values('product__product_type').annotate(total=Sum('quantity'))
        yearly_sales = Order.objects.filter(order_date__gte=now()-timedelta(days=365))

        context = {
            'total_sales': total_sales,
            'sales_avg': sales_avg,
            'sales_modes': sales_modes,
            'sales_median': sales_median,
            'age_avg': age_avg,
            'age_median': age_median,
            'popular_product_type': popular_product_type,
            'most_profitable_product_type': most_profitable_product_type,
            'products_by_orders': products_by_orders,
            'monthly_sales': monthly_sales,
            'yearly_sales': yearly_sales,
        }
        return render(request, 'statistic.html', context)


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
                    factory.busy_until += timedelta(seconds=int(order.quantity * order.product.production_time.total_seconds() ))
                    order.completion_date = factory.busy_until
                    order.price = order.quantity * order.product.price * (1 if not order.promo_code else (order.promo_code.discount/100.))
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
        productmodels = ProductModel.objects.all()  # Добавляем модели продуктов
        is_employee = request.user.groups.filter(name='Employees').exists() if request.user.is_authenticated else False
        is_superuser = request.user.is_superuser if request.user.is_authenticated else False
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')
        product_type = request.GET.get('producttype')
        product_model = request.GET.get('productmodel')  # Добавляем фильтр по модели продукта
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
            if product_model:  # Применяем фильтр по модели продукта
                products = products.filter(product_model=product_model)
        context = {
            'products': products,
            'producttypes': producttypes,
            'productmodels': productmodels,  # Добавляем модели продуктов в контекст
            'is_employee': is_employee,
            'is_superuser': is_superuser,
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clients = Client.objects.all().order_by('city')
        context['clients_by_city'] = {k: list(v) for k, v in groupby(clients, key=lambda x: x.city)}
        return context


class OrderListView(ListView):
    model = Order
    template_name = 'orders.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'orders'