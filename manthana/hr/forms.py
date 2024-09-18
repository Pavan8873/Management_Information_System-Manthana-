from admission.models import CustomUser
from master_mgmt.models import *
from django import forms
from django.forms import ChoiceField

class AddEmployeeForm(forms.Form):
    employee_name = forms.CharField(label="Name", max_length=80,widget=forms.TextInput(attrs={"class":"form-control"}))
    employee_emp_id = forms.CharField(label="Employee ID",max_length=10,widget=forms.TextInput(attrs={"class":"form-control"}))
    employee_gender_choices = [(1,"Male"),(2,"Female"),(3,"Others")]
    employee_gender=forms.ChoiceField(label="Gender",choices=employee_gender_choices,widget=forms.Select(attrs={"class":"form-control"}))
    employee_profile_pic = forms.ImageField(label="Photo",widget=forms.FileInput(attrs={"class":"form-control"}))
    employee_designation=forms.CharField(label="Designation",max_length=80,widget=forms.TextInput(attrs={"class":"form-control"}))
    employee_qualification = forms.CharField(label="Qualification",max_length=80,widget=forms.TextInput(attrs={"class":"form-control"}))
    employee_cellphone = forms.IntegerField(label="Phone Number", widget=forms.NumberInput(attrs={"class":"form-control"}))
    employee_dob = forms.DateField(label="Date of Birth",widget=forms.DateInput(attrs={"type":"date","class":"form-control"}))
    employee_joining_date = forms.DateField(label="Joining Date",widget=forms.NumberInput(attrs={"type":"date","class":"form-control"}))
    employee_email = forms.EmailField(label="E-mail", max_length=130,widget=forms.EmailInput(attrs={"class":"form-control"}))
    employee_pan = forms.CharField(label="Pan Number", max_length=10,widget=forms.TextInput(attrs={"class":"form-control"}))
    employee_aadhar = forms.IntegerField(label="Aadhar Number",widget=forms.NumberInput(attrs={"class":"form-control"}))
    employee_voter_id = forms.CharField(label="Voter ID", max_length=10,widget=forms.TextInput(attrs={"class":"form-control"}))
    employee_postal_address = forms.CharField(label="Address", max_length=150,widget=forms.Textarea(attrs={"class":"form-control"}))
    
    employee_religion_list = []
    employee_bld_group_list = []
    employee_dept_list = []
    employee_usertype_list = []

    try:
        religion = Religion.objects.all()
        for relg in religion:
            relgName = (relg.id, relg.name)
            employee_religion_list.append(relgName)
        
        bldgrp = BloodGroup.objects.all().order_by('name')
        for bg in bldgrp:
            bldgrpname = (bg.id, bg.name)
            employee_bld_group_list.append(bldgrpname)
        
        dept = Department.objects.all()
        for dname in dept:
            deptname = (dname.dept_id, dname.dept_name)
            employee_dept_list.append(deptname)

        usrtype = UserType.objects.all()
        for utype in usrtype:
            uname = (utype.id, utype.usertype_name)
            employee_usertype_list.append(uname)

    except Exception as e:
        print(e)
    
    # employee_type_data=[(1,"Admin"),(2,"Teaching Staff"),(3,"Student"),(4,"Non Teaching Staff"),(5,"Developer")]
    employee_type = forms.ChoiceField(label="Employee Type",choices=employee_usertype_list,widget=forms.Select(attrs={"class":"form-control"}))
    employee_religion=forms.ChoiceField(label="Religion",choices=employee_religion_list,widget=forms.Select(attrs={"class":"form-control"}))
    employee_subcaste = forms.CharField(label="Sub Caste", max_length=80,widget=forms.TextInput(attrs={"class":"form-control"}))
    employee_bld_group = forms.ChoiceField(label="Blood Group",choices=employee_bld_group_list,widget=forms.Select(attrs={"class":"form-control"}))
    employee_dept = forms.ChoiceField(label="Department",choices=employee_dept_list,widget=forms.Select(attrs={"class":"form-control"}))

class EditEmployeeForm(forms.Form):
    employee_name = forms.CharField(label="Name", max_length=80,widget=forms.TextInput(attrs={"class":"form-control"}))
    employee_emp_id = forms.CharField(label="Employee ID",max_length=10,widget=forms.TextInput(attrs={"class":"form-control"}))
    employee_gender_choices = [(1,"Male"),(2,"Female"),(3,"Others")]
    employee_gender=forms.ChoiceField(label="Gender",choices=employee_gender_choices,widget=forms.Select(attrs={"class":"form-control"}))
    employee_profile_pic = forms.ImageField(label="Photo",widget=forms.FileInput(attrs={"class":"form-control"}))
    employee_designation=forms.CharField(label="Designation",max_length=80,widget=forms.TextInput(attrs={"class":"form-control"}))
    employee_qualification = forms.CharField(label="Qualification",max_length=80,widget=forms.TextInput(attrs={"class":"form-control"}))
    employee_cellphone = forms.IntegerField(label="Phone Number",widget=forms.NumberInput(attrs={"class":"form-control"}))
    employee_dob = forms.DateField(label="Date of Birth",widget=forms.NumberInput(attrs={"type":"date","class":"form-control"}))
    employee_joining_date = forms.DateField(label="Joining Date",widget=forms.NumberInput(attrs={"type":"date","class":"form-control"}))
    employee_email = forms.EmailField(label="E-mail", max_length=130,widget=forms.EmailInput(attrs={"class":"form-control"}))
    employee_pan = forms.CharField(label="Pan Number", max_length=10,widget=forms.TextInput(attrs={"class":"form-control"}))
    employee_aadhar = forms.IntegerField(label="Aadhar Number",widget=forms.NumberInput(attrs={"class":"form-control"}))
    employee_voter_id = forms.CharField(label="Voter ID", max_length=10,widget=forms.TextInput(attrs={"class":"form-control"}))
    employee_postal_address = forms.CharField(label="Address", max_length=200,widget=forms.Textarea(attrs={"class":"form-control"}))
    
    employee_religion_list = []
    employee_bld_group_list = []
    employee_dept_list = []

    try:
        religion = Religion.objects.all()
        for relg in religion:
            relgName = (relg.id, relg.name)
            employee_religion_list.append(relgName)
        
        bldgrp = BloodGroup.objects.all().order_by('name')
        for bg in bldgrp:
            bldgrpname = (bg.id, bg.name)
            employee_bld_group_list.append(bldgrpname)
        
        dept = Department.objects.all()
        for dname in dept:
            deptname = (dname.dept_id, dname.dept_name)
            employee_dept_list.append(deptname)

    except:
        pass
    
    employee_type_data=[(1,"Admin"),(2,"Teaching Staff"),(3,"Student"),(4,"Non Teaching Staff"),(5,"Developer")]
    employee_type = forms.ChoiceField(label="Employee Type",choices=employee_type_data,widget=forms.Select(attrs={"class":"form-control"}))
    employee_religion=forms.ChoiceField(label="Religion",choices=employee_religion_list,widget=forms.Select(attrs={"class":"form-control"}))
    employee_subcaste = forms.CharField(label="Sub Caste", max_length=80,widget=forms.TextInput(attrs={"class":"form-control"}))
    employee_bld_group = forms.ChoiceField(label="Blood Group",choices=employee_bld_group_list,widget=forms.Select(attrs={"class":"form-control"}))
    employee_dept = forms.ChoiceField(label="Department",choices=employee_dept_list,widget=forms.Select(attrs={"class":"form-control"}))