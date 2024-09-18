from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.urls.base import reverse
from admission.models import CustomUser, Student_Details
from rbac import context_processors
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from rbac.models import RightCategory, RightDetails, RightType, UserRights
from rbac.context_processors import categories_processor
from hr.models import Employee_Details
import base64
from django.db import transaction


# Create your views here.
@login_required
def add_department(request):
    form=AddDepartmentForm()
    DeptInfo=Department.objects.all()
    return render(request,"add_departments.html",{"form":form,'DeptInfo':DeptInfo})

@login_required
def CreateDepartment(request):
    DeptInfo=Department.objects.all()
    if request.method!="POST":
        context={'DeptInfo':DeptInfo}
        return render(request,"add_departments.html",context=context)
    else:
        form=AddDepartmentForm(request.POST)
        if form.is_valid():
            abbr=form.cleaned_data["dept_abbr"]
            name=form.cleaned_data["dept_name"]
            start_year=form.cleaned_data["start_year"]
            close_year=form.cleaned_data["close_year"]
            try:
                deptcnt=Department.objects.filter(dept_abbr=abbr,dept_name=name).count()
                if deptcnt == 0:
                    right=Department.objects.create(dept_abbr=abbr,dept_name=name,start_year=start_year,close_year=close_year)
                    messages.success(request,"Department Added Successfully")
                    return HttpResponseRedirect(reverse("AddDepartment"))
                else:
                    messages.error(request,"Department Already Exists")
                    context={'DeptInfo':DeptInfo}
                    return HttpResponseRedirect(reverse("AddDepartment"))
            except Exception as e:
                messages.error(request,"Failed to Add Department")
                return HttpResponseRedirect(reverse("AddDepartment"))
        else:
            context={'DeptInfo':DeptInfo}
            return render(request,"add_departments.html",context=context)

@login_required
def edit_department(request,dept_id):
   
    dept=Department.objects.get(dept_id=dept_id)
    form=EditDepartmentForm()
    form.fields['dept_abbr'].initial=dept.dept_abbr
    form.fields['dept_name'].initial=dept.dept_name
    form.fields['start_year'].initial=dept.start_year
    form.fields['close_year'].initial=dept.close_year
    context={'form':form,'dept_id':dept_id}
    return render(request,"edit_department.html",context=context)

@login_required
def EditDepartment(request):
    dept_id = int(request.POST.get('dept_id'))
   
    if request.method!="POST":
        return render(request,"add_departments.html")
    else:
        form=EditDepartmentForm(request.POST)
        if form.is_valid():
            abbr=form.cleaned_data["dept_abbr"]
            name=form.cleaned_data["dept_name"]
            start_year=form.cleaned_data["start_year"]
            close_year=form.cleaned_data["close_year"]
            try:
                deptcnt=Department.objects.filter(dept_abbr=abbr,dept_name=name).count()
                if deptcnt == 0:
                    dept = Department.objects.get(dept_id = dept_id)
                    dept.dept_abbr = abbr
                    dept.dept_name = name
                    dept.start_year = start_year
                    dept.close_year = close_year
                    dept.save()
                    messages.success(request,"Department Updated Successfully")
                    return HttpResponseRedirect(reverse("EditDepartment",kwargs={'dept_id':dept_id}))
                else:
                    messages.error(request,"Department Already Exists")
                    return HttpResponseRedirect(reverse("EditDepartment",kwargs={'dept_id':dept_id}))
            except Exception as e:
                print(e)
                messages.error(request,"Failed to Update Department")
                return HttpResponseRedirect(reverse("EditDepartment",kwargs={'dept_id':dept_id}))
        else:
            return render(request,"edit_department.html")

@login_required
def add_religion(request):
    form=AddReligionForm()
    ReligionInfo=Religion.objects.all()
    return render(request,"add_religion.html",{"form":form,'ReligionInfo':ReligionInfo})

@login_required
def CreateReligion(request):
    ReligionInfo=Religion.objects.all()
    if request.method!="POST":
        context={'ReligionInfo':ReligionInfo}
        return render(request,"add_religion.html",context=context)
    else:
        form=AddReligionForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data["name"]
            try:
                religioncnt=Religion.objects.filter(name=name).count()
                print(religioncnt)
                if religioncnt == 0:
                    religion=Religion.objects.create(name=name)
                    messages.success(request,"Religion Added Successfully")
                    return HttpResponseRedirect(reverse("AddReligion"))
                else:
                    messages.error(request,"Religion Already Exists")
                    context={'ReligionInfo':ReligionInfo}
                    return HttpResponseRedirect(reverse("AddReligion"))
            except Exception as e:
                print(e)
                messages.error(request,"Failed to Add Religion")
                return HttpResponseRedirect(reverse("AddReligion"))
        else:
            context={'ReligionInfo':ReligionInfo}
            return render(request,"add_religion.html",context=context)

@login_required
def edit_religion(request,religion_id):
    religion=Religion.objects.get(id=religion_id)
    form=EditReligionForm()
    form.fields['name'].initial=religion.name
    context={'form':form,'religion_id':religion_id}
    return render(request,"edit_religion.html",context=context)

@login_required
def EditReligion(request):
    religion_id = int(request.POST.get('religion_id'))
   
    if request.method!="POST":
        return render(request,"add_religion.html")
    else:
        form=EditReligionForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data["name"]
            try:
                religioncnt=Religion.objects.filter(name=name).count()
                if religioncnt == 0:
                    religion = Religion.objects.get(id = religion_id)
                    religion.name = name
                    religion.save()
                    messages.success(request,"Religion Updated Successfully")
                    return HttpResponseRedirect(reverse("EditReligion",kwargs={'religion_id':religion_id}))
                else:
                    messages.error(request,"Religion Already Exists")
                    return HttpResponseRedirect(reverse("EditReligion",kwargs={'religion_id':religion_id}))
            except Exception as e:
                print(e)
                messages.error(request,"Failed to Update Religion")
                return HttpResponseRedirect(reverse("EditReligion",kwargs={'religion_id':religion_id}))
        else:
            context={'religion_id':religion_id}
            return render(request,"edit_religion.html",context=context)

@login_required
def add_states(request):
    form=AddStatesForm()
    StatesInfo=States.objects.all()
    return render(request,"add_states.html",{"form":form,'StatesInfo':StatesInfo})

@login_required
def CreateStates(request):
    StatesInfo=States.objects.all()
    if request.method!="POST":
        context={'StatesInfo':StatesInfo}
        return render(request,"add_states.html",context=context)
    else:
        form=AddStatesForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data["name"]
            try:
                statecnt=Religion.objects.filter(name=name).count()
                if statecnt == 0:
                    state=States.objects.create(name=name)
                    messages.success(request,"State Added Successfully")
                    return HttpResponseRedirect(reverse("AddStates"))
                else:
                    messages.error(request,"State Already Exists")
                    context={'StatesInfo':StatesInfo}
                    return HttpResponseRedirect(reverse("AddStates"))
            except Exception as e:
                print(e)
                messages.error(request,"Failed to Add State")
                return HttpResponseRedirect(reverse("AddStates"))
        else:
            context={'StatesInfo':StatesInfo}
            return render(request,"add_states.html",context=context)

@login_required
def edit_states(request,state_id):
    state=States.objects.get(id=state_id)
    form=EditStatesForm()
    form.fields['name'].initial=state.name
    context={'form':form,'state_id':state_id}
    return render(request,"edit_states.html",context=context)

@login_required
def EditStates(request):
    state_id = int(request.POST.get('state_id'))
    if request.method!="POST":
        return render(request,"add_states.html")
    else:
        form=EditStatesForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data["name"]

            try:
                statecnt=States.objects.filter(name=name).count()
                if statecnt == 0:
                    state = States.objects.get(id = state_id)
                    state.name = name
                    state.save()
                    messages.success(request,"State Updated Successfully")
                    return HttpResponseRedirect(reverse("EditStates",kwargs={'state_id':state_id}))
                else:
                    messages.error(request,"State Already Exists")
                    return HttpResponseRedirect(reverse("EditStates",kwargs={'state_id':state_id}))
            except Exception as e:
                print(e)
                messages.error(request,"Failed to Update State")
                return HttpResponseRedirect(reverse("EditStates",kwargs={'state_id':state_id}))
        else:
            context={'state_id':state_id}
            return render(request,"edit_states.html",context=context)

@login_required
def add_bloodgroup(request):
    form=AddBloodGroupForm()
    BGInfo=BloodGroup.objects.all()
    return render(request,"add_bloodgroup.html",{"form":form,'BGInfo':BGInfo})

@login_required
def CreateBloodGroup(request):
    BGInfo=BloodGroup.objects.all()
    if request.method!="POST":
        context={'BGInfo':BGInfo}
        return render(request,"add_bloodgroup.html",context=context)
    else:
        form=AddBloodGroupForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data["name"]
            try:
                bgcnt=BloodGroup.objects.filter(name=name).count()
                if bgcnt == 0:
                    state=BloodGroup.objects.create(name=name)
                    messages.success(request,"Blood Group Added Successfully")
                    return HttpResponseRedirect(reverse("AddBloodGroup"))
                else:
                    messages.error(request,"Blood Group Already Exists")
                    context={'BGInfo':BGInfo}
                    return HttpResponseRedirect(reverse("AddBloodGroup"))
            except Exception as e:
                print(e)
                messages.error(request,"Failed to Add Blood Group")
                return HttpResponseRedirect(reverse("AddBloodGroup"))
        else:
            context={'BGInfo':BGInfo}
            return render(request,"add_bloodgroup.html",context=context)

@login_required
def edit_bloodgroup(request,bg_id):
    bg=BloodGroup.objects.get(id=bg_id)
    form=EditBloodGroupForm()
    form.fields['name'].initial=bg.name
    context={'form':form,'bg_id':bg_id}
    return render(request,"edit_bloodgroup.html",context=context)

@login_required
def EditBloodGroup(request):
    bg_id = int(request.POST.get('bg_id'))
    if request.method!="POST":
        return render(request,"add_bloodgroup.html")
    else:
        form=EditBloodGroupForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data["name"]
            try:
                bgcnt=BloodGroup.objects.filter(name=name).count()
                if bgcnt == 0:
                    bg = BloodGroup.objects.get(id = bg_id)
                    bg.name = name
                    bg.save()
                    messages.success(request,"Blood Group Updated Successfully")
                    return HttpResponseRedirect(reverse("EditBloodGroup",kwargs={'bg_id':bg_id}))
                else:
                    messages.error(request,"Blood Group Already Exists")
                    return HttpResponseRedirect(reverse("EditBloodGroup",kwargs={'bg_id':bg_id}))
            except Exception as e:
                print(e)
                messages.error(request,"Failed to Update Blood Group")
                return HttpResponseRedirect(reverse("EditBloodGroup",kwargs={'bg_id':bg_id}))
        else:
            context={'bg_id':bg_id}
            return render(request,"edit_bloodgroup.html",context=context)

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
            employee_profile_pic=form.cleaned_data["employee_profile_pic"]
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
            employee_religion = Religion.objects.get(id = int(employee_religion))

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
@login_required
def add_academicyear(request):
    form=AddAcademicYearForm()
    AcaYearInfo=AcademicYear.objects.all()
    return render(request,"add_academicyear.html",{"form":form,'AcaYearInfo':AcaYearInfo})

@login_required
def CreateAcademicYear(request):
    AcadYearInfo=AcademicYear.objects.all()
    if request.method!="POST":
        context={'AcadYearInfo':AcadYearInfo}
        return render(request,"add_academicyear.html",context=context)
    else:
        form=AddAcademicYearForm(request.POST)
        if form.is_valid():
            acayear=form.cleaned_data["aca_year"]

            try:
                acayearcount=AcademicYear.objects.filter(acayear=acayear).count()
                if acayearcount == 0:
                    AcademicYear.objects.create(acayear=acayear)
                    messages.success(request,"Academic Year Added Successfully")
                    return HttpResponseRedirect(reverse("AddAcademicYear"))
                else:
                    messages.error(request,"Academic Year Already Exists")
                    context={'AcadYearInfo':AcadYearInfo}
                    return HttpResponseRedirect(reverse("AddAcademicYear"))
            except Exception as e:
                messages.error(request,"Failed to Academic Year")
                return HttpResponseRedirect(reverse("AddAcademicYear"))
        else:
            context={'AcadYearInfo':AcadYearInfo}
            return render(request,"add_academicyear.html",context=context)

@login_required
def edit_acayear(request,acayear_id):
    acayear=AcademicYear.objects.get(id=acayear_id)
    form=EditAcademicYearForm()
    form.fields['aca_year'].initial=acayear.acayear
    context={'form':form,'acayear_id':acayear_id}
    return render(request,"edit_acayear.html",context=context)

@login_required
def EditAcaYear(request):
    acayear_id = int(request.POST.get('acayear_id'))
    
    if request.method!="POST":
        return render(request,"edit_academicyear.html")
    else:
        form=EditAcademicYearForm(request.POST)
        if form.is_valid():
            aca_year=form.cleaned_data["aca_year"]

            try:
                acacount=AcademicYear.objects.filter(acayear=aca_year).count()
                if acacount == 0:
                    academicyear = AcademicYear.objects.get(id = acayear_id)
                    academicyear.acayear = aca_year
                    academicyear.save()
                    messages.success(request,"Academic Year Updated Successfully")
                    return HttpResponseRedirect(reverse("Editacayear",kwargs={'acayear_id':acayear_id}))
                else:
                    messages.error(request,"Academic Year Already Exists")
                    return HttpResponseRedirect(reverse("Editacayear",kwargs={'acayear_id':acayear_id}))
            except Exception as e:
                messages.error(request,"Failed to Update Academic Year")
                return HttpResponseRedirect(reverse("Editacayear",kwargs={'acayear_id':acayear_id}))
        else:
            context={'acayear_id':acayear_id}
            return render(request,"edit_academicyear.html",context=context)

#Division mastermanagement
@login_required
def add_division(request):
    form=AddDivisionForm()
    DivInfo=Division.objects.all()
    return render(request,"add_division.html",{"form":form,'DivInfo':DivInfo})

@login_required
def CreateDivision(request):
    DivisionInfo=Division.objects.all()
    if request.method!="POST":
        context={'DivisionInfo':DivisionInfo}
        return render(request,"add_division.html",context=context)
    else:
        form=AddDivisionForm(request.POST)
        if form.is_valid():
            div=form.cleaned_data["divname"]

            try:
                divcounts=Division.objects.filter(division=div).count()
                if divcounts == 0:
                    Division.objects.create(division=div)
                    messages.success(request,"Division Added Successfully")
                    return HttpResponseRedirect(reverse("AddDivision"))
                else:
                    messages.error(request,"Division Already Exists")
                    context={'DivisionInfo':DivisionInfo}
                    return HttpResponseRedirect(reverse("AddDivision"))
            except Exception as e:
                messages.error(request,"Failed to Division")
                return HttpResponseRedirect(reverse("AddDivision"))
        else:
            context={'DivisionInfo':DivisionInfo}
            return render(request,"add_division.html",context=context)

#room management
@login_required
def add_room(request):
    form=AddRoomForm()
    Roominfo=Room.objects.all()
    return render(request,"add_room.html",{"form":form,'Roominfo':Roominfo})

@login_required
def CreateRoom(request):
    RoomInfo=Room.objects.all()
    if request.method!="POST":
        context={'RoomInfo':RoomInfo}
        return render(request,"add_room.html",context=context)
    else:
        form=AddRoomForm(request.POST)
        if form.is_valid():
            room=form.cleaned_data["roomname"]
            row=form.cleaned_data["rowname"]
            col=form.cleaned_data["colname"]
            seats=form.cleaned_data["total_seats"]

            try:
                roomcounts=Room.objects.filter(room_name=room).count()
                if roomcounts == 0:
                    Room.objects.create(room_name=room,row=row,column=col,Total_seats=seats)
                    messages.success(request,"Room Added Successfully")
                    return HttpResponseRedirect(reverse("AddRooms"))
                else:
                    messages.error(request,"Room Already Exists")
                    context={'RoomInfo':RoomInfo}
                    return HttpResponseRedirect(reverse("AddRooms"))
            except Exception as e:
                print(e)
                messages.error(request,"Failed to Room")
                return HttpResponseRedirect(reverse("AddRooms"))
        else:
            context={'RoomInfo':RoomInfo}
            return render(request,"add_room.html",context=context)

@login_required
def edit_room(request,room_id):
    roominfo=Room.objects.get(room_id=room_id)
    form=EditRoomForm()
    form.fields['roomname'].initial=roominfo.room_name
    context={'form':form,'room_id':room_id}
    return render(request,"edit_room.html",context=context)

@login_required
def EditRoom(request):
    room_id = int(request.POST.get('room_id'))
    if request.method!="POST":
        return render(request,"edit_room.html")
    else:
        form=EditRoomForm(request.POST)
        if form.is_valid():
            roomfield=form.cleaned_data["roomname"]
            row=form.cleaned_data["rowname"]
            col=form.cleaned_data["colname"]
            seats=form.cleaned_data["total_seats"]
            print(row)
            try:
                roomcount=Room.objects.filter(room_name=roomfield).count()
                if roomcount == 0:
                    roomcol = Room.objects.get(room_id = room_id)
                    roomcol.room_name = roomfield
                    roomcol.row = row
                    roomcol.column = col
                    roomcol.Total_seats = seats
                    roomcol.save()
                    messages.success(request,"Room Updated Successfully")
                    return HttpResponseRedirect(reverse("Editroom",kwargs={'room_id':room_id}))
                else:
                    messages.error(request,"Room Already Exists")
                    return HttpResponseRedirect(reverse("Editroom",kwargs={'room_id':room_id}))
            except Exception as e:
                messages.error(request,"Failed to Update Room")
                return HttpResponseRedirect(reverse("Editroom",kwargs={'room_id':room_id}))
        else:
            context={'room_id':room_id}
            return render(request,"edit_room.html.html",context=context)


@login_required
def edit_division(request,div_id):
    divinfo=Division.objects.get(id=div_id)
    form=EditDivisionForm()
    form.fields['divname'].initial=divinfo.division
    context={'form':form,'div_id':div_id}
    return render(request,"edit_division.html",context=context)

@login_required
def EditDivision(request):
    div_id = int(request.POST.get('div_id'))
    if request.method!="POST":
        return render(request,"edit_division.html")
    else:
        form=EditDivisionForm(request.POST)
        if form.is_valid():
            divfield=form.cleaned_data["divname"]
            try:
                divcount=Division.objects.filter(division=divfield).count()
                if divcount == 0:
                    divcol = Division.objects.get(id = div_id)
                    divcol.division = divfield
                    divcol.save()
                    messages.success(request,"Division Updated Successfully")
                    return HttpResponseRedirect(reverse("Editdivision",kwargs={'div_id':div_id}))
                else:
                    messages.error(request,"Division Already Exists")
                    return HttpResponseRedirect(reverse("Editdivision",kwargs={'div_id':div_id}))
            except Exception as e:
                messages.error(request,"Failed to Update Division")
                return HttpResponseRedirect(reverse("Editdivision",kwargs={'div_id':div_id}))
        else:
            context={'div_id':div_id}
            return render(request,"edit_division.html.html",context=context)

#User Type mastermanagement view 
@login_required
def add_usertype(request):
    form=AddUsertypeForm()
    usertypeinfo=UserType.objects.all()
    return render(request,"add_usertype.html",{"form":form,'usertypeinfo':usertypeinfo})

@login_required
def CreateUserType(request):
    usertypeinfo=UserType.objects.all()
    if request.method!="POST":
        context={'usertypeinfo':usertypeinfo}
        return render(request,"add_usertype.html",context=context)
    else:
        form=AddUsertypeForm(request.POST)
        if form.is_valid():
            usertypeId=form.cleaned_data["usertype_id"]
            usertypename=form.cleaned_data["Usertype_Name"]

            try:
                usertypecount=UserType.objects.filter(usertype_id=usertypeId,usertype_name=usertypename).count()
                if usertypecount == 0:
                    UserType.objects.create(usertype_id=usertypeId,usertype_name=usertypename)
                    messages.success(request,"User Type Added Successfully")
                    return HttpResponseRedirect(reverse("AddUserType"))
                else:
                    messages.error(request,"User Type Already Exists")
                    context={'usertypeinfo':usertypeinfo}
                    return HttpResponseRedirect(reverse("AddUserType"))
            except Exception as e:
                messages.error(request,"Failed to add user type")
                return HttpResponseRedirect(reverse("AddUserType"))
        else:
            context={'usertypeinfo':usertypeinfo}
            return render(request,"add_usertype.html",context=context)

@login_required
def edit_usertype(request,usertype_id):
    
    divinfo=UserType.objects.get(id=usertype_id)
    form=EditUsertypeForm()
    form.fields['usertype_id'].initial=divinfo.usertype_id
    form.fields['Usertype_Name'].initial=divinfo.usertype_name
    context={'form':form,'usertype_id':usertype_id}
    return render(request,"edit_usertype.html",context=context)

@login_required
def EditUsertype(request):
    usertype_id = int(request.POST.get('usertype_id'))
    if request.method!="POST":       
        return render(request,"edit_division.html")
    else:
        form=EditUsertypeForm(request.POST)
        if form.is_valid():
            usertypeid=form.cleaned_data["usertype_id"]
            usertypename=form.cleaned_data["Usertype_Name"]
            try:
                usertypecount=UserType.objects.filter(usertype_id=usertypeid, usertype_name=usertypename).count()
                if usertypecount == 0:
                    usertype_info = UserType.objects.get(id = usertype_id)
                    usertype_info.usertype_id = usertypeid
                    usertype_info.usertype_name = usertypename
                    usertype_info.save()
                    messages.success(request,"UserType Updated Successfully")
                    return HttpResponseRedirect(reverse("Editusertype",kwargs={'usertype_id':usertype_id}))
                else:
                    messages.error(request,"UserType Already Exists")
                    return HttpResponseRedirect(reverse("Editusertype",kwargs={'usertype_id':usertype_id}))
            except Exception as e:
                messages.error(request,"Failed to Update UserType")
                return HttpResponseRedirect(reverse("Editusertype",kwargs={'usertype_id':usertype_id}))
        else:
            context={'usertype_id':usertype_id}
            return render(request,"edit_usertype.html",context=context)

@login_required
def reset_password(request):
    form=PasswordResetForm(request.user, request.POST)
    return render(request,"reset_password.html",{"form":form})

@login_required
def ResetPassword(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.user, request.POST)
        if form.is_valid():
            user_name=form.cleaned_data["user_id"]
            password=form.cleaned_data["password1"]
            try:
                username=CustomUser.objects.get(id=user_name)
                user=CustomUser.objects.filter(id=user_name)
                email = None
                for usr in user:
                    #check for employee
                    if usr.user_type == 2 or usr.user_type == 4 or usr.user_type == 6 or usr.user_type == 7:
                        emp = Employee_Details.objects.get(employee_emp_id = usr.username)
                        email = emp.employee_email
                    #To check developer type
                    if usr.user_type == 5:
                        emp = Employee_Details.objects.get(employee_emp_id = usr.username)
                        email = emp.employee_email
                    #check for student
                    elif usr.user_type == 3:
                        student = Student_Details.objects.get(st_uid = usr.username)
                        email = student.st_email_id
                    #check for admin
                    #this condition shall never be checked!!
                    elif usr.user_type == 1:
                        usrType = usr.user_type

            except Exception as e:
                print(e)
                return { }
            if email is None:
                email = username+"@sdmcet.ac.in"            
            user = CustomUser.objects.update_user(email = email, username = username, password=password)
            messages.success(request, 'Password Changed successfully!')
            return redirect('reset_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordResetForm(request.user, request.POST)
    return render(request, 'reset_password.html', {'form': form})

# Admission Quota Master management
@login_required
def add_Quota(request):
    form=AddQuotaForm()
    quota=Admission_Quota.objects.all()
    try:
        userName=CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        return HttpResponseRedirect('/')
    return render(request,"add_quota.html",{"form":form, 'username':userName,'quota':quota})

@login_required
def CreateQuota(request):
    quota=Admission_Quota.objects.all()
    if request.method!="POST":
        # userName=CustomUser.objects.get(id=request.user.id)
        # context={'username':userName,'quota':quota}
        context={'quota':quota}
        return render(request,"add_quota.html",context=context)
    else:
        form=AddQuotaForm(request.POST)
        if form.is_valid():
            quotaname=form.cleaned_data["Name"]

            try:
                quotacount=Admission_Quota.objects.filter(name=quotaname).count()
                if quotacount == 0:
                    Admission_Quota.objects.create(name=quotaname)
                    messages.success(request,"Quota Added Successfully")
                    return HttpResponseRedirect(reverse("AddQuota"))
                else:
                    messages.error(request,"Quota Already Exists")
                    context={'username':userName,'quota':quota}
                    return HttpResponseRedirect(reverse("AddQuota"))
            except Exception as e:
                messages.error(request,"Failed to add user type")
                return HttpResponseRedirect(reverse("AddQuota"))
        else:
            userName=CustomUser.objects.get(id=request.user.id)
            context={'username':userName,'quota':quota}
            return render(request,"add_quota.html",context=context)


@login_required
def edit_quota(request,quota_id):
    userName=CustomUser.objects.get(id=request.user.id)
    quotaInfo=Admission_Quota.objects.get(id=quota_id)
    form=EditQuotaForm()
    form.fields['Name'].initial=quotaInfo.name
    context={'form':form,'username':userName,'quota_id':quota_id}
    return render(request,"edit_quota.html",context=context)

@login_required
def EditQuota(request):
    quota_id = int(request.POST.get('quota_id'))
    userName=CustomUser.objects.get(id=request.user.id)
    if request.method!="POST":
        # userName=CustomUser.objects.get(id=request.user.id)
        # context={'username':userName}
        return render(request,"edit_quota.html")
    else:
        form=EditQuotaForm(request.POST)
        if form.is_valid():
            quotaname=form.cleaned_data["Name"]
            try:
                quotacount=Admission_Quota.objects.filter(id=quota_id, name=quotaname).count()
                if quotacount == 0:
                    quotaInfo = Admission_Quota.objects.get(id = quota_id)
                    quotaInfo.name = quotaname
                    quotaInfo.save()
                    messages.success(request,"Quota Updated Successfully")
                    return HttpResponseRedirect(reverse("Editquota",kwargs={'quota_id':quota_id}))
                else:
                    messages.error(request,"Quota Already Exists")
                    context={'username':userName}
                    return HttpResponseRedirect(reverse("Editquota",kwargs={'quota_id':quota_id}))
            except Exception as e:
                messages.error(request,"Failed to Update Quota")
                return HttpResponseRedirect(reverse("Editquota",kwargs={'quota_id':quota_id}))
        else:
            # context={'username':userName,'usertype_id':usertype_id}
            return render(request,"edit_quota.html")

# Months Master management
@login_required
def add_Months(request):
    form=AddMonthsForm()
    month=Months.objects.all()
    try:
        userName=CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        return HttpResponseRedirect('/')
    return render(request,"add_month.html",{"form":form, 'username':userName,'month':month})

@login_required
def CreateMonths(request):
    month=Months.objects.all()
    if request.method!="POST":
        # userName=CustomUser.objects.get(id=request.user.id)
        # context={'username':userName,'quota':quota}
        context={'month':month}
        return render(request,"add_month.html",context=context)
    else:
        form=AddMonthsForm(request.POST)
        if form.is_valid():
            monthname=form.cleaned_data["Name"]

            try:
                monthcount=Months.objects.filter(name=monthname).count()
                if monthcount == 0:
                    Months.objects.create(name=monthname)
                    messages.success(request,"Month Added Successfully")
                    return HttpResponseRedirect(reverse("AddMonths"))
                else:
                    messages.error(request,"Month Already Exists")
                    context={'username':userName,'month':month}
                    return HttpResponseRedirect(reverse("AddMonths"))
            except Exception as e:
                messages.error(request,"Failed to add Month")
                return HttpResponseRedirect(reverse("AddMonths"))
        else:
            userName=CustomUser.objects.get(id=request.user.id)
            context={'username':userName,'month':month}
            return render(request,"add_month.html",context=context)


@login_required
def edit_month(request,month_id):
    userName=CustomUser.objects.get(id=request.user.id)
    monthInfo=Months.objects.get(id=month_id)
    form=EditMonthsForm()
    form.fields['Name'].initial=monthInfo.name
    context={'form':form,'username':userName,'month_id':month_id}
    return render(request,"edit_month.html",context=context)

@login_required
def EditMonth(request):
    month_id = int(request.POST.get('month_id'))
    # userName=CustomUser.objects.get(id=request.user.id)
    if request.method!="POST":
        # userName=CustomUser.objects.get(id=request.user.id)
        # context={'username':userName}
        return render(request,"edit_month.html")
    else:
        form=EditMonthsForm(request.POST)
        if form.is_valid():
            monthname=form.cleaned_data["Name"]
            try:
                monthcount=Months.objects.filter(id=month_id, name=monthname).count()
                if monthcount == 0:
                    monthInfo = Months.objects.get(id = month_id)
                    monthInfo.name = monthname
                    monthInfo.save()
                    messages.success(request,"Month Updated Successfully")
                    return HttpResponseRedirect(reverse("Editmonth",kwargs={'month_id':month_id}))
                else:
                    messages.error(request,"Month Already Exists")
                    # context={'username':userName}
                    return HttpResponseRedirect(reverse("Editmonth",kwargs={'month_id':month_id}))
            except Exception as e:
                messages.error(request,"Failed to Update Month")
                return HttpResponseRedirect(reverse("Editmonth",kwargs={'month_id':month_id}))
        else:
            # context={'username':userName,'usertype_id':usertype_id}
            return render(request,"edit_month.html")

# Category Master Management
@login_required
def add_Category(request):
    form=AddCategoryForm()
    cat=Category.objects.all()
    try:
        pass
        # userName=CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        return HttpResponseRedirect('/')
    return render(request,"add_Category.html",{'form':form,'cat':cat})

@login_required
def CreateCategory(request):
    cat=Category.objects.all()
    if request.method!="POST":
        # userName=CustomUser.objects.get(id=request.user.id)
        context={'cat':cat}
        return render(request,"add_Category.html",context=context)
    else:
        form=AddCategoryForm(request.POST)
        if form.is_valid():
            categoryname=form.cleaned_data["Name"]
            try:
                categroycount=Category.objects.filter(name=categoryname).count()
                if categroycount == 0:
                    Category.objects.create(name=categoryname)
                    messages.success(request,"Category Added Successfully")
                    return HttpResponseRedirect(reverse("AddCategory"))
                else:
                    messages.error(request,"Category Already Exists")
                    context={'cat':cat}
                    return HttpResponseRedirect(reverse("AddCategory"))
            except Exception as e:
                messages.error(request,"Failed to add Category")
                return HttpResponseRedirect(reverse("AddCategory"))
        else:
            # userName=CustomUser.objects.get(id=request.user.id)
            context={'cat':cat}
            return render(request,"add_Category.html",context=context)

@login_required
def edit_category(request,category_id):
    userName=CustomUser.objects.get(id=request.user.id)
    categoryInfo=Category.objects.get(id=category_id)
    form=EditCategoryForm()
    form.fields['Name'].initial=categoryInfo.name
    context={'form':form,'username':userName,'category_id':category_id}
    return render(request,"edit_category.html",context=context)

@login_required
def EditCategory(request):
    category_id = int(request.POST.get('category_id'))
    userName=CustomUser.objects.get(id=request.user.id)
    if request.method!="POST":
        userName=CustomUser.objects.get(id=request.user.id)
        context={'username':userName}
        return render(request,"edit_category.html", context = context)
    else:
        form=EditCategoryForm(request.POST)
        if form.is_valid():
            categoryname=form.cleaned_data["Name"]
            try:
                categorycount=Category.objects.filter(id=category_id, name=categoryname).count()
                if categorycount == 0:
                    categoryInfo = Category.objects.get(id = category_id)
                    categoryInfo.name = categoryname
                    categoryInfo.save()
                    messages.success(request,"Category Updated Successfully")
                    return HttpResponseRedirect(reverse("EditCategory",kwargs={'category_id':category_id}))
                else:
                    messages.error(request,"Category Already Exists")
                    # context={'username':userName}
                    return HttpResponseRedirect(reverse("EditCategory",kwargs={'category_id':category_id}))
            except Exception as e:
                messages.error(request,"Failed to Update Category")
                return HttpResponseRedirect(reverse("EditCategory",kwargs={'category_id':category_id}))
        else:
            # context={'username':userName,'usertype_id':usertype_id}
            return render(request,"edit_category.html")

#Semester master management
@login_required
def add_Semester(request):
    form=AddSemesterForm()
    # semester=Semester.objects.all()
    try:
        userName=CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        return HttpResponseRedirect('/')
    return render(request,"add_Semester.html",{"form":form, 'username':userName,'semester':semester})

@login_required
def CreateSemester(request):
    semester=Semester.objects.all()
    if request.method!="POST":
        # userName=CustomUser.objects.get(id=request.user.id)
        # context={'username':userName,'quota':quota}
        context={'semester':semester}
        return render(request,"add_Semester.html",context=context)
    else:
        form=AddSemesterForm(request.POST)
        if form.is_valid():
            sem=form.cleaned_data["Name"]

            try:
                semcount=Category.objects.filter(name=sem).count()
                if semcount == 0:
                    Semester.objects.create(name=sem)
                    messages.success(request,"Semester Added Successfully")
                    return HttpResponseRedirect(reverse("AddSemester"))
                else:
                    messages.error(request,"Semester Already Exists")
                    context={'username':userName,'semester':semester}
                    return HttpResponseRedirect(reverse("AddSemester"))
            except Exception as e:
                messages.error(request,"Failed to add Semester")
                return HttpResponseRedirect(reverse("AddSemester"))
        else:
            userName=CustomUser.objects.get(id=request.user.id)
            context={'username':userName,'semester':semester}
            return render(request,"add_Semester.html",context=context)

@login_required
def edit_semester(request,sem_id):
    userName=CustomUser.objects.get(id=request.user.id)
    semInfo=Semester.objects.get(id=sem_id)
    form=EditSemesterForm()
    form.fields['Name'].initial=semInfo.name
    context={'form':form,'username':userName,'sem_id':sem_id}
    return render(request,"edit_semester.html",context=context)

@login_required
def EditSemester(request):
    sem_id = int(request.POST.get('sem_id'))
    # userName=CustomUser.objects.get(id=request.user.id)
    if request.method!="POST":
        # userName=CustomUser.objects.get(id=request.user.id)
        # context={'username':userName}
        return render(request,"edit_semester.html")
    else:
        form=EditSemesterForm(request.POST)
        if form.is_valid():
            semname=form.cleaned_data["Name"]
            try:
                semcount=Semester.objects.filter(id=sem_id, name=semname).count()
                if semcount == 0:
                    semInfo = Semester.objects.get(id = sem_id)
                    semInfo.name = semname
                    semInfo.save()
                    messages.success(request,"Semester Updated Successfully")
                    return HttpResponseRedirect(reverse("EditSemester",kwargs={'sem_id':sem_id}))
                else:
                    messages.error(request,"Semester Already Exists")
                    # context={'username':userName}
                    return HttpResponseRedirect(reverse("EditSemester",kwargs={'sem_id':sem_id}))
            except Exception as e:
                messages.error(request,"Failed to Update Semester")
                return HttpResponseRedirect(reverse("EditSemester",kwargs={'sem_id':sem_id}))
        else:
            # context={'username':userName,'usertype_id':usertype_id}
            return render(request,"edit_semester.html")

#External Valuators college list master management
@login_required
def add_ExtValCollege(request):
    form=AddExtValCollegeForm()
    extclglist=ExtValuatorCollegeName.objects.all()
    try:
        userName=CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        return HttpResponseRedirect('/')
    return render(request,"add_ExtCollegeName.html",{"form":form, 'username':userName,'extclglist':extclglist})

@login_required
def CreateExtValCollege(request):
    extclglist=ExtValuatorCollegeName.objects.all()
    if request.method!="POST":
        context={'extclglist':extclglist}
        return render(request,"add_ExtCollegeName.html",context=context)
    else:
        form=AddExtValCollegeForm(request.POST)
        if form.is_valid():
            collegename=form.cleaned_data["Name"]
            try:
                collgelist=ExtValuatorCollegeName.objects.filter(name=collegename).count()
                if collgelist == 0:
                    ExtValuatorCollegeName.objects.create(name=collegename)
                    messages.success(request,"College Added Successfully")
                    return HttpResponseRedirect(reverse("AddExtValCollege"))
                else:
                    messages.error(request,"College Already Exists")
                    context={'username':userName,'collgelist':collgelist}
                    return HttpResponseRedirect(reverse("AddExtValCollege"))
            except Exception as e:
                messages.error(request,"Failed to add College")
                return HttpResponseRedirect(reverse("AddExtValCollege"))
        else:
            userName=CustomUser.objects.get(id=request.user.id)
            context={'username':userName,'extclglist':extclglist}
            return render(request,"add_ExtCollegeName.html",context=context)


@login_required
def edit_College(request,clg_id):
    # userName=CustomUser.objects.get(id=request.user.id)
    collegeInfo=ExtValuatorCollegeName.objects.get(id=clg_id)
    form=EditExtValCollegeForm()
    form.fields['Name'].initial=collegeInfo.name
    context={'form':form,'clg_id':clg_id}
    return render(request,"edit_College.html",context=context)

@login_required
def EditExtValCollege(request):
    clg_id = int(request.POST.get('clg_id'))
    # userName=CustomUser.objects.get(id=request.user.id)
    if request.method!="POST":
        # userName=CustomUser.objects.get(id=request.user.id)
        # context={'username':userName}
        return render(request,"edit_College.html")
    else:
        form=AddExtValCollegeForm(request.POST)
        if form.is_valid():
            collegename=form.cleaned_data["Name"]
            try:
                colllgecount=ExtValuatorCollegeName.objects.filter(id=clg_id, name=collegename).count()
                if colllgecount == 0:
                    collegeInfo = ExtValuatorCollegeName.objects.get(id = clg_id)
                    collegeInfo.name = collegename
                    collegeInfo.save()
                    messages.success(request,"College Updated Successfully")
                    return HttpResponseRedirect(reverse("EditExtValCollege",kwargs={'clg_id':clg_id}))
                else:
                    messages.error(request,"College Already Exists")
                    # context={'username':userName}
                    return HttpResponseRedirect(reverse("EditExtValCollege",kwargs={'clg_id':clg_id}))
            except Exception as e:
                messages.error(request,"Failed to Update College")
                return HttpResponseRedirect(reverse("EditExtValCollege",kwargs={'clg_id':clg_id}))
        else:
            # context={'username':userName,'usertype_id':usertype_id}
            return render(request,"edit_College.html")

#Grade Mapping master management
@login_required
def add_Gradempping(request):
    form=AddGradeMappingForm()
    gradelist=GradeMapping.objects.all().order_by('-GradeScheme')
    try:
        userName=CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        return HttpResponseRedirect('/')
    return render(request,"add_GradeMapping.html",{"form":form, 'username':userName,'gradelist':gradelist})

@login_required
def CreateGradempping(request):
    gradelist=GradeMapping.objects.all()
    if request.method!="POST":
        context={'gradelist':gradelist}
        return render(request,"add_GradeMapping.html",context=context)
    else:
        form=AddGradeMappingForm(request.POST)
        if form.is_valid():
            minmarks = form.cleaned_data["MinMarks"]
            MaxMarks = form.cleaned_data["MaxMarks"]
            GradePoints = form.cleaned_data["GradePoints"]
            Grade = form.cleaned_data["Grade"]
            GradeScheme = form.cleaned_data["GradeScheme"]
            TotalMarks = form.cleaned_data["TotalMarks"]
            try:
                grdlistcnt=GradeMapping.objects.filter(Grade=Grade,GradeScheme=GradeScheme,TotalMarks=TotalMarks).count()
                print(grdlistcnt)
                if grdlistcnt == 0:
                    GradeMapping.objects.create(MinMarks=minmarks,MaxMarks=MaxMarks,GradePoints=GradePoints,Grade=Grade,GradeScheme=GradeScheme,TotalMarks=TotalMarks)
                    messages.success(request,"Grade Added Successfully")
                    return HttpResponseRedirect(reverse("AddGradempping"))
                else:
                    print("Inside else")
                    messages.error(request,"Grade Already Exists")
                    # context={'username':userName,'gradelist':gradelist}
                    return HttpResponseRedirect(reverse("AddGradempping"))
            except Exception as e:
                print(e)
                messages.error(request,"Failed to add Grade")
                return HttpResponseRedirect(reverse("AddGradempping"))
        else:
            context={'gradelist':gradelist}
            return render(request,"add_GradeMapping.html",context=context)


@login_required
def edit_Gradempping(request,grademapping_id):
    # userName=CustomUser.objects.get(id=request.user.id)
    gradeInfo=GradeMapping.objects.get(id=grademapping_id)
    form=EditGradeMappingForm()
    form.fields['MinMarks'].initial=gradeInfo.MinMarks
    form.fields['MaxMarks'].initial=gradeInfo.MaxMarks
    form.fields['GradePoints'].initial=gradeInfo.GradePoints
    form.fields['Grade'].initial=gradeInfo.Grade
    form.fields['GradeScheme'].initial=gradeInfo.GradeScheme
    form.fields['TotalMarks'].initial=gradeInfo.TotalMarks
    context={'form':form,'grademapping_id':grademapping_id}
    return render(request,"edit_Gradempping.html",context=context)

@login_required
def EditGradempping(request):
    grademapping_id = int(request.POST.get('grademapping_id'))
    if request.method!="POST":
        return render(request,"edit_Gradempping.html")
    else:
        form=EditGradeMappingForm(request.POST)
        if form.is_valid():
            MinMarks=form.cleaned_data["MinMarks"]
            MaxMarks=form.cleaned_data["MaxMarks"]
            GradePoints=form.cleaned_data["GradePoints"]
            Grade=form.cleaned_data["Grade"]
            GradeScheme=form.cleaned_data["GradeScheme"]
            TotalMarks=form.cleaned_data["TotalMarks"]
            try:
                grdlst=GradeMapping.objects.filter(id=grademapping_id,MinMarks=MinMarks,MaxMarks=MaxMarks,GradePoints=GradePoints,Grade=Grade,GradeScheme=GradeScheme,TotalMarks=TotalMarks).count()
                if grdlst == 0:
                    gradeInfo = GradeMapping.objects.get(id = grademapping_id)
                    gradeInfo.MinMarks = MinMarks
                    gradeInfo.MaxMarks = MaxMarks
                    gradeInfo.GradePoints = GradePoints
                    gradeInfo.Grade = Grade
                    gradeInfo.GradeScheme = GradeScheme
                    gradeInfo.TotalMarks = TotalMarks
                    gradeInfo.save()
                    messages.success(request,"Grade Updated Successfully")
                    return HttpResponseRedirect(reverse("EditGradempping",kwargs={'grademapping_id':grademapping_id}))
                else:
                    messages.error(request,"Grade Already Exists")
                    return HttpResponseRedirect(reverse("EditGradempping",kwargs={'grademapping_id':grademapping_id}))
            except Exception as e:
                messages.error(request,"Failed to Update Grade")
                return HttpResponseRedirect(reverse("EditGradempping",kwargs={'grademapping_id':grademapping_id}))
        else:
            return render(request,"edit_Gradempping.html")

#Course Type master management
@login_required
def add_AddCoursetype(request):
    form=AddCourseTypeForm(request.POST)
    courselist=CourseType.objects.all()
    try:
        userName=CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        return HttpResponseRedirect('/')
    return render(request,"add_CourseType.html",{"form":form,"courselist":courselist})

@login_required
def CreateCoursetype(request):
    courselist=CourseType.objects.all()
    if request.method!="POST":
        context={'courselist':courselist}
        return render(request,"add_CourseType.html",context=context)
    else:
        form=AddCourseTypeForm(request.POST)
        if form.is_valid():
            Coursetype = form.cleaned_data["Coursetype"]
            try:
                courselistcnt=CourseType.objects.filter(Coursetype=Coursetype).count()
                if courselistcnt == 0:
                    CourseType.objects.create(Coursetype=Coursetype)
                    messages.success(request,"Course Type Added Successfully")
                    return HttpResponseRedirect(reverse("AddCoursetype"))
                else:
                    messages.error(request,"Course Type Already Exists")
                    # context={'username':userName,'gradelist':gradelist}
                    return HttpResponseRedirect(reverse("AddCoursetype"))
            except Exception as e:
                print(e)
                messages.error(request,"Failed to add Course Type")
                return HttpResponseRedirect(reverse("AddCoursetype"))
        else:
            context={'courselist':courselist}
            return render(request,"add_CourseType.html",context=context)


@login_required
def edit_Coursetype(request,coursetype_id):
    coursetypeInfo=CourseType.objects.get(id=coursetype_id)
    form=EditCourseTypeForm()
    form.fields['Coursetype'].initial=coursetypeInfo.Coursetype
    context={'form':form,'coursetype_id':coursetype_id}
    return render(request,"edit_Coursetype.html",context=context)

@login_required
def EditCoursetype(request):
    coursetype_id = int(request.POST.get('coursetype_id'))
    if request.method!="POST":
        return render(request,"edit_Coursetype.html")
    else:
        form=EditCourseTypeForm(request.POST)
        if form.is_valid():
            Coursetype=form.cleaned_data["Coursetype"]
            try:
                courselst=CourseType.objects.filter(id=coursetype_id,Coursetype=Coursetype).count()
                if courselst == 0:
                    coursetypeInfo = CourseType.objects.get(id = coursetype_id)
                    coursetypeInfo.Coursetype = Coursetype
                    coursetypeInfo.save()
                    messages.success(request,"Course Type Updated Successfully")
                    return HttpResponseRedirect(reverse("EditCoursetype",kwargs={'coursetype_id':coursetype_id}))
                else:
                    messages.error(request,"Course Type Already Exists")
                    return HttpResponseRedirect(reverse("EditCoursetype",kwargs={'coursetype_id':coursetype_id}))
            except Exception as e:
                messages.error(request,"Failed to Update Course Type")
                return HttpResponseRedirect(reverse("EditCoursetype",kwargs={'coursetype_id':coursetype_id}))
        else:
            return render(request,"edit_Coursetype.html")