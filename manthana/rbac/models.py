from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib import admin

# Create your models here.
class RightType(models.Model):
    type=models.SmallIntegerField(primary_key=True, default=None)
    desc=models.CharField(max_length=15,default="Master")
    objects=models.Manager()

    def __str__(self):
        return str(self.type)

class RightCategory(models.Model):
    category=models.SmallIntegerField(primary_key=True, default=None)
    desc=models.CharField(max_length=30,default="Academics")
    objects=models.Manager()

    def __str__(self):
        return str(self.desc)

class RightDetails(models.Model):
    id=models.AutoField(primary_key=True)
    abbr=models.CharField(max_length=50,null=False,default='right_abbr')
    details=models.CharField(max_length=50,null=False,default='right_description')
    category=models.ForeignKey('RightCategory',on_delete=CASCADE)
    type=models.ForeignKey('RightType',on_delete=CASCADE,default=1)
    objects=models.Manager()

    def __str__(self):
        return str(self.details)

class UserRights(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey('admission.CustomUser',on_delete=CASCADE)
    right=models.ForeignKey('RightDetails',on_delete=CASCADE,default=1)
    objects=models.Manager()
