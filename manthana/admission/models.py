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

# Create your models here.
class CustomUserManager (UserManager):
    def _create_user(self, email, username, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email = email, username = username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, username, password, **extra_fields)

    def update_user(self, email, username, password=None):
        user = CustomUser.objects.get(username=username)
        user.email = self.normalize_email(email)
        user.password = make_password(password)
        user.save()
        return user

class CustomUser(AbstractUser):
    # user_type_data=((1,"Admin"),(2,"Employee"),(3,"Student"))
    user_type_data=[(1,"Admin"),(2,"Teaching Staff"),(3,"Student"),(4,"Non Teaching Staff"),(5,"Developer")]
    user_type=models.SmallIntegerField(default=1,choices=user_type_data)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()

    def __str__(self):
        return str(self.username)

class Admin(DirtyFieldsMixin, models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class EmployeeAdmin(admin.ModelAdmin):
    list_display=('emp_id','emp_fname','emp_lname','emp_emailId','emp_dept')

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Student_Details(DirtyFieldsMixin, models.Model):
    st_id = models.AutoField(primary_key = True, default = None)
    # admin=models.ForeignKey(CustomUser,on_delete=models.CASCADE,default=1)
    st_profile_pic = models.ImageField(upload_to = 'student/%Y/%m/%d' ,default=False)
    st_uid = models.CharField(unique = True, max_length=10, null=True)
    st_usn_old = models.CharField(max_length=10,null=True,unique=True)
    st_usn_new = models.CharField(max_length=10,null=True,unique=True)
    st_name = models.CharField(max_length=50, null=False, default= None)
    st_branch_applied = models.ForeignKey(Department, default=1, on_delete=CASCADE)
    # st_branch_applied_new_id = models.ForeignKey(Department, default=1, on_delete=CASCADE)    
    # st_branch_applied_old_id = models.ForeignKey(Department, default=1, on_delete=CASCADE)
    
    # st_acad_year = models.CharField(max_length=8,default="2020-21",null=False)
    st_acad_year = models.ForeignKey(AcademicYear, default=1, on_delete=CASCADE)

    adm_date = models.DateField(auto_now_add=False,null=False, default=now)
    st_adm_applied = models.CharField(max_length = 15,null=True)

    # st_adm_quota_data = [(1,"CET"),(2,"SNQ"),(3,"COMEDK"),(4,"MANAGEMENT"),(5,"PGCET")]
    # st_adm_quota = models.SmallIntegerField(default=1,choices=st_adm_quota_data)

    st_adm_quota = models.ForeignKey(Admission_Quota, default=1, on_delete=CASCADE)

    st_medium_data = [(1,"Non-Kannada"),(2,"Kannada"),(3,"Foreign National")]
    st_medium = models.SmallIntegerField(default=1,choices=st_medium_data)  
    
    st_dob = models.DateField(auto_now_add=False, null=False, default=now)

    st_gender_data = [(1,"Male"),(2,"Female"),(3,"Others")]
    st_gender = models.SmallIntegerField(default=1,choices=st_gender_data)

    st_locality_data = [(1,"Urban"),(2,"Rural")]
    st_locality = models.SmallIntegerField(default=1,choices=st_locality_data)

    st_bld_group = models.ForeignKey(BloodGroup,default=1,on_delete=CASCADE)
    st_pob = models.CharField(max_length=30,null=True)
    st_mother_tongue = models.CharField(max_length = 15,null=True)

    st_nationality_data = [(1,"Indian"),(2,"Other")]
    st_nationality = models.SmallIntegerField(default=1,choices=st_nationality_data)

    st_religion = models.ForeignKey(Religion,default=1,on_delete=CASCADE)
    st_caste=models.CharField(max_length=15,null=False, default="Hindu")
    st_subcaste = models.CharField(max_length=15,null=True)

    # st_category_data = [(1,"gm"),(2,"sc"),(3,"st"),(4,"cat1"),(5,"2a"),(6,"2b"),(7,"3a"),(8,"3b")]
    # st_category = models.SmallIntegerField(default=1,choices=st_category_data)

    st_category = models.ForeignKey(Category, default=1, on_delete=CASCADE)
    st_mobile_no = models.CharField(max_length=13,null=False,default="1234567890")
    st_email_id = models.CharField(max_length=30,null=True)
    st_aadhar_no = models.BigIntegerField(null=True)
    st_extracurr_activity = models.CharField(max_length=400,null=True)
    st_father_name = models.CharField(max_length=50,null=False, default="father")
    st_mother_name = models.CharField(max_length=50,null=False, default="mother")
    st_father_occupation = models.CharField(max_length=25,null=True)
    st_mother_occupation = models.CharField(max_length=25,null=True)
    st_father_income = models.BigIntegerField(null=False, default=500000)
    st_mother_income = models.BigIntegerField(null=True)
    st_father_mobile_no = models.CharField(max_length=13,null=False, default="1234567890")
    st_mother_mobile_no = models.CharField(max_length=13,null=True)
    st_father_pan = models.CharField(max_length=10,null=True)
    st_mother_pan = models.CharField(max_length=10,null=True)
    st_father_email_id = models.CharField(max_length=30,null=True)
    st_mother_email_id = models.CharField(max_length=30,null=True)
    st_parent_address = models.TextField(max_length=200,null=False, default="parent permanent address")
    st_parent_address_city = models.CharField(max_length=30,null=False, default="Dharwad")
    st_parent_address_district = models.CharField(max_length=30,null=False, default="Dharwad")
    st_parent_address_state = models.ForeignKey('master_mgmt.States',on_delete=CASCADE,related_name='pstate',default=1)
    st_parent_address_pincode = models.CharField(max_length=6,null=False, default="580025")
    st_postal_address = models.TextField(max_length=200,null=False, default="parent postal address")
    st_postal_address_city = models.CharField(max_length=30,null=False, default="Dharwad")
    st_postal_address_district = models.CharField(max_length=30,null=False, default="Dharwad")
    st_postal_address_state = models.ForeignKey('master_mgmt.States',on_delete=CASCADE,related_name='pstlstate',default=1)
    st_postal_address_pincode = models.BigIntegerField(null=False, default=580025)
    st_local_guardian_addr = models.CharField(max_length=200,null=True)
    st_guardian_mobile_no = models.CharField(max_length=13,null=True)
    st_health_issues = models.CharField(max_length=50, null=True)
    st_guardian_email = models.CharField(max_length=30, null=True)

    st_adm_date = models.DateField(auto_now_add=False,null=False, default='2022-05-01')
    st_total_fees = models.IntegerField(null=False, default=60000)
    st_rt_no = models.CharField(max_length=50, null=False)

    created_by = models.CharField(max_length=150, null=True)
    created_time = models.DateTimeField(editable=False, null=True)
    last_edited_by = models.CharField(max_length=150, null=True)
    last_edited_time = models.DateTimeField(null=True)

    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.st_id)

class Previous_10th_Academic_Details(DirtyFieldsMixin, models.Model):
    ug_pacad_10th_id = models.AutoField(primary_key=True)
    sslc_uid = models.ForeignKey('Student_Details',on_delete=CASCADE)
    ug_pacad_10th_board = models.CharField(max_length=20,null=False, default="X-Board")
    ug_pacad_10th_schoolname = models.CharField(max_length=60,null=False, default="X-School")
    ug_pacad_10th_pass_month = models.ForeignKey('master_mgmt.Months', related_name='xmonth', on_delete=CASCADE, default=1)
    ug_pacad_10th_pass_year = models.IntegerField(null=False, default=2010)
    ug_pacad_10th_pass_state = models.ForeignKey('master_mgmt.States',on_delete=CASCADE,related_name='xstate',default=1)
    ug_pacad_10th_medium = models.CharField(max_length=15, null=False, default="English")
    ug_pacad_10th_reg_no = models.CharField(max_length=15,null=False, default="123456789012345")
    ug_pacad_10th_total_marks_cgpa = models.FloatField(null=False, default=100.00)
    ug_pacad_10th_percentage_cgpa = models.FloatField(null=False, default=100.00)

    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.ug_pacad_10th_id

class Previous_12th_Academic_Details(DirtyFieldsMixin, models.Model):
    ug_pacad_12th_id = models.AutoField(primary_key=True)
    puc_uid = models.ForeignKey('Student_Details',on_delete=CASCADE)
    ug_pacad_12th_board = models.CharField(max_length=20,null=True)
    ug_pacad_12th_schoolname = models.CharField(max_length=60,null=True)
    ug_pacad_12th_pass_month = models.ForeignKey('master_mgmt.Months', related_name='xiimonth', on_delete=CASCADE, null=True)
    ug_pacad_12th_pass_year = models.IntegerField(null=True)
    ug_pacad_12th_pass_state = models.ForeignKey('master_mgmt.States',on_delete=CASCADE,related_name='xiistate', null=True)
    ug_pacad_12th_medium = models.CharField(max_length=15, null=True)
    ug_pacad_12th_reg_no = models.CharField(max_length=15,null=True)
    ug_pacad_12th_total_marks = models.SmallIntegerField(null=True)
    ug_pacad_12th_percentage = models.FloatField(null=True)
    ug_pacad_12th_physics_marks = models.SmallIntegerField(null=True)
    ug_pacad_12th_chemistry_marks = models.SmallIntegerField(null=True)
    ug_pacad_12th_maths_marks = models.SmallIntegerField(null=True)
    ug_pacad_12th_bio_cs_marks = models.SmallIntegerField(null=True)
    ug_pacad_12th_pcm_total_marks = models.SmallIntegerField(null=True)
    ug_pacad_12th_pcm_percentage = models.FloatField(null=True)

    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.ug_pacad_12th_id

class Previous_dip_Academic_Details(DirtyFieldsMixin, models.Model):
    ug_pacad_dip_id = models.AutoField(primary_key=True)
    dip_uid = models.ForeignKey('Student_Details',on_delete=CASCADE)
    ug_pacad_dip_board = models.CharField(max_length=20,null=True)
    ug_pacad_dip_schoolname = models.CharField(max_length=60,null=True)
    ug_pacad_dip_pass_month = models.CharField(max_length = 10, null=True)
    ug_pacad_dip_pass_year = models.CharField(max_length = 4, null=True)
    ug_pacad_dip_pass_state = models.ForeignKey('master_mgmt.States',null=True,on_delete=CASCADE,default=1)
    ug_pacad_dip_medium = models.CharField(max_length=15, null=True)
    ug_pacad_dip_reg_no = models.CharField(max_length=15,null=True)
    ug_pacad_dip_5th_marks = models.SmallIntegerField(null=True)
    ug_pacad_dip_6th_marks = models.SmallIntegerField(null=True)
    ug_pacad_dip_total_marks = models.SmallIntegerField(null=True)
    ug_pacad_total_percentage = models.FloatField(null=True)

    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.ug_pacad_dip_id

class CET_Admission_Details_UG(DirtyFieldsMixin, models.Model):  
    cet_id = models.AutoField(primary_key=True) 
    cet_uid = models.ForeignKey('Student_Details',on_delete=CASCADE)
    cet_order_no = models.CharField(max_length=20,null=True)
    cet_no = models.CharField(max_length=20,null=True)
    cet_rank = models.IntegerField(null=True)
    cet_cat_claimed = models.CharField(max_length=10,null=True)
    cet_cat_allotted = models.CharField(max_length=10,null=True)
    cet_allot_date = models.DateField(auto_now_add=False,null=True)
    cet_kea_fees_paid = models.BigIntegerField(null=True)
    cet_college_fees_paid = models.BigIntegerField(null=True)
    cet_total_fees_paid = models.BigIntegerField(null=True)
    cet_challan_date = models.DateField(auto_now_add=False,null=True)
    cet_challan_no = models.IntegerField(null=True)

    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.cet_id

class COMEDK_Admission_Details_UG(DirtyFieldsMixin, models.Model):
    comedk_id = models.AutoField(primary_key=True) 
    comedk_uid = models.ForeignKey('Student_Details',on_delete=CASCADE)
    comedk_sl_no = models.CharField(max_length=15,null=True)
    comedk_tat_no = models.CharField(max_length=15,null=True)
    comedk_rank = models.BigIntegerField(null=True)
    comedk_cat_allotted = models.CharField(max_length=10,null=True)
    comedk_allot_date = models.DateField(auto_now_add=False,null=True)
    comedk_fees_paid = models.IntegerField(null=True)
    comedk_college_fees_paid = models.IntegerField(null=True)
    comedk_challan_date = models.DateField(auto_now_add=False,null=True)
    comedk_challan_no = models.IntegerField(null=True)

    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.comedk_id

class MGMT_Admission_Details_UG(DirtyFieldsMixin, models.Model):
    mgmt_id = models.AutoField(primary_key=True) 
    mgmt_uid = models.ForeignKey('Student_Details',on_delete=CASCADE)
    mgmt_rank = models.IntegerField(null=True)
    #mgmt_exam = models.CharField(max_length=20,null=True)
    #mgmt_comedk = models.CharField(max_length=20,null=True)

    mgmt_exam_data = [(1,"CET"),(2,"COMEDK"),(3,"CET/COMEDK")]
    #mgmt_exam = models.SmallIntegerField(default=1,choices=mgmt_exam_data)
    mgmt_exam = models.SmallIntegerField(null=True, choices=mgmt_exam_data)

    mgmt_college_fees_paid = models.IntegerField(null=True)
    mgmt_challan_date = models.DateField(auto_now_add=False,null=True)
    mgmt_challan_no = models.IntegerField(null=True)

    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.mgmt_id

class Lateralentry_Admission_Details_UG(DirtyFieldsMixin, models.Model):
    dip_id = models.AutoField(primary_key=True) 
    dip_uid = models.ForeignKey('Student_Details',on_delete=CASCADE)
    dip_adm_order_no = models.CharField(max_length=20,null=True)
    dip_dcet_no = models.CharField(max_length=10,null=True)
    dip_rank = models.IntegerField(null=True)
    dip_cat_claimed = models.CharField(max_length=10,null=True)
    dip_cat_allotted = models.CharField(max_length=10,null=True)
    dip_allot_date = models.DateField(auto_now_add=False,null=True)
    dip_fees_paid = models.IntegerField(null=True)
    dip_college_fees_paid = models.IntegerField(null=True)
    dip_total_fees_paid = models.IntegerField(null=True)
    dip_challan_date = models.DateField(auto_now_add=False,null=True)
    dip_challan_no = models.IntegerField(null=True)

    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.dip_id)

class Previous_Academic_Details_PG(DirtyFieldsMixin, models.Model):
    pg_pacad_id = models.AutoField(primary_key=True)
    pg_uid = models.ForeignKey('Student_Details',on_delete=CASCADE)
    pg_pacad_10th_board = models.CharField(max_length=20,null=False,default="KSEEB")
    pg_pacad_10th_reg_no = models.CharField(max_length=15,null=False,default="123456789")
    pg_pacad_10th_pass_month = models.CharField(max_length=10,null=False,default="January")
    pg_pacad_10th_pass_year = models.CharField(max_length=4,null=False,default="2010")
    pg_pacad_10th_total_marks_cgpa = models.FloatField(null=False,default=625)
    pg_pacad_10th_percentage_cgpa = models.FloatField(null=False,default=10.0)
    pg_pacad_10th_class_obtained = models.CharField(max_length=20,null=False,default="Distinction") 
    pg_pacad_12th_board= models.CharField(max_length=20,null=True)
    pg_pacad_12th_reg_no = models.CharField(max_length=15,null=True)
    pg_pacad_12th_pass_month = models.CharField(max_length=10,null=True)
    pg_pacad_12th_pass_year = models.CharField(max_length=7,null=True)
    pg_pacad_12th_total_marks = models.SmallIntegerField(null=True)
    pg_pacad_12th_percentage = models.SmallIntegerField(null=True)
    pg_pacad_12th_class_obtained = models.CharField(max_length=20,null=True) 
    pg_pacad_degree_university = models.CharField(max_length=60,null=False,default="VTU") 
    pg_pacad_degree_reg_no = models.CharField(max_length=15,null=False,default="2SD20CS000")
    pg_pacad_degree_pass_month = models.CharField(max_length=10,null=False,default="January")
    pg_pacad_degree_pass_year = models.CharField(max_length=4,null=False,default="2018")
    pg_pacad_degree_percentage_cgpa = models.FloatField(null=False,default=600)
    pg_pacad_be_percentage_5_8 = models.FloatField(null=False,default=10.0)
    pg_pacad_degree_class_obtained = models.CharField(max_length=20,null=False,default="Distinction")

    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.pg_pacad_id

class PGCET_Admission_Details_PG(DirtyFieldsMixin, models.Model):  
    pgcet_id = models.AutoField(primary_key=True) 
    pgcet_uid = models.ForeignKey('Student_Details',on_delete=CASCADE)
    pgcet_order_no = models.CharField(max_length=20,null=True)
    pgcet_no = models.CharField(max_length=20,null=True)
    pgcet_rank = models.IntegerField(null=True)
    pgcet_cat_claimed = models.CharField(max_length=10,null=True)
    pgcet_cat_allotted = models.CharField(max_length=10,null=True)
    pgcet_allot_date = models.DateField(auto_now_add=False,null=True)
    pgcet_kea_fees_paid = models.IntegerField(null=True)
    pgcet_college_fees_paid = models.IntegerField(null=True)
    pgcet_total_fees_paid = models.IntegerField(null=True)
    pgcet_challan_date = models.DateField(auto_now_add=False,null=True)
    pgcet_challan_no = models.IntegerField(null=True)

    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.pgcet_id

class MGMT_Admission_Details_PG(DirtyFieldsMixin, models.Model):
    mgmt_pg_id = models.AutoField(primary_key=True) 
    mgmt_pg_uid = models.ForeignKey('Student_Details',on_delete=CASCADE)
    mgmt_pg_rank = models.IntegerField(null=True)
    #mgmt_pg_exam = models.CharField(max_length=20,null=True)
    #mgmt_exampg_data = [(5,"PGCET"),(4,"MGMT"),(9,"PGCET/MGMT")]
    mgmt_exampg_data = [(5,"PGCET")]
    mgmt_exampg = models.SmallIntegerField(null=True, choices=mgmt_exampg_data)

    mgmt_pg_college_fees_paid = models.IntegerField(null=True)
    mgmt_pg_challan_date = models.DateField(auto_now_add=False,null=True)
    mgmt_pg_challan_no = models.IntegerField(null=True)

    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.mgmt_pg_id

class Previous_Transfer_College_Details(DirtyFieldsMixin, models.Model):
    ug_ptcd_id = models.AutoField(primary_key=True)
    clg_trns_exam_type = models.IntegerField(null=True) 
    clgtrns_st_uid = models.ForeignKey('Student_Details',on_delete=CASCADE)
    ug_ptcd_college_name = models.CharField(max_length=60,null=True)
    ug_ptcd_admitted_sem = models.CharField(max_length=10,null=True)
    ug_ptcd_credits_earned = models.IntegerField(null=True)
    ug_ptcd_credits_remaining = models.IntegerField(null=True)
    ug_ptcd_admitted_cgpa = models.FloatField(null=True)
    
    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.st_uid

class Document_Details(DirtyFieldsMixin, models.Model):
    doc_ug_id = models.AutoField(primary_key=True) 
    doc_uid = models.ForeignKey('Student_Details',on_delete=CASCADE)
    alt_order_copy = models.IntegerField(null=False, default=1)
    st_10th_marks_card = models.BooleanField(null=False,default=False)
    st_dip_marks_card = models.BooleanField(null=True,default=False)
    st_12th_marks_card = models.BooleanField(null=True)
    st_degree_certificate = models.BooleanField(null=True,default=False)
    st_study_cerfiticate = models.BooleanField(null=False,default=False)
    st_income_certificate = models.BooleanField(null=True,default=False)
    st_tulu_certificate = models.BooleanField(null=True,default=False)
    st_eligibility_certificate = models.BooleanField(null=True,default=False)
    st_migration_certificate = models.BooleanField(null=True,default=False)
    st_transfer_certificate = models.BooleanField(null=False,default=False)
    st_aadhar_card = models.BooleanField(null=True,default=False)
    st_pan_card = models.BooleanField(null=True,default=False)

    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.doc_ug_id)

class RoleDetail(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_type = models.CharField(max_length=100,null=False)
    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.role_type

class RoleDetailAdmin(admin.ModelAdmin):
    list_display=('role_id','role_type')

class Privilege(models.Model):
    pr_id = models.AutoField(primary_key=True)
    pr_user_id = models.ForeignKey('CustomUser',on_delete=CASCADE)
    role_id = models.ForeignKey('RoleDetail',on_delete=CASCADE)
    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.pr_id)

class PrivilegeAdmin(admin.ModelAdmin):
    list_display=('pr_id','pr_user_id','role_id')

class Admission_Higher_Semester_Details(models.Model):
    admit_higher_id = models.AutoField(primary_key = True, default = None)
    acad_cal_odd = models.CharField(max_length=7,null=True)
    acad_cal_even = models.CharField(max_length=7,null=True)
    # sem_type = models.SmallIntegerField(null=True)
    semester= models.SmallIntegerField(unique = True,null=False,default=3)
    dept_id = models.ForeignKey(Department,on_delete=CASCADE)
    st_uid = models.ForeignKey(Student_Details,on_delete=CASCADE)
    admit_higher_fees = models.IntegerField(null=True)
    admit_higher_challan_no = models.IntegerField(null=True)

    class Meta:
        unique_together = (('acad_cal_odd','acad_cal_even','semester','dept_id','st_uid'),)

    objects=models.Manager()

    def str(self):
        return str(self.admit_higher_id)
        
@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    pass
    # if created:
    #     if instance.user_type==1:
    #         Admin.objects.create(admin=instance)
    #     if instance.user_type==2:
    #         Employee.objects.create(admin=instance)
    #     if instance.user_type==3:
    #         Student_Details.objects.create(admin=instance)

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    pass
    # if instance.user_type==1:
    #     instance.admin.save()
    # if instance.user_type==2:
    #     instance.employee.save()
    # if instance.user_type==3:
    #     instance.student_details.save()
