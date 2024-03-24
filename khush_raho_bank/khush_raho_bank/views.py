from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.sessions.models import Session
from django.utils import timezone
from members.models import Account
from django.http import HttpResponse
from django.template import loader

def view(request):
    fname = request.session.get('fname', None)
    template = loader.get_template('index.html')
    
    if fname:
        context = {'message': f'Welcome, {fname}'}
    else:
        context = {'message': 'Please login to continue.'}
    
    return HttpResponse(template.render(context, request))
