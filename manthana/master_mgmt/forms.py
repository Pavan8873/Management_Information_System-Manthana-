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
class AddDepartmentForm(forms.Form):
    dept_abbr = forms.CharField(label="Department Abbrevation", max_length=6,widget=forms.TextInput(attrs={"class":"form-control"}))
    dept_name = forms.CharField(label="Department Name", max_length=60,widget=forms.TextInput(attrs={"class":"form-control"}))
    start_year = forms.DateField(label="Start Year",widget=forms.NumberInput(attrs={"type":"date","class":"form-control"}))
    close_year = forms.DateField(label="Close Year",widget=forms.NumberInput(attrs={"type":"date","class":"form-control"}))

class EditDepartmentForm(forms.Form):
    dept_abbr = forms.CharField(label="Department Abbrevation", max_length=6,widget=forms.TextInput(attrs={"class":"form-control"}))
    dept_name = forms.CharField(label="Department Name", max_length=60,widget=forms.TextInput(attrs={"class":"form-control"}))
    start_year = forms.DateField(label="Start Year",widget=forms.NumberInput(attrs={"type":"date","class":"form-control"}))
    close_year = forms.DateField(label="Close Year",widget=forms.NumberInput(attrs={"type":"date","class":"form-control"}))

class AddReligionForm(forms.Form):
    name = forms.CharField(label="Name of the Religion", max_length=60,widget=forms.TextInput(attrs={"class":"form-control"}))
    
class EditReligionForm(forms.Form):
    name = forms.CharField(label="Name of the Religion", max_length=60,widget=forms.TextInput(attrs={"class":"form-control"}))

class AddStatesForm(forms.Form):
    name = forms.CharField(label="State Name", max_length=60,widget=forms.TextInput(attrs={"class":"form-control"}))
    
class EditStatesForm(forms.Form):
    name = forms.CharField(label="State Name", max_length=60,widget=forms.TextInput(attrs={"class":"form-control"}))

class AddBloodGroupForm(forms.Form):
    name = forms.CharField(label="Blood Group", max_length=15,widget=forms.TextInput(attrs={"class":"form-control"}))
    
class EditBloodGroupForm(forms.Form):
    name = forms.CharField(label="Blood Group", max_length=15,widget=forms.TextInput(attrs={"class":"form-control"}))

class AddAcademicYearForm(forms.Form):
    aca_year = forms.CharField(label="Academic Year", max_length=10,widget=forms.TextInput(attrs={"class":"form-control"}))

class EditAcademicYearForm(forms.Form):
    aca_year = forms.CharField(label="Academic Year", max_length=10,widget=forms.TextInput(attrs={"class":"form-control"}))

class AddDivisionForm(forms.Form):
    divname = forms.CharField(label="Division", max_length=2,widget=forms.TextInput(attrs={"class":"form-control"}))

class AddRoomForm(forms.Form):
    roomname = forms.CharField(label="room_name", max_length=10,widget=forms.TextInput(attrs={"class":"form-control"}))
    rowname = forms.CharField(label="Row", max_length=2,widget=forms.TextInput(attrs={"class":"form-control"}))
    colname = forms.CharField(label="Column", max_length=2,widget=forms.TextInput(attrs={"class":"form-control"}))
    total_seats = forms.CharField(label="Total_Seats", max_length=3,widget=forms.TextInput(attrs={"class":"form-control"}))

class EditDivisionForm(forms.Form):
    divname = forms.CharField(label="Division", max_length=2,widget=forms.TextInput(attrs={"class":"form-control"}))

class EditRoomForm(forms.Form):
    roomname = forms.CharField(label="room_name", max_length=10,widget=forms.TextInput(attrs={"class":"form-control"}))
    rowname = forms.CharField(label="Row", max_length=2,widget=forms.TextInput(attrs={"class":"form-control"}))
    colname = forms.CharField(label="Column", max_length=2,widget=forms.TextInput(attrs={"class":"form-control"}))
    total_seats = forms.CharField(label="Total_Seats", max_length=3,widget=forms.TextInput(attrs={"class":"form-control"}))

class AddUsertypeForm(forms.Form):
    usertype_id = forms.IntegerField(label="User Type ID(1-10)",widget=forms.NumberInput(attrs={"class":"form-control"}))
    Usertype_Name = forms.CharField(label="User Type Name", max_length=20,widget=forms.TextInput(attrs={"class":"form-control"}))

class EditUsertypeForm(forms.Form):
    usertype_id = forms.IntegerField(label="User Type ID(1-10)",widget=forms.NumberInput(attrs={"class":"form-control"}))
    Usertype_Name = forms.CharField(label="User Type Name", max_length=20,widget=forms.TextInput(attrs={"class":"form-control"}))

class AddQuotaForm(forms.Form):
    Name = forms.CharField(label="Admission Quota", max_length=20,widget=forms.TextInput(attrs={"class":"form-control"}))

class EditQuotaForm(forms.Form):
    Name = forms.CharField(label="Admission Quota", max_length=20,widget=forms.TextInput(attrs={"class":"form-control"}))

class AddMonthsForm(forms.Form):
    Name = forms.CharField(label="Month Name", max_length=15,widget=forms.TextInput(attrs={"class":"form-control"}))

class EditMonthsForm(forms.Form):
    Name = forms.CharField(label="Month Name", max_length=15,widget=forms.TextInput(attrs={"class":"form-control"}))

class AddCategoryForm(forms.Form):
    Name = forms.CharField(label="Category Name", max_length=10,widget=forms.TextInput(attrs={"class":"form-control"}))

class EditCategoryForm(forms.Form):
    Name = forms.CharField(label="Category Name", max_length=10,widget=forms.TextInput(attrs={"class":"form-control"}))


class AddSemesterForm(forms.Form):
    Name = forms.CharField(label="Semester", max_length=5,widget=forms.TextInput(attrs={"class":"form-control"}))

class EditSemesterForm(forms.Form):
    Name = forms.CharField(label="Semester", max_length=5,widget=forms.TextInput(attrs={"class":"form-control"}))

class AddExtValCollegeForm(forms.Form):
    Name = forms.CharField(label="External valuators College Name", max_length=150,widget=forms.TextInput(attrs={"class":"form-control"}))

class EditExtValCollegeForm(forms.Form):
    Name = forms.CharField(label="External valuators College Name", max_length=150,widget=forms.TextInput(attrs={"class":"form-control"}))

class AddGradeMappingForm(forms.Form):
    MinMarks = forms.IntegerField(label="Min Marks", widget=forms.TextInput(attrs={"class":"form-control"}))
    MaxMarks = forms.IntegerField(label="Max Marks", widget=forms.TextInput(attrs={"class":"form-control"}))
    GradePoints = forms.IntegerField(label="Grade Points", widget=forms.TextInput(attrs={"class":"form-control"}))
    Grade = forms.CharField(label="Grade", widget=forms.TextInput(attrs={"class":"form-control"}))
    GradeScheme = forms.IntegerField(label="Grade Scheme", widget=forms.TextInput(attrs={"class":"form-control"}))
    ExamType_Total_Marks=[(0,"--Select Exam Type--"),(100,"SEE"),(50,"CIE")]
    TotalMarks = forms.ChoiceField(label="Exam Type",choices=ExamType_Total_Marks,widget=forms.Select(attrs={"class":"form-control"}))

class EditGradeMappingForm(forms.Form):
    MinMarks = forms.IntegerField(label="Min Marks", widget=forms.TextInput(attrs={"class":"form-control"}))
    MaxMarks = forms.IntegerField(label="Max Marks", widget=forms.TextInput(attrs={"class":"form-control"}))
    GradePoints = forms.IntegerField(label="Grade Points", widget=forms.TextInput(attrs={"class":"form-control"}))
    Grade = forms.CharField(label="Grade", widget=forms.TextInput(attrs={"class":"form-control"}))
    GradeScheme = forms.IntegerField(label="Grade Scheme",widget=forms.TextInput(attrs={"class":"form-control"}))
    ExamType_Total_Marks=[(100,"SEE"),(50,"CIE")]
    TotalMarks = forms.ChoiceField(label="Total Marks",choices=ExamType_Total_Marks,widget=forms.Select(attrs={"class":"form-control"}))

class AddCourseTypeForm(forms.Form):
    Coursetype = forms.CharField(label="Course Type", max_length=150,widget=forms.TextInput(attrs={"class":"form-control"}))

class EditCourseTypeForm(forms.Form):
    Coursetype = forms.CharField(label="Course Type", max_length=150,widget=forms.TextInput(attrs={"class":"form-control"}))

class PasswordResetForm(forms.Form):
    """
    A form that lets admin change their password by entering the new password
    """
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    required_css_class = 'required'
    user_list = []

    try:
        users = CustomUser.objects.all()
        for uname in users:
            if uname.username.lower() == "admin" or uname.username.lower() == "administrator":
                pass
            else:
                username = (uname.id, uname.username)
                user_list.append(username)
    except:
        pass

    user_id = forms.ChoiceField(label="User Name",
        choices=user_list,
        widget=forms.Select(attrs={"class":"form-control"})
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class":"form-control"}),
        strip=False,
        help_text="Enter the password of your choice.",
    )
    
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class":"form-control"}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    field_order = ['user_id', 'password1', 'password2']
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2