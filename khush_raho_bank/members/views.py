from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *

def members(request):
    mymembers = Account.objects.all().values()
    template = loader.get_template('datashowfilter.html')
    context = {
    'mymembers': mymembers,
    }
    return HttpResponse(template.render(context,request))

def details(request,id):
    mymember = Customer.objects.get(custid=id)
    template = loader.get_template('details.html')
    context = {
    'mymember': mymember,
    }
    return HttpResponse(template.render(context,request))