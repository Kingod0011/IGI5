from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^main/$', views.index, name='main'),
    re_path(r'^about/$', views.about, name='about'),
    re_path(r'^news/$', views.news, name='news'),
    re_path(r'^faq/$', views.faq, name='faq'),
    re_path(r'^contacts/$', views.news, name='contacts'),
    re_path(r'^vacancies/$', views.vacancy_list, name='vacancies'),
    path('add_random_news', views.add_random_news, name='add_random_news')
]
