from django.db import models
from datetime import datetime,date
# Create your models here.
class Customer (models.Model):
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    city = models.CharField(max_length=15)
    mobileno = models.CharField(max_length=10)
    dob = models.DateTimeField("date of birth")
    
    def __int__(self) -> int:
        return self.id      
    

class Account (models.Model):
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    aod = models.DateField('last accessed',default=date.today())
    savings = models.IntegerField(default=0)
    current = models.IntegerField(default=0)
    fixed = models.IntegerField(default=0)
    pin = models.IntegerField()
    loan = models.IntegerField(default=0)
    loan_date = models.DateField('loan date',null=True)
    fixed_date = models.DateField('fixed date',null=True)
    principle_amt = models.IntegerField(default = 0)
    
    def __int__(self) -> int:
        return self.id