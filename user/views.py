from django.shortcuts import render,HttpResponse
from django.template import loader
from .models import Customer, Account
from django.http import request
# Create your views here.

def index(request):
    Cust = Account.objects.all()
    template = loader.get_template("user/index.html")
    context = {
        "User":Cust,
    }
    return HttpResponse(template.render(context,request))

def Customer_Check(request, Customer_id):
    return HttpResponse("This is customer %s."%Customer_id)