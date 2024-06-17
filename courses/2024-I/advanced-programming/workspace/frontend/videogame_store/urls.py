from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='store_home'),
    path('contact/', views.contact, name='store_contact'),
    path('login/', views.login, name='store_login'),
    path('videogames_list/', views.videogames_list, name='store_videogames_list')
]
