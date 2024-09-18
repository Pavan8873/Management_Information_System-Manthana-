from django.db import models
from academics.models import *
from master_mgmt.models import *
# Create your models here.

class Exam_Details(models.Model):
    exam_details_id = models.AutoField(primary_key=True)
    acad_year = models.ForeignKey(AcademicYear,to_field='acayear',on_delete=CASCADE)
    semester = models.SmallIntegerField(null=False)
    acad_cal_id = models.ForeignKey(Academic_Calendar,db_column="acad_cal_id",on_delete=CASCADE)
    duration_theory_from = models.DateField(auto_now_add=False,null=False)
    duration_theory_to = models.DateField(auto_now_add=False,null=False)
    duration_lab_from = models.DateField(auto_now_add=False,null=True)
    duration_lab_to = models.DateField(auto_now_add=False,null=True)
    exam_type = models.SmallIntegerField(null=False)
    description = models.CharField(max_length=50,null=False)
        
    class Meta:
        unique_together = (('exam_type','acad_cal_id'),)
    
    objects=models.Manager()
    
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.exam_details_id)

class External_Valuator(models.Model):
    ext_valuator_id = models.AutoField(primary_key=True)
    ext_valuator_name = models.CharField(max_length=15,null=False)
    ext_valuator_college = models.ForeignKey(ExtValuatorCollegeName,db_column='ext_valuator_college',on_delete=CASCADE)
    ext_valuator_department = models.CharField(max_length=25)
    ext_valuator_designation = models.CharField(max_length=25)
    ext_valuator_pan = models.CharField(max_length=10,null=False,unique=True)
    ext_valuator_phone =models.CharField(max_length=10,null=False,unique=True)

    objects=models.Manager()

    def str(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.ext_valuator_id)

class SEE_Valuator(models.Model):
    valuator_id = models.AutoField(primary_key=True)
    valuator_type = models.CharField(max_length=1,null=False)
    valuator_empId = models.ForeignKey(Employee_Details,blank=True,null=True,db_column="valuator_empId",on_delete=CASCADE)
    valuator_pan = models.ForeignKey(External_Valuator,to_field="ext_valuator_pan",db_column="valuator_pan",blank=True,null=True,on_delete=CASCADE)
    course_code = models.ForeignKey(Scheme_Details,to_field="course_code",db_column="course_code",on_delete=CASCADE)
    exam_details_id = models.ForeignKey(Exam_Details,db_column="exam_details_id",on_delete=CASCADE)

    class Meta:
        unique_together = (('valuator_empId','course_code','exam_details_id'),)
    
    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.valuator_id)

class SEE_timetable(models.Model):
    see_att_date_id = models.AutoField(primary_key=True)
    scheme_details_id = models.ForeignKey(Scheme_Details,on_delete=CASCADE)
    exam_id = models.ForeignKey(Exam_Details,on_delete=CASCADE) 
    exam_date = models.DateField(auto_now_add=False,null=True)
    acad_cal_id = models.ForeignKey(Academic_Calendar,on_delete=CASCADE)
    attendance_flag = models.SmallIntegerField(null=True)
    absentees_count = models.SmallIntegerField(null=True)  
    exam_time = models.CharField(max_length=5,null=False)       

    class Meta:
        unique_together = (('acad_cal_id','exam_id','scheme_details_id'),)
    
    objects=models.Manager()
    
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.see_att_date_id)        

class Bar_Code(models.Model):
    serial_no = models.AutoField(primary_key=True)
    st_id = models.ForeignKey(Student_Details, on_delete=CASCADE)
    barcode = models.CharField(max_length=15,null=False)
    exam_id = models.ForeignKey(Exam_Details, on_delete=CASCADE,related_name="exam_barCode")

    class Meta:
        unique_together = (('st_id','barcode','exam_id'),)
    
    objects=models.Manager()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.serial_no)


class Exam_HallTicket(models.Model): 
    hall_ticket_id = models.AutoField(primary_key=True) 
    exam_id = models.ForeignKey(Exam_Details,db_column="exam_id",on_delete=CASCADE) 
    st_uid = models.ForeignKey(Student_Details, on_delete=CASCADE)
    ht_application_no = models.CharField(unique = True, max_length=10, null=True)
    objects=models.Manager() 
 
    class Meta:
        unique_together=(('exam_id','st_uid'))

    def str(self): 
        """String for representing the MyModelName object (in Admin site etc.).""" 
        return self.hall_ticket_id

class Exam_HallTicket_Details(models.Model):
    ht_details_id = models.AutoField(primary_key=True)
    hall_ticket_id = models.ForeignKey(Exam_HallTicket,on_delete=CASCADE, related_name = 'hallTicketDetails')
    academics_master_details_id = models.ForeignKey(Academics_Master_Details,on_delete=CASCADE)  

    def str(self): 
        """String for representing the MyModelName object (in Admin site etc.).""" 
        return str(self.ht_details_id)

class Exam_Attendance(models.Model):
    see_att_id = models.AutoField(primary_key=True)
    ht_details_id = models.ForeignKey(Exam_HallTicket_Details,on_delete=CASCADE)
    st_uid = models.ForeignKey(Student_Details, to_field="st_uid", db_column="st_uid", on_delete=CASCADE)
    attendance_Status = models.CharField(max_length=1,null=False, default='P')

    class Meta:
        unique_together = (('st_uid', 'ht_details_id'),)

    objects=models.Manager()

    def str(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.see_att_id  

class MPC_Report(models.Model):
    mpc_report_id = models.AutoField(primary_key=True)
    see_att_id = models.ForeignKey(Exam_Attendance,db_column="see_att_id",on_delete=CASCADE)
    mpc_description = models.CharField(max_length=40,null=True)
    reported_by = models.ForeignKey(Employee_Details,db_column="reported_by",on_delete=CASCADE)
    reporter_designation = models.CharField(max_length=15,null=False)

    class Meta:
        unique_together = (('see_att_id', 'reported_by'),)
    objects=models.Manager()

    def str(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.mpc_report_id

class Makeup_Exam_Registration(models.Model):
    makeup_exam_reg_id = models.AutoField(primary_key=True)
    acad_cal_id = models.ForeignKey(Academic_Calendar,db_column="acad_cal_id",on_delete=CASCADE)
    branch = models.ForeignKey(Department,db_column="branch",on_delete=CASCADE)
    st_uid = models.ForeignKey(Student_Details,to_field="st_uid",db_column="st_uid",on_delete=CASCADE)
    scheme_details_id = models.ForeignKey(Scheme_Details,db_column="scheme_details_id",on_delete=CASCADE)
    exemption_from_grade_reduction = models.BooleanField(null=True,default=False)
    reason_for_application = models.CharField(max_length=50,null=True)
    exam_id = models.ForeignKey(Exam_Details,db_column="exam_id",on_delete=CASCADE)

    class Meta:
        unique_together = (('st_uid', 'scheme_details_id'),)
    
    objects=models.Manager()

    def str(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.makeup_exam_reg_id

class Exam_QP(models.Model):
    exam_qp_id = models.AutoField(primary_key=True)
    exam_id = models.ForeignKey(Exam_Details, on_delete=CASCADE,related_name="exam_QP")
    course_code = models.ForeignKey(Scheme_Details, on_delete=CASCADE)

    class Meta:
        unique_together = (('exam_id','course_code'),)
    
    objects=models.Manager()
    
    def _str_(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.exam_qp_id)

class Exam_QP_Pattern(models.Model):
    qp_pattern_id = models.AutoField(primary_key=True)
    qnum = models.SmallIntegerField(null=True)
    subqnum =  models.CharField(max_length=1)
    max_marks = models.SmallIntegerField(null=True)
    co = models.ManyToManyField(Course_Outcome)
    exam_qp_id = models.ForeignKey(Exam_QP, on_delete=CASCADE,related_name="exam_QP_pattern")
    
    class Meta:
        unique_together = (('qnum', 'subqnum', 'exam_qp_id'),)

    def str(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.qp_pattern_id

class Exam_Bitwise_Marks(models.Model):
    bitwise_marks_id = models.AutoField(primary_key=True)
    code_number = models.CharField(max_length=30,null=False)
    obtained_marks = models.SmallIntegerField(null=False, default=0)
    qp_pattern_id = models.ForeignKey(Exam_QP_Pattern, on_delete=CASCADE,related_name="exam_QP_bitwise_marks")
    valuation_type = models.SmallIntegerField(null=False)
    
    class Meta:
        unique_together = (('code_number','qp_pattern_id','valuation_type'),)

    def str(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.bitwise_marks_id

class SEE_Total_Marks(models.Model):
    valuation_id = models.AutoField(primary_key=True)
    st_id = models.ForeignKey(Student_Details, on_delete=CASCADE)
    total_valuation_marks = models.SmallIntegerField(null=False, default=0)
    grade_obtained = models.CharField(max_length=1,null=False)
    valuation_type = models.SmallIntegerField(null=False)
    exam_qp_id = models.ForeignKey(Exam_QP, on_delete=CASCADE)
    
    
    class Meta:
        unique_together = (('st_id','exam_qp_id','valuation_type'),)

    def str(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.valuation_id

class Exam_Results(models.Model):
    exam_results_id = models.AutoField(primary_key=True)
    exam_id = models.ForeignKey(Exam_Details, on_delete=CASCADE,related_name="exam_result")
    st_id = models.ForeignKey(Student_Details, on_delete=CASCADE)
    st_branch = models.ForeignKey(Department, on_delete=CASCADE)
    scheme_details_id = models.ForeignKey(Scheme_Details, on_delete=CASCADE)
    acad_cal_id = models.ForeignKey(Academic_Calendar,db_column="acad_cal_id",on_delete=CASCADE)
    semester = models.SmallIntegerField(null=True)
    academics_master_details_id = models.ForeignKey(Academics_Master_Details, on_delete=CASCADE)
    # exam_marks = models.SmallIntegerField(null=False, default=0)
    see_marks = models.SmallIntegerField(null=False, default=0)         #newly added attribute
    final_marks = models.SmallIntegerField(null=False, default=0)         #newly added attribute
    exam_old_grade = models.CharField(max_length=1,null=False)
    exam_new_grade = models.CharField(max_length=1,null=False)
    exam_gp_earned = models.SmallIntegerField(null=True)
    exam_type = models.SmallIntegerField(null=True)
    grade_mapping_id = models.ForeignKey(GradeMapping, on_delete=CASCADE)

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.exam_results_id)
    