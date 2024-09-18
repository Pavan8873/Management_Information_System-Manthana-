'''
from ast import mod
from asyncio.windows_events import NULL '''
import datetime
from django.contrib import admin
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import DateField, NullBooleanField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from admission.models import CustomUser
from master_mgmt.models import Department


#Employee details
class Employee_Details(models.Model):
    employee_id = models.AutoField(primary_key=True)
    employee_type_data=[(1,"Admin"),(2,"Teaching Staff"),(3,"Student"),(4,"Non Teaching Staff"),(5,"Developer")]
    employee_type=models.SmallIntegerField(default=2,choices=employee_type_data)
    emp_login=models.ForeignKey('admission.CustomUser',to_field = 'username', db_column = 'emp_login', on_delete=models.CASCADE)
    # emp_login=models.CharField(max_length=7,null=False,unique=True)
    employee_name = models.CharField(max_length=25,null=False)
    employee_emp_id = models.CharField(max_length=10,unique=True,null=False)
    employee_gender_data = [(1,"Male"),(2,"Female"),(3,"Others")]
    employee_gender = models.SmallIntegerField(default=1,choices=employee_gender_data)
    employee_profile_pic = models.ImageField(upload_to = 'employee/%Y/%m/%d' ,default=False)
    employee_dept_id = models.ForeignKey(Department,on_delete=CASCADE)
    employee_designation = models.CharField(max_length=20,null=False)
    employee_qualification = models.CharField(max_length=20,null=False)
    employee_cellphone = models.CharField(max_length=15,null=False,unique=True)
    employee_dob = models.DateField(auto_now_add=False,null=False)
    employee_bld_group_data = [(1,"A +ve"),(2,"A -ve"),(3,"B +ve"),(4,"B -ve"),(5,"AB +ve"),(6,"AB -ve"),(7,"O +ve"),(8,"O -ve")]
    employee_bld_group = models.SmallIntegerField(default=1,choices=employee_bld_group_data)
    employee_joining_date = models.DateField(null=False)
    employee_email = models.CharField(max_length=50,null=False) 
    employee_pan = models.CharField(max_length=15,null=False,unique=True) 
    employee_aadhar = models.CharField(max_length=15,null=False,unique=True) 
    employee_voter_id = models.CharField(max_length=15,null=False,unique=True) 
    # employee_religion_data = [(1,"Hindu"),(2,"Muslim"),(3,"Christian"),(4,"Jain"),(5,"Sikh"),(6,"Buddhist"),(7,"Others")]
    employee_religion = models.ForeignKey('master_mgmt.Religion',default=1,on_delete=CASCADE)
    employee_subcaste = models.CharField(max_length=15,null=True)
    employee_postal_address = models.CharField(max_length=50,null=False) 

    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.employee_id)
