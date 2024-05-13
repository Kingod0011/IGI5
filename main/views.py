import random
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from urllib.error import HTTPError
from django.core.files import File
from django.shortcuts import render, redirect
from translate import Translator
from .models import Articles, CompanyInfo, FAQ, Vacancy
from django.contrib.auth.decorators import login_required, user_passes_test
import requests
import logging
import pytz
from django.utils import timezone
from datetime import datetime, timezone


def superuser_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_superuser,
        login_url='/login/',
        redirect_field_name=None
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def vacancy_list(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'vacancies.html', {'vacancies': vacancies})

def index(request):
    latest_article = Articles.objects.last() 

    date_utc = datetime.now(timezone.utc)
    current_date = date_utc.astimezone()
    user_timezone = str(current_date.tzinfo)
    utc_offset = current_date.utcoffset().total_seconds() / 3600
    
    return render(request, 'main/index.html', {
        'latest_article': latest_article,
        'current_date': current_date,
        'user_timezone': user_timezone,
        'utc_offset': utc_offset,
        
    })
def about(request):
    company_info = CompanyInfo.objects.last()
    return render(request, 'main/about.html', {'company_info': company_info})

def news(request):
    articles = Articles.objects.order_by('-id')
    return render(request, 'main/news.html', {'articles': articles})

def faq(request):
    faq_items = FAQ.objects.order_by('-date_added')
    return render(request, 'main/faq.html', {'faq_items': faq_items})

@login_required
@superuser_required
def add_random_news(request):
    logger = logging.getLogger(__name__)
    response = requests.get('https://newsapi.org/v2/everything?q=furniture&apiKey=06584602a5cf476f801424734b0a24db')
    data = response.json()
    articles = data['articles']
    random.shuffle(articles) 
    for article_data in articles:
        title = article_data.get('title')
        summary = article_data.get('description')
        image_url = article_data.get('urlToImage')

        if title and summary and image_url:
            translator = Translator(to_lang="ru")
            title_ru = translator.translate(title)
            summary_ru = translator.translate(summary)

            img_temp = NamedTemporaryFile(delete=True)
            try:
                img_temp.write(urlopen(image_url).read())
            except HTTPError as e:
                logger.warning(f"HTTP error occurred: {e}")
                continue
            img_temp.flush()

            article = Articles(title=title_ru, summary=summary_ru)
            article.image.save(f"{title}.jpg", File(img_temp))
            article.save()
            break  
    logging.info("Add new news")
    return redirect("/main/")

