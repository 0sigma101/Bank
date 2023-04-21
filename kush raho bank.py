import random
import csv
from datetime import date,timedelta
import datetime
import re
def custid():
    con=mysql.connector.connect(host='localhost',user='root',passwd='59560508',database='bank')#establishing sql table connection
    if con.is_connected():#checking if connection established
        try:
            mycursor=con.cursor()
            sql='select max(custid) from customer'#selecting customer id from the table
            mycursor.execute(sql)
            result=mycursor.fetchall()
            result=int(result[0][-1])
            result=result+1#increasing customer id by 1
            return result
        finally:
            con.close()
    else:
        print('Connection not established')


def check(email):#using module re
    regex='^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex,email)):  
        print("Valid Email")
    else:  
        return "Invalid Email"

            
def create():    
    con=mysql.connector.connect(host='localhost',user='root',passwd='59560508',database='bank')#establishing sql table connection
    if con.is_connected():#checking if connection established
        try:
            mycursor=con.cursor()
            fname=input('Enter first name')
            while fname==None or fname=='':#checking if user just pressed enter at input side 
                print('Try again')
                fname=input('Enter first name')    
            today=date.today()#taking todays dateas creation date
            dateofcreation=today
            cust=custid()#to get custid
            lname=input('Enter last name')
            while lname==None or lname=='':#checking for empty lname
                print('Try again')
                lname=input('Enter last name')
            city=input('Enter city')
            while city==None or city=='':
                print('Try again')
                city=input('Enter city')
            code=createcode()#refarral code
            mobileno=int(input('Enter mobile number'))  
            while len(str(mobileno))!=10:#checking for len of mobile number
                print('Try again')
                moblieno=int(input('Enter mobile number'))
            email=input('Enter your Email ID')
            while check(email)=='Invalid Email':#checking validity of email by regex of re
                print('Try again')
                email=input('Enter your Email ID')
            dob=input('Enter date of birth(yyyy-mm-dd)')
            dob=datetime.datetime.strptime(dob,'%Y-%m-%d')
            delta=today-dob.date()#we take number of days
            if (delta.days/365.2425)<18:#we check for age limit as 18+
                print('Cannot create account')
            else:
                f=open('terms and condition.txt','r')#this is a text file which has terms and conditions
                f=f.read()
                print(f)
                a=input('Do you agree with these Terms and Conditions ?')
                a=a.upper()
                if a in 'YES':
                    pass
                else:
                    return
                b=captcha()#here we make random captcha for checkig if there is no bot on the user side
                print(b)
                a=input('Enter the above captcha')
                if a==b:#if captcha is correct we create account
                    sql='insert into customer values(%s,%s,%s,%s,%s,%s,%s);'#values into customer table
                    data=(cust,fname,lname,city,mobileno,dob,code)
                    mycursor.execute(sql,data)
                    sql='insert into account values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'#values into account table
                    pin=int(input('Create your four digit pin'))
                    while len(str(pin))!=4:#checking pin to be of len 4
                        pin=int(input('Create your four digit pin'))
                    data=(accountno(),cust,date.today(),0,0,0,pin,0,None,None,0)
                    mycursor.execute(sql,data)
                    con.commit()
                    referralcode()
                    print('Account created')
                    print('Your account number is',data[0])#user needs to remember his account number for some places like changing password
                else:                                   
                    print('Wrong captcha entered')
        finally:
                con.close()
    else:
        print('connection noy established') 

  
def login():#this is login function this is one of the option as the program runs
    global datediff
    global ac_no
    global pin
    ac_no=input('Enter your account number')
    pin=int(input('Enter your pin number'))
    check=''#bool of emty string is false use as a value to check if successful login happened
    sql='select * from account where acnumber="%s" and pin=%s'%(ac_no,pin)
    mycursor.execute(sql)
    try:
        check=mycursor.fetchall()
    except:
        check=''
    if bool(check) == True:
        print('You have successfully logged in')
        today=date.today()
        rad='select aod from account where acnumber=%s and pin=%s'%(int(ac_no),pin)#here we update the date user latest logged in
        mycursor.execute(rad)
        rad=mycursor.fetchall()
        rad=rad[0][0]
        con.commit()
        delta=today-rad
        datediff=delta.days
        bsav='select savings_account from account where acnumber=%s and pin=%s'%(int(ac_no),pin)#here we take money to give interest but we give equivalent interest per day
        mycursor.execute(bsav)
        bsav=mycursor.fetchall()
        bsav=bsav[0][0]
        i=0
        while i<datediff:
            if bsav!='NULL':
                r=bsav*0.00546#rhis accounts to 2% pa rate of interest
                bsav+=r#adding to the value as the iteratorprogresses
                i+=1
        sql='update account set savings_account=%s where acnumber=%s'%(bsav,ac_no)#updating the values
        mycursor.execute(sql)
        sql='update account set aod=%s where acnumber=%s;'#updating the values
        data=(today,ac_no)
        mycursor.execute(sql,data)
        con.commit()
        sql='select date_of_loan from account where acnumber=%s and pin=%s'%(int(ac_no),pin)
        mycursor.execute(sql)
        result=mycursor.fetchall()

        result=result[0][0]

        if result != None:

            MoneyToLoanAccount()#this function checks for loan and if there is any loan ammount to be paid however it is users resposibilities to add money to his account  
        return 'y'
    else:
        print('Account number or password is wrong')
        return 'x'


def captcha():# creates a random captcha for bot checking
    import random
    l=4
    b=''
    for i in range(l):
        a=str(random.randint(ord('0'),ord('z')))    
        b+=a
    return b

def createcode():#creates refferal code by taking previous refferal code in database and incressing it by one,two or three
    con=mysql.connector.connect(host='localhost',user='root',passwd='59560508',database='bank')#establishing connection
    if con.is_connected():#checking if connection established
        try:
            mycursor=con.cursor()
            sql='select max(code) from customer'
            mycursor.execute(sql)
            code=mycursor.fetchall()
            code=int(code[0][0])
            f=random.randint(1,3)#increses code
            code=code+f#the refferal code generated is reater than the previous referral code
            return code
        finally:
            con.close()#closing connection
    else:
        print('connection not established') 
    
   
    
def referralcode():#checking if new user added any referralcode if yes then we give him some money
    con=mysql.connector.connect(host='localhost',user='root',passwd='59560508',database='bank')#establishing connection
    if con.is_connected():#checking if connection made successfully
        try:
            mycursor=con.cursor()
            code=createcode()
            ask=input('Do you have a referal code?')
            if ask in ('YES','Y','y','yes','Yes'):
                sql='select code from customer where acnumber="%s" and pin=%s'%(ac_no,pin)
                mycursor.execute(sql)
                cde=mycursor.fetchall()
                cde=cde[0]
                inputcode=input('Enter a code')
                if inputcode==cde:
                    sql1='select balance_saving from account where acnumber="%s"'%(ac_no)
                    mycursor.execute(sql1)
                    balance_sav=mycursor.fetchall()
                    balance_sav+=100
                    sql='update account set balance_saving="%s" where acnumber="%s"'.format(balance_sav,ac_no)
                    mycursor.execute(sql)
                    con.commit()
        finally:
            con.close()#closing connection
    else:
        print('connection not established')


def accountno():#wew take account nuber and iuncrease it by 1
    con=mysql.connector.connect(host='localhost',user='root',passwd='59560508',database='bank')#establishing connection
    if con.is_connected():#checking connection
        try:
            mycursor=con.cursor()
            sql='select max(acnumber) from account'
            mycursor.execute(sql)
            result=mycursor.fetchall()
            result=int(result[0][-1])
            result=result+1#increasing account number by 1 
            return result
        finally:
            con.close()#closing connection
    else:
        print('connection noy established')

    
def details():# here we give option to change password and to check passbook
    print('1 To change password\n2 To check passbook')
    i=input('Enter your choice')
    con=mysql.connector.connect(host='localhost',user='root',passwd='59560508',database='bank')
    if con.is_connected():
        try:
            mycursor=con.cursor()
            if i=='1':#to change password
                b=input('Account_no.')
                a=input('Enter your passord')
                sql='select pin from account where acnumber="%s";'%(b)
                mycursor.execute(sql)
                pswd=mycursor.fetchall()
                pswd=pswd[0][0]
                if int(a)==pswd:
                    newpswd=input('Enter new password')#new password
                    while len(newpswd)!=4:
                        newpswd=int(input('Create your four digit pin'))
                    sql='update account set pin=%s where pin=%s;'
                    data=(newpswd,pswd)
                    mycursor.execute(sql,data)
                    con.commit()
                    print('Change successful')#prints when executes sucessfully
            elif i=='2':
                b=ac_no
                reading_passbook(b)#reading passbook it is a csv file and is iterater on basis of account number
        finally:
            con.close()

    
def loans():#here user takes loans
    amount=int(input('Enter amount to be taken as a loan'))
    while amount<0:#checking for -ve money
        amount=int(input('enter positive amount'))
    lamount=amount*1.2
    if amount<100000:
        print('Eligible for 6 month loan')
        sql='update account set loan_account=%s,principle_amount=%s where acnumber=%s'%(lamount,amount,ac_no)
        mycursor.execute(sql)
        con.commit()
        sql1='update account set current_account=current_account+%s where acnumber="%s" and pin=%s'%(amount,ac_no,pin)
        mycursor.execute(sql1)
        print('You need to pay',int((amount*1.2)/6),'every month')#amount with interest
        con.commit()
    elif amount>=100000:#condition ammount
        print('Consult our loan manager,cap')


def MoneyToLoanAccount():#by this user pays off his loan
    sql='select principle_amount from account where acnumber="%s" and pin=%s'%(ac_no,pin)
    mycursor.execute(sql)
    result=mycursor.fetchall()
    result=result[0][0]
    emi=int((result*1.2)/6)#emi to be paid actually decrease    s after every insatallment
    print('The amount to be paid is',emi)
    today=date.today()
    rad='select date_of_loan from account where acnumber=%s and pin=%s'%(int(ac_no),pin)
    mycursor.execute(rad)
    rad=mycursor.fetchall()
    rad=rad[0][0]
    con.commit()
    delta=today-rad
    datediff=delta.days
    sql1='select loan_account from account where acnumber="%s";'%(ac_no)#  add money as name
    mycursor.execute(sql1)
    balance_sav=mycursor.fetchall()
    balance_sav=balance_sav[0][0]
    if datediff>=30 and balance_sav>0:#checking date for payment of loan
        diff=datediff//30
        balance_sav-=emi*diff
        sql='update account set loan_account={} where acnumber={}'.format(balance_sav,ac_no)#  add money as name
        mycursor.execute(sql)
        con.commit()
        amount=emi*diff
        sql2='update account set date_of_loan="%s" where acnumber=%s'%(rad+timedelta(days=30*diff),ac_no)#updating date of loan to latest one
        sql='select savings_account from account where acnumber="%s" and pin =%s'%(ac_no,pin)#adding money to savings
        mycursor.execute(sql2)
        mycursor.execute(sql)
        result=mycursor.fetchall()
        result=result[0][0]
        con.commit()
        if amount>result:
            print('Insufficient funds\nAdd balance immediately!')
        else:
            result-=amount
            sql='update account set savings_account=%s where acnumber="%s" and pin=%s'%(result,ac_no,pin)
            print(emi*diff,'is being deducted as loan')
            mycursor.execute(sql)
            con.commit()
            enter_passbook(ac_no,balance_sav,'debited, given as loan','khush raho bank')
    else:
        print('Loan payment date not arrived')


def svings():
    print('1 Add\n2 Transfer\n3 Cash withdrawl\n4 Exit')
    a=int(input('Enter your choice'))
    if a==1:#to add money
        con=mysql.connector.connect(host='localhost',user='root',passwd='59560508',database='bank')#establishing connection to con
        if con.is_connected():#to check connection
            try:
                mycursor=con.cursor()
                money=int(input('Enter amount of money'))#money to be added
                while money<0:#checking negative money
                    money=int(input('enter positive amount'))
                sql='select savings_account from account where acnumber="%s"'%(ac_no)
                mycursor.execute(sql)
                balance_sav=mycursor.fetchall()
                balance_sav=balance_sav[0][0]
                balance_sav+=money#saving balance+ money added
                sql2='update account set savings_account=%s where acnumber="%s"'%(balance_sav,ac_no)
                mycursor.execute(sql2)
                print(money,'added')
                print('Your balance in saving account is',balance_sav)#balance in saving is printed
                enter_passbook(ac_no,money,'credited,added','NA')#adding to pasbook
                con.commit()
            finally:
                con.close()        
    elif a==2:#tranferring money
        con=mysql.connector.connect(host='localhost',user='root',passwd='59560508',database='bank')
        if con.is_connected():
            try:
                mycursor=con.cursor()
                sql9='select loan_account from account where acnumber="%s" and pin=%s'%(ac_no,pin)
                mycursor.execute(sql9)
                result=mycursor.fetchall()
                result=result[0][0]
                result=(result*1.2)/6
                con.commit()
                a=int(input('Enter amount of money to be tranferred'))
                if a<0:
                    a=int(input('Enter positive amount'))
                b=int(input('Enter account no. of recipient'))
                sql1='select savings_account from account where acnumber="%s"'%(ac_no)#  add money as name
                sql2='select savings_account from account where acnumber="%s"'%(b)
                mycursor.execute(sql1)
                balance_sav=mycursor.fetchall()
                balance_sav=balance_sav[0][0]
                if balance_sav>a+result:#result is loan emi as a security payment
                    mycursor.execute(sql2)
                    balance_sav2=mycursor.fetchall()
                    balance_sav2=balance_sav2[0][0]
                    balance_sav2+=a#recipient
                    mycursor.execute(sql1)
                    balance_sav=mycursor.fetchall()
                    balance_sav=balance_sav[0][0]
                    balance_sav-=a#giver
                else:
                    print('Minimum balance violated cannot transact')
                sql='update account set savings_account={} where acnumber={}'.format(balance_sav2,b)#  add money as name
                sql2='update account set savings_account={} where acnumber={}'.format(balance_sav,ac_no)
                mycursor.execute(sql)
                mycursor.execute(sql2)
                con.commit()
                print(a,'transferred to',b)
                print('your balance is', balance_sav)
                enter_passbook(ac_no,a,'transferred',b)
                enter_passbook(b,a,'recieved',b)
            finally:
                con.close()
    elif a==3:#withdrawl
        con=mysql.connector.connect(host='localhost',user='root',passwd='59560508',database='bank')
        if con.is_connected():
            try:
                mycursor=con.cursor()
                sql9='select loan_account from account where acnumber="%s" and pin=%s'%(ac_no,pin)
                mycursor.execute(sql9)
                result=mycursor.fetchall()
                result=result[0][0]
                result=(result*1.2)/6
                con.commit()
                a=int(input('Enter amount of money'))
                if a<0:
                    a=int(input('Enter positive amount'))
                sql1='select savings_account from account where acnumber="%s";'%(ac_no)#  add money as name
                mycursor.execute(sql1)
                balance_sav=mycursor.fetchall()
                balance_sav=balance_sav[0][0]
                if balance_sav>a+result:#result is loan emi as a security payment
                    balance_sav-=a
                    sql='update account set savings_account={} where acnumber={}'.format(balance_sav,ac_no)#  add money as name
                    mycursor.execute(sql)
                    enter_passbook(ac_no,a,'debited,withdrawn','NA')
                    print('your balance saving acount is', balance_sav)
                    print(a,'withdrawn')
                    con.commit()
                else:
                    print('Minimum balance violated cannot transact')
            finally:
                con.close()
    elif a==4:
        pass
                
        
def current():
    print('1 Add\n2 Transfer\n3 Cash withdrawl\n4 Exit')
    a=int(input('enter your choice'))
    if a==1:#adding money
        con=mysql.connector.connect(host='localhost',user='root',passwd='59560508',database='bank')

        if con.is_connected():
            try:
                mycursor=con.cursor()
                a=int(input('Enter amount of money'))
                if a<0:
                    a=int(input('enter positive amount'))
                sql1='select current_account from account where acnumber="%s"'%(ac_no)#  add money as name
                mycursor.execute(sql1)
                balance_sav=mycursor.fetchall()
                balance_sav=balance_sav[0][0]
                balance_sav+=a
                sql='update account set current_account="%s" where acnumber="%s"'%(balance_sav,ac_no)#  add money as name
                mycursor.execute(sql)
                print(a,'added')
                print('your balance current account is', balance_sav)
                enter_passbook(ac_no,a,'credited,added','NA')
                con.commit()
            finally:
                con.close()
    elif a==2:
        con=mysql.connector.connect(host='localhost',user='root',passwd='59560508',database='bank')

        if con.is_connected():
            try:
                mycursor=con.cursor()
                a=int(input('enter amount of money'))
                if a<0:
                    a=int(input('enter positive amount'))#ac_no=int(input('Enter your account number'))
                b=int(input('enter account no. of recipient'))
                sql1='select current_account from account where acnumber={}'.format(ac_no)#  add money as name
                sql2='select current_account from account where acnumber={}'.format(b)
                mycursor.execute(sql1)
                balance_sav=mycursor.fetchall()
                balance_sav=balance_sav[0][0]
                if balance_sav>a+500:#500 as a security payment
                    mycursor.execute(sql2)
                    balance_sav2=mycursor.fetchall()
                    balance_sav2=balance_sav2[0][0]
                    balance_sav2+=a
                    mycursor.execute(sql1)
                    balance_sav=mycursor.fetchall()
                    balance_sav=balance_sav[0][0]
                    balance_sav-=a
                    sql='update account set current_account={} where acnumber={}'.format(balance_sav2,b)#  add money as name
                    sql2='update account set current_account={} where acnumber={}'.format(balance_sav,ac_no)
                    mycursor.execute(sql)
                    mycursor.execute(sql2)
                    con.commit()
                    enter_passbook(ac_no,a,'transferred',b)
                    print(a,'transferred')
                    print('your balance is', balance_sav)
                    enter_passbook(b,a,'recieved',b)
                else:
                    print('Minimum balance violated cannot transact')     
            finally:
                con.close()
    elif a==3:
        con=mysql.connector.connect(host='localhost',user='root',passwd='59560508',database='bank')

        if con.is_connected():
            try:
                mycursor=con.cursor()
                a=int(input('Enter amount of money'))
                sql1='select current_account from account where acnumber={};'.format(ac_no)#  add money as name
                mycursor.execute(sql1)
                balance_sav=mycursor.fetchall()
                balance_sav=balance_sav[0][0]
                if balance_sav>a+500:
                    balance_sav-=a
                    sql='update account set current_account={} where acnumber={};'.format(balance_sav,ac_no)#  add money as name
                    mycursor.execute(sql)
                    enter_passbook(ac_no,a,'debited,withdrawn','NA')
                    print('your balance is', balance_sav)
                    print(a,'withdrawn')
                    con.commit()
                else:
                    print('Minimum balance violated cannot transact')
            finally:
                con.close()
    elif a==4:
        pass

    
def fixed():
    print('1 to create FD\n2 FD withdrawl\n3 Exit')
    a=int(input('Enter your choice'))
    if a==1:#making fd
        con=mysql.connector.connect(host='localhost',user='root',passwd='59560508',database='bank')
        if con.is_connected():
            try:
                mycursor=con.cursor()
                sql='select fixed_deposit from account where acnumber=%s'%(ac_no)
                mycursor.execute(sql)
                fixed=mycursor.fetchall()
                fixed=fixed[0][0]
                if fixed==0:#checking if there is no fd before
                    a=int(input('Enter amount of money'))
                    if a<0:
                        a=int(input('enter positive only'))
                    sql1='select fixed_deposit from account where acnumber=%s'%(ac_no)#  add money as name
                    mycursor.execute(sql1)
                    balance_sav=mycursor.fetchall()
                    balance_sav=balance_sav[0][0]
                    balance_sav+=a
                    sql='update account set fixed_deposit=%s where acnumber=%s'%(balance_sav,ac_no)#  add money as name
                    mycursor.execute(sql)
                    today=date.today()
                    sql='update account set date_of_fixed="%s" where acnumber=%s'%(str(today),ac_no)
                    mycursor.execute(sql)
                    print('your balance is', balance_sav)
                    enter_passbook(ac_no,a,'credited,added','NA')
                    con.commit()
                else:
                    print('Cannot add funds yet')
            finally:
                con.close()               
    elif a==2:
        con=mysql.connector.connect(host='localhost',user='root',passwd='59560508',database='bank')

        if con.is_connected():
                mycursor=con.cursor()
                pin=int(input('Enter pin'))
                sql='select date_of_fixed from account where acnumber=%s and pin=%s'%(ac_no,pin)
                mycursor.execute(sql)
                dof=mycursor.fetchall()
                dof=dof[0][0]
                today=date.today()
                delta=today-dof
                if delta.days>1825:  #date atwhich FD ends
                    sql1='select fixed_deposit from account where acnumber=%s'%(ac_no)#add money as name
                    mycursor.execute(sql1)
                    balance_sav=mycursor.fetchall()
                    balance_sav=balance_sav[0][0]
                    datediff=1825
                    interest(0.06369)
                    sql='update account set fixed_deposit=%s where acnumber=%s'%(balance_sav,ac_no)#  add money as name
                    mycursor.execute(sql)
                    print(balance_sav,'withdrawn')
                    sql='update account set fixed_deposit=0 and savings_account=savings_account+balance_sav where acnumber=%s'%(ac_no)
                    mycursor.execute(sql)
                    enter_passbook(ac_no,balance_sav,'debited,withdrawn','NA')
                    mycursor.commit()
                else:
                    print('Cannot remove funds yet')
                con.close()
        elif a==3:
            pass
            
def transactions():#it is like indirect recursion
    print('1 Manage savings\n2 Manage current\n3 Manage fixed\n4 Exit')
    a=int(input('enter your choice'))
    if a==1:
        svings()
    elif a==2:
        current()
    elif  a==3:
        fixed()
    elif a==4:
        pass

def interest(rate):
    si=datediff*rate*balance_sav/100
    balance_sav+=si


def heading_passbook():
    with open('passbook.csv','w') as passb:
        writer=csv.writer(passb)
        writer.writerow(['account number','date','money','cr/db','recipient'])
def enter_passbook(acnumber,money,c,f):#enter values to passbook
    with open('passbook.csv','a') as passb:
        today=date.today()
        writer=csv.writer(passb)
        writer.writerow([acnumber,today,money,c,f])
def reading_passbook(acnumber):#to read passbook
    with open('passbook.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        print('[account number, date, money, description, recipient]')
        for row in reader:
            if row==[]:
                continue
            elif row[0]==acnumber:
                print(row)
            else:
                continue


#front end
import mysql.connector
con=mysql.connector.connect(host='localhost',user='root',passwd='59560508',database='bank')

if con.is_connected():
    try:
        mycursor=con.cursor()
        print('1 To login\n2 To create account')
        v=int(input('Enter your choice'))
        if v==1:
            check=login()
            if check=='y':
                while True:
                    print('1 for Account details\n2 for Transactions\n3 for Loans\n4 Exit')
                    y=int(input('Enter your choice'))
                    if y==1:
                        details()
                    elif y==2:
                        transactions()
                    elif y==3:
                        print('1.To take loan\n2.To make loan payment')
                        a=input('Enter your choice')
                        if a=='1':
                            sql='select principle_amount from account where acnumber="%s" and pin=%s'%(ac_no,pin)
                            mycursor.execute(sql)
                            result=mycursor.fetchall()
                            result=result[0][0]
                            sql='update account set date_of_loan="%s" where acnumber="%s"'%(str(date.today()),ac_no)
                            mycursor.execute(sql)
                            con.commit()
                            if int(result)==0:
                                loans()
                        elif a=='2':
                            MoneyToLoanAccount()
                    elif y==4:
                        break
        elif v==2:
            create()
    finally:
        con.close()#very imp step
else:
    print('connection noy established')
