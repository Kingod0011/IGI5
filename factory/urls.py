from django.urls import path
from . import views
from .views import RegistrationView, HomePageView, ProfileView, EditProfileView, ClientListView, OrderListView, order_create
from .views import StatisticView
from django.urls import path, re_path
from django.views.generic.base import RedirectView


urlpatterns = [
    #path('', views.index),
    #path('', "admin/"),
    path('register/', RegistrationView.as_view(), name='register'),
    path('home/', HomePageView.as_view(), name='home'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('clients/', ClientListView.as_view(), name='clients'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('order/create/<int:product_id>/', order_create, name='create_order'),
    path('statistic/', StatisticView.as_view(), name='statistic'),
    re_path(r'^$', RedirectView.as_view(url='/home/')),
]