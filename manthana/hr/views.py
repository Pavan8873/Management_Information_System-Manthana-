from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls.base import reverse
from admission.models import CustomUser, Student_Details
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from hr.models import Employee_Details
import base64
from django.db import transaction

# Create your views here.

#Employee Static view
@login_required
def add_employee(request):
    form=AddEmployeeForm()
    empdetails=Employee_Details.objects.all()
    deptLists = Department.objects.all()
    return render(request,"add_employee.html",{"form":form,'empdetails':empdetails,'deptLists':deptLists})

def image_as_base64(image_file, format='jpeg'):
    """
    :param `image_file` for the complete path of image.
    :param `format` is format for image, eg: `png` or `jpg`.
    """
    if not os.path.isfile(image_file):
        return None
    
    encoded_string = ''
    with open(image_file, 'rb') as img_f:
        encoded_string = base64.b64encode(img_f.read())
    return 'data:image/%s;base64,%s' % (format, encoded_string)

@login_required
def CreateEmployee(request):
    empdetails=Employee_Details.objects.all()
    deptLists = Department.objects.all()
    if request.method!="POST":
        context={'empdetails':empdetails,'deptLists':deptLists}
        return render(request,"add_employee.html",context=context)
    else:
        form=AddEmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            employee_name=form.cleaned_data["employee_name"]
            employee_emp_id=form.cleaned_data["employee_emp_id"]
            employee_gender=form.cleaned_data["employee_gender"]
            print(employee_gender)
            employee_profile_pic=form.cleaned_data["employee_profile_pic"]
            print(employee_profile_pic)
            employee_designation=form.cleaned_data["employee_designation"]
            employee_qualification=form.cleaned_data["employee_qualification"]
            employee_cellphone=form.cleaned_data["employee_cellphone"]
            employee_dob=form.cleaned_data["employee_dob"]
            employee_joining_date=form.cleaned_data["employee_joining_date"]
            employee_email=form.cleaned_data["employee_email"]
            employee_pan=form.cleaned_data["employee_pan"]
            employee_aadhar=form.cleaned_data["employee_aadhar"]
            employee_voter_id=form.cleaned_data["employee_voter_id"]
            employee_postal_address=form.cleaned_data["employee_postal_address"]
            employee_type=form.cleaned_data["employee_type"]
            employee_religion=form.cleaned_data["employee_religion"]
            employee_subcaste=form.cleaned_data["employee_subcaste"]
            employee_bld_group=form.cleaned_data["employee_bld_group"]
            employee_dept=form.cleaned_data["employee_dept"]
            
            employee_dept=Department.objects.get(dept_id = int(employee_dept))
            
            # with open(employee_profile_pic, 'rb') as img_f:
            #     employee_profile_pic_base64=base64.b64encode(img_f.read())
            # b64_img = 'data:image/%s;base64,%s' % ('jpeg', employee_profile_pic_base64)
            # print(b64_img)
            try:
                bgcnt=Employee_Details.objects.filter(employee_emp_id=employee_emp_id).count()
                
                if bgcnt == 0:
                    with transaction.atomic():
                        user = CustomUser.objects.create_user(email = employee_email, username = employee_emp_id,password = str(employee_dob), user_type = employee_type)
                        emp_login = CustomUser.objects.get(username=employee_emp_id) #ForeignKey value
                        EmpRecord=Employee_Details.objects.create(employee_type = employee_type, employee_name = employee_name, 
                                                            employee_emp_id = employee_emp_id, employee_gender = employee_gender, emp_login = emp_login, 
                                                            employee_profile_pic = employee_profile_pic, employee_dept_id = employee_dept,
                                                            employee_designation = employee_designation,  employee_qualification = employee_qualification, 
                                                            employee_cellphone = employee_cellphone, employee_dob = employee_dob, 
                                                            employee_bld_group = employee_bld_group, employee_joining_date = employee_joining_date, 
                                                            employee_email = employee_email, employee_pan = employee_pan, employee_aadhar = employee_aadhar, 
                                                            employee_voter_id = employee_voter_id, employee_religion = Religion.objects.get(id = employee_religion), 
                                                            employee_subcaste = employee_subcaste, employee_postal_address = employee_postal_address)
                        
                        messages.success(request,"Employee Added Successfully")
                        return HttpResponseRedirect(reverse("AddEmployee"))
                else:
                    messages.error(request,"Employee Already Exists")
                    context={'empdetails':empdetails,'deptLists':deptLists}
                    return HttpResponseRedirect(reverse("AddEmployee"))
            except Exception as e:
                print(e)
                messages.error(request,"Failed to Add Employee")
                return HttpResponseRedirect(reverse("AddEmployee"))
        else:
            context={'empdetails':empdetails, 'deptLists':deptLists}
            return render(request,"add_employee.html",context=context)

@login_required
def edit_employee(request,emp_id):
    emp=Employee_Details.objects.get(employee_id=emp_id)
    form=EditEmployeeForm()
    form.fields['employee_type'].initial=emp.employee_type
    form.fields['employee_name'].initial=emp.employee_name
    form.fields['employee_emp_id'].initial=emp.employee_emp_id
    form.fields['employee_gender'].initial=emp.employee_gender
    form.fields['employee_profile_pic'].initial=emp.employee_profile_pic
    form.fields['employee_dept'].initial=emp.employee_dept_id
    form.fields['employee_designation'].initial=emp.employee_designation
    form.fields['employee_qualification'].initial=emp.employee_qualification
    form.fields['employee_cellphone'].initial=emp.employee_cellphone
    form.fields['employee_dob'].initial=emp.employee_dob
    form.fields['employee_bld_group'].initial=emp.employee_bld_group
    form.fields['employee_joining_date'].initial=emp.employee_joining_date
    form.fields['employee_email'].initial=emp.employee_email
    form.fields['employee_pan'].initial=emp.employee_pan
    form.fields['employee_aadhar'].initial=emp.employee_aadhar
    form.fields['employee_voter_id'].initial=emp.employee_voter_id
    form.fields['employee_religion'].initial=emp.employee_religion
    form.fields['employee_subcaste'].initial=emp.employee_subcaste
    form.fields['employee_postal_address'].initial=emp.employee_postal_address
    context={'form':form,'emp_id':emp_id}
    return render(request,"edit_employee.html",context=context)

@login_required
def EditEmployee(request):
    emp_id = int(request.POST.get('emp_id'))
    if request.method!="POST":
        return render(request,"add_employee.html")
    else:
        form=EditEmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            employee_type=form.cleaned_data["employee_type"]
            employee_name=form.cleaned_data["employee_name"]
            employee_emp_id=form.cleaned_data["employee_emp_id"]
            employee_gender=form.cleaned_data["employee_gender"]
            employee_profile_pic=form.cleaned_data["employee_profile_pic"]
            employee_dept_id=form.cleaned_data["employee_dept"]
            employee_designation=form.cleaned_data["employee_designation"]
            employee_qualification=form.cleaned_data["employee_qualification"]
            employee_cellphone=form.cleaned_data["employee_cellphone"]
            employee_dob=form.cleaned_data["employee_dob"]
            employee_bld_group=form.cleaned_data["employee_bld_group"]
            employee_joining_date=form.cleaned_data["employee_joining_date"]
            employee_email=form.cleaned_data["employee_email"]
            employee_pan=form.cleaned_data["employee_pan"]
            employee_aadhar=form.cleaned_data["employee_aadhar"]
            employee_voter_id=form.cleaned_data["employee_voter_id"]
            employee_religion=form.cleaned_data["employee_religion"]
            employee_subcaste=form.cleaned_data["employee_subcaste"]
            employee_postal_address=form.cleaned_data["employee_postal_address"]
            employee_dept=Department.objects.get(dept_id = int(employee_dept_id))

            try:
                empcnt=Employee_Details.objects.filter(employee_emp_id=employee_emp_id,employee_type = employee_type,
                                            employee_name=employee_name, employee_gender=employee_gender,
                                            employee_dept_id=employee_dept, employee_designation=employee_designation,
                                            employee_qualification = employee_qualification, employee_profile_pic = employee_profile_pic,
                                            employee_cellphone = employee_cellphone, employee_dob = str(employee_dob),
                                            employee_bld_group = employee_bld_group, employee_joining_date = employee_joining_date,
                                            employee_email = employee_email, employee_pan = employee_pan,
                                            employee_aadhar = employee_aadhar, employee_voter_id = employee_voter_id, 
                                            employee_religion = employee_religion, employee_subcaste = employee_subcaste,
                                            employee_postal_address = employee_postal_address).count()
                if empcnt == 0:
                    emp = Employee_Details.objects.get(employee_id=emp_id)
                    emp.employee_type = employee_type
                    emp.employee_name = employee_name
                    emp.employee_emp_id = employee_emp_id
                    emp.employee_gender = employee_gender
                    emp.employee_profile_pic = employee_profile_pic
                    emp.employee_dept_id = employee_dept
                    emp.employee_designation = employee_designation
                    emp.employee_qualification = employee_qualification
                    emp.employee_cellphone = employee_cellphone
                    emp.employee_dob = employee_dob
                    emp.employee_bld_group = employee_bld_group
                    emp.employee_joining_date = employee_joining_date
                    emp.employee_email = employee_email
                    emp.employee_pan = employee_pan
                    emp.employee_aadhar = employee_aadhar
                    emp.employee_voter_id = employee_voter_id
                    emp.employee_religion = employee_religion
                    emp.employee_subcaste = employee_subcaste
                    emp.employee_postal_address = employee_postal_address
                    with transaction.atomic():
                        emp.save()
                        user = CustomUser.objects.update_user(email = emp.employee_email, username = emp.employee_emp_id, password=str(emp.employee_dob))
                    
                    messages.success(request,"Employee Updated Successfully")
                    return HttpResponseRedirect(reverse("EditEmployee",kwargs={'emp_id':emp_id}))
                else:
                    messages.error(request,"Employee Already Exists")
                    return HttpResponseRedirect(reverse("EditEmployee",kwargs={'emp_id':emp_id}))
            except Exception as e:
                print(e)
                messages.error(request,"Failed to Update Employee")
                return HttpResponseRedirect(reverse("EditEmployee",kwargs={'emp_id':emp_id}))
        else:
            context={'emp_id':emp_id}
            return render(request,"edit_employee.html",context=context)