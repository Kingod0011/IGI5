from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Client, Product, Order, PromoCode, Factory, ProductModel, Reviews
import datetime

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.group = Group.objects.get(name='Clients')
        self.user.groups.add(self.group)
        self.client.login(username='testuser', password='12345')

        self.test_client = Client.objects.create(
            user=self.user,
            name='Test Client',
            phone='+375 (29) 123-45-67',
            city='Test City',
            address='Test Address',
            company='Test Company',
            date_of_birth=datetime.date(1990, 1, 1),
            is_deleted=False
        )

        self.product_type = ProductType.objects.create(name='Test Product Type')
        self.product_model = ProductModel.objects.create(name='Test Product Model')

        self.product = Product.objects.create(
            name='Test Product',
            code='TP1',
            product_type=self.product_type,
            product_model=self.product_model,
            price=100.00,
            production_time=datetime.timedelta(minutes=30),
            is_producing=True
        )

        self.order = Order.objects.create(
            order_date=datetime.datetime.now(),
            completion_date=datetime.datetime.now() + datetime.timedelta(days=1),
            client_name=self.test_client.name,
            product_name=self.product.name,
            client=self.test_client,
            product=self.product,
            pickup_point=None,
            price=self.product.price,
            quantity=1,
            promo_code=None
        )

    def test_home_GET(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_order_create_POST(self):
        response = self.client.post(reverse('create_order', args=[self.product.id]))
        self.assertEquals(response.status_code, 200)

    def test_profile_GET(self):
        response = self.client.get(reverse('profile'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'client_view.html')

    def test_edit_profile_GET(self):
        response = self.client.get(reverse('edit_profile'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'client_edit.html')

    def test_clients_GET(self):
        response = self.client.get(reverse('clients'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'clients.html')

    def test_orders_GET(self):
        response = self.client.get(reverse('orders'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders.html')

    def test_statistic_GET(self):
        response = self.client.get(reverse('statistic'))
        self.assertEquals(response.status_code, 302)

    def test_contacts_GET(self):
        response = self.client.get(reverse('contacts'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'employees.html')

    def test_promocodes_GET(self):
        response = self.client.get(reverse('promocodes'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'promocodes.html')

    def test_reviews_GET(self):
        response = self.client.get(reverse('reviews'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews.html')

    def test_add_random_client_GET(self):
        response = self.client.get(reverse('add_random_client'))
        self.assertEquals(response.status_code, 302)
