from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='store_home'),
    path('contact/', views.contact, name='store_contact'),
    path('login/', views.login, name='store_login'),
]
