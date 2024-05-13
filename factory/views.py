from django.views import View
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm,ClientForm, EmployeeForm, OrderForm, ReviewForm
from django.contrib.auth.models import User, Group
from .models import Product, ProductType, Client, Employee, Order, PromoCode, Factory, ProductModel, Reviews
from django.db.models import Q, Count, Sum
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from functools import wraps
from django.http import HttpResponse, HttpResponseBadRequest
from datetime import date, timedelta, datetime
from itertools import groupby
from django.utils.timezone import now
from collections import Counter
import requests
from statistics import mean, mode, median, StatisticsError
import matplotlib.pyplot as plt
import matplotlib
import random
import logging
import time
from django.contrib.staticfiles.storage import staticfiles_storage
from decimal import Decimal

logger = logging.getLogger(__name__)

def superuser_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_superuser,
        login_url='/login/',
        redirect_field_name=None
    )
    if function:
        return actual_decorator(function)
    return actual_decorator



class ClientsOnlyView(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Clients').exists()

class EmployeesOrSuperuserView(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Employees').exists() or self.request.user.is_superuser

class EmployeesOrClientsView(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Employees').exists() or self.request.user.groups.filter(name='Clients').exists()

class AnonymousRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated

class SuperuserOnlyView(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

def add_review_view(request):
    error = ''
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user.client
            review.client_name = request.user.client.name 
            review.save()
            return redirect('reviews')
        else:
            error = 'Форма была неверной'

    form = ReviewForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'add_review.html', data)


def in_clients_group(user):
    return user.groups.filter(name='Clients').exists()

def in_employees_group(user):
    return user.groups.filter(name='Employees').exists()

@login_required
@superuser_required
def add_random_client(request):
    response = requests.get('https://randomuser.me/api/')
    data = response.json()
    user_data = data['results'][0]
    username = user_data['login']['username']
    password = 'password'
    name = user_data['name']['first'] + " " + user_data['name']['last']
    dob = datetime.strptime(user_data['dob']['date'], "%Y-%m-%dT%H:%M:%S.%fZ").date()
    part1 = random.randint(10, 99)
    part2 = random.randint(100, 999)
    part3 = random.randint(10, 99)
    part4 = random.randint(10, 99)
    phone = f"+375 ({part1}) {part2}-{part3}-{part4}"
    address = f"{user_data['location']['street']['name']} {user_data['location']['street']['number']}"
    city = user_data['location']['city']
    company = "Silly Socks"
    user = User.objects.create_user(username=username, password=password)
    group = Group.objects.get(name='Clients')  
    user.groups.add(group)
    client = Client(user=user, name=name, date_of_birth=dob, address=address, phone=phone, city=city, company=company)
    client.save()
    logging.info("Add new client")
    return redirect('/main/')

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


class StatisticView(SuperuserOnlyView,View):
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

        data=Product.objects.values('product_type').annotate(total_profit=Sum('order__price')).order_by('-total_profit')

        product_types = [item['product_type'] for item in data]
        total_profits = [item['total_profit'] for item in data]
        print(staticfiles_storage.url('my_plot2.png'))
        #plt.bar(product_types, total_profits)
        #plt.xlabel('Product')
        #plt.ylabel('Total Orders')
        #plt.title('Total Orders by Product')
        #plt.savefig('static/my_plot2.png')

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
            'yearly_sales': yearly_sales
        }
        return render(request, 'statistic.html', context)

@login_required
@user_passes_test(in_clients_group)
def order_create(request, product_id):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Clients').exists():
            if request.method == 'POST':
                form = OrderForm(request.POST)
                if form.is_valid():
                    order = form.save(commit=False)
                    promo = form.cleaned_data['promo']
                    promo_code = PromoCode.objects.filter(code=promo).first()
                    print(promo_code)
                    print(promo)
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
                    discount = 1 if not order.promo_code else (order.promo_code.discount/Decimal(100.))
                    order.price = order.quantity * order.product.price * discount
                    order.save()
                    factory.save()
                    logging.info("Add new order")
                    return HttpResponse(f'Ваш заказ будет готов: {factory.busy_until}')
            else:
                form = OrderForm()
                logging.info("Submitting an order creation form")
            return render(request, 'order_create.html', {'form': form})
        else:
            logging.warning("Attempt to create an order by someone other than the client")
            return redirect('login')
    else:
        logging.warning("Unauthorized user")
        return redirect('login')
    
class RegistrationView(AnonymousRequiredMixin, View):
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
                logging.info("Add new client")
                return redirect('/')
            else:
                print(form.errors)
        else:
            logging.info("Submitting an order registration form")
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




class ProfileView(EmployeesOrClientsView, View):
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

class EditProfileView(EmployeesOrClientsView, View):
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
                    logging.info("Edit info")
                    return redirect('profile')
            else:
                form = FormClass(instance=instance)

            return render(request, template_name, {'form': form})
        else:
            return redirect('login')

    get = handle_request
    post = handle_request


class ClientListView(EmployeesOrSuperuserView, ListView):
    model = Client
    template_name = 'clients.html'  
    context_object_name = 'clients'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clients = Client.objects.all().order_by('city')
        context['clients_by_city'] = {k: list(v) for k, v in groupby(clients, key=lambda x: x.city)}
        return context


class OrderListView(EmployeesOrSuperuserView, ListView):
    model = Order
    template_name = 'orders.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'orders'