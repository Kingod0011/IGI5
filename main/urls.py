from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.index, name='main'),
    path('about/', views.about, name='about'),
    path('news/', views.news, name='news'),
    path('faq/', views.faq, name='faq'),
    path('contacts/', views.news, name='contacts'),
    path('vacancies/', views.vacancy_list, name='vacancies'),
]
