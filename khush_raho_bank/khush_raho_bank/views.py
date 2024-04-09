from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.sessions.models import Session
from django.utils import timezone
from members.models import Account
from django.http import HttpResponse
from django.template import loader
from members.models import *

def view(request):
    fname = request.session.get("fname", None)
    lname = request.session.get("lname",None)
    city = request.session.get("city", None)
    mobileno = request.session.get("mobileno",None)
    if fname:
        template = loader.get_template('index_with_login.html')
        context = {'message': [f'Welcome, {fname} {lname}', f"You live in {city}", f"Your phone no is {mobileno}"] }
    else:
        template = loader.get_template('index_without_login.html')
        context = {'message': 'Please login to continue.'}
    
    return HttpResponse(template.render(context, request))
