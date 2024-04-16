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

def checkbalance(account_number,account_type,amount):
    user = Account.objects.filter(acnumber=account_number).first()
    if(account_type == "savings"):
        if(user.savings_account>(user.loan_account*1.2)/6+amount):
            return True
    elif(account_type=="current"):
        if(user.current_account>(user.loan_account*1.2)/6+amount):
            return True
    return False

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
    context = {'message': [f'Welcome, {request.session["fname"]}'] }
    return HttpResponse(template.render(context,request))

def transact(request):
    user = Account.objects.get(acnumber=request.session['acnum'],pin=request.session['pin'])
    if request.method == "POST":
        print(request)
        transaction_type = request.POST["transaction_type"]
        account_type = request.POST['account_type']
        pin = int(request.POST['pin'])
        amount = int(request.POST['amount'])
        if(transaction_type == 'transfer_money'):
            pin = int(request.POST['transfer_pin'])
            amount = int(request.POST['transfer_amount'])
            if(user.pin == pin):
                recacount = request.POST['recipient_account']
                recipient = Account.objects.filter(acnumber=recacount).first()
                if not recipient:
                    messages.error(request, 'Recipient account does not exist!')
                    return redirect('/home/')
                if(account_type == "savings" ):
                    if(checkbalance(request.session['acnum'],account_type,amount)):
                        recipient.current_account += amount
                        user.savings_account -= amount
                    else:
                        messages.error(request, 'Low on Balance!')
                        return redirect('/home/')
                elif(account_type == "current"):
                    if(checkbalance(request.session['acnum'],account_type,amount)):
                        recipient.current_account += amount
                        user.current_account -= amount
                    else:
                        messages.error(request, 'Low on Balance!')
                        return redirect('/home/')
                recipient.save()
                user.save()
            else:
                messages.error(request, 'Wrong Password!')
                return redirect('transact')
        elif(transaction_type == 'add_money'):
            pin = int(request.POST['pin'])
            amount = int(request.POST['amount'])
            if(user.pin == pin):
                if(account_type == "savings"):
                    user.savings_account += amount
                elif(account_type == "current"):
                    user.current_account += amount
                user.save()
            else:
                messages.error(request, 'Wrong Password!')
                return redirect('transact')
        elif(transaction_type == 'withdraw_money'):
            pin = int(request.POST['withdraw_pin'])
            amount = int(request.POST['withdraw_amount'])
            if(user.pin == pin):
                if(account_type == "savings"):
                    if(checkbalance(request.session['acnum'],account_type,amount)):
                        user.savings_account -= amount
                    else:
                        messages.error(request, 'Low on Balance!')
                        return redirect('/home/')
                elif(account_type == "current"):
                    if(checkbalance(request.session['acnum'],account_type,amount)):
                        user.current_account -= amount
                    else:
                        messages.error(request, 'Low on Balance!')
                        return redirect('/home/')
                user.save()
            else:
                messages.error(request, 'Wrong Password!')
                return redirect('transact')
        elif(transaction_type=="self_transfer"):
            pin = int(request.POST['self_pin'])
            amount = int(request.POST['self_amount'])
            if(user.pin == pin):
                if(account_type == "savings" ):
                    if(checkbalance(request.session['acnum'],account_type,amount)):
                        user.savings_account-=amount
                        user.current_account+=amount
                    else:
                        messages.error(request, 'Low on Balance! Some payment yet to be made so please transfer lesser amount')
                        return redirect('/transact/')
                elif(account_type == "current" ):
                    if(checkbalance(request.session['acnum'],account_type,amount)):
                        user.current_account-=amount
                        user.savings_account+=amount
                    else:
                        messages.error(request, 'Low on Balance! Some payment yet to be made so please transfer lesser amount')
                        return redirect('/transact/')
                user.save()
            else:
                messages.error(request, 'Wrong Password!')
                return redirect('transact')
        messages.success(request, " ".join(transaction_type.split("_"))+' Successful')
        return redirect('/home/')
    template = loader.get_template('transact.html')
    context = {'message': [f'Welcome, {request.session["fname"]}'] }
    return HttpResponse(template.render(context,request))


