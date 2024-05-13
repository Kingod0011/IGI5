from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Client, Product, Order, PromoCode, Factory, ProductModel, Reviews
import datetime
from django.test import TestCase
from django.test import Client as Cli

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Client as ClientModel, ProductType, ProductModel, Product, PromoCode, PickupPoint, Order
from datetime import datetime, timedelta

class RegistrationViewTest(TestCase):
    def test_registration_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

class HomePageViewTest(TestCase):
    def test_home_page_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

class ProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='testuser', password='12345')
        test_user = User.objects.get(id=1)
        group = Group.objects.create(name='Clients')
        test_user.groups.add(group)
        ClientModel.objects.create(user=test_user, name='Test Client', phone='+375 (29) 123-45-67', city='Test City', address='Test Address', date_of_birth=datetime.now())

    def test_profile_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

class EditProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='testuser', password='12345')
        test_user = User.objects.get(id=1)
        group = Group.objects.create(name='Clients')
        test_user.groups.add(group)
        ClientModel.objects.create(user=test_user, name='Test Client', phone='+375 (29) 123-45-67', city='Test City', address='Test Address', date_of_birth=datetime.now())

    def test_edit_profile_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)

class ClientListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='testuser', password='12345')
        test_user = User.objects.get(id=1)
        group = Group.objects.create(name='Employees')
        test_user.groups.add(group)
        ClientModel.objects.create(user=test_user, name='Test Client', phone='+375 (29) 123-45-67', city='Test City', address='Test Address', date_of_birth=datetime.now())

    def test_client_list_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('clients'))
        self.assertEqual(response.status_code, 200)


from django.test import TestCase
from .forms import RegistrationForm, ClientForm, EmployeeForm
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class RegistrationFormTest(TestCase):
    def test_registration_form(self):
        form_data = {'login': 'testuser', 'password': '12345', 'name': 'Test Client', 'phone': '+375 (29) 123-45-67', 'city': 'Test City', 'address': 'Test Address', 'date_of_birth': datetime.now() - timedelta(days=20*365)}
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

class ClientFormTest(TestCase):
    def test_client_form(self):
        form_data = {'name': 'Test Client', 'phone': '+375 (29) 123-45-67', 'city': 'Test City', 'address': 'Test Address', 'date_of_birth': datetime.now() - timedelta(days=20*365)}
        form = ClientForm(data=form_data)
        self.assertTrue(form.is_valid())

class EmployeeFormTest(TestCase):
    def test_employee_form(self):
        form_data = {'name': 'Test Employee', 'phone': '+375 (29) 123-45-67', 'email': 'testemployee@example.com', 'date_of_birth': datetime.now() - timedelta(days=20*365)}
        form = EmployeeForm(data=form_data)
        self.assertTrue(form.is_valid())


from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Client, ProductType, ProductModel, Product, Employee, PromoCode, PickupPoint, Order, Factory, Reviews
from .forms import OrderForm
from django.contrib.auth.models import User
from datetime import datetime, timedelta



class ClientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='testuser', password='12345')
        test_user = User.objects.get(id=1)
        Client.objects.create(user=test_user, name='Test Client', phone='+375 (29) 123-45-67', city='Test City', address='Test Address', date_of_birth=datetime.now())

    def test_client_content(self):
        client = Client.objects.get(id=1)
        expected_object_name = f'{client.name}'
        self.assertEqual(expected_object_name, 'Test Client')

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Client, ProductType, ProductModel, Product, Employee, PromoCode, PickupPoint, Order, Factory, Reviews
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class ClientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='testuser', password='12345')
        test_user = User.objects.get(id=1)
        Client.objects.create(user=test_user, name='Test Client', phone='+375 (29) 123-45-67', city='Test City', address='Test Address', date_of_birth=datetime.now())

    def test_client_content(self):
        client = Client.objects.get(id=1)
        expected_object_name = f'{client.name}'
        self.assertEqual(expected_object_name, 'Test Client')

class ProductTypeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ProductType.objects.create(name='Test Product Type')

    def test_product_type_content(self):
        product_type = ProductType.objects.get(name='Test Product Type')
        expected_object_name = f'{product_type.name}'
        self.assertEqual(expected_object_name, 'Test Product Type')

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ProductModel.objects.create(name='Test Product Model')

    def test_product_model_content(self):
        product_model = ProductModel.objects.get(name='Test Product Model')
        expected_object_name = f'{product_model.name}'
        self.assertEqual(expected_object_name, 'Test Product Model')

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ProductType.objects.create(name='Test Product Type')
        ProductModel.objects.create(name='Test Product Model')
        Product.objects.create(name='Test Product', code='P123', product_type=ProductType.objects.get(name='Test Product Type'), product_model=ProductModel.objects.get(name='Test Product Model'), price=100.00, production_time=timedelta(days=1))

    def test_product_content(self):
        product = Product.objects.get(id=1)
        expected_object_name = f'{product.name}'
        self.assertEqual(expected_object_name, 'Test Product')


class ClinicTests(TestCase):
    def setUp(self):
        self.client = Cli()

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_registration_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_contacts_view(self):
        response = self.client.get(reverse('contacts'))
        self.assertEqual(response.status_code, 200)

    def test_vacancies_view(self):
        response = self.client.get(reverse('vacancies'))
        self.assertEqual(response.status_code, 200)

    def test_reviews_view(self):
        response = self.client.get(reverse('reviews'))
        self.assertEqual(response.status_code, 200)

    def test_promocodes_view(self):
        response = self.client.get(reverse('promocodes'))
        self.assertEqual(response.status_code, 200)


