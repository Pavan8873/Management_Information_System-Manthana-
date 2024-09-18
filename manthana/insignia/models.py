import datetime
from operator import truediv
from trace import Trace
from dirtyfields import DirtyFieldsMixin
from django.contrib import admin
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import DateField, NullBooleanField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from master_mgmt.models import *
from django.utils.timezone import now

class Event(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100,null=False)
    type=models.CharField(max_length=100)
    dep=models.CharField(max_length=10)
    day=models.CharField(max_length=10)  
class List(models.Model):
    id=models.AutoField(primary_key=True)
    eventid=models.CharField(max_length=100)
    email = models.EmailField()
    college = models.CharField(max_length=100,null=True)
    names = models.TextField()         
    leader=models.CharField(max_length=100,null=True)                                    
    number = models.CharField(max_length=20,null=True)
    event=models.ForeignKey(Event, on_delete=CASCADE)
    numberofpar=models.CharField(max_length=10,null=True) 
    payment=models.CharField(max_length=10,null=True)
    pay_id=models.CharField(max_length=50,null=True)
class winners(models.Model):
    id=models.AutoField(primary_key=True)
    college = models.CharField(max_length=100)
    names = models.TextField()                                           
    number = models.CharField(max_length=20)
    event=models.ForeignKey(Event, on_delete=CASCADE)
    now=models.CharField(max_length=10)
    winner=models.CharField(max_length=10)
    inid=models.CharField(max_length=50)
class feedback(models.Model):
    id=models.AutoField(primary_key=True) 
    names = models.TextField() 
    email = models.EmailField()
    event = models.ForeignKey(Event, on_delete=CASCADE)
    overall=models.CharField(max_length=3)
    q1=models.CharField(max_length=20)
    q2=models.CharField(max_length=20)
    q3=models.CharField(max_length=20)
    q4=models.CharField(max_length=20)
    question5=models.CharField(max_length=20)
    question6=models.CharField(max_length=20)
    question7=models.CharField(max_length=20)
    question8=models.CharField(max_length=20)
    response = models.TextField() 
