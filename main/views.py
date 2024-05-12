from django.shortcuts import render
from .models import Articles, CompanyInfo, FAQ, Vacancy

def vacancy_list(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'vacancies.html', {'vacancies': vacancies})

def index(request):
    latest_article = Articles.objects.last()
    return render(request, 'main/index.html', {'latest_article': latest_article})

def about(request):
    company_info = CompanyInfo.objects.last()
    return render(request, 'main/about.html', {'company_info': company_info})

def news(request):
    articles = Articles.objects.order_by('-id')
    return render(request, 'main/news.html', {'articles': articles})

def faq(request):
    faq_items = FAQ.objects.order_by('-date_added')
    return render(request, 'main/faq.html', {'faq_items': faq_items})