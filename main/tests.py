

from django.test import TestCase, Client
from django.urls import reverse
from .models import Articles, CompanyInfo, FAQ

class MainTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_news_view(self):
        response = self.client.get(reverse('news'))
        self.assertEqual(response.status_code, 200)

    def test_faq_view(self):
        response = self.client.get(reverse('faq'))
        self.assertEqual(response.status_code, 200)

    def test_add_cosmetology_news_view(self):
        response = self.client.get(reverse('add_random_news'))
        self.assertEqual(response.status_code, 302)

    def test_articles_model(self):
        article = Articles.objects.create(title='Test title', summary='Test summary')
        self.assertEqual(str(article), 'Test title')

    def test_company_info_model(self):
        company_info = CompanyInfo.objects.create(info='Test info')
        self.assertEqual(str(company_info), 'Some information')

    def test_faq_model(self):
        faq = FAQ.objects.create(question='Test question', answer='Test answer')
        self.assertEqual(str(faq), 'Test question')