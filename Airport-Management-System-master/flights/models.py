#from concurrent.futures.thread import _worker
#from msilib.schema import ServiceControl, ServiceInstall
#from multiprocessing.connection import Client
from multiprocessing.connection import Client
from turtle import title
from autoslug import AutoSlugField
from django.db import models
#from django.contrib.auth.models import Abstract 
from client.models import client
#from handyman.models import handyman
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
import datetime
import django.utils.timezone
# Create your models here.


class service(models.Model):
    title = models.CharField(max_length=10000)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='KES')
    date = datetime
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
      
class ClientService(models.Model):
    slug = AutoSlugField(populate_from='code')
    code = models.CharField(max_length=100)
    service = models.ForeignKey(service, on_delete=models.CASCADE, null=True)
    #handyman = models.ForeignKey(handyman,on_delete=models.CASCADE,null=True)
    date1 = models.DateField()
    active = models.BooleanField(default=True,)
    send = models.BooleanField(editable=False,default=False)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='KES')
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
    Day = models.DateTimeField()
      

class Appointment(models.Model):
    slug = AutoSlugField(populate_from='code')
    code = models.CharField(max_length=20)
    service = models.ForeignKey(service, on_delete=models.CASCADE, null=True)
    ClientService = models.ForeignKey(ClientService, on_delete=models.CASCADE, null=True)
    client = models.ForeignKey(client, on_delete=models.CASCADE, null=True)
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)


#class Service(models.Model):
 #   title = models.CharField(max_length=10000)
  #  date = models.DateTimeField()
   # price = MoneyField(max_digits=14, decimal_places=2, default_currency='KES')
   
        

