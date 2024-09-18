from django.db import models
from dirtyfields import DirtyFieldsMixin
from django.contrib import admin
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models.deletion import CASCADE
  
class Department(models.Model):
    dept_id=models.AutoField(primary_key=True)
    dept_abbr=models.CharField(max_length=6,null=False)
    dept_name=models.CharField(max_length=60,null=False)
    start_year=models.DateField(auto_now=False,auto_now_add=False)
    close_year=models.DateField(auto_now=False,auto_now_add=False,null=True,blank=True)
    
    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.dept_name)

class DepartmentAdmin(admin.ModelAdmin):
    list_display=('dept_id','dept_abbr','dept_name','start_year','close_year')

class Religion(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=60,null=False,unique=True)

    objects=models.Manager()

    def __str__(self):
        return str(self.name)

class BloodGroup(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=15,null=False,unique=True)

    objects=models.Manager()

    def __str__(self):
        return str(self.name)

class States(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=60,null=False,default="Karnataka",unique=True)

    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.name)

class AcademicYear(models.Model):
    id=models.AutoField(primary_key=True)
    acayear=models.CharField(max_length=8,default="2020-21",null=True,unique=True)

    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.acayear

class Division(models.Model):
    id=models.AutoField(primary_key=True)
    division=models.CharField(max_length=2,default="A",null=True,unique=True)

    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.division

class Room(models.Model):
    room_id=models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=10,null=True,unique=True)
    row = models.SmallIntegerField(null=True)
    column = models.SmallIntegerField(null=True)
    Total_seats = models.SmallIntegerField(null=True)
   
    
    objects=models.Manager()

    def _str_(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.room_name)


class UserType(models.Model):
    id=models.AutoField(primary_key=True)
    usertype_id=models.SmallIntegerField(default=2)
    usertype_name = models.CharField(max_length=20,null=False)
    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.usertype_name

class Admission_Quota(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=20,null=False,unique=True)
    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.name)


class Months(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=15,null=False,unique=True)
    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.name)

class Category(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=10,default = "GM", null=False)
    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.name)

class Semester(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=4,null=False)
    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.id)
class Detained_type(models.Model):
    id=models.AutoField(primary_key=True)
    Detained_type=models.CharField(max_length=60,null=False,unique=True)

    objects=models.Manager()

    def __str__(self):
        return str(self.Detained_type)
class ExtValuatorCollegeName(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,null=False,unique=True)
    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.name)

class GradeMapping(models.Model):
    id=models.AutoField(primary_key=True)
    MinMarks = models.SmallIntegerField(null=False)
    MaxMarks = models.SmallIntegerField(null=False)
    GradePoints = models.SmallIntegerField(null=False)
    Grade = models.CharField(max_length=1,null=False)
    GradeScheme = models.SmallIntegerField(null=False)
    TotalMarks = models.IntegerField(null=False)
    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.Grade)

class CourseType(models.Model):
    id=models.AutoField(primary_key=True)
    Coursetype = models.CharField(max_length=150,null=False,unique=True)
    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.Coursetype)
