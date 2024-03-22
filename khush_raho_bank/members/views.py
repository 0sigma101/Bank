from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from .models import *
from datetime import datetime

def custid():
    custid = Customer.objects.all().values("custid")[len(Customer.objects.all().values("custid"))-1]['custid']+1
    return custid

def acnum():
    acnum = Account.objects.all().values("acnumber")[len(Account.objects.all().values("acnumber"))-1]['acnumber']+1
    return acnum

def redeem(code):
    person = Account.objects.get(acnumber=code)
    person.current_account+=200
    person.save()

def members(request):
    mymembers = Account.objects.all().values()
    template = loader.get_template('datashowfilter.html')
    context = {
    'mymembers': mymembers,
    }
    return HttpResponse(template.render(context,request))

def loginsignup(request):
    template = loader.get_template('loginsignup.html')
    context = {}
    return HttpResponse(template.render(context,request))
    
def loginprocess(request):
    if request.method == "POST":
        acnumber = request.POST['acnumber']
        password = request.POST['passwd']
        try:
            user = Account.objects.get(acnumber=acnumber, pin=password)
            # You can also use Django's built-in authentication
            # from django.contrib.auth import authenticate, login
            # user = authenticate(request, acnumber=acnumber, password=password)
            if user:
                # Login successful, redirect to a success page or homepage
                return HttpResponse("Login Success")
            else:
                # Login failed
                return HttpResponse("Login Failed")
        except AuthUser.DoesNotExist:
            # Login failed
            return HttpResponse("Login Failed")
    template = loader.get_template('login.html')
    context = {}
    return HttpResponse(template.render(context, request))

def signupprocess(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        city = request.POST['city']
        mobileno = request.POST['mobileno']
        email = request.POST['email']
        dob = request.POST['dob']
        pin = request.POST['pin']
        code = request.POST['code']
        redeem(code)
        Account_data = Account(acnumber = acnum(),custid = custid(),aod = datetime.today(),savings_account = 0,current_account = 0,fixed_deposit = 0,pin = pin)
        Customer_data = Customer(custid = custid(),fname = fname,lname = lname,city = city,mobileno = mobileno,email = email,dob = dob,code = Account_data.acnumber)
        Account_data.save()
        Customer_data.save()
    template = loader.get_template('signup.html')
    context = {}
    return HttpResponse(template.render(context, request))

def details(request,id):
    mymember = Customer.objects.get(custid=id)
    template = loader.get_template('details.html')
    context = {
    'mymember': mymember,
    }
    return HttpResponse(template.render(context,request))