from django.urls import path
from .views import contact_page
from django import urls
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', contact_page, name='contact'),
    path('contactus/', views.contactus, name='contactus'),
]
