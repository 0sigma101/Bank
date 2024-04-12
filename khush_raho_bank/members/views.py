from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.sessions.models import Session
from django.contrib import messages
from .models import *
from datetime import datetime
from django.utils import timezone

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
        except Account.DoesNotExist:
            user = None

        if user is not None:
            cust = Customer.objects.get(custid = user.custid)
            request.session['fname'] = cust.fname
            request.session['lname'] = cust.lname
            request.session['city'] = cust.city
            request.session['mobileno'] = cust.mobileno
            request.session['acnum'] = user.acnumber
            request.session['pin'] = user.pin
            request.session['last_login'] = timezone.now().isoformat()
            
            messages.success(request, 'Login Successful!')
            return redirect('/home/')
        else:
            messages.error(request, 'Invalid Credentials!')
            return redirect('loginprocess')

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
        
        account_data = Account(acnumber=acnum(), custid=custid(), aod=datetime.today(), savings_account=0, current_account=0, fixed_deposit=0, pin=pin)
        customer_data = Customer(custid=custid(), fname=fname, lname=lname, city=city, mobileno=mobileno, email=email, dob=dob, code=account_data.acnumber)
        
        account_data.save()
        customer_data.save()
        try:
            user = Account.objects.get(acnumber=account_data.acnumber, pin=account_data.pin)
        except Account.DoesNotExist:
            user = None

        if user is not None:
            # Manually set session and log user in
            cust = Customer.objects.get(custid = user.custid)
            request.session['fname'] = cust.fname
            request.session['lname'] = cust.lname
            request.session['city'] = cust.city
            request.session['mobileno'] = cust.mobileno
            request.session['acnum'] = user.acnumber
            request.session['pin'] = user.pin
            request.session['last_login'] = timezone.now().isoformat()
            request.session['user'] = user
            request.session['last_login'] = timezone.now().isoformat()
            messages.success(request, 'Signup Successful!')
            return redirect('/home/')
        else:
            messages.error(request, 'Signup Failed!')
            return redirect('signupprocess')
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

def chngpswd(request):
    user = Account.objects.get(acnumber=request.session['acnum'],pin=request.session['pin'])
    if request.method == "POST":
        oldpassword = request.POST["oldpass"]
        newpassword = request.POST['newpass']
        if(user.pin == int(oldpassword)):
            user.pin=int(newpassword)
            user.save()
            messages.success(request, 'Password!')
            return redirect('/home/')
        else:
            messages.error(request, f'Wrong oldpassword!')
            return redirect('chngpswd')
    template = loader.get_template('chngpswd.html')
    context = {'message': [f'Welcome, {user.pin}'] }
    return HttpResponse(template.render(context,request))
