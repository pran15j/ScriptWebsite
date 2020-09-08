from django.urls import path
from django import urls
from django.conf.urls import url
from . import views
from .views import candidate_login_page, candidate_register_page, employee_login_page, employee_register_page


urlpatterns = [
    path('', views.index, name='index'),
    path('invited_user/',views.invited_user,name='newuser'),
    url('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',views.activate_account, name='activate'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout,name='logout'),
    path('home/', views.home, name='home'),
    path('candidate/login', candidate_login_page, name='candidate-login'),
    path('candidate/register', candidate_register_page, name='candidate-register'),
    path('employee/login', employee_login_page, name='employee-login'),
    path('employee/register', employee_register_page, name='employee-register')
]
