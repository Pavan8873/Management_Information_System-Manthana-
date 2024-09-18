
import datetime
from random import choices
from django.contrib import admin
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import DateField, NullBooleanField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from pymysql import NULL
from admission.models import Admission_Higher_Semester_Details, Student_Details
from master_mgmt.models import AcademicYear, Department, Division
from hr.models import Employee_Details

# Create your models here.
class Academic_Calendar(models.Model):
    acad_cal_id = models.AutoField(primary_key=True)
    acad_cal_acad_year = models.ForeignKey(AcademicYear,default=1,on_delete=CASCADE)
    #acad_cal_acad_year = models.CharField(max_length=7,null=True)
   # acad_cal_sem_data = [(1,"1st Semester"),(2,"2nd Semester"),(3,"3rd Semester"),(4,"4th Semester"),(5,"5th Semester"),(6,"6th Semester"),(7,"7th Semester"),(8,"8th Semester")]
  #  acad_cal_sem = models.SmallIntegerField(default=1,choices=acad_cal_sem_data)
    acad_cal_sem = models.SmallIntegerField(null=True)
    acad_cal_type = models.SmallIntegerField(null=True)
    acad_cal_induction_program_from = models.DateField(auto_now_add=False,null=True)
    acad_cal_induction_program_to = models.DateField(auto_now_add=False,null=True)
    acad_cal_teaching_commences = models.DateField(auto_now_add=False,null=True)
    
    acad_cal_reg_date_from = models.DateField(auto_now_add=False,null=True)
    acad_cal_reg_date_to = models.DateField(auto_now_add=False,null=True)
    acad_cal_reg_last_date_fee = models.DateField(auto_now_add=False,null=True)
    acad_cal_att_display_ia_1 = models.DateField(auto_now_add=False,null=True)
    
    acad_cal_ia_1_from = models.DateField(auto_now_add=False,null=True)
    acad_cal_ia_1_to = models.DateField(auto_now_add=False,null=True)
    acad_cal_commn_to_parent_ia_1 = models.DateField(auto_now_add=False,null=True)
    acad_cal_drop_course = models.DateField(auto_now_add=False,null=True)
    acad_cal_att_display_ia_2 = models.DateField(auto_now_add=False,null=True)
    acad_cal_ia_2_from = models.DateField(auto_now_add=False,null=True)
    acad_cal_ia_2_to = models.DateField(auto_now_add=False,null=True)
    acad_cal_commn_to_parent_ia_2 = models.DateField(auto_now_add=False,null=True)
    acad_cal_withdraw_course = models.DateField(auto_now_add=False,null=True)
    acad_cal_parents_meet = models.DateField(auto_now_add=False,null=True)
    acad_cal_st_feedback_from = models.DateField(auto_now_add=False,null=True)
    acad_cal_st_feedback_to = models.DateField(auto_now_add=False,null=True)
    acad_cal_ia_3_from = models.DateField(auto_now_add=False,null=True)
    acad_cal_ia_3_to = models.DateField(auto_now_add=False,null=True)
    acad_cal_last_day_teaching = models.DateField(auto_now_add=False,null=True)
    acad_cal_see_lab_from = models.DateField(auto_now_add=False,null=True)
    acad_cal_see_lab_to = models.DateField(auto_now_add=False,null=True)
    acad_cal_cie_marks_display = models.DateField(auto_now_add=False,null=True)
    acad_cal_attendance_display = models.DateField(auto_now_add=False,null=True)
    acad_cal_commn_to_parent_cie = models.DateField(auto_now_add=False,null=True)
    acad_cal_see_theory_from = models.DateField(auto_now_add=False,null=True)
    acad_cal_see_theory_to = models.DateField(auto_now_add=False,null=True)
    acad_cal_intersem_recess_from = models.DateField(auto_now_add=False,null=True)
    acad_cal_intersem_recess_to = models.DateField(auto_now_add=False,null=True)
    acad_cal_results_declaration = models.DateField(auto_now_add=False,null=True)
    acad_cal_makeup_from = models.DateField(auto_now_add=False,null=True)
    acad_cal_makeup_to = models.DateField(auto_now_add=False,null=True)

    class Meta:
       unique_together = (('acad_cal_acad_year', 'acad_cal_sem','acad_cal_type'),) 

    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.acad_cal_id)

class Scheme_Allotment(models.Model):
    scheme_allotment_id = models.AutoField(primary_key=True)
    acad_cal_id = models.ForeignKey(Academic_Calendar,db_column="acad_cal_id",on_delete=CASCADE)  
    course_sem = models.SmallIntegerField(null=False)
    scheme_series = models.SmallIntegerField(null=False)
    class Meta:
       unique_together = (('acad_cal_id','course_sem'),) 
    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.scheme_allotment_id)        

class Scheme_Details(models.Model):
    scheme_details_id = models.AutoField(primary_key=True)
    course_code = models.CharField(max_length=15,unique=True,null=False)
    course_title = models.CharField(max_length=50,null=False)
    credits = models.SmallIntegerField(null=False,default=1)
    ltps = models.CharField(max_length=8,null=False)
    course_type = models.CharField(max_length=10)
    sem_allotted = models.SmallIntegerField(null=False, default=1)
    is_credit = models.BooleanField(null=True,default=False)
    scheme_series = models.SmallIntegerField(null=False, default=1)
    offered_by = models.ForeignKey(Department,db_column="offered_by",on_delete=CASCADE)
    max_cie_marks = models.SmallIntegerField(null=False, default=50)
    min_cie_marks = models.SmallIntegerField(null=False, default=20)
    max_see_marks = models.SmallIntegerField(null=True, default=50)
    min_see_marks = models.SmallIntegerField(null=True, default=20)
    min_total_pass_marks = models.SmallIntegerField(null=False, default=40)
    max_total_marks = models.SmallIntegerField(null=False, default=100)
    deduction = models.SmallIntegerField(null=True, default=0)
    program= models.SmallIntegerField(null=True, default=0)
    open= models.SmallIntegerField(null=True, default=0)
    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.scheme_details_id)

class First_Year_Student_Course_Registration_Details(models.Model):
    first_year_st_course_reg_id = models.AutoField(primary_key=True)
    acad_cal_id = models.ForeignKey(Academic_Calendar,db_column="acad_cal_id",on_delete=CASCADE)
    semester = models.SmallIntegerField(default=1)
    first_year_cycle = models.CharField(max_length=10,null=False)
    st_uid = models.ForeignKey(Student_Details, to_field="st_uid", db_column="st_uid", on_delete=CASCADE)
    st_branch = models.ForeignKey(Department,db_column="st_branch",on_delete=CASCADE)
    scheme_details_id = models.ForeignKey(Scheme_Details,db_column="scheme_details_id",on_delete=CASCADE)
    registration_status = models.CharField(max_length=2,null=False,default='R')
    batch_no = models.CharField(max_length=2,default='B0')

    class Meta:
        unique_together = (('acad_cal_id', 'st_uid','scheme_details_id'),)

    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.first_year_st_course_reg_id)

class Faculty_Course_Allotment(models.Model):
    faculty_course_id = models.AutoField(primary_key=True)
    ''' 
    The "to_field" is actually the name of the field in the Foreign model.
    The "db_column" is the name of the field that you want to rename the foreignkey to in the local model
    Otherwise the field will be called faculty_id_id as per standard Django naming.
    '''
    employee_emp_id = models.ForeignKey(Employee_Details,to_field="employee_emp_id",db_column="employee_emp_id", on_delete=CASCADE) 
    #acad_year = models.CharField(max_length=7,null=False,default="2020-21")
    acad_year = models.ForeignKey(AcademicYear,to_field="id", on_delete=CASCADE)
    sem = models.SmallIntegerField(null=False,default=1)
    division = models.ForeignKey(Division,default=1,on_delete=CASCADE)
    course_code = models.ForeignKey(Scheme_Details, to_field="course_code", db_column="course_code", default="11UCSC111", on_delete=CASCADE)
    session_count = models.SmallIntegerField(null=True)
    batch_no = models.CharField(max_length=2,default='B0')
    acad_cal_type = models.SmallIntegerField(null=True)

    class Meta:
        unique_together = (('employee_emp_id','acad_cal_type', 'acad_year','sem','division','course_code','batch_no'),)

    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.faculty_course_id)

class student_attendance(models.Model):
    student_attd_id = models.AutoField(primary_key=True)
    acad_cal_id =  models.ForeignKey(Academic_Calendar,on_delete=CASCADE)
    scheme_details_id = models.ForeignKey(Scheme_Details,on_delete=CASCADE)
    division = models.CharField(max_length=2,null=False)
    faculty_id = models.ForeignKey(Employee_Details,to_field="employee_emp_id",db_column="employee_emp_id", on_delete=CASCADE) 
    st_uid = models.ForeignKey(Student_Details, to_field="st_uid", db_column="st_uid", on_delete=CASCADE)
    status = models.CharField(max_length=170,null=False)
    No_classes_attended = models.SmallIntegerField(null=True,default=0)
    Percentage_of_attendance = models.FloatField(null=True, blank=True)
    batch_no = models.CharField(max_length=2,default='B0')
    


    def str(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.student_attd_id)

class student_Attendance_date(models.Model):
    student_attd_date_id = models.AutoField(primary_key=True)
    faculty_id = models.ForeignKey(Employee_Details,to_field="employee_emp_id",db_column="employee_emp_id", on_delete=CASCADE) 
    acad_cal_id =  models.ForeignKey(Academic_Calendar,on_delete=CASCADE)
    scheme_details_id = models.ForeignKey(Scheme_Details,on_delete=CASCADE)
    session_index = models.SmallIntegerField(null=True)
    division = models.CharField(max_length=2,null=False)
    attendance_date = models.DateField(auto_now_add=False,null=True)
    attendance_time = models.CharField(max_length=10,null=False,default = None)
    absentees_count = models.SmallIntegerField(null=True)
    batch_no = models.CharField(max_length=2,default='B0')

    def str(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.student_attd_date_id)

class Declare_Assessment(models.Model):
    declare_assessment_id = models.AutoField(primary_key=True)
    acad_cal_id = models.ForeignKey(Academic_Calendar,db_column="acad_cal_id",on_delete=CASCADE)
    sem = models.SmallIntegerField(null=False)
    assessment_type = models.CharField(max_length=10,null=False)
    max_marks = models.SmallIntegerField(null=False, default=20)
    date = models.DateField(auto_now_add=False,null=False)
    scheme_details_id = models.ForeignKey(Scheme_Details,db_column="scheme_details_id",on_delete=CASCADE)

    class Meta:
        unique_together = (('assessment_type', 'scheme_details_id','max_marks','acad_cal_id'),)

    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.declare_assessment_id 

class Cycle_Division_allotment(models.Model):
    cycle_div_allot_id = models.AutoField(primary_key=True)
    acad_cal_id = models.ForeignKey(Academic_Calendar,db_column="acad_cal_id",on_delete=CASCADE)
    sem = models.SmallIntegerField(null=False)
    cycle = models.CharField(max_length=1,null=False)
    div = models.CharField(max_length=1,null=False)

    class Meta:
        unique_together = (('acad_cal_id','div','sem'),)
    
    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.cycle_div_allot_id)

class Student_Division_Allotment(models.Model):
    div_allot_id = models.AutoField(primary_key=True)
    st_uid = models.ForeignKey(Student_Details, to_field="st_uid", db_column="st_uid", on_delete=CASCADE)
    division = models.ForeignKey(Division,default=1,on_delete=CASCADE)
    acad_cal_id = models.ForeignKey(Academic_Calendar,db_column="acad_cal_id",on_delete=CASCADE)

    dept = models.ForeignKey(Department, default =1, on_delete=CASCADE)
    class Meta:
        unique_together = (('acad_cal_id','st_uid'),)
    
    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        #typecasted to string on getting exception in load_student()
        return str(self.div_allot_id) 

class UG_Student_Division_Allotment(models.Model):
    ug_div_allot_id = models.AutoField(primary_key=True)
    st_uid = models.ForeignKey(Student_Details, to_field="st_uid", db_column="st_uid", on_delete=CASCADE)
    ug_division = models.ForeignKey(Division,default=1,on_delete=CASCADE)
    acad_cal_id = models.ForeignKey(Academic_Calendar,db_column="acad_cal_id",on_delete=CASCADE)
    offered_by = models.ForeignKey(Department,db_column="offered_by",on_delete=CASCADE)
    class Meta:
        unique_together = (('acad_cal_id','st_uid','offered_by'),)
    
    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        #typecasted to string on getting exception in load_student()
        return str(self.ug_div_allot_id) 

class First_Year_Course_Details(models.Model):
    first_year_course_id = models.AutoField(primary_key=True)
    scheme_details_id = models.ForeignKey(Scheme_Details,to_field="scheme_details_id", db_column="scheme_details_id", on_delete=CASCADE)
    first_year_sem = models.SmallIntegerField(null=False)
    first_year_cycle = models.CharField(max_length=10,null=False)
    acad_cal_id = models.ForeignKey(Academic_Calendar,db_column="acad_cal_id",on_delete=CASCADE)
    
    class Meta:
        unique_together = (('scheme_details_id','first_year_cycle','acad_cal_id'),)
    
    objects=models.Manager()
    
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.first_year_course_id)

class Feedback_Questionnaire(models.Model):
        feedback_que_id = models.AutoField(primary_key=True)
        feedback_que_no = models.IntegerField(null=False)
        feedback_que_desc = models.CharField(max_length=100,null=False)
        feedback_course_type = models.CharField(max_length=5,null=False)
        
        objects=models.Manager()

        def str(self):
            """String for representing the MyModelName object (in Admin site etc.)."""
            return self.feedback_que_id

class UG_Student_Course_Registration_Details(models.Model):
    ug_st_course_id = models.AutoField(primary_key=True)
    acad_cal_id = models.ForeignKey(Academic_Calendar,db_column="acad_cal_id",on_delete=CASCADE)
    semester = models.SmallIntegerField(null=False)
    division = models.ForeignKey(Division,default=1,on_delete=CASCADE)
    st_uid = models.ForeignKey(Student_Details,to_field="st_uid",db_column="st_uid",on_delete=CASCADE)
    st_branch = models.ForeignKey(Department,db_column="st_branch",on_delete=CASCADE)
    scheme_details_id = models.ForeignKey(Scheme_Details,db_column="scheme_details_id",on_delete=CASCADE)
    registration_status = models.CharField(max_length=1,null=False,default='R')
    batch_no = models.CharField(max_length=2,default='B0')

    class Meta:
        unique_together = (('acad_cal_id', 'st_uid','scheme_details_id'),)

    objects=models.Manager()

    def str(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.ug_st_course_id)

class Student_Promotion_List(models.Model):
    st_promotion_id = models.AutoField(primary_key=True)
    acad_cal_id_odd = models.ForeignKey(Academic_Calendar,db_column="acad_cal_id_odd",related_name="odd_sem_id",default=3, on_delete=CASCADE)
    acad_cal_id_even = models.ForeignKey(Academic_Calendar,db_column="acad_cal_id_even",related_name="even_sem_id",default=4, on_delete=CASCADE)
    st_name = models.CharField(max_length=50, null=True)
    #semester = models.SmallIntegerField(null=False)
    offered_by = models.ForeignKey(Department,db_column="offered_by",on_delete=CASCADE)
    st_uid = models.ForeignKey(Student_Details, to_field="st_uid",db_column="st_uid",on_delete=CASCADE)

    class Meta:
        unique_together = (('acad_cal_id_odd','acad_cal_id_even','offered_by','st_uid'),)

    objects=models.Manager()

    def str(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.st_promotion_id)

class Course_Equivalence(models.Model):
        course_equivalence_id = models.AutoField(primary_key=True)
        old_course_code = models.CharField(max_length=10,null=False)
        new_course_code = models.CharField(max_length=10,null=False)
        old_scheme_details_id = models.ForeignKey(Scheme_Details,on_delete=CASCADE,related_name='old_scheme_details_id')
        new_scheme_details_id = models.ForeignKey(Scheme_Details,on_delete=CASCADE,related_name='new_scheme_details_id')

        class Meta:
            unique_together = (('old_course_code', 'new_course_code','old_scheme_details_id','new_scheme_details_id'),)
        objects=models.Manager()

        def str(self):
            """String for representing the MyModelName object (in Admin site etc.)."""
            return self.course_equivalence_id

class Declare_Assessment(models.Model):
    declare_assessment_id = models.AutoField(primary_key=True)
    acad_cal_id = models.ForeignKey(Academic_Calendar,on_delete=CASCADE)
    sem = models.SmallIntegerField(null=False)
    assessment_type = models.CharField(max_length=10,null=False)
    max_marks = models.SmallIntegerField(null=False, default=20)
    ans_q = models.SmallIntegerField(null=True)
    date = models.DateField(auto_now_add=False,null=False)
    scheme_details_id = models.ForeignKey(Scheme_Details,on_delete=CASCADE)

    class Meta:
        unique_together = (('assessment_type', 'scheme_details_id','max_marks','acad_cal_id'),)

    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.declare_assessment_id 

class Course_Outcome(models.Model):
    co_num = models.SmallIntegerField(primary_key=True, default=None)
    co_name = models.CharField(max_length=3, null=True)

    objects=models.Manager()

    def _str_(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.co_num
 
class Assessment_Pattern_Question(models.Model):
    assessment_pattern_num_id = models.AutoField(primary_key=True)
    qnum = models.SmallIntegerField(null=True)
    is_compulsory = models.SmallIntegerField(null=True, default=0)
    max_marks = models.SmallIntegerField(null=True)
    declare_assessment_id = models.ForeignKey(Declare_Assessment, on_delete=CASCADE, related_name = 'questions')

    objects=models.Manager()

    class Meta:
        unique_together = (('qnum','declare_assessment_id'),)

class Assessment_Pattern_Sub_Question(models.Model):
    assessment_pattern_sbqnum_id = models.AutoField(primary_key=True)
    assessment_pattern_qnum_id = models.ForeignKey(Assessment_Pattern_Question, on_delete=CASCADE, related_name = 'subquestion')
    subqnum = models.CharField(max_length=1)
    max_marks = models.SmallIntegerField(null=True)
    co = models.ManyToManyField(Course_Outcome)

    objects=models.Manager()
    class Meta:
        unique_together = (('assessment_pattern_qnum_id', 'subqnum',),)


class BitWise_Marks(models.Model):
    bitwise_marks_id = models.AutoField(primary_key=True)
    st_uid = models.ForeignKey(Student_Details,on_delete=CASCADE)
    qnum = models.SmallIntegerField(null=False)
    subqnum = models.CharField(max_length=10,null=False)
    obtained_marks = models.SmallIntegerField(null=False, default=0)
    assessment_pattern_id = models.ForeignKey(Assessment_Pattern_Question,on_delete=CASCADE,related_name='assessmentpattern')


    class Meta:
        unique_together = (('st_uid', 'qnum','subqnum','assessment_pattern_id'),)

    objects=models.Manager()

    # def __str__(self):
    #     """String for representing the MyModelName object (in Admin site etc.)."""
    #     return self.bitwise_marks_id 


class Academics_Master_Details(models.Model):
    academics_master_details_id = models.AutoField(primary_key=True)
    st_uid = models.ForeignKey(Student_Details,to_field="st_uid",db_column="st_uid", on_delete=CASCADE)
    #st_branch = models.ForeignKey(Department,db_column="st_branch",on_delete=CASCADE,default=1)
    st_branch_applied = models.ForeignKey(Department, default =1, on_delete=CASCADE)
    scheme_details_id = models.ForeignKey(Scheme_Details,db_column="scheme_details_id",on_delete=CASCADE,default=1)
    acad_cal_id = models.ForeignKey(Academic_Calendar,to_field="acad_cal_id", db_column="acad_cal_id", on_delete=CASCADE,default=1)
    semester = models.ForeignKey(First_Year_Student_Course_Registration_Details, db_column="semester", on_delete=CASCADE)
    division = models.ForeignKey(Student_Division_Allotment,db_column="division",on_delete=CASCADE,default=1)
    #classes_attended = models.ForeignKey(student_attendance,db_column="classes_attended", on_delete=CASCADE,default=1)
    No_classes_attended = models.ForeignKey(student_attendance,db_column="No_classes_attended", on_delete=CASCADE,default=0)
    classes_held = models.ForeignKey(Faculty_Course_Allotment,db_column="classes_held", on_delete=CASCADE,default=1)
    ia1_marks = models.SmallIntegerField(null=False,default=0)
    ia2_marks = models.SmallIntegerField(null=False,default=0)
    ia3_marks = models.SmallIntegerField(null=False,default=0)
    cta_marks = models.SmallIntegerField(null=False,default=0)
    cie_marks = models.SmallIntegerField(null=False,default=0)
    cie_grade = models.CharField(max_length=1, null=False,default='F')
    registration_status = models.CharField(max_length=1, null=False,default='0')
    final_cie_eligibility_status = models.SmallIntegerField(null=False,default=0)
    final_att_eligibility_status = models.SmallIntegerField(null=False,default=0)

    objects=models.Manager()

    def _str_(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.academics_master_details_id

class Student_current_status(models.Model):
    st_id = models.AutoField(primary_key=True)
    st_uid = models.ForeignKey(Student_Details, on_delete=CASCADE)
    semester = semester = models.SmallIntegerField(null=True)
    branch = models.ForeignKey(Department, on_delete=CASCADE)
    total_credits_earned = models.SmallIntegerField(null=True)
    acad_year = models.ForeignKey(Academic_Calendar,on_delete=CASCADE)
    division = models.ForeignKey(Student_Division_Allotment, on_delete=CASCADE)
    cgpa = models.FloatField(null=True, blank=True)
    sgpa = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ()

    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.st_id 
class Detained_Students(models.Model):
    dt_st_id = models.AutoField(primary_key=True)
    st_uid = models.ForeignKey(Student_Details, on_delete=CASCADE)
    semester = semester = models.SmallIntegerField(null=True)
    branch = models.ForeignKey(Department, on_delete=CASCADE)
    acad_year = models.ForeignKey(AcademicYear,on_delete=CASCADE)
    division = models.ForeignKey(Division, on_delete=CASCADE)
    scheme_details_id = models.ForeignKey(Scheme_Details,on_delete=CASCADE)

   

    class Meta:
        unique_together = ()

    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.dt_st_id
class ProgramOutcome(models.Model):
    po_number = models.CharField(max_length=10, unique=True)  # Example: PO-1, PO-2, etc.
    short_title = models.CharField(max_length=100)  # Example: Engineering knowledge, Problem analysis, etc.
    description = models.TextField()  # Full description of the Program Outcome

    def __str__(self):
        return f"{self.po_number} - {self.short_title}"
class CourseOutcome(models.Model):
    co_number = models.CharField(max_length=10)  # e.g., "CO-1"
              # Description of the CO

    def __str__(self):
        return f"{self.co_number} - {self.co_description}"

class CourseOutcomePO(models.Model):
    LEVEL_CHOICES = [
        ('Substantial', 'Substantial Level (3)'),
        ('Moderate', 'Moderate Level (2)'),
        ('Slight', 'Slight Level (1)'),
    ]

    acad_cal_id = models.ForeignKey('Academic_Calendar', on_delete=models.CASCADE)
    scheme_details_id = models.ForeignKey('Scheme_Details', on_delete=models.CASCADE)
    co = models.ForeignKey('CourseOutcome', on_delete=models.CASCADE)
    po = models.ForeignKey('ProgramOutcome', on_delete=models.CASCADE)
    mapping_level = models.CharField(max_length=12, choices=LEVEL_CHOICES)
    co_description = models.CharField(max_length=500, blank=True)  # Limited length

    class Meta:
        unique_together = ('acad_cal_id', 'scheme_details_id', 'co', 'po', 'mapping_level')

    def __str__(self):
        return (f"CO: {self.co.co_name} - {self.co_description} | "
                f"PO: {self.po.po_number} - {self.po.short_title} | "
                f"Academic Calendar: {self.acad_cal_id} | "
                f"Scheme: {self.scheme_details_id} | "
                f"Mapping Level: {self.mapping_level}")
