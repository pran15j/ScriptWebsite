from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth
import json
import os
from . import models
import pdb
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import time
from django.db.models import Q
import base64
from .token_generator import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
# copied from blog
import os
from django.conf import settings
from django.templatetags.static import static
import datetime
from dateutil.relativedelta import relativedelta


# Create your views here.
def index(request):
    return render(request, 'main_page.html', {'message':""})

@csrf_exempt
def invited_user(request):
    #pdb.set_trace()
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception as e:
        data = request.POST
    # pdb.set_trace()
    firstname = data.get('firstname').lower()
    print('fname',firstname)
    lastname = data.get('lastname').lower()
    print('lname',lastname)
    email=data.get('email').lower()
    print('email',email)
    password = data.get('password')
    print('pass',password)
    user_existed = User.objects.filter(username=email)
    if user_existed:
        return JsonResponse({'status':'False','message':'Email Already Exist'}, status=400)
    if (email and password):
        try:
            user=User.objects.create_user(first_name=firstname,last_name=lastname,username=email,email=email,password=password,is_active=False)
            user.save()
        except:
            user = None
        if user:
            # auth.login(request,user)
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('administration/activate_account.html', {
                'user': user,
                'password': password,
                'domain': '127.0.0.1:8000',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = email
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            # return HttpResponse('We have sent you an email, please confirm your email address to complete registration')
            return JsonResponse({'status':'true','message':'Invitation Sent'}, status=200)   
        else:
            return JsonResponse({'status':'False','message':'Problem Creating User'}, status=400) 
    else:
        return JsonResponse({'status':'False','message':'Please Fill All Details'}, status=400)

def activate_account(request, uidb64, token):
    # pdb.set_trace()
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print(uid,user)
        h = account_activation_token.check_token(user, token)
        if user and h==True:
            user.is_active = True
            user.save()
            login(request,user)
            name = user.first_name.capitalize()
            first = name.upper()
            last = user.last_name.upper()
            ini = first[0] + last[0]
            
            return render(request, 'administration/candidate-login.html',{'message':'done','ini':ini,'userletter':name})
        else:
            return HttpResponse('Activation link is invalid!')

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        return HttpResponse('Try again after some time!')


@csrf_exempt
def login(request,user=None):
    # pdb.set_trace();
    if user != None:
        if user.is_authenticated:
            auth.login(request,user)
            # print(request.user.is_superuser)
            return JsonResponse({'status':'true','message':'Loggin'}, status=200)
    else:
        data = json.loads(request.body.decode('utf-8'))
        if not data:
            return JsonResponse({'status':'False','message':'No Data Received'}, status=400)
        username = data.get('username').lower()
        print('user',username)
        password = data.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return JsonResponse({'status':'true','message':'Logged In'}, status=200)   
        else:
            return JsonResponse({'status':'false','message':'Incorrect Id Or Password'}, status=400)

def home(request):
    if request.user.is_authenticated:
        user = request.user
        name = user.first_name.capitalize()
        first = name.upper()
        last = user.last_name.upper()
        ini = first[0] + last[0]
        
        return render(request, 'home.html',{'message':'done','ini':ini,'userletter':name})
    else:
        return render(request, 'administration/candidate-login.html', {'message':"1st page"})

def logout(request):
    auth.logout(request)
    # Redirect to a success page
    return render(request, 'main_page.html', {'message':"1st page"})

def candidate_login_page(request):
    return render(request, 'administration/candidate-login.html')

def candidate_register_page(request):
    return render(request, 'administration/candidate-register.html')

def employee_login_page(request):
    return render(request, 'administration/employee-login.html')

def employee_register_page(request):
    return render(request, 'administration/employee-register.html')
