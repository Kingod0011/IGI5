from django.urls import path
from . import views
from .views import RegistrationView, HomePageView, ProfileView, EditProfileView, ClientListView, OrderListView, order_create
from .views import StatisticView, employee_list, promocode_list, reviews_list, add_random_client
from django.urls import path, re_path
from django.views.generic.base import RedirectView


urlpatterns = [
    re_path(r'^register/$', RegistrationView.as_view(), name='register'),
    re_path(r'^home/$', HomePageView.as_view(), name='home'),
    re_path(r'^profile/$', ProfileView.as_view(), name='profile'),
    re_path(r'^edit_profile/$', EditProfileView.as_view(), name='edit_profile'),
    re_path(r'^clients/$', ClientListView.as_view(), name='clients'),
    re_path(r'^orders/$', OrderListView.as_view(), name='orders'),
    re_path(r'^order/create/(?P<product_id>\d+)/$', order_create, name='create_order'),
    re_path(r'^statistic/$', StatisticView.as_view(), name='statistic'),
    re_path(r'^contacts/$', employee_list, name='contacts'),
    re_path(r'^promocodes/$', promocode_list, name='promocodes'),
    re_path(r'^reviews/$', reviews_list, name='reviews'),
    re_path(r'^$', RedirectView.as_view(url='/home/')),
    path('add_random_client/', add_random_client, name='add_random_client'),
    path('add_review', views.add_review_view, name='add_review'),
]