from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth
import json
from django.core import mail
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
import pdb

# Create your views here.

def contact_page(request):
    return render(request, 'contact/contact.html')

@csrf_exempt
def contactus(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception as e:
        data = request.POST
    name = data.get('name')
    email = data.get('email')
    msg = data.get('msg')
    try:
        send_mail(
        'Script Foundation: New incoming Query!!!',
        """
        Client Name :  {}
        Client id : {}
        Message : {}.

        """.format(name,email,msg),
        'scriptfoundation@gmail.com',
        ['niteshnagpal@outlook.com'],
        fail_silently=False,
        )
        return JsonResponse({"status":"1","message":"Success"},status=200)
    except Exception as exp:
        print(exp)
        return JsonResponse({"status":"0","message":"Failed"},status=400)
