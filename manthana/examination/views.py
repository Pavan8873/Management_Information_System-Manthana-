import tempfile
import math
from django.shortcuts import render
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from weasyprint import HTML
from admission.models import *
from master_mgmt.models import *
from academics.models import *
from examination.models import *
from hr.models import *
from django.db import transaction
from django.template.loader import render_to_string
from django.db.models import Max
from django.utils import timezone
from datetime import datetime

# Create your views here.
def loadExamDetails(request):
    academic_year_tbl = AcademicYear.objects.all().order_by('-acayear')
    # academic_year_tbl = AcademicYear.objects.all().order_by('-acayear')[:2]
    return render(request,"exam_details.html",{'academic_year_tbl':academic_year_tbl})

#Only Regular / Makeup Exam Details
def addExamDetails(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        acad_year = None
        sem = None
        acad_cal_id = None
        exam_type = None
        
        try:
            acad_year = request.POST.get("acad_cal_acad_year")
            acadyr = AcademicYear.objects.get(acayear = acad_year).id
            print(acadyr)
            print("lll")
            sem = int(request.POST.get("acad_cal_sem"))
            exam_type = int(request.POST.get("exam_type"))
            print(exam_type)
            
            # exam_desc = request.POST.get("exam_desc")
            see_theory_from = request.POST.get("acad_cal_see_theory_from")
            see_theory_to = request.POST.get("acad_cal_see_theory_to")
            see_lab_from = request.POST.get("acad_cal_see_lab_from")
            see_lab_to = request.POST.get("acad_cal_see_lab_to")
            if(exam_type==1 or exam_type==2 or exam_type ==3): # Regular Semester
                
                acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id=acadyr,acad_cal_sem=sem,acad_cal_type=1)
                print(acad_cal_id)
            if(exam_type==4 or exam_type==5 or exam_type ==6): # Regular Semester
                
                acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id=acadyr,acad_cal_sem=sem,acad_cal_type=2)
                print(acad_cal_id)
            
            exam_desc = None

            if(exam_type==1 and sem==1):
                exam_desc = acad_year+" SEE (Regular) "+str(sem)+"st sem"
            elif(exam_type==1 and sem==2):
                exam_desc = acad_year+" SEE (Regular) "+str(sem)+"nd sem"
            elif(exam_type==1 and sem==3):
                print(exam_type)
                exam_desc = acad_year+" SEE (Regular) "+str(sem)+"rd sem"
            elif(exam_type==1 and (sem>=4 and sem<=8)):
                exam_desc = acad_year+" SEE (Regular) "+str(sem)+"th sem"
            
            if(exam_type==2 and sem==1):
                exam_desc = acad_year+" Makeup Exam "+str(sem)+"st sem"
            elif(exam_type==2 and sem==2):
                exam_desc = acad_year+" Makeup Exam "+str(sem)+"nd sem"
            elif(exam_type==2 and sem==3):
                exam_desc = acad_year+" Makeup Exam "+str(sem)+"rd sem"
            elif(exam_type==2 and (int(sem)>=4 and int(sem)<=8)):
                exam_desc = acad_year+" Makeup Exam "+str(sem)+"th sem"
            
            
            if(exam_type==3 and sem==1):
                exam_desc = acad_year+" Special Makeup Exam  "+str(sem)+"st sem"
            elif(exam_type==3 and sem==2):
                exam_desc = acad_year+" Special Makeup Exam  "+str(sem)+"nd sem"
            elif(exam_type==3 and sem==3):
                exam_desc = acad_year+" Special Makeup Exam  "+str(sem)+"rd sem"
            elif(exam_type==3 and (int(sem)>=4 and int(sem)<=8)):
                exam_desc = acad_year+" Special Makeup Exam "+str(sem)+"th sem"

            if(exam_type==4 and sem==1):
                exam_desc = acad_year+" STC Exam  "+str(sem)+"st sem"
            elif(exam_type==4 and sem==2):
                exam_desc = acad_year+"  STC Exam  "+str(sem)+"nd sem"
            elif(exam_type==4 and sem==3):
                exam_desc = acad_year+"  STC Exam  "+str(sem)+"rd sem"
            elif(exam_type==4 and (int(sem)>=4 and int(sem)<=8)):
                exam_desc = acad_year+"  STC Exam "+str(sem)+"th sem"

            if(exam_type==5 and sem==1):
                exam_desc = acad_year+" STC Makup Exam  "+str(sem)+"st sem"
            elif(exam_type==5 and sem==2):
                exam_desc = acad_year+"  STC Makup Exam  "+str(sem)+"nd sem"
            elif(exam_type==5 and sem==3):
                exam_desc = acad_year+" STC Makup Exam  "+str(sem)+"rd sem"
            elif(exam_type==5 and (int(sem)>=4 and int(sem)<=8)):
                exam_desc = acad_year+"  STC Makup Exam "+str(sem)+"th sem"
            
            if(exam_type==6 and sem==1):
                exam_desc = acad_year+" Sepcial STC  Exam  "+str(sem)+"st sem"
            elif(exam_type==6 and sem==2):
                exam_desc = acad_year+" Sepcial STC  Exam  "+str(sem)+"nd sem"
            elif(exam_type==6 and sem==3):
                exam_desc = acad_year+" Sepcial STC  Exam "+str(sem)+"rd sem"
            elif(exam_type==6 and (int(sem)>=4 and int(sem)<=8)):
                exam_desc = acad_year+"  Sepcial STC  Exam "+str(sem)+"th sem"
            acad_year_id = AcademicYear.objects.get(id=acadyr)
            exam_details_obj = Exam_Details.objects.create(acad_year=acad_year_id,semester=sem,acad_cal_id=acad_cal_id,exam_type=exam_type,duration_theory_from=see_theory_from,duration_theory_to=see_theory_to,duration_lab_from=see_lab_from,duration_lab_to=see_lab_to,description=exam_desc)
            messages.success(request,"Exam Details entered!")
        except Academic_Calendar.DoesNotExist:
            messages.error(request,"Enter correct Academic Year & Semester!")
        except Exception as e:
            print(e)
            messages.error(request,e)
            # messages.error(request,"Duplicate entry not allowed!")
        return loadExamDetails(request) 

def loadExternalValuatorsPage(request):
    ext_colleges_tbl = ExtValuatorCollegeName.objects.all()
    return render(request,"external_valuator.html",{'ext_colleges_tbl':ext_colleges_tbl})

def addExternalValuators(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        ext_valuator_name = None
        ext_valuator_college = None
        ext_valuator_department= None
        ext_valuator_designation = None
        ext_valuator_pan = None
        ext_valuator_phone = None
    try:
        ext_valuator_name = request.POST.get('valuator_name') 
        ext_valuator_college = request.POST.get('college_name') 
        ext_valuator_department = request.POST.get('department') 
        ext_valuator_designation = request.POST.get('designation') 
        ext_valuator_pan = request.POST.get('pan_no')
        ext_valuator_phone = request.POST.get('phone_no')
        
        ext_valuator_obj = External_Valuator.objects.create(ext_valuator_name=ext_valuator_name,ext_valuator_college=ExtValuatorCollegeName.objects.get(id=ext_valuator_college),ext_valuator_department=ext_valuator_department,ext_valuator_designation=ext_valuator_designation,ext_valuator_pan=ext_valuator_pan,ext_valuator_phone=ext_valuator_phone)
        messages.success(request,"Added External Valuator - Prof."+ext_valuator_name+"")
    except IntegrityError:
            messages.error(request,"Duplicate entry NOT allowed!")
    except Exception as e:
            print(e)
            messages.error(request,e)
    return loadExternalValuatorsPage(request)

def loadSEEValuatorsPage(request):
    exam_list = Exam_Details.objects.all().order_by('-acad_year')[:3]
    # exam_list = Exam_Details.objects.all().values('description')[:1]
    return render(request,"valuationRights.html",{'exam_list':exam_list,'department': Department.objects.all()})

def assignRightsToValuators(request):
    valuator_type = None
    valuator_empId = None
    valuator_pan = None
    course_code = None
    exam_type = None

    try:
        valuator_type = request.POST.get('valuator_type')
        #valuator_empid = request.POST.get('valuator_empid')
        course_code = request.POST.get('course_code')
        subj_code = Scheme_Details.objects.get(course_code=course_code)
        #course_title = request.POST.get('course_title')
        #college_name = request.POST.get('college_name')
        #acad_year = request.POST.get('acad_year')
        #semester = request.POST.get('sem')
        print(valuator_type)
        exam_type = request.POST.get('exam_descr')
        print(exam_type)
        exam_id = Exam_Details.objects.get(exam_details_id=exam_type)

        if(valuator_type == '1'):
            try:
                print("Inside Internal valuator")
                valuator_empId = request.POST.get('valuator_empid')
                empid = Employee_Details.objects.get(employee_emp_id=valuator_empId)
                see_valuator_obj = SEE_Valuator.objects.create(valuator_type=str(valuator_type),valuator_empId=empid,course_code=subj_code,exam_details_id=exam_id)
            except Employee_Details.DoesNotExist:
                messages.error(request,"Incorrect emp ID")
        else:
            try:
                valuator_pan =  request.POST.get('pan_no')
                pan = External_Valuator.objects.get(ext_valuator_pan=valuator_pan)
                see_valuator_obj = SEE_Valuator.objects.create(valuator_type=str(valuator_type),valuator_pan=pan,course_code=subj_code,exam_details_id=exam_id)
            except Employee_Details.DoesNotExist:
                messages.error(request,"Incorrect PAN")

        messages.success(request,"Added Valuator Details!")
    
    except Exception as e:
        print(e)
        messages.error(request,e)
        # return loadSEEValuatorsPage(request)
    
    return loadSEEValuatorsPage(request)

# code to handle ajax request
def loadSEESubjects(request):
    dept_id = request.GET.get('offered_by')
    sem = request.GET.get('sem')
    exam_id = request.GET.get('exam_descr')
    acad_cal_id = Exam_Details.objects.get(exam_details_id=exam_id).acad_cal_id
    series = None
    courselist = None
    try:
        series = Scheme_Allotment.objects.get(acad_cal_id=acad_cal_id,course_sem=sem).scheme_series
    except Scheme_Allotment.DoesNotExist:
        return render(request, "see_subjects_dropdown.html", {'courselist': courselist})
        # return JsonResponse({"error":"Err : Scheme not allotted"},status=500)
    try:
        courselist = Scheme_Details.objects.filter(sem_allotted=sem, scheme_series=series, offered_by_id=dept_id).order_by('course_code')
    except Scheme_Details.DoesNotExist:
        return render(request, "see_subjects_dropdown.html", {'courselist': courselist})
        # return JsonResponse({"error":"Err : No Subjects found"},status=500)
    return render(request, "see_subjects_dropdown.html", {'courselist': courselist})

def loadSubjectsSEETimetable(request):
    dept_id = request.GET.get('offered_by')
    sem = request.GET.get('sem')
    acadyear = request.GET.get('acad_year')
    exam_descr = request.GET.get('exam_descr')
    print(exam_descr)
    if 'regular' in exam_descr.lower():
        acad_cal_type = 1
    elif 'stc' in exam_descr.lower():
        acad_cal_type = 2
    print(acad_cal_type,"pp")
    acadcal_id = Academic_Calendar.objects.get(acad_cal_acad_year=acadyear,acad_cal_sem=sem,acad_cal_type=acad_cal_type)
    series = None
    courselist = None
    try:
        series = Scheme_Allotment.objects.get(acad_cal_id=acadcal_id,course_sem=sem).scheme_series
    except Scheme_Allotment.DoesNotExist:
        # return render(request, "see_subjects_dropdown.html", {'courselist': courselist})
        return JsonResponse({"error":"Err : Scheme not allotted"},status=500)
    try:
        courselist = Scheme_Details.objects.filter(sem_allotted=sem, scheme_series=series, offered_by_id=dept_id).order_by('course_code')
        print(courselist)
    except Scheme_Details.DoesNotExist:
        # return render(request, "see_subjects_dropdown.html", {'courselist': courselist})
        return JsonResponse({"error":"Err : No Subjects found"},status=500)
    return render(request, "see_subjects_dropdown.html", {'courselist': courselist})

def generate_see_timetable(request):
    userName=CustomUser.objects.get(id=request.user.id)
    if request.POST:
            
    
        date = request.POST['examdate']
        acad_year = request.POST['acad_year']
        course_code = request.POST['course_code']
        #exam_time = request.POST['examtime']
        exam_descr = request.POST['exam_descr']
        sem = request.POST['sem']
        print(exam_descr)
        if 'regular' in exam_descr.lower():
            acad_cal_type = 1
        elif 'stc' in exam_descr.lower():
            acad_cal_type = 2
        print(acad_cal_type,"pp")
        acadcal_id = Academic_Calendar.objects.get(acad_cal_acad_year=acad_year,acad_cal_sem=sem,acad_cal_type=acad_cal_type)
        sem = Scheme_Details.objects.get(course_code=course_code).sem_allotted
        acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year=acad_year,acad_cal_sem=sem,acad_cal_type=acad_cal_type).acad_cal_id   
        exam_id = Exam_Details.objects.get(acad_cal_id=acad_cal_id,description=exam_descr,semester=sem)
        try:
            SEE_timetable_obj = SEE_timetable.objects.create(scheme_details_id=Scheme_Details.objects.get(course_code=course_code),exam_id=exam_id,exam_date=date,acad_cal_id=Academic_Calendar.objects.get(acad_cal_id=acad_cal_id),attendance_flag=0,absentees_count=0)
            # SEE_timetable_obj = SEE_timetable.objects.create(scheme_details_id=Scheme_Details.objects.get(course_code=course_code),exam_id=exam_id,exam_date=date,exam_time=exam_time,acad_cal_id=Academic_Calendar.objects.get(acad_cal_id=acad_cal_id),attendance_flag=0,absentees_count=0)
        except IntegrityError:
            messages.error(request, "Duplicate entry not allowed!")
            return render(request,"generate_see_timetable.html",{'calender': Academic_Calendar.objects.values('acad_cal_acad_year').distinct(),'scheme_detail':Scheme_Details.objects.all(),'exam_list':Exam_Details.objects.all(),'department': Department.objects.all()})
        messages.success(request,"Added the exam date for "+course_code) 
        return render(request,"generate_see_timetable.html",{'calender': Academic_Calendar.objects.values('acad_cal_acad_year').distinct(),'scheme_detail':Scheme_Details.objects.all(),'exam_list':Exam_Details.objects.all(),'department': Department.objects.all()})
    else:
        return render(request,"generate_see_timetable.html",{'calender': AcademicYear.objects.all(),'scheme_detail':Scheme_Details.objects.all(),'exam_list':Exam_Details.objects.all(),'department': Department.objects.all()})   

'''def gen_barcode(request):
    userName=CustomUser.objects.get(id=request.user.id)
    if request.method!="POST":
        departments = Department.objects.all()
        course_obj = Scheme_Details.objects.all()
        # exams  = Exam_Details.objects.order_by('-acad_year')[:2]
        exams  = Exam_Details.objects.order_by('-acad_year')
        return render(request,"generateBarCode.html",{'username':userName,'departments':departments, 'course_obj':course_obj, 'exams':exams})

    else:
        btn_clicked = request.POST.get("btn_clicked")
        exam_id = request.POST.get("exam_id")
        department = request.POST.get("department")
        exam = Exam_Details.objects.get(exam_details_id=exam_id)
        if btn_clicked == "generate_qrcode_submit":
            userName=CustomUser.objects.get(id=request.user.id)
            departments = Department.objects.all()
            studentList = Student_Details.objects.all()
            studentCount = Student_Details.objects.all().count()
            
            coursesOfExam = Exam_QP.objects.filter(exam_id=exam_id)
            coursesOfDept = coursesOfExam.filter(course_code__offered_by=department)

            for course in coursesOfDept:
                scheme_details_id = course.course_code_id

                #getting "hall_ticket_id"'s of the exam    Ex: all hall-tickets for {"2020-21 Regular SEE Exam Odd Sem(5) Dec21-Jan22"}
                halticketsOfExam = Exam_HallTicket.objects.filter(exam_id=exam_id)

                #getting halltickets of the previously retrived hall-tickets
                halticketDetailsOfExam = Exam_HallTicket_Details.objects.filter(hall_ticket_id__in = halticketsOfExam)

                #getting all "ht_details_id"'s for a particular course 
                ht_details_id = halticketDetailsOfExam.filter(academics_master_details_id__scheme_details_id = scheme_details_id)

                #getting all the student list with the "ht_details_id"'s and present for the exam
                studentsAttended = Exam_Attendance.objects.filter(ht_details_id__in = ht_details_id, attendance_status = 1).values('st_uid')

                # total_stds = studentsAttended.count()

                # no_of_packets = 100 + total_stds/10

                packet = 100

                std_counter = 1
                
                for student in studentsAttended :
                    schemeDetails = Scheme_Details.objects.get(scheme_details_id = scheme_details_id)
                    exam = Exam_Details.objects.get(exam_details_id=exam_id)
                    branchCode = schemeDetails.offered_by.code

                    examType = exam.exam_type

                    # Ex for 2021-22 getting only 22
                    ay = exam.acad_cal_id.acad_cal_acad_year.split("-")[1]

                    sem = exam.semester

                    #getting last 2 characters of code ex : 18UCSL603 => 03 
                    course = schemeDetails.course_code[-2:]

                    script_no = (std_counter%11)
                    std_counter+=1

                    print("std_counter")
                    print(std_counter)

                    if(script_no%11 == 0):
                        script_no = 1
                        std_counter+=1
                        packet +=1

                    # var1 = "Hello"
                    # var2 = "World"
                    # "{} {}".format(var1, var2)
                    # var3 = > Hello World
                    code = "{}{}{}{}{}{}-{}".format(branchCode, ay, examType, sem, course, packet, script_no)

                    std = Student_Details.objects.get(st_id = student['st_uid'])

                    barcode_generate =  Bar_Code.objects.create(st_id=std,barcode=code,exam_id=exam)
                    barcode_generate.save()

            return HttpResponseRedirect('generate_barcode')
        if btn_clicked == "generate_qrcode_pdf":

            program = None
            
            userName=CustomUser.objects.get(id=request.user.id)
            barcodeList = Bar_Code.objects.filter(exam_id = exam)
            print(barcodeList)

            st_temp = barcodeList[0].st_id

            if "BE" in st_temp.st_uid :
                program = "BE"
            if "MTECH" in st_temp.st_uid :
                program = "MTECH"
            if "MBA" in st_temp.st_uid :
                program = "MBA"

            barcodes = dict()

            coursesOfExam = Exam_QP.objects.filter(exam_id=exam_id)
            coursesOfDept = coursesOfExam.filter(course_code__offered_by=department)
            
            examType = exam.exam_type
            # Ex for 2021-22 getting only 22
            ay = exam.acad_cal_id.acad_cal_acad_year.split("-")[1]
            sem = exam.semester
            for course in coursesOfDept:
                scheme_details_id = course.course_code_id
                schemeDetails = Scheme_Details.objects.get(scheme_details_id = scheme_details_id)
                course_code = schemeDetails.course_code[-2:]
                branchCode = schemeDetails.offered_by.code
                code = "{}{}{}{}{}".format(branchCode, ay, examType, sem, course_code)
                barcodeListOfCourse = barcodeList.filter(barcode__startswith=code)
                barcodes[schemeDetails] = barcodeListOfCourse

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'inline; attachment; filename='+"ack_pdf_ug"+str(datetime.now())+".pdf"
            response['Content-Transfer-Encoding'] = 'binary'

            dept = Department.objects.get(dept_id = department)
            html_string = render_to_string('barcode_pdf.html',{'username':userName,'barcodes':barcodes, 'exam':exam, "dept":dept, "program":program})
            html = HTML(string=html_string, base_url=request.build_absolute_uri())

            result = html.write_pdf()

            with tempfile.NamedTemporaryFile(delete=True) as output:
                output.write(result)
                output.flush()

                output=open(output.name, 'rb')
                response.write(output.read())

            return response'''

def generate_hallticket(request):
    userName=CustomUser.objects.get(id=request.user.id)
    departments = Department.objects.all()
    course_obj = Scheme_Details.objects.all()
    exams  = Exam_Details.objects.order_by('-acad_year')
    return render(request,"gen_hallticket.html",{'username':userName,'departments':departments, 'course_obj':course_obj, 'exams':exams})

'''
def gen_hallTicket(request):
    print("Function call")
    userName=CustomUser.objects.get(id=request.user.id)
    if request.method!="POST":
        departments = Department.objects.all()
        course_obj = Scheme_Details.objects.all()
        # exams  = Exam_Details.objects.order_by('-acad_year')[:2]
        exams  = Exam_Details.objects.order_by('-acad_year')
        return render(request,"gen_hallticket.html",{'username':userName,'departments':departments, 'course_obj':course_obj, 'exams':exams})
    
    else:
        btn_clicked = request.POST.get("btn_clicked")

        exam_id = request.POST.get("exam_id")
        department = request.POST.get("department")

        exam = Exam_Details.objects.get(exam_details_id=exam_id)
        if btn_clicked == "generate_hallticket_submit":
            print("Inside button function")
            coursesOfExam = Exam_QP.objects.filter(exam_id=exam_id)
            coursesOfDept = coursesOfExam.filter(course_code__offered_by=department)

            acad_cal_id = exam.acad_cal_id
            coursesOfDept = coursesOfExam.filter(course_code__offered_by=department).values_list('course_code_id', flat=True).distinct()
            sequence_no=100
            student_id_list = Academics_Master_Details.objects.filter(acad_cal_id_id=acad_cal_id,scheme_details_id__in=coursesOfDept,st_branch=1).values_list('st_uid', flat=True).distinct()

            branchCode = Department.objects.get(dept_id=department).code
            # Ex for 2021-22 getting only 22
            ay = exam.acad_cal_id.acad_cal_acad_year.split("-")[1]
            sem = exam.semester
            print("Before Loop")
            for st_id in student_id_list:
                # "9-digit number to be generated according to following pattern:
                # 1) First digist represents UG/PG. U --> UG, P--> PG
                # 2) Next 2-digits represent Current Academic Year (Eg: AY 2022-23 --> 22)
                # 3) Next 2-digits represent Department (Eg: CS - 01)
                # 4) Next 1-digit represnets semseter
                # 5) Next 3-digits represents sequence number"

                student = Student_Details.objects.get(st_id=st_id)

                prev_created_hallticket = Exam_HallTicket.objects.get(Q(st_uid=student, exam_id__acad_cal_id__acad_cal_acad_year= exam.acad_cal_id.acad_cal_acad_year) & ~Q(exam_id=exam))
                print("Within Loop")
                if "BE" in student.st_uid:
                    fd = "U"
                else:
                    fd = "P"
                code = "{}{}{}{}{}".format(fd, ay, branchCode, sem, sequence_no)
                sequence_no+=1

                try:
                    exam_hallTicket = Exam_HallTicket.objects.create(exam_id=exam, st_uid=student, ht_application_no=code)

                    student_master_details_list = Academics_Master_Details.objects.filter(st_uid=student,acad_cal_id_id=acad_cal_id,scheme_details_id__in=coursesOfDept)

                except Exception as e:
                    print("Exception occur")
                    pass

                for smd in student_master_details_list:
                    try:
                        Exam_HallTicket_Details.objects.create(hall_ticket_id=exam_hallTicket, academics_master_details_id=smd)
                    except Exception as e:
                        pass

                
            userName=CustomUser.objects.get(id=request.user.id)
            departments = Department.objects.all()
            course_obj = Scheme_Details.objects.all()
            # exams  = Exam_Details.objects.order_by('-acad_year')[:2]
            exams  = Exam_Details.objects.order_by('-acad_year')

            return render(request,"gen_hallticket.html",{'username':userName,'departments':departments, 'course_obj':course_obj, 'exams':exams})

        if btn_clicked == "generate_hallticket_pdf":
            program = None
            acad_cal_id = exam.acad_cal_id
            branchCode = Department.objects.get(dept_id=department).code

            exam_qps_of_branch = Exam_QP.objects.filter(exam_id=exam)
            course_reg_for_exam_by_branch = exam_qps_of_branch.filter(course_code__offered_by=department).values_list('course_code_id', flat=True).distinct()

            hall_tickets_details_of_exam_of_dept = Exam_HallTicket_Details.objects.filter(hall_ticket_id__exam_id = exam, academics_master_details_id__scheme_details_id__in = course_reg_for_exam_by_branch)

            hall_tickets_of_exam_of_dept_list = hall_tickets_details_of_exam_of_dept.values_list('hall_ticket_id', flat=True).distinct()

            hall_tickets_of_exam_of_dept_list = Exam_HallTicket.objects.filter(hall_ticket_id__in = hall_tickets_of_exam_of_dept_list).order_by('st_uid__st_usn')[:30]

            st_temp = hall_tickets_of_exam_of_dept_list[0].st_uid

            if "BE" in st_temp.st_uid :
                program = "BE"
            if "MTECH" in st_temp.st_uid :
                program = "MTECH"
            if "MBA" in st_temp.st_uid :
                program = "MBA"
            

            ht_list = dict()
            for hallTicket in hall_tickets_of_exam_of_dept_list:
                ht_details = dict()
                student = hallTicket.st_uid
                usn = student.st_usn
                courses_reg_for_exam_by_student = hallTicket.hallTicketDetails.values_list('academics_master_details_id__scheme_details_id', flat=True).distinct()
                scheme_details_reg_for_exam_by_student = Scheme_Details.objects.filter(scheme_details_id__in = courses_reg_for_exam_by_student)
                courses = dict()
                for index, course in enumerate(scheme_details_reg_for_exam_by_student):
                    courses[index]=course
                ht_details["hall_ticket"] = hallTicket
                ht_details["student"] = student                    
                ht_details["courses"] = courses
                ht_list[usn] = ht_details

            dept = Department.objects.get(dept_id = department)

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'inline; attachment; filename='+"hallticket"+str(datetime.now())+".pdf"
            response['Content-Transfer-Encoding'] = 'binary'

            userName=CustomUser.objects.get(id=request.user.id)
            html_string = render_to_string('gen_hallticket_pdf.html',{'username':userName, 'ht_list': ht_list, "exam":exam, "dept":dept, "program":program})
            html = HTML(string=html_string, base_url=request.build_absolute_uri())

            result = html.write_pdf()

            with tempfile.NamedTemporaryFile(delete=True) as output:
                output.write(result)
                output.flush()

                output=open(output.name, 'rb')
                response.write(output.read())

            return response
'''

def MPCReport(request):
    username=CustomUser.objects.get(id=request.user.id)
    return render(request,"MpcReport.html",{'username':username,'department':Department.objects.all(),'exam_list':Exam_Details.objects.all()})  

def addMpcReport(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        acad_year = None
        sem = None
        exam_type = None
        course_code = None
        st_uid = None
        designation = None
        report_by = None
        desc = None
        exam_det_id = None
        hall_ticket_id = None
        reporter_id = None
        attendance = None

        try:
            exam_desc = request.POST.get("exam_descr")
            acad_year = Exam_Details.objects.get(exam_details_id=exam_desc).acad_cal_id.acad_cal_acad_year 
            sem = request.POST.get("acad_cal_sem")
            exam_type = Exam_Details.objects.get(exam_details_id=exam_desc).exam_type
            course_code = request.POST.get("course_code")
            
            st_uid = request.POST.get("st_uid")
            designation = request.POST.get("designation")
            report_by = request.POST.get("reporter_id")
            desc = request.POST.get("desc") 

        except Academic_Calendar.DoesNotExist:
            messages.error(request, "Please check Academic Year and enter")
            username = CustomUser.objects.get(id=request.user.id)
            context = {'username':username,'department':Department.objects.all(),'exam_list':Exam_Details.objects.all()}
            return render(request,"MpcReport.html",context=context)

        try:
            exam_det_id = Exam_Details.objects.get(acad_year=acad_year,semester=sem,exam_type=exam_type) 
        
        except Exam_Details.DoesNotExist:
            messages.error(request, "No exam information for this details. Enter correct data")
            username = CustomUser.objects.get(id=request.user.id)
            context = {'username':username,'department':Department.objects.all(),'exam_list':Exam_Details.objects.all()}
            return render(request,"MpcReport.html",context=context)

        except Exception as e:
            print(e)

        try:
            hall_ticket_id = Exam_HallTicket.objects.get(exam_id=exam_det_id,st_uid=st_uid)

        except Exam_HallTicket.DoesNotExist:
            messages.error(request, "No hall ticket information for this student. Enter correct data")
            username = CustomUser.objects.get(id=request.user.id)
            context = {'username':username,'department':Department.objects.all(),'exam_list':Exam_Details.objects.all()}
            return render(request,"MpcReport.html",context=context)

        except Exception as e:
            print(e)

        try:
            schm_det_id = Scheme_Details.objects.get(course_code=course_code)
            acad_mid = Academics_Master_Details.objects.get(st_uid=st_uid,scheme_details_id=schm_det_id)
            
        except Academics_Master_Details.DoesNotExist:
            messages.error(request, "Student has not registered for this course. Enter correct data")
            username = CustomUser.objects.get(id=request.user.id)
            context = {'username':username,'department':Department.objects.all(),'exam_list':Exam_Details.objects.all()}
            return render(request,"MpcReport.html",context=context)
        try:
            ht_id = Exam_HallTicket_Details.objects.get(hall_ticket_id=hall_ticket_id,academics_master_details_id=acad_mid)
            see_attid = Exam_Attendance.objects.get(ht_details_id=ht_id)
            attendance = Exam_Attendance.objects.get(ht_details_id=ht_id).attendance_Status
            reporter_id = Employee_Details.objects.get(faculty_emp_id=report_by)
    
        except Exam_Attendance.DoesNotExist:
            messages.error(request, "No information for these details. Enter correct data")
            username = CustomUser.objects.get(id=request.user.id)
            context = {'username':username,'department':Department.objects.all(),'exam_list':Exam_Details.objects.all()}
            return render(request,"MpcReport.html",context=context)

        except Exception as e:
            print(e)

        try:
            btn_value = request.POST["btn_mpc"]
            if btn_value == "register":
                if(attendance == 'P'):
                    mpc_report_obj = MPC_Report.objects.create(see_att_id=see_attid,mpc_description=desc,reported_by=reporter_id,reporter_designation=designation)
                    mpc_report_obj.save()
                    messages.success(request,"Success! MPC Reported for Student with Id - "+st_uid)
                else:
                    messages.warning(request,"The Student is absent you cannot assign mpc report")
            if btn_value == "update":
                mpc_id = request.POST.get('mpc_report_id')
                mpc_report_obj = MPC_Report.objects.get(mpc_report_id=mpc_id)
                mpc_report_obj.see_att_id = see_attid
                mpc_report_obj.mpc_description = desc
                mpc_report_obj.reported_by = reporter_id
                mpc_report_obj.reporter_designation = designation
                attendance = see_attid.attendance_Status
                if(attendance == 'P'):
                    mpc_report_obj.save()
                    messages.success(request,"Success! Updated Successfully")
                else:
                    messages.warning(request,"The Student is absent you cannot assign mpc report")
        except IntegrityError:
            messages.warning(request,"Already Reported for Student with Id - "+st_uid)   
        except Exception as e:
            print(e)
        username = CustomUser.objects.get(id=request.user.id)
        context = {'prv':prv,'username':username,'department':Department.objects.all(),'exam_list':Exam_Details.objects.all()}
        return render(request,"MpcReport.html",context=context) 

def view_mpc_report(request):
    username=CustomUser.objects.get(id=request.user.id)
    mpc_report_obj = MPC_Report.objects.all()
    return render(request,"Edit_MpcReport.html",{'username':username,'department':Department.objects.all()})


def EditMPCReport(request,mpc_report_id):
    username = CustomUser.objects.get(id=request.user.id)
    mpcid = MPC_Report.objects.get(mpc_report_id=mpc_report_id)  
    seeid = Exam_Attendance.objects.get(see_att_id=mpcid.see_att_id.see_att_id)  #1
    htid=seeid.ht_details_id    #1
    amid = Exam_HallTicket_Details.objects.get(ht_details_id=htid.ht_details_id).academics_master_details_id
    acad_cal_id = amid.acad_cal_id
    acad_yr = Academic_Calendar.objects.get(acad_cal_id=acad_cal_id.acad_cal_id).acad_cal_acad_year
    hallid = Exam_HallTicket_Details.objects.get(ht_details_id=htid.ht_details_id).hall_ticket_id
    examid = Exam_HallTicket.objects.get(hall_ticket_id=hallid.hall_ticket_id).exam_id
    schmid = amid.scheme_details_id.scheme_details_id
    coursecode = Scheme_Details.objects.get(scheme_details_id=schmid).course_code
    sem = amid.semester
    ss = Scheme_Allotment.objects.get(acad_cal_id=acad_cal_id,course_sem=sem).scheme_series
    course_list = Scheme_Details.objects.filter(scheme_series=ss,sem_allotted=sem,offered_by=Department.objects.get(dept_name=amid.st_branch).dept_id)
    
    return render(request,"MpcReport.html",{'username':username,'department':Department.objects.all(),'exam_desc':examid,'exam_list':Exam_Details.objects.all(),'mpc_obj':mpcid,'acad_year':acad_yr,'coursecode':coursecode,'sem':sem,'branch':amid.st_branch,'stuid':amid.st_uid,'desig':mpcid.reporter_designation,'repid':mpcid.reported_by.faculty_emp_id,'desc':mpcid.mpc_description,'course_list':course_list})

def SearchMpcStudent(request):
    username=CustomUser.objects.get(id=request.user.id)
    department = Department.objects.all()
    if request.POST:
        Acad_Year = request.POST.get('acad_cal_acad_year')
        Branch = request.POST['offered_by']
        Sem = request.POST['acad_cal_sem']
        Exam_type = request.POST.get('exam_type')
        Uid = request.POST['st_uid']  
        Course_code = request.POST['course_code']
        
       
        # Search parameter is Academic Year
        if Acad_Year != "0" :
            exam_details_obj_ids = Exam_Details.objects.filter(acad_year=Acad_Year) # 3 4
            hall_ticket_ids = Exam_HallTicket.objects.filter(exam_id__in=exam_details_obj_ids)   #1 2
            ht_ids = Exam_HallTicket_Details.objects.filter(hall_ticket_id__in=hall_ticket_ids)   # 1 2 3
            see_att_ids = Exam_Attendance.objects.filter(ht_details_id__in=ht_ids)   # 1 2 3
            SearchParm = MPC_Report.objects.filter(see_att_id__in=see_att_ids).values_list('mpc_report_id',flat=True)  # 1 3
            if not SearchParm.exists():
                messages.error(request,"Student Details Not Found")
                return render(request,"Edit_MpcReport.html",{'username':username,'department':department})
            mpc_seeid = MPC_Report.objects.filter(see_att_id__in=see_att_ids).values_list('see_att_id',flat=True)
            see_htid = Exam_Attendance.objects.filter(see_att_id__in=mpc_seeid).values('ht_details_id')
            acadmid = Exam_HallTicket_Details.objects.filter(ht_details_id__in=see_htid).values_list('academics_master_details_id',flat=True)
            hallid = Exam_HallTicket_Details.objects.filter(ht_details_id__in=see_htid).values('hall_ticket_id')
            examid = Exam_HallTicket.objects.filter(hall_ticket_id__in=hallid).values_list('exam_id',flat=True)
            
            st_name = []
            st_dept = []
            st_sem = []
            st_year = []
            st_sub = []
            etype = []

            for s in acadmid:
                st_dept.append(Academics_Master_Details.objects.get(academics_master_details_id=s).st_branch)
                st_sem.append(Academics_Master_Details.objects.get(academics_master_details_id=s).semester)
            
            stuids = Academics_Master_Details.objects.filter(academics_master_details_id__in=acadmid).values_list('st_uid',flat=True)
            for s in stuids:
                st_name.append(Student_Details.objects.get(st_uid=s).st_name)

            acad_id = Academics_Master_Details.objects.filter(academics_master_details_id__in=acadmid).values_list('acad_cal_id',flat=True)
            for i in acad_id:
                st_year.append(Academic_Calendar.objects.get(acad_cal_id=i).acad_cal_acad_year)

            schmid = Academics_Master_Details.objects.filter(academics_master_details_id__in=acadmid).values_list('scheme_details_id',flat=True)
            for id in schmid:
                st_sub.append(Scheme_Details.objects.get(scheme_details_id=id).course_title)
            
            for e in examid:
                etype.append(Exam_Details.objects.get(exam_details_id=e).exam_type)
            
            st_details = zip(st_name,st_sem,st_year,st_sub,etype,st_dept,SearchParm)
            
            
            return render(request,"Edit_MpcReport.html",{'username':username,'department':department,'students':st_details})
        
        # Search parameter is by Branch
        if Branch != "0":
            amid = Academics_Master_Details.objects.filter(st_branch=Branch).values_list('academics_master_details_id',flat=True)
            htids = Exam_HallTicket_Details.objects.filter(academics_master_details_id__in=amid)
            seeids = Exam_Attendance.objects.filter(ht_details_id__in=htids)
            SearchParm = MPC_Report.objects.filter(see_att_id__in=seeids).values_list('mpc_report_id',flat=True)
            
            st_name = []
            name=[]
            year=[]
            st_dept = []
            st_sem = []
            st_year = []
            st_sub = []
            etype = []

            mpc_seeid = MPC_Report.objects.filter(mpc_report_id__in=SearchParm).values_list('see_att_id',flat=True)
            see_htid = Exam_Attendance.objects.filter(see_att_id__in=mpc_seeid).values_list('ht_details_id',flat=True)
            hall_amid = Exam_HallTicket_Details.objects.filter(ht_details_id__in=see_htid).values_list('academics_master_details_id',flat=True)
            hall_hallid = Exam_HallTicket_Details.objects.filter(ht_details_id__in=see_htid).values_list('hall_ticket_id',flat=True)
            examid = Exam_HallTicket.objects.filter(hall_ticket_id__in=hall_hallid).values_list('exam_id',flat=True)

            for a in hall_amid:
                st_dept.append(Academics_Master_Details.objects.get(academics_master_details_id=a).st_branch)
                st_sem.append(Academics_Master_Details.objects.get(academics_master_details_id=a).semester)
                name.append(Academics_Master_Details.objects.get(academics_master_details_id=a).st_uid.st_uid)
                year.append(Academics_Master_Details.objects.get(academics_master_details_id=a).acad_cal_id.acad_cal_id)
                st_sub.append(Academics_Master_Details.objects.get(academics_master_details_id=a).scheme_details_id.course_title)
            for n in name:
                st_name.append(Student_Details.objects.get(st_uid=n).st_name)
            for a in year:
                st_year.append(Academic_Calendar.objects.get(acad_cal_id=a).acad_cal_acad_year)
            for e in examid:
                etype.append(Exam_Details.objects.get(exam_details_id=e).exam_type)
            

            st_details = zip(st_name,st_sem,st_year,st_sub,etype,st_dept,SearchParm)
            if not SearchParm.exists():
                messages.error(request,"Student Details Not Found")
                return render(request,"Edit_MpcReport.html",{'prv':prv,'username':username,'department':department,'students':st_details})

            return render(request,"Edit_MpcReport.html",{'prv':prv,'username':username,'department':department,'students':st_details})

        # Search parameter is by Semester
        if Sem != "0":
            amid = Academics_Master_Details.objects.filter(semester=Sem).values_list('academics_master_details_id',flat=True)
            htids = Exam_HallTicket_Details.objects.filter(academics_master_details_id__in=amid)
            seeids = Exam_Attendance.objects.filter(ht_details_id__in=htids)
            SearchParm = MPC_Report.objects.filter(see_att_id__in=seeids).values_list('mpc_report_id',flat=True)
            if not SearchParm.exists():
                messages.error(request,"Student Details Not Found")
                return render(request,"Edit_MpcReport.html",{'prv':prv,'username':username,'department':department})

            st_name = []
            name=[]
            year=[]
            st_dept = []
            st_sem = []
            st_year = []
            st_sub = []
            etype = []

            mpc_seeid = MPC_Report.objects.filter(mpc_report_id__in=SearchParm).values_list('see_att_id',flat=True)
            see_htid = Exam_Attendance.objects.filter(see_att_id__in=mpc_seeid).values_list('ht_details_id',flat=True)
            hall_amid = Exam_HallTicket_Details.objects.filter(ht_details_id__in=see_htid).values_list('academics_master_details_id',flat=True)
            hall_hallid = Exam_HallTicket_Details.objects.filter(ht_details_id__in=see_htid).values_list('hall_ticket_id',flat=True)
            examid = Exam_HallTicket.objects.filter(hall_ticket_id__in=hall_hallid).values_list('exam_id',flat=True)

            for a in hall_amid:
                st_dept.append(Academics_Master_Details.objects.get(academics_master_details_id=a).st_branch)
                st_sem.append(Academics_Master_Details.objects.get(academics_master_details_id=a).semester)
                name.append(Academics_Master_Details.objects.get(academics_master_details_id=a).st_uid.st_uid)
                year.append(Academics_Master_Details.objects.get(academics_master_details_id=a).acad_cal_id.acad_cal_id)
                st_sub.append(Academics_Master_Details.objects.get(academics_master_details_id=a).scheme_details_id.course_title)
            for n in name:
                st_name.append(Student_Details.objects.get(st_uid=n).st_name)
            for a in year:
                st_year.append(Academic_Calendar.objects.get(acad_cal_id=a).acad_cal_acad_year)
            for e in examid:
                etype.append(Exam_Details.objects.get(exam_details_id=e).exam_type)
            
    
            st_details = zip(st_name,st_sem,st_year,st_sub,etype,st_dept,SearchParm)
            return render(request,"Edit_MpcReport.html",{'prv':prv,'username':username,'department':department,'students':st_details})

        # Search parameter is by Exam type
        if Exam_type != "0":
            examid = Exam_Details.objects.filter(exam_type=Exam_type)
            hallid = Exam_HallTicket.objects.filter(exam_id__in=examid).values_list('hall_ticket_id',flat=True)
            htid = Exam_HallTicket_Details.objects.filter(hall_ticket_id__in=hallid).values_list('ht_details_id',flat=True)
            seeid = Exam_Attendance.objects.filter(ht_details_id__in=htid).values_list('see_att_id',flat=True)
            SearchParm = MPC_Report.objects.filter(see_att_id__in=seeid).values_list('mpc_report_id',flat=True)
            
            if not SearchParm.exists():
                messages.error(request,"Student Details Not Found")
                return render(request,"Edit_MpcReport.html",{'prv':prv,'username':username,'department':department})
            st_name = []
            name=[]
            year=[]
            st_dept = []
            st_sem = []
            st_year = []
            st_sub = []
            etype = []

            mpc_seeid = MPC_Report.objects.filter(mpc_report_id__in=SearchParm).values_list('see_att_id',flat=True)
            see_htid = Exam_Attendance.objects.filter(see_att_id__in=mpc_seeid).values_list('ht_details_id',flat=True)
            hall_amid = Exam_HallTicket_Details.objects.filter(ht_details_id__in=see_htid).values_list('academics_master_details_id',flat=True)
            hall_hallid = Exam_HallTicket_Details.objects.filter(ht_details_id__in=see_htid).values_list('hall_ticket_id',flat=True)
            examid = Exam_HallTicket.objects.filter(hall_ticket_id__in=hall_hallid).values_list('exam_id',flat=True)

            for a in hall_amid:
                st_dept.append(Academics_Master_Details.objects.get(academics_master_details_id=a).st_branch)
                st_sem.append(Academics_Master_Details.objects.get(academics_master_details_id=a).semester)
                name.append(Academics_Master_Details.objects.get(academics_master_details_id=a).st_uid.st_uid)
                year.append(Academics_Master_Details.objects.get(academics_master_details_id=a).acad_cal_id.acad_cal_id)
                st_sub.append(Academics_Master_Details.objects.get(academics_master_details_id=a).scheme_details_id.course_title)
            for n in name:
                st_name.append(Student_Details.objects.get(st_uid=n).st_name)
            for a in year:
                st_year.append(Academic_Calendar.objects.get(acad_cal_id=a).acad_cal_acad_year)
            for e in examid:
                etype.append(Exam_Details.objects.get(exam_details_id=e).exam_type)
            

            st_details = zip(st_name,st_sem,st_year,st_sub,etype,st_dept,SearchParm)
            return render(request,"Edit_MpcReport.html",{'prv':prv,'username':username,'department':department,'students':st_details})

        # Search parameter is by Exam type
        if Uid != "":
            amid = Academics_Master_Details.objects.filter(st_uid=Uid).values_list('academics_master_details_id',flat=True)
            htids = Exam_HallTicket_Details.objects.filter(academics_master_details_id__in=amid)
            seeids = Exam_Attendance.objects.filter(ht_details_id__in=htids)
            SearchParm = MPC_Report.objects.filter(see_att_id__in=seeids).values_list('mpc_report_id',flat=True)
            
            if not SearchParm.exists():
                messages.error(request,"Student Details Not Found")
                return render(request,"Edit_MpcReport.html",{'prv':prv,'username':username,'department':department})

            st_name = []
            name=[]
            year=[]
            st_dept = []
            st_sem = []
            st_year = []
            st_sub = []
            etype = []

            mpc_seeid = MPC_Report.objects.filter(mpc_report_id__in=SearchParm).values_list('see_att_id',flat=True)
            see_htid = Exam_Attendance.objects.filter(see_att_id__in=mpc_seeid).values_list('ht_details_id',flat=True)
            hall_amid = Exam_HallTicket_Details.objects.filter(ht_details_id__in=see_htid).values_list('academics_master_details_id',flat=True)
            hall_hallid = Exam_HallTicket_Details.objects.filter(ht_details_id__in=see_htid).values_list('hall_ticket_id',flat=True)
            examid = Exam_HallTicket.objects.filter(hall_ticket_id__in=hall_hallid).values_list('exam_id',flat=True)

            for a in hall_amid:
                st_dept.append(Academics_Master_Details.objects.get(academics_master_details_id=a).st_branch)
                st_sem.append(Academics_Master_Details.objects.get(academics_master_details_id=a).semester)
                name.append(Academics_Master_Details.objects.get(academics_master_details_id=a).st_uid.st_uid)
                year.append(Academics_Master_Details.objects.get(academics_master_details_id=a).acad_cal_id.acad_cal_id)
                st_sub.append(Academics_Master_Details.objects.get(academics_master_details_id=a).scheme_details_id.course_title)
            for n in name:
                st_name.append(Student_Details.objects.get(st_uid=n).st_name)
            for a in year:
                st_year.append(Academic_Calendar.objects.get(acad_cal_id=a).acad_cal_acad_year)
            for e in examid:
                etype.append(Exam_Details.objects.get(exam_details_id=e).exam_type)
            
    
            st_details = zip(st_name,st_sem,st_year,st_sub,etype,st_dept,SearchParm)
            return render(request,"Edit_MpcReport.html",{'prv':prv,'username':username,'department':department,'students':st_details})

        # Search parameter is by Exam type
        if Course_code != "":
            schmid = Scheme_Details.objects.get(course_code=Course_code)
            amid = Academics_Master_Details.objects.filter(scheme_details_id=schmid).values_list('academics_master_details_id',flat=True)
            htids = Exam_HallTicket_Details.objects.filter(academics_master_details_id__in=amid)
            seeids = Exam_Attendance.objects.filter(ht_details_id__in=htids)
            SearchParm = MPC_Report.objects.filter(see_att_id__in=seeids).values_list('mpc_report_id',flat=True)
            
            if not SearchParm.exists():
                messages.error(request,"Student Details Not Found")
                return render(request,"Edit_MpcReport.html",{'prv':prv,'username':username,'department':department})

            st_name = []
            name=[]
            year=[]
            st_dept = []
            st_sem = []
            st_year = []
            st_sub = []
            etype = []

            mpc_seeid = MPC_Report.objects.filter(mpc_report_id__in=SearchParm).values_list('see_att_id',flat=True)
            see_htid = Exam_Attendance.objects.filter(see_att_id__in=mpc_seeid).values_list('ht_details_id',flat=True)
            hall_amid = Exam_HallTicket_Details.objects.filter(ht_details_id__in=see_htid).values_list('academics_master_details_id',flat=True)
            hall_hallid = Exam_HallTicket_Details.objects.filter(ht_details_id__in=see_htid).values_list('hall_ticket_id',flat=True)
            examid = Exam_HallTicket.objects.filter(hall_ticket_id__in=hall_hallid).values_list('exam_id',flat=True)

            for a in hall_amid:
                st_dept.append(Academics_Master_Details.objects.get(academics_master_details_id=a).st_branch)
                st_sem.append(Academics_Master_Details.objects.get(academics_master_details_id=a).semester)
                name.append(Academics_Master_Details.objects.get(academics_master_details_id=a).st_uid.st_uid)
                year.append(Academics_Master_Details.objects.get(academics_master_details_id=a).acad_cal_id.acad_cal_id)
                st_sub.append(Academics_Master_Details.objects.get(academics_master_details_id=a).scheme_details_id.course_title)
            for n in name:
                st_name.append(Student_Details.objects.get(st_uid=n).st_name)
            for a in year:
                st_year.append(Academic_Calendar.objects.get(acad_cal_id=a).acad_cal_acad_year)
            for e in examid:
                etype.append(Exam_Details.objects.get(exam_details_id=e).exam_type)
    
    
            st_details = zip(st_name,st_sem,st_year,st_sub,etype,st_dept,SearchParm)
            return render(request,"Edit_MpcReport.html",{'prv':prv,'username':username,'department':department,'students':st_details})

        else:
            messages.error(request, "Please Enter Atleast One Field to Search")
            return render(request,"Edit_MpcReport.html",{'prv':prv,'username':username,'department':department})
       
    else:
        return render(request,"Edit_MpcReport.html",{'prv':prv,'username':username,'department':department})


def MakeUpExamRegistration(request):
    username=CustomUser.objects.get(id=request.user.id)
    examid = Exam_Details.objects.all().values_list('exam_details_id',flat=True)
    exam_list = []
    for e in examid:
        exam_type = Exam_Details.objects.get(exam_details_id=e).exam_type
        if exam_type == 2:
            exam_list.append(Exam_Details.objects.get(exam_details_id=e))
    print("jj")
    return render(request,"MakeupExamRegistration.html",{'username':username,'department':Department.objects.all(),'exam_list':exam_list})

def backLogExamRegistration(request):
    username=CustomUser.objects.get(id=request.user.id)
    examid = Exam_Details.objects.all().values_list('exam_details_id',flat=True)
    exam_list = []
    for e in examid:
        exam_type = Exam_Details.objects.get(exam_details_id=e).exam_type
        if exam_type == 2:
            exam_list.append(Exam_Details.objects.get(exam_details_id=e))
    print("888")
    return render(request,"BacklogRegistration.html",{'username':username,'department':Department.objects.all(),'exam_list':exam_list})
def addMakeupExam(request):
    username=CustomUser.objects.get(id=request.user.id)
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        examid = Exam_Details.objects.all().values_list('exam_details_id',flat=True)
        exam_list = []
        for e in examid:
            exam_type = Exam_Details.objects.get(exam_details_id=e).exam_type
            if exam_type == 2:
                exam_list.append(Exam_Details.objects.get(exam_details_id=e))

        exam_id = None
        branch = None
        stuid = None
        subject = None
        exempted = None
        reason = None

        try:
            exam_id = request.POST.get('exam_descr')
            acad_year = Exam_Details.objects.get(exam_details_id=exam_id).acad_cal_id
            branch = request.POST.get('offered_by')
            stuid = request.POST.get('st_uid')
            print(stuid)
            subject = request.POST.get('course_code')
            print(subject)
            exempted = request.POST.get('is_exempted')
            reason = request.POST.get('reason')
  
        except Exception as e:
            print(e)
        try:
            schmid = Scheme_Details.objects.get(course_code=subject)
        except Scheme_Details.DoesNotExist:
            messages.error(request,"Invalid Information. Enter correct data")
            return render(request,"MakeupExamRegistration.html",{'username':username,'department':Department.objects.all(),'exam_list':exam_list})
        try:
            btn_value = request.POST["btn_makeup"]
            if btn_value == "register":
                makeup_reg_obj = Makeup_Exam_Registration.objects.create(acad_cal_id=acad_year,branch=Department.objects.get(dept_id=branch),st_uid=Student_Details.objects.get(st_uid=stuid),scheme_details_id=schmid,exemption_from_grade_reduction=exempted,reason_for_application=reason,exam_id=Exam_Details.objects.get(exam_details_id=exam_id))
                makeup_reg_obj.save()
                messages.success(request,"Success! Student "+stuid+" has registered for "+subject) 
        
            if btn_value == "update":
                makeup_id = request.POST.get('makeup_exam_reg_id')
                makeup_obj = Makeup_Exam_Registration.objects.get(makeup_exam_reg_id=makeup_id)
                makeup_obj.acad_cal_id = acad_year
                makeup_obj.branch = Department.objects.get(dept_id=branch)
                makeup_obj.st_uid = Student_Details.objects.get(st_uid=stuid)
                makeup_obj.scheme_details_id = schmid
                makeup_obj.exemption_from_grade_reduction = exempted
                makeup_obj.reason_for_application = reason
                makeup_obj.exam_id = Exam_Details.objects.get(exam_details_id=exam_id)
                makeup_obj.save()
                messages.success(request,"Success! Updated Successfully")
        except IntegrityError:
            messages.warning(request,"Student "+stuid+" has already registered for - "+subject)   
        except Exception as e:
            print(e)
        username=CustomUser.objects.get(id=request.user.id)
        return render(request,"MakeupExamRegistration.html",{'username':username,'department':Department.objects.all(),'exam_list':exam_list})


def loadStudentRegisteredSubjects(request):
    dept_id = request.GET.get('offered_by')
    stuid = request.GET.get('st_uid')
    st_id = Student_Details.objects.get(st_uid=stuid)
    print("st id")
    print(st_id)
    exam_id = request.GET.get('exam_descr')
    sem = Exam_Details.objects.get(exam_details_id=exam_id).semester
    acad_yr = Exam_Details.objects.get(exam_details_id=exam_id).acad_year
    if 'regular' in exam_id.lower():
        acad_cal_type = 1
    elif 'stc' in exam_id.lower():
        acad_cal_type = 2
    print(acad_cal_type,"pp")
    acadcal_id = Academic_Calendar.objects.get(acad_cal_acad_year=acadyear,acad_cal_sem=sem,acad_cal_type=acad_cal_type)

    courselist = None
    try:
        schmid = Exam_Results.objects.filter(acad_cal_id=acad_cal_id,semester=sem,st_id=st_id,st_branch=Department.objects.get(dept_id=dept_id).dept_id,exam_new_grade="F").values_list('scheme_details_id',flat=True)
        print(schmid)
    except Exam_Results.DoesNotExist:
        return render(request, "see_subjects_dropdown.html", {'courselist': courselist})
        # return JsonResponse({"error":"Err : Scheme not allotted"},status=500)
    try:
        courselist = Scheme_Details.objects.filter(scheme_details_id__in=schmid).order_by('course_code')
        print(courselist)
    except Scheme_Details.DoesNotExist:
        return render(request, "see_subjects_dropdown.html", {'courselist': courselist})
        # return JsonResponse({"error":"Err : No Subjects found"},status=500)
    return render(request, "see_subjects_dropdown.html", {'courselist': courselist})
    

def view_makeup_register(request):
    username=CustomUser.objects.get(id=request.user.id)
    examid = Exam_Details.objects.all().values_list('exam_details_id',flat=True)
    exam_list = []
    for e in examid:
        exam_type = Exam_Details.objects.get(exam_details_id=e).exam_type
        if exam_type == 2:
            exam_list.append(Exam_Details.objects.get(exam_details_id=e))
    return render(request,"Edit_MakeupExam.html",{'prv':prv,'username':username,'department':Department.objects.all(),'exam_list':exam_list})

def SearchMakeupStudent(request):
    username=CustomUser.objects.get(id=request.user.id)
    examid = Exam_Details.objects.all().values_list('exam_details_id',flat=True)
    exam_list = []
    for e in examid:
        exam_type = Exam_Details.objects.get(exam_details_id=e).exam_type
        if exam_type == 2:
            exam_list.append(Exam_Details.objects.get(exam_details_id=e))
    
    if request.POST:
        exam_det_id = request.POST.get('exam_descr')
        uid = request.POST['st_uid']
        branch = request.POST['offered_by']

        if exam_det_id != None:
            SearchParam = Makeup_Exam_Registration.objects.filter(exam_id=exam_det_id).values_list('makeup_exam_reg_id',flat=True)
            dept = Makeup_Exam_Registration.objects.filter(exam_id=exam_det_id).values_list('branch',flat=True)
            sch_id = Makeup_Exam_Registration.objects.filter(exam_id=exam_det_id).values_list('scheme_details_id',flat=True)
            exam_ids = Makeup_Exam_Registration.objects.filter(exam_id=exam_det_id).values_list('exam_id',flat=True)
            st_uid = Makeup_Exam_Registration.objects.filter(exam_id=exam_det_id).values_list('st_uid',flat=True)
            
            st_details = student_info(exam_ids,dept,sch_id,st_uid,SearchParam)
            return render(request,"Edit_MakeupExam.html",{'prv':prv,'username':username,'department':Department.objects.all(),'exam_list':exam_list,'students':st_details})

        if branch != "0":
            SearchParam = Makeup_Exam_Registration.objects.filter(branch=branch).values_list('makeup_exam_reg_id',flat=True)
            exam_ids = Makeup_Exam_Registration.objects.filter(branch=branch).values_list('exam_id',flat=True)
            dept = Makeup_Exam_Registration.objects.filter(branch=branch).values_list('branch',flat=True)
            sch_id = Makeup_Exam_Registration.objects.filter(branch=branch).values_list('scheme_details_id',flat=True)
            st_uid = Makeup_Exam_Registration.objects.filter(branch=branch).values_list('st_uid',flat=True)
           
            st_details = student_info(exam_ids,dept,sch_id,st_uid,SearchParam)
            return render(request,"Edit_MakeupExam.html",{'prv':prv,'username':username,'department':Department.objects.all(),'exam_list':exam_list,'students':st_details})

        if uid != "":
            SearchParam = Makeup_Exam_Registration.objects.filter(st_uid=uid).values_list('makeup_exam_reg_id',flat=True)
            exam_ids = Makeup_Exam_Registration.objects.filter(st_uid=uid).values_list('exam_id',flat=True)
            dept = Makeup_Exam_Registration.objects.filter(st_uid=uid).values_list('branch',flat=True)
            sch_id = Makeup_Exam_Registration.objects.filter(st_uid=uid).values_list('scheme_details_id',flat=True)
            st_uid = Makeup_Exam_Registration.objects.filter(st_uid=uid).values_list('st_uid',flat=True)
            
            st_details = student_info(exam_ids,dept,sch_id,st_uid,SearchParam)
            return render(request,"Edit_MakeupExam.html",{'prv':prv,'username':username,'department':Department.objects.all(),'exam_list':exam_list,'students':st_details})

        else:
            messages.error(request, "Please Enter Atleast One Field to Search")
            return render(request,"Edit_MakeupExam.html",{'username':username,'department':Department.objects.all(),'exam_list':exam_list})    
    else:
        return render(request,"Edit_MakeupExam.html",{'username':username,'department':Department.objects.all(),'exam_list':exam_list})   

def student_info(exam_ids,dept,sch_id,st_uid,SearchParam) :
    st_name = []
    dept_list = []
    sem = []
    acad_yr = []
    subject_list = []

    for e in exam_ids:
        sem.append(Exam_Details.objects.get(exam_details_id=e).semester)
        acad_yr.append(Exam_Details.objects.get(exam_details_id=e).acad_year)
    
    for d in dept:
        dept_list.append(Department.objects.get(dept_id=d).dept_name)

    for s in sch_id:
        subject_list.append(Scheme_Details.objects.get(scheme_details_id=s).course_title)

    for s in st_uid:
        st_name.append(Student_Details.objects.get(st_uid=s).st_name)
    return zip(st_name,dept_list,sem,acad_yr,subject_list,SearchParam)

def EditMakeupExamRegister(request,makeup_exam_reg_id):
    username = CustomUser.objects.get(id=request.user.id)
    examid = Exam_Details.objects.all().values_list('exam_details_id',flat=True)
    exam_list = []
    for e in examid:
        exam_type = Exam_Details.objects.get(exam_details_id=e).exam_type
        if exam_type == 2:
            exam_list.append(Exam_Details.objects.get(exam_details_id=e))

    makeup_id = Makeup_Exam_Registration.objects.get(makeup_exam_reg_id=makeup_exam_reg_id) 
    exam_id = Makeup_Exam_Registration.objects.get(makeup_exam_reg_id=makeup_exam_reg_id).exam_id
    dept = Makeup_Exam_Registration.objects.get(makeup_exam_reg_id=makeup_exam_reg_id).branch
    stuid = Makeup_Exam_Registration.objects.get(makeup_exam_reg_id=makeup_exam_reg_id).st_uid
    schm_id = Makeup_Exam_Registration.objects.get(makeup_exam_reg_id=makeup_exam_reg_id).scheme_details_id
    exemption = Makeup_Exam_Registration.objects.get(makeup_exam_reg_id=makeup_exam_reg_id).exemption_from_grade_reduction
    reason = Makeup_Exam_Registration.objects.get(makeup_exam_reg_id=makeup_exam_reg_id).reason_for_application
    return render(request,"MakeupExamRegistration.html",{'username':username,'department':Department.objects.all(),'exam_list':exam_list,'makeup_obj':makeup_id,'exam_desc':exam_id,'branch':dept,'stuid':stuid,'coursecode':schm_id,'exemption':exemption,'reason':reason})
# def see_student_attendance(request):
#     if request.method!="POST":
#         userName=CustomUser.objects.get(id=request.user.id)
#         course_obj = Scheme_Details.objects.all()
#         exams =  Exam_Details.objects.all()
#         department = Department.objects.all()
#         return render(request,"see_attendance.html",{'username':userName,'course_obj':course_obj, 'department':department, 'exams': exams})
#     else:
#         userName=CustomUser.objects.get(id=request.user.id)
#         if request.POST:
#             exam_desc = request.POST['exam_desc']
#             scheme_details_id = request.POST['subject']
#             attend_date = None
#             dept_id = request.POST['dept']
#             sem = request.POST['sem']
#             course_code = Scheme_Details.objects.get(scheme_details_id=scheme_details_id).course_code
        

#             Exam_Details_obj = Exam_Details.objects.get(description = exam_desc,semester=sem)
#             print(Exam_Details_obj.acad_cal_id)
#             acad_cal_id = Exam_Details_obj.acad_cal_id
        
#             Exam_Details_obj_id = Exam_Details.objects.get(acad_cal_id =acad_cal_id,semester=sem,description=exam_desc).exam_details_id
#             print(Exam_Details_obj_id)
        
#             exam_date = SEE_timetable.objects.get(scheme_details_id=scheme_details_id,exam_id=Exam_Details_obj_id,acad_cal_id=acad_cal_id).exam_date
        
#             attend_date=exam_date
        
#             scheme_obj = Scheme_Details.objects.get(scheme_details_id = scheme_details_id)
#             print(scheme_obj,"scheme_obj")

#             Academics_Master_Details_obj = Academics_Master_Details.objects.filter(acad_cal_id = acad_cal_id,scheme_details_id = scheme_details_id,st_branch_applied_id = dept_id,semester =sem)
#             makeup_exam_registration = Makeup_Exam_Registration.objects.filter(
#                 acad_cal_id=acad_cal_id,
#                 branch=dept_id
#             ).values_list('st_uid', flat=True)

#             print(makeup_exam_registration)

            
#             ab = Academics_Master_Details.objects.filter(
#                 acad_cal_id=acad_cal_id,
#                 scheme_details_id=scheme_details_id,
#                 st_branch_applied_id=dept_id,
#                 st_uid__in=makeup_exam_registration
#             )
#             print(ab, "nnn")
#             for a in Academics_Master_Details_obj:
#                 print(a.academics_master_details_id)

#             print(len(Academics_Master_Details_obj))

#             #if len(Academics_Master_Details_obj) == 0:
#              #   messages.error(request, "Details Not Found")
#             #return render(request,"see_attendance.html",{'calender': Academic_Calendar.objects.all(),'scheme_detail':Scheme_Details.objects.all(),'department': Department.objects.all()})

#             print(Academics_Master_Details_obj)
#             hall_tickets = [] #list of hall ticket ID
#             students_uid = []
#             student_names = []
#             hall_ticket_details_id = [] #list of hall ticket Details ID

#             for master_id in ab:
#                 hallticket_details_obj = Exam_HallTicket_Details.objects.get(academics_master_details_id=master_id,hall_ticket_id_id=Exam_HallTicket.objects.get(hall_ticket_id = h_id,exam_id=Exam_Details_obj_id))
#                 hall_ticket_details_id.append(hallticket_details_obj.ht_details_id)

#                 hall_ticket_id = hallticket_details_obj.hall_ticket_id.hall_ticket_id
#                 print(hall_ticket_id)
#                 hall_tickets.append(hall_ticket_id)
        
#             for h_id in hall_tickets:
#                 print("##")
#                 print(h_id)
#                 SEE_Hallticket_obj = Exam_HallTicket.objects.get(hall_ticket_id = h_id,exam_id=Exam_Details_obj_id)
#                 st_uid = SEE_Hallticket_obj.st_uid
#                 print(st_uid)
#                 students_uid.append(st_uid)

#             for s_id in students_uid:
#                 Student_Details_obj = Student_Details.objects.get(st_uid = s_id.st_uid)
#                 st_name = Student_Details_obj.st_name
#                 print(st_name)
#                 student_names.append(st_name)


#             student_details_set = zip(students_uid,hall_tickets,student_names,hall_ticket_details_id)
#             btn_value = request.POST["btn_clicked"]
            
#             if btn_value == "register":  
                
#                 SEE_timetable_obj = SEE_timetable.objects.get(scheme_details_id=scheme_details_id,exam_id=Exam_Details_obj_id,acad_cal_id=acad_cal_id)
#                 attendance_check_flag = SEE_timetable_obj.attendance_flag
#                 if attendance_check_flag == 1:
#                     messages.warning(request,"You have already Submitted Attendance Successfully for "+course_code) 
#                     return render(request,"see_attendance.html",{'calender': Academic_Calendar.objects.all(),'scheme_detail':Scheme_Details.objects.all(),'department': Department.objects.all()})
#                 else:
#                     edit_flag = 0
#                     return render(request,"see_attendance_list.html",{'attend_date':attend_date,'scheme_detail':scheme_obj,'sem':sem,'acad_cal_id':acad_cal_id,'student_details_set':student_details_set,'exam_desc':exam_desc,'edit_flag':edit_flag})
            
#         else:
#             return render(request,"see_attendance.html",{'calender': Academic_Calendar.objects.all(),'scheme_detail':Scheme_Details.objects.all(),'department': Department.objects.all()})
def see_student_attendance(request):
    if request.method!="POST":
        userName=CustomUser.objects.get(id=request.user.id)
        course_obj = Scheme_Details.objects.all()
        exams =  Exam_Details.objects.all()
        department = Department.objects.all()
        return render(request,"see_attendance.html",{'username':userName,'course_obj':course_obj, 'department':department, 'exams': exams})
    else:
        userName=CustomUser.objects.get(id=request.user.id)
        if request.POST:
            exam_desc = request.POST['exam_desc']
            scheme_details_id = request.POST['subject']
            attend_date = None
            dept_id = request.POST['dept']
            sem = request.POST['sem']
            course_code = Scheme_Details.objects.get(scheme_details_id=scheme_details_id).course_code
        

            Exam_Details_obj = Exam_Details.objects.get(description = exam_desc,semester=sem)
            print(Exam_Details_obj.acad_cal_id)
            acad_cal_id = Exam_Details_obj.acad_cal_id
        
            Exam_Details_obj_id = Exam_Details.objects.get(acad_cal_id =acad_cal_id,semester=sem,description=exam_desc).exam_details_id
            print(Exam_Details_obj_id)
            print(scheme_details_id,Exam_Details_obj_id,acad_cal_id)
            exam_date = SEE_timetable.objects.get(scheme_details_id=scheme_details_id,exam_id=Exam_Details_obj_id,acad_cal_id=acad_cal_id).exam_date
        
            attend_date=exam_date
        
            scheme_obj = Scheme_Details.objects.get(scheme_details_id = scheme_details_id)

            Academics_Master_Details_obj = Academics_Master_Details.objects.filter(acad_cal_id = acad_cal_id,scheme_details_id = scheme_details_id,st_branch_applied_id = dept_id,semester =sem)
            
            for a in Academics_Master_Details_obj:
                print(a.academics_master_details_id)

            print(len(Academics_Master_Details_obj))

            #if len(Academics_Master_Details_obj) == 0:
             #   messages.error(request, "Details Not Found")
            #return render(request,"see_attendance.html",{'calender': Academic_Calendar.objects.all(),'scheme_detail':Scheme_Details.objects.all(),'department': Department.objects.all()})

            
            hall_tickets = [] #list of hall ticket ID
            students_uid = []
            student_names = []
            hall_ticket_details_id = [] #list of hall ticket Details ID
            print(Academics_Master_Details_obj)

            for master_id in Academics_Master_Details_obj:
                print("ppppppppppppp")
                print(master_id)
                Exam = Exam_Details.objects.get(acad_cal_id =acad_cal_id,semester=sem,description=exam_desc).exam_type

                if Exam == 2:
                    hallticket_details_obj = Exam_HallTicket_Details.objects.filter(academics_master_details_id=master_id).order_by('ht_details_id')[1]
                else:
                    if master_id :
                        hallticket_details_obj = Exam_HallTicket_Details.objects.get(academics_master_details_id=master_id)
                        print(hallticket_details_obj,"pp")
                    else:
                        master_id+1
                hall_ticket_details_id.append(hallticket_details_obj.ht_details_id)

                hall_ticket_id = hallticket_details_obj.hall_ticket_id.hall_ticket_id
                print(hall_ticket_id)
                hall_tickets.append(hall_ticket_id)
        
            for h_id in hall_tickets:
                print("##")
                print(h_id)
                SEE_Hallticket_obj = Exam_HallTicket.objects.get(hall_ticket_id = h_id,exam_id=Exam_Details_obj_id)
                st_uid = SEE_Hallticket_obj.st_uid
                print(st_uid)
                students_uid.append(st_uid)

            for s_id in students_uid:
                Student_Details_obj = Student_Details.objects.get(st_uid = s_id.st_uid)
                st_name = Student_Details_obj.st_name
                print(st_name)
                student_names.append(st_name)


            student_details_set = zip(students_uid,hall_tickets,student_names,hall_ticket_details_id)
            btn_value = request.POST["btn_clicked"]
            
            if btn_value == "register":  
                
                SEE_timetable_obj = SEE_timetable.objects.get(scheme_details_id=scheme_details_id,exam_id=Exam_Details_obj_id,acad_cal_id=acad_cal_id)
                attendance_check_flag = SEE_timetable_obj.attendance_flag
                if attendance_check_flag == 1:
                    messages.warning(request,"You have already Submitted Attendance Successfully for "+course_code) 
                    return render(request,"see_attendance.html",{'calender': Academic_Calendar.objects.all(),'scheme_detail':Scheme_Details.objects.all(),'department': Department.objects.all()})
                else:
                    edit_flag = 0
                    return render(request,"see_attendance_list.html",{'attend_date':attend_date,'scheme_detail':scheme_obj,'sem':sem,'acad_cal_id':acad_cal_id,'student_details_set':student_details_set,'exam_desc':exam_desc,'edit_flag':edit_flag})
            
        else:
            return render(request,"see_attendance.html",{'calender': Academic_Calendar.objects.all(),'scheme_detail':Scheme_Details.objects.all(),'department': Department.objects.all()})

def see_student_attendance_list(request,attend_date,course_code,acad_cal_id,exam_desc):
    userName=CustomUser.objects.get(id=request.user.id)
    if request.POST:
        attend_date = attend_date
        course_code = course_code
        acad_cal_id = acad_cal_id
        exam_desc=exam_desc
        st_list = request.POST.getlist("checked_allot")   
        
        
        scheme_detail_obj = Scheme_Details.objects.get(course_code = course_code)

        scheme_details_id = scheme_detail_obj.scheme_details_id
        branch = scheme_detail_obj.offered_by

        sem = scheme_detail_obj.sem_allotted

      
        exam_id = Exam_Details.objects.get(description=exam_desc,acad_cal_id=acad_cal_id,semester=sem).exam_details_id
        

        hall_tickets_details_id = []
        students_uid = []
     
        Academics_Master_Details_obj = Academics_Master_Details.objects.filter(acad_cal_id = acad_cal_id,scheme_details_id = scheme_details_id,st_branch_applied_id = branch,semester =sem)

        for master_id in Academics_Master_Details_obj:
            Exam = Exam_Details.objects.get(acad_cal_id =acad_cal_id,semester=sem,description=exam_desc).exam_type

            if Exam == 2:
                hallticket_details_obj = Exam_HallTicket_Details.objects.filter(academics_master_details_id=master_id).order_by('ht_details_id')[1]
            else:
                hallticket_details_obj = Exam_HallTicket_Details.objects.get(academics_master_details_id=master_id)
            hall_tickets_details_id.append(hallticket_details_obj.ht_details_id)
            # print(ht_details_id)
            # hall_tickets_details_id.append(ht_details_id)


        flag = 0
        absentee_count = 0

        
        for ht_det_id in hall_tickets_details_id:
            flag = 0
            for st in st_list:
                st = int(st)
                if st == ht_det_id:
                    flag = 1
                    break
            if flag == 1:
                #continue
                see_attendance_obj = Exam_Attendance.objects.get(ht_details_id=ht_det_id)
                see_attendance_obj.attendance_Status = 'P'
                see_attendance_obj.save()
            else:
                absentee_count = absentee_count + 1
                see_attendance_obj = Exam_Attendance.objects.get(ht_details_id=ht_det_id)
                see_attendance_obj.attendance_Status = 'A'
                see_attendance_obj.save()

        SEE_timetable_obj = SEE_timetable.objects.get(scheme_details_id=scheme_details_id,exam_id=exam_id,acad_cal_id=acad_cal_id)
        SEE_timetable_obj.attendance_flag = 1
        SEE_timetable_obj.absentees_count = absentee_count
        SEE_timetable_obj.save()

        btn_value = request.POST["btn_see_val"] 
        if btn_value == "register": 
             messages.success(request,"Attendance Submitted Successfully for "+course_code) 
        else:
            messages.success(request,"Attendance Updated Successfully for "+course_code)
       
        return render(request,"see_attendance.html",{'calender': Academic_Calendar.objects.all(),'scheme_detail':Scheme_Details.objects.all(),'department': Department.objects.all()})
            
    else:
        return render(request,"see_attendance.html",{'calender': Academic_Calendar.objects.all(),'scheme_detail':Scheme_Details.objects.all(),'department': Department.objects.all()})

def edit_see_student_attendance(request):
    userName=CustomUser.objects.get(id=request.user.id)
    if request.POST:
        exam_desc = request.POST['exam_desc']
        scheme_details_id = request.POST['subject']
        attend_date = None
        dept_id = request.POST['dept']
        sem = request.POST['sem']

        course_code = Scheme_Details.objects.get(scheme_details_id=scheme_details_id).course_code
       

        Exam_Details_obj = Exam_Details.objects.get(description = exam_desc,semester=sem)
        print(Exam_Details_obj.acad_cal_id)
        acad_cal_id = Exam_Details_obj.acad_cal_id
       
        Exam_Details_obj_id = Exam_Details.objects.get(acad_cal_id =acad_cal_id,semester=sem,description=exam_desc).exam_details_id
       
        exam_date = SEE_timetable.objects.get(scheme_details_id=scheme_details_id,exam_id=Exam_Details_obj_id,acad_cal_id=acad_cal_id).exam_date
        print(exam_date)
        
        attend_date=exam_date
       
       
        scheme_obj = Scheme_Details.objects.get(scheme_details_id = scheme_details_id)

        Academics_Master_Details_obj = Academics_Master_Details.objects.filter(acad_cal_id = acad_cal_id,scheme_details_id = scheme_details_id,st_branch_applied_id = dept_id,semester =sem)
        
        for a in Academics_Master_Details_obj:
            print(a.academics_master_details_id)
            print("***************")
        print(len(Academics_Master_Details_obj))

        if len(Academics_Master_Details_obj) == 0:
          messages.error(request, "Details Not Found")
          return render(request,"see_attendance.html",{'calender': Academic_Calendar.objects.all(),'scheme_detail':Scheme_Details.objects.all(),'department': Department.objects.all()})

      
       
        hall_tickets = []
        students_uid = []
        student_names = []
        hall_ticket_details_id = []
        attendance_old_list = []

        for master_id in Academics_Master_Details_obj:
            Exam = Exam_Details.objects.get(acad_cal_id =acad_cal_id,semester=sem,description=exam_desc).exam_type

            if Exam == 2:
                hallticket_details_obj = Exam_HallTicket_Details.objects.filter(academics_master_details_id=master_id).order_by('ht_details_id')[1]
            else:
                hallticket_details_obj = Exam_HallTicket_Details.objects.get(academics_master_details_id=master_id)
            hall_ticket_details_id.append(hallticket_details_obj.ht_details_id)

            hall_ticket_id = hallticket_details_obj.hall_ticket_id.hall_ticket_id
           
            hall_tickets.append(hall_ticket_id)
      
        for h_id in hall_tickets:
            print("##")
            print(h_id)
            SEE_Hallticket_obj = Exam_HallTicket.objects.get(hall_ticket_id = h_id,exam_id=Exam_Details_obj_id)
            st_uid = SEE_Hallticket_obj.st_uid
            print(st_uid)
            students_uid.append(st_uid)

        
        for s_id in students_uid:
            Student_Details_obj = Student_Details.objects.get(st_uid = s_id.st_uid)
            st_name = Student_Details_obj.st_name
            print(st_name)
            student_names.append(st_name)

        
        for ht_det_id in hall_ticket_details_id:
            print(ht_det_id,"ht_det_id")
            SEE_attendance_obj = Exam_Attendance.objects.get(ht_details_id=ht_det_id)
            attendance_old_list.append(SEE_attendance_obj.attendance_Status)
        
       

        edit_flag = 1
        student_details_set = zip(students_uid,hall_tickets,student_names,hall_ticket_details_id,attendance_old_list)
        
        SEE_timetable_obj = SEE_timetable.objects.get(scheme_details_id=scheme_details_id,exam_id=Exam_Details_obj_id,acad_cal_id=acad_cal_id)
        absentee_count = SEE_timetable_obj.absentees_count

       
        attendance_check_flag = SEE_timetable_obj.attendance_flag
        if attendance_check_flag == 0:
                messages.warning(request,"You have not yet took the Attendance for "+course_code) 
                return render(request,"edit_see_attendance.html",{'calender': Academic_Calendar.objects.all(),'scheme_detail':Scheme_Details.objects.all(),'department': Department.objects.all()})
        else:
            return render(request,"see_attendance_list.html",{'attend_date':attend_date,'scheme_detail':scheme_obj,'sem':sem,'acad_cal_id':acad_cal_id,'student_details_set':student_details_set,'exam_desc':exam_desc,'edit_flag':edit_flag,'absentee_count':absentee_count})

    else:
        return render(request,"edit_see_attendance.html",{'exams':Exam_Details.objects.all(),'calender': Academic_Calendar.objects.all(),'scheme_detail':Scheme_Details.objects.all(),'department': Department.objects.all()})

def temporary_hallticket_details(request):
    userName=CustomUser.objects.get(id=request.user.id)
    if request.POST:
        master_detail_id = request.POST['master_detail_id'] 
        hall_ticket_id = request.POST['hallticket_id'] 

        print(master_detail_id)
        print(hall_ticket_id)


        hallticket_details_obj= Exam_HallTicket_Details.objects.create(hall_ticket_id = Exam_HallTicket.objects.get(hall_ticket_id = hall_ticket_id),academics_master_details_id = Academics_Master_Details.objects.get(academics_master_details_id=master_detail_id))
        hallticket_details_obj.save()

        #=======creation of SEE attendance Table==========
        hallticket_details_obj_id = Exam_HallTicket_Details.objects.get(hall_ticket_id=hall_ticket_id,academics_master_details_id=master_detail_id).ht_details_id


        academic_master_detail_obj = Academics_Master_Details.objects.get(academics_master_details_id=master_detail_id)
        st_uid = academic_master_detail_obj.st_uid.st_uid

        see_attendance_obj = Exam_Attendance.objects.create(ht_details_id=Exam_HallTicket_Details.objects.get(ht_details_id=hallticket_details_obj_id),st_uid=Student_Details.objects.get(st_uid=st_uid),attendance_Status='P')
        see_attendance_obj.save()
        

        messages.success(request,"Success") 
        return render(request,"temporary_hallticket_details.html",{'calender': Academic_Calendar.objects.all(),'scheme_detail':Scheme_Details.objects.all(),'department': Department.objects.all()})
    else:
        return render(request,"temporary_hallticket_details.html",{'calender': Academic_Calendar.objects.all(),'scheme_detail':Scheme_Details.objects.all(),'department': Department.objects.all()})

def exam_qp(request):
    if request.method!="POST":
        userName=CustomUser.objects.get(id=request.user.id)
        # course_obj = Scheme_Details.objects.all()
        exams =  Exam_Details.objects.all()
        departments = Department.objects.all()
        return render(request,"exam_qp.html",{'username':userName,'departments':departments, 'exams': exams})
    else:
        userName=CustomUser.objects.get(id=request.user.id)
        btn_clicked = request.POST.get("btn_clicked")
        # acad_year = None
        # sem = None
        # acad_cal_id = None
        # exam_type = None
        exam_details_id = None
        if btn_clicked == "get_exam_details":
            print("oooooooooooooooo")
            exam_details_id = request.POST.get('exam_id')
            exam_desc = Exam_Details.objects.get(exam_details_id=exam_details_id).description
            series = None
            courselist = None
            print(exam_desc.lower())
            if '1st' in exam_desc.lower():
                print("0000")
                sem = 1
            if '2nd' in exam_desc.lower():
                print("00007")
                sem=2
            if '3rd' in exam_desc.lower():
                sem=3
            if '4th' in exam_desc.lower():
                sem=4
            if '5th' in exam_desc.lower():
                sem=5
            if '6th' in exam_desc.lower():
                sem=6
            if '7th' in exam_desc.lower():
                sem=7
            if '8th' in exam_desc.lower():
                sem=8
            department = request.POST.get("department")

            acad_cal_id = Exam_Details.objects.get(exam_details_id=exam_details_id).acad_cal_id
            
         
            
            series = Scheme_Allotment.objects.get(acad_cal_id=acad_cal_id,course_sem=sem).scheme_series
           
                # return JsonResponse({"error":"Err : Scheme not allotted"},status=500)
            
            course_obj = Scheme_Details.objects.filter(sem_allotted=sem, scheme_series=series, offered_by_id=department).order_by('course_code')
       


            # course_obj = Scheme_Details.objects.all()

            # acad_year = request.POST.get("acad_cal_acad_year")
            # sem = request.POST.get("acad_cal_sem")
            # exam_type = int(request.POST.get("exam_type"))
            # exam_type = int(request.POST.get("exam_type"))

            # exam_details_id = request.POST.get("exam_id")
            # department = request.POST.get("department")
            exam = None
            examList  = None
            
            department = Department.objects.get(dept_id=department)
            
            try:
                # if(exam_type==1 or exam_type==2): # Regular Semester
                #     acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year=acad_year,acad_cal_sem=sem)
                exam = Exam_Details.objects.get(exam_details_id= exam_details_id)
            except:
                messages.error(request,"No records for enetered details")
                return HttpResponseRedirect('exam_qp')
            try:
                examList = Exam_QP.objects.filter(exam_id = exam)
            except:
                messages.error(request,"Could not fetch exam qp list")
            print(course_obj,"course_objcourse_objcourse_obj")
            return render(request,"exam_qp.html",{'username':userName,'department':department, 'exam': exam, 'course_obj':course_obj, 'examList':examList})
        if btn_clicked == "add_course":
            course_obj = Scheme_Details.objects.all()
            course_name = request.POST.get("course_name")
            # course = course_name.split("-")
            # print(course[0].strip())
            # print(type(course[1].strip()))
            course_id = Scheme_Details.objects.get(course_code = course_name)
            exam_details_id = request.POST.get("exam_details_id")
            department = request.POST.get("department")
            exam = Exam_Details.objects.get(exam_details_id=exam_details_id)

            exam_desc = Exam_Details.objects.get(exam_details_id=exam_details_id).description
            acad_cal_id = Exam_Details.objects.get(exam_details_id=exam_details_id).acad_cal_id
            
            series = None
            courselist = None
            print(exam_desc.lower())
            if '1st' in exam_desc.lower():
                print("0000")
                sem = 1
            if '2nd' in exam_desc.lower():
                print("00007")
                sem=2
            if '3rd' in exam_desc.lower():
                sem=3
            if '4th' in exam_desc.lower():
                sem=4
            if '5th' in exam_desc.lower():
                sem=5
            if '6th' in exam_desc.lower():
                sem=6
            if '7th' in exam_desc.lower():
                sem=7
            if '8th' in exam_desc.lower():
                sem=8
            series = Scheme_Allotment.objects.get(acad_cal_id=acad_cal_id,course_sem=sem).scheme_series
            print(department,"ppppppp")
            department = Department.objects.get(dept_name=department)
            
            course_obj = Scheme_Details.objects.filter(sem_allotted=sem, scheme_series=series, offered_by_id=department).order_by('course_code')
            # print(course_name)
            # print(department)
            # print(str(course_id.scheme_details_id))
            try:
                Exam_QP.objects.create(exam_id=exam, course_code=course_id)
            except IntegrityError: 
                        messages.error(request, "Error! Duplicate entry not possible")
            messages.success(request, "Success! Course Added Sucessfully")
            # if(exam_type==1 or exam_type==2): # Regular Semester
            #     acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year=acad_year,acad_cal_sem=sem)
            # exam = Exam_Details.objects.get(acad_cal_id = acad_cal_id, exam_type = exam_type, semester=sem)
            try:
                examList = Exam_QP.objects.filter(exam_id = exam)
            except:
                pass
            print(examList)
            return render(request,"exam_qp.html",{'username':userName,'department':department, 'exam': exam, 'course_obj':course_obj, 'examList':examList})
            # return render(request,"exam_qp.html",{'username':userName,'department':department, 'exam': exam, 'course_obj':course_obj})

def add_exam_qp_pattern(request, id):
    userName=CustomUser.objects.get(id=request.user.id)
    print('id : '+str(id))
        # course_obj = Scheme_Details.objects.all()
    exam_qp = Exam_QP.objects.get(exam_qp_id=id)
    cos = Course_Outcome.objects.all()
    # scheme = Scheme_Details.objects.get(scheme_details_id=exam_qp.course_code_id)  # Replace with correct relationship
    # total_marks = scheme.max_see_marks  # Assuming Scheme_Details has a 'total_marks' field
    # print("//////////////////////////////////////////")
    # print(total_marks,"total_markstotal_markstotal_markstotal_markstotal_markstotal_markstotal_marks")
    #     # Set the question range based on total_marks
    # question_range = 10  # Default range
    # if total_marks == 50:
    #     question_range = 5  # Adjust the number of questions for 50 marks
    # # departments = Department.objects.all()
    return render(request,"exam_qp_pattern.html",{'username':userName,'cos':cos, 'exam_qp': exam_qp})

#not listed on urls.py - To be checked
def exam_qp_pattern(request):
    if request.method!="POST":
        userName=CustomUser.objects.get(id=request.user.id)
        # course_obj = Scheme_Details.objects.all()
        cos = Course_Outcome.objects.all()
        # departments = Department.objects.all()
        return render(request,"exam_qp_pattern.html",{'username':userName,'cos':cos})
    else:
        exam_qp_id = request.POST.get('exam_qp_id')
        exam_qp = Exam_QP.objects.get(exam_qp_id=exam_qp_id)

        print('exam_qp')
        print(exam_qp)

        # Getting how many course outcomes are there in the data_base
        no_of_cos = Course_Outcome.objects.all().count()
        # scheme = Scheme_Details.objects.get(scheme_details_id=exam_qp.course_code_id)  # Replace with correct relationship
        # total_marks = scheme.max_see_marks  # Assuming Scheme_Details has a 'total_marks' field
        # print("//////////////////////////////////////////")
        # print(total_marks,"total_markstotal_markstotal_markstotal_markstotal_markstotal_markstotal_marks")
        # # Set the question range based on total_marks
        # question_range = 10  # Default range
        # if total_marks == 50:
        #     question_range = 5  # Adjust the number of questions for 50 marks

        # with transaction.atomic():
        for i in range(1,int(10)+1):
            no_of_sub_questions = request.POST.get('q-'+str(i)+'-sub-q')
            print('no_of_sub_questions')
            print(no_of_sub_questions)
            max_marks = request.POST.get('q-'+str(i)+'-max-marks')
            print('max_marks')
            print(max_marks)
            for j in range(1, int(no_of_sub_questions)+1):
                subqmarks = request.POST.get('q-'+str(i)+'-sub-q-'+chr(97+j-1)+'-marks')
                
                print('subqmarks')
                print(subqmarks)

                co_list = []
                for k in range(1, int(no_of_cos)+1):
                    coi ='q-'+str(i)+'-sub-q-'+chr(97+j-1)+'-cos-input-'+str(k)
                    co = request.POST.get(coi)

                    if co is not None:
                        co_list.append(co)

                print('co_list')
                print(co_list)

                try:
                    # (1062, "Duplicate entry '1-1' for key 'academics_exam_qp_pattern.academics_exam_qp_pattern_qnum_exam_qp_id_id_f1a3d11d_uniq'")
                    # pass
                    exam_qp_pattern = Exam_QP_Pattern.objects.create(qnum=str(i), subqnum=chr(97+j-1), max_marks=subqmarks, exam_qp_id=exam_qp)
                    exam_qp_pattern.save()
                    exam_qp_pattern.co.set(Course_Outcome.objects.filter(co_num__in=co_list))
                except IntegrityError: 
                    messages.error(request, "Error! Duplicate entry not possible")

            print('----------------------------------------------------------------')
            print('')
            print('')
            print('')
                
        messages.success(request, "Success! Assessment Pattern Added Sucessfully")

        
        userName=CustomUser.objects.get(id=request.user.id)
        course_obj = Scheme_Details.objects.all()
        department = request.POST.get("department")
        exam = Exam_Details.objects.get(exam_details_id = exam_qp.exam_id.exam_details_id)
        examList = Exam_QP.objects.filter(exam_id = exam)
        return render(request,"exam_qp.html",{'username':userName,'department':department, 'exam': exam, 'course_obj':course_obj, 'examList':examList})

        cos = Course_Outcome.objects.all() # All Course_Outcome object for displaying in UI
        sd = Scheme_Details.objects.all()  # All Scheme_Details object for displaying in UI
        userName=CustomUser.objects.get(id=request.user.id)

        # exam_qp = Exam_QP.objects.get(exam_qp_id=exam_qp_id)
        # assessments = Declare_Assessment.objects.all().filter(acad_cal_id = assessment.acad_cal_id, scheme_details_id = assessment.scheme_details_id ,sem = assessment.sem)
        return render(request,"exam_qp_pattern.html",{'username':userName,'departments':departments})


def edit_exam_qp_pattern(request, id):
    if request.method!= "POST":
        cos = Course_Outcome.objects.all() # All Course_Outcome object for displaying in UI
        # assessment = Declare_Assessment.objects.get(declare_assessment_id=id)
        exam_qp = Exam_QP.objects.get(exam_qp_id=id)
        userName=CustomUser.objects.get(id=request.user.id)

        # details = dict()
        qlist = dict()
        # no_of_questions = assessment.questions.all().values('qnum').distinct().count()
        # no_of_questions_to_be_answered = assessment.ans_q

        # details['assessment'] = assessment
        # details['no_of_questions'] = no_of_questions
        # details['no_of_questions_to_be_answered'] = no_of_questions_to_be_answered

        for i in range(1, 11):

            # question = assessment.questions.get(qnum=i)
            qnum = dict()
            # qnum['compulsory'] = 
            # qnum['max_marks'] =  Exam_QP_Pattern.objects.get(qnum=i, exam_qp_id=exam_qp).max_marks

            # Exam_QP_Pattern.objects.get(qnum=i, exam_qp_id=exam_qp).count

            no_of_sub_questions =  Exam_QP_Pattern.objects.filter(qnum=i, exam_qp_id=exam_qp).count()
            sub_q_list = dict()
            qnum['no_of_sub_questions'] = no_of_sub_questions
            ##for unit
            if(i%2==0):
                qnum['unit'] = int(i/2)
            else:
                qnum['unit'] = int((i+1)/2)
            for j in range(1, int(no_of_sub_questions)+1):

                max_marks = Exam_QP_Pattern.objects.get(qnum=i, subqnum = chr(97+j-1) ,exam_qp_id=exam_qp).max_marks
                # max_marks = question.subquestion.get(subqnum=chr(97+j-1)).max_marks
                co = Exam_QP_Pattern.objects.get(qnum=i, subqnum = chr(97+j-1) ,exam_qp_id=exam_qp).co.all().values('co_num')
                sub_q = dict()

                sub_q['max_marks'] = max_marks
                sub_q['co'] = co
                sub_q_list[chr(97+j-1)] = sub_q
            qnum['sub_q_list'] = sub_q_list
            
            qlist[i] = qnum

        print(qlist)

        return render(request,"edit_exam_qp_pattern.html", {'username':userName,'cos':cos, 'qlist': qlist, 'exam_qp':exam_qp})
        # return render(request,"exam_qp_pattern.html",{'username':userName, 'cos': cos, 'assessment': assessment , 'details': details, 'qlist': qlist})
    else :
        exam_qp = Exam_QP.objects.get(exam_qp_id=id)
        with transaction.atomic():
            try:
                exam_qp.exam_QP_pattern.all().delete()
                print(exam_qp.exam_QP_pattern.all())
            except Exception as e:
                print(e)
                messages.error(request, "Error! Cannot delete the assessment")

            
            # exam_qp_id = request.POST.get('exam_qp_id')
            # exam_qp = Exam_QP.objects.get(exam_qp_id=exam_qp_id)

            # print('exam_qp')
            # print(exam_qp)

            # Getting how many course outcomes are there in the data_base
        no_of_cos = Course_Outcome.objects.all().count()

        for i in range(1,int(10)+1):
            no_of_sub_questions = request.POST.get('q-'+str(i)+'-sub-q')
            print('no_of_sub_questions')
            print(no_of_sub_questions)
            max_marks = request.POST.get('q-'+str(i)+'-max-marks')
            print('max_marks')
            print(max_marks)
            for j in range(1, int(no_of_sub_questions)+1):
                subqmarks = request.POST.get('q-'+str(i)+'-sub-q-'+chr(97+j-1)+'-marks')
                
                print('subqmarks')
                print(subqmarks)

                co_list = []
                for k in range(1, int(no_of_cos)+1):
                    coi ='q-'+str(i)+'-sub-q-'+chr(97+j-1)+'-cos-input-'+str(k)
                    co = request.POST.get(coi)

                    if co is not None:
                        co_list.append(co)

                print('co_list')
                print(co_list)

                try:
                    # pass
                    print(str(i)+"-"+str(j))
                    exam_qp_pattern = Exam_QP_Pattern.objects.create(qnum=str(i), subqnum=chr(97+j-1), max_marks=subqmarks, exam_qp_id=exam_qp)
                    print(exam_qp_pattern)
                    
                    exam_qp_pattern.save()
                    exam_qp_pattern.co.set(Course_Outcome.objects.filter(co_num__in=co_list))
                # except IntegrityError: 
                #     messages.error(request, "Error! Duplicate entry not possible")
                except IntegrityError: 
                    messages.error(request, "Error! Duplicate entry not possible")


            print('----------------------------------------------------------------')
            print('')
            print('')
            print('')
                
        messages.success(request, "Success! Assessment Pattern Added Sucessfully")

        userName=CustomUser.objects.get(id=request.user.id)
        course_obj = Scheme_Details.objects.all()
        department = request.POST.get("department")
        exam = Exam_Details.objects.get(exam_details_id = exam_qp.exam_id.exam_details_id)
        examList = Exam_QP.objects.filter(exam_id = exam)
        return render(request,"exam_qp.html",{'username':userName,'department':department, 'exam': exam, 'course_obj':course_obj, 'examList':examList})

# def external_exam_bitwise(request):
#     if request.method!="POST":
#         userName=CustomUser.objects.get(id=request.user.id)
#         departments = Department.objects.all()
#         course_obj = Scheme_Details.objects.all()
#         # exams  = Exam_Details.objects.order_by('-acad_year')[:2]
#         exams  = Exam_Details.objects.order_by('-acad_year')
#         return render(request,"external_exam_bitwise.html",{'username':userName,'departments':departments, 'course_obj':course_obj, 'exams':exams})
#     else:
#         userName=CustomUser.objects.get(id=request.user.id)
#         btn_clicked = request.POST.get("btn_clicked")
#         sem = None
#         acad_cal_id = None
#         exam_type = None
        
        
#         exam_id = request.POST.get("exam_id")
#         department = request.POST.get("department")
#         course_name = request.POST.get("course_name")
#         evaluation_type = request.POST.get("evaluation_type")
#         print(evaluation_type)
#         course = course_name.split("-")
#         exam = Exam_Details.objects.get(exam_details_id=exam_id)

#         course_list = Exam_QP.objects.filter(exam_id=exam)
#         branch = Department.objects.get(dept_id=department)
#         print("ppppp")
#         print(course_list)

#         try:
#             exam = Exam_Details.objects.get(exam_details_id=exam_id)
#         except:
#             messages.error(request,"No records for enetered details")
#             return HttpResponseRedirect('external_exam_bitwise')
#         try:
#             course_id = Scheme_Details.objects.get(course_title = course[0].strip(),course_code = course[1].strip())
#             exam_qp = Exam_QP.objects.get(course_code=course_id,exam_id=exam)
#             print("ppp")
#             print(exam_qp)
#         except:
#             messages.error(request,"No records for enetered details")
#             return HttpResponseRedirect('external_exam_bitwise')

#         if not exam_qp.exam_QP_pattern.all().exists():
#             messages.error(request,"QP pattern not found for the selected exam")
#             return HttpResponseRedirect('external_exam_bitwise')

#         units = dict()
#         qnum=1
        
#         for i in range(1,6):
#             que = dict()
#             ques = Exam_QP_Pattern.objects.filter(exam_qp_id=exam_qp).distinct()
#             for j in range(1,3):
#                 subques = Exam_QP_Pattern.objects.filter(exam_qp_id=exam_qp,qnum=j)
#                 que[qnum] = subques
#                 qnum += 1
            
#             units[i] = que
#         print("llll")
#         print(units)
#         if btn_clicked == "get_exam_details":    
#             return render(request,"external_exam_bitwise.html",{'username':userName,'units': units,'department':department, 'exam': exam,'course_name':course_name,'evaluation_type':evaluation_type})
#         with transaction.atomic():
#             if btn_clicked == "add_student_marks":
#                 code_no = request.POST.get("code-number")
#                 qnum = 1
#                 for i in range(1,6):
#                     for j in range(1,3):
#                         subques = Exam_QP_Pattern.objects.filter(exam_qp_id=exam_qp,qnum=qnum)
#                         for subque in subques:
#                             marks = request.POST.get("unit-"+str(i)+"-q-"+str(qnum)+"-subq-"+str(subque.subqnum)+"-marks")
#                             if marks is None or marks == "":
#                                 marks=0
#                             print(code_no,marks,subque,evaluation_type)
#                             addExamBitWiseMarks = Exam_Bitwise_Marks.objects.create(code_number=str(code_no),obtained_marks=marks,qp_pattern_id_id=subque.qp_pattern_id,valuation_type=evaluation_type)
#                             print(addExamBitWiseMarks)
#                             addExamBitWiseMarks.save()
#                         qnum += 1
#                 ##############################
                
#                 st_id = Bar_Code.objects.get(barcode=code_no).st_id
                            
#                 #total marks to be added to the qurery dynamically from the patern
#                 total_eval_marks = int(request.POST.get("total_eval_marks"))
#                 print(total_eval_marks)
#                 if int(evaluation_type) ==1 :
#                     if total_eval_marks < 38:
#                         seegrade = 'F'
#                         addSEETotalMarks = SEE_Total_Marks.objects.create(st_id = st_id, total_valuation_marks= total_eval_marks, grade_obtained = seegrade, valuation_type = evaluation_type, exam_qp_id=exam_qp)
#                         master_detail_id = Academics_Master_Details.objects.get(st_uid=st_id,acad_cal_id_id=exam.acad_cal_id,scheme_details_id=course_id,st_branch_applied_id=2)
#                         final_marks = (int(total_eval_marks/2)) +  master_detail_id.cie_marks
#                         grade = GradeMapping.objects.get(MinMarks__lte = total_eval_marks, MaxMarks__gte = total_eval_marks, TotalMarks = 100)   
#                         # exam_result = Exam_Results.objects.get(semester=exam.semester,acad_cal_id=exam.acad_cal_id,st_id=st_id,exam_type=1)
#                         Exam_Results.objects.create(semester=exam.semester,acad_cal_id=exam.acad_cal_id,st_id=st_id,exam_id=exam,st_branch_id=department,scheme_details_id=course_id,exam_type=evaluation_type,see_marks=total_eval_marks,final_marks=final_marks,exam_new_grade=seegrade,exam_gp_earned=grade.GradePoints,grade_mapping_id=grade,academics_master_details_id=master_detail_id)
#                         # Total gradepoint earned (20-06-2023)
#                         #total_gp_earned = (chal_exam_result.exam_gp_earned*Scheme_Details.objects.get(course_title = course[0].strip()).credits)
#                         #print(total_gp_earned)
#                         #Academics_student_current_status.filter(scheme_details_id = scheme_details_id,st_uid=student).update(cie_marks = cie_marks,cie_grade=grade)
#                     elif total_eval_marks==38:
#                         # Add 02 gracemarks - - - 2% of Max Marks in SEE
#                         total_eval_marks = 40
#                         seegrade = 'E'
#                         addSEETotalMarks = SEE_Total_Marks.objects.create(st_id = st_id, total_valuation_marks= total_eval_marks, grade_obtained = seegrade, valuation_type = evaluation_type, exam_qp_id=exam_qp)
#                         master_detail_id = Academics_Master_Details.objects.get(st_uid=st_id,acad_cal_id_id=exam.acad_cal_id,scheme_details_id=course_id,st_branch_applied_id=2)
#                         final_marks = (int(total_eval_marks/2)) +  master_detail_id.cie_marks
#                         grade = GradeMapping.objects.get(MinMarks__lte = final_marks, MaxMarks__gte = final_marks, TotalMarks = 100)   
#                         # exam_result = Exam_Results.objects.get(semester=exam.semester,acad_cal_id=exam.acad_cal_id,st_id=st_id,exam_type=1)
#                         Exam_Results.objects.create(semester=exam.semester,acad_cal_id=exam.acad_cal_id,st_id=st_id,exam_id=exam,st_branch_id=department,scheme_details_id=course_id,exam_type=evaluation_type,see_marks=total_eval_marks,final_marks=final_marks,exam_new_grade=grade.Grade,exam_gp_earned=grade.GradePoints,grade_mapping_id=grade,academics_master_details_id=master_detail_id)
#                         #total_gp_earned = (chal_exam_result.exam_gp_earned*Scheme_Details.objects.get(course_title = course[0].strip()).credits)
#                         #print(total_gp_earned)
#                     else:
#                         grade = GradeMapping.objects.get(MinMarks__lte = total_eval_marks, MaxMarks__gte = total_eval_marks, TotalMarks = 100)   
#                         addSEETotalMarks = SEE_Total_Marks.objects.create(st_id = st_id, total_valuation_marks= total_eval_marks, grade_obtained = grade, valuation_type = evaluation_type, exam_qp_id=exam_qp)
#                         print('hello')
#                         print(st_id,exam.acad_cal_id,course_id)
#                         print(Academics_Master_Details.objects.get(academics_master_details_id=26).st_uid)
#                         print(Academics_Master_Details.objects.get(academics_master_details_id=26).acad_cal_id_id)
#                         print(Academics_Master_Details.objects.get(academics_master_details_id=26).scheme_details_id)
#                         print(Academics_Master_Details.objects.get(academics_master_details_id=26).st_branch_applied_id)
#                         master_detail_id = Academics_Master_Details.objects.get(st_uid = st_id,acad_cal_id_id=exam.acad_cal_id,scheme_details_id=course_id,st_branch_applied_id=2)
#                         final_marks = (int(total_eval_marks/2)) +  master_detail_id.cie_marks
#                         grade = GradeMapping.objects.get(MinMarks__lte = final_marks, MaxMarks__gte = final_marks, TotalMarks = 100)   
#                         # exam_result = Exam_Results.objects.get(semester=exam.semester,acad_cal_id=exam.acad_cal_id,st_id=st_id,exam_type=1)
#                         Exam_Results.objects.create(semester=exam.semester,acad_cal_id=exam.acad_cal_id,st_id=st_id,exam_id=exam,st_branch_id=department,scheme_details_id=course_id,exam_type=evaluation_type,see_marks=total_eval_marks,final_marks=final_marks,exam_new_grade=grade.Grade,exam_gp_earned=grade.GradePoints,grade_mapping_id=grade,academics_master_details_id=master_detail_id)
#                         #total_gp_earned = (chal_exam_result.exam_gp_earned*Scheme_Details.objects.get(course_title = course[0].strip()).credits)
#                         #print(total_gp_earned)
    
#                 if int(evaluation_type) ==2 :
#                     grade = GradeMapping.objects.get(MinMarks__lte = total_eval_marks, MaxMarks__gte = total_eval_marks, TotalMarks = 100)   
#                     addSEETotalMarks = SEE_Total_Marks.objects.create(st_id = st_id, total_valuation_marks= total_eval_marks, grade_obtained = grade, valuation_type = evaluation_type, exam_qp_id=exam_qp)
#                     master_detail_id = Academics_Master_Details.objects.get(st_uid=st_id,acad_cal_id_id=exam.acad_cal_id,scheme_details_id=course_id,st_branch_applied_id=2)
#                     final_marks = (int(total_eval_marks/2)) +  master_detail_id.cie_marks
#                     grade = GradeMapping.objects.get(MinMarks__lte = final_marks, MaxMarks__gte = final_marks, TotalMarks = 100)
#                     rev_exam_result = Exam_Results.objects.get(semester=exam.semester,acad_cal_id=exam.acad_cal_id,st_id=st_id,exam_type=1)
#                     Exam_Results.objects.create(exam_old_grade=rev_exam_result.exam_new_grade,semester=exam.semester,acad_cal_id=exam.acad_cal_id,st_id=st_id,exam_id=exam,st_branch_id=department,scheme_details_id=course_id,exam_type=evaluation_type,see_marks=total_eval_marks,final_marks=final_marks,exam_new_grade=grade.Grade,exam_gp_earned=grade.GradePoints,grade_mapping_id=grade,academics_master_details_id=master_detail_id)
#                     total_gp_earned = (chal_exam_result.exam_gp_earned*Scheme_Details.objects.get(course_title = course[0].strip()).credits)
#                     print(total_gp_earned)
#                 elif int(evaluation_type) == 3:
#                     grade = GradeMapping.objects.get(MinMarks__lte = total_eval_marks, MaxMarks__gte = total_eval_marks, TotalMarks = 100)   
#                     addSEETotalMarks = SEE_Total_Marks.objects.create(st_id = st_id, total_valuation_marks= total_eval_marks, grade_obtained = grade, valuation_type = evaluation_type, exam_qp_id=exam_qp)
#                     master_detail_id = Academics_Master_Details.objects.get(st_uid=st_id,acad_cal_id_id=exam.acad_cal_id,scheme_details_id=course_id,st_branch_applied_id=2)
#                     final_marks = (int(total_eval_marks/2)) +  master_detail_id.cie_marks
#                     grade = GradeMapping.objects.get(MinMarks__lte = final_marks, MaxMarks__gte = final_marks, TotalMarks = 100)
#                     chal_exam_result = Exam_Results.objects.get(semester=exam.semester,acad_cal_id=exam.acad_cal_id,st_id=st_id,exam_type=1)
#                     Exam_Results.objects.create(exam_old_grade=chal_exam_result.exam_new_grade,semester=exam.semester,acad_cal_id=exam.acad_cal_id,st_id=st_id,exam_id=exam,st_branch_id=department,scheme_details_id=course_id,exam_type=evaluation_type,see_marks=total_eval_marks,final_marks=final_marks,exam_new_grade=grade.Grade,exam_gp_earned=grade.GradePoints,grade_mapping_id=grade,academics_master_details_id=master_detail_id)
#                    # Total gradepoint earned
#                     total_gp_earned = (chal_exam_result.exam_gp_earned*Scheme_Details.objects.get(course_title = course[0].strip()).credits)
#                     print(total_gp_earned)
#                     if chal_exam_result.exam_new_grade != 'F':
#                         if chal_exam_result.exam_old_grade != 'F':
#                             total_credits_earned = Scheme_Details.objects.get(course_title = course[0].strip()).credits
#                         else:
#                             total_credits_earned = 0
#                     print(total_credits_earned)
#                     Student_current_status.objects.filter(st_uid=master_detail_id.st_uid).update(total_credits_earned = total_credits_earned) 
#                 # else:
#                 #     Exam_Results.objects.create(semester=exam.semester,acad_cal_id=exam.acad_cal_id,st_id=st_id,exam_id=exam,st_branch_id=department,scheme_details_id=course_id,exam_type=evaluation_type,exam_marks=final_marks,exam_new_grade=grade.Grade,exam_gp_earned=grade.GradePoints,grade_mapping_id=grade,academics_master_details_id=master_detail_id)
                
#                 st_list = Exam_Results.objects.filter(exam_id = exam, exam_type = evaluation_type).values('st_id').distinct()

#                 students_list = Exam_HallTicket.objects.filter(exam_id = exam,st_uid_id__in=st_list)

#                 # for st in st_list:
#                 #     print(st['st_id'])
#                 #     students_list = Exam_HallTicket.objects.filter(exam_id = exam,st_uid_id=st['st_id'])

#                 #     print(students_list)

#                 student_results = dict()

#                 for student in students_list:

#                     course_grades = dict()
#                     total_credits = 0
#                     total_points = 0
#                     earned_crs = 0
#                     for course in course_list:
#                         st_grade = Exam_Results.objects.get(st_branch = branch, exam_id = exam, exam_type = evaluation_type,scheme_details_id = course.course_code, st_id = student.st_uid)
#                         print("sdfsbdfhbsd11")
#                         if st_grade.exam_new_grade != "F":
#                             print("sdfsbdfhbsd")
#                             earned_crs += int(st_grade.scheme_details_id.credits)
#                         total_credits += int(st_grade.scheme_details_id.credits)
#                         course_grades[course] = st_grade
#                         total_points += (int(st_grade.scheme_details_id.credits) * int(st_grade.exam_gp_earned))
#                     sgpa = (total_points/total_credits)

#                     Student_current_status.objects.filter(st_uid=master_detail_id.st_uid).update(sgpa = sgpa)
                    
#                 messages.success(request, "Success! Marks Added Sucessfully")
#                 return render(request,"external_exam_bitwise.html",{'username':userName,'units': units,'department':department, 'exam': exam,'course_name':course_name,'evaluation_type':evaluation_type})
#         return render(request,"external_exam_bitwise.html")
def external_exam_bitwise(request):
    if request.method != "POST":
        userName = CustomUser.objects.get(id=request.user.id)
        departments = Department.objects.all()
        course_obj = Scheme_Details.objects.all()
        exams = Exam_Details.objects.order_by('-acad_year')
        return render(request, "external_exam_bitwise.html", {'username': userName, 'departments': departments, 'course_obj': course_obj, 'exams': exams})
    else:
        userName = CustomUser.objects.get(id=request.user.id)
        btn_clicked = request.POST.get("btn_clicked")
        sem = None
        acad_cal_id = None
        exam_type = None
        
        exam_id = request.POST.get("exam_id")
        department = request.POST.get("department")
        course_name = request.POST.get("course_name")
        evaluation_type = request.POST.get("evaluation_type")
        
        
        exam = Exam_Details.objects.get(exam_details_id=exam_id)
        course_list = Exam_QP.objects.filter(exam_id=exam)
        branch = Department.objects.get(dept_id=department)

        try:
            exam = Exam_Details.objects.get(exam_details_id=exam_id)
            print(exam,"ooooooo")
        except:
            messages.error(request, "No records for entered details")
            return HttpResponseRedirect('external_exam_bitwise')
        
        try:
            print("llllllllll,course_id",course_name)
            course_id = Scheme_Details.objects.get(course_code=course_name)
            print(course_id,exam)
            exam_qp = Exam_QP.objects.get(course_code=course_id, exam_id=exam)
            print(exam_qp)
        except:
            messages.error(request, "No records for entered details")
            return HttpResponseRedirect('external_exam_bitwise')
        print(exam_qp.exam_QP_pattern.all().exists())
        if not exam_qp.exam_QP_pattern.all().exists():
            messages.error(request, "QP pattern not found for the selected exam")
            return HttpResponseRedirect('external_exam_bitwise')

        units = dict()
        qnum = 1
        
        for i in range(1, 6):
            que = dict()
            ques = Exam_QP_Pattern.objects.filter(exam_qp_id=exam_qp).distinct()
            for j in range(1, 3):
                subques = Exam_QP_Pattern.objects.filter(exam_qp_id=exam_qp, qnum=j)
                que[qnum] = subques
                qnum += 1
            
            units[i] = que

        if btn_clicked == "get_exam_details":    
            print("iiiiiiiiiii")
            return render(request, "external_exam_bitwise.html", {'username': userName, 'units': units, 'department': department, 'exam': exam, 'course_name': course_name, 'evaluation_type': evaluation_type})
        
        with transaction.atomic():
            if btn_clicked == "add_student_marks":
                code_no = request.POST.get("code-number")
                qnum = 1
                for i in range(1, 6):
                    for j in range(1, 3):
                        subques = Exam_QP_Pattern.objects.filter(exam_qp_id=exam_qp, qnum=qnum)
                        for subque in subques:
                            marks = request.POST.get("unit-" + str(i) + "-q-" + str(qnum) + "-subq-" + str(subque.subqnum) + "-marks")
                            if marks is None or marks == "":
                                marks = 0
                            addExamBitWiseMarks = Exam_Bitwise_Marks.objects.create(code_number=str(code_no), obtained_marks=marks, qp_pattern_id_id=subque.qp_pattern_id, valuation_type=evaluation_type)
                            addExamBitWiseMarks.save()
                        qnum += 1
                
                st_id = Bar_Code.objects.get(barcode=code_no).st_id
                total_eval_marks = int(request.POST.get("total_eval_marks"))
                print(total_eval_marks,"total_eval_markstotal_eval_markstotal_eval_markstotal_eval_markstotal_eval_marks")
                
                if int(evaluation_type) == 1:
                    if total_eval_marks < 38:
                        seegrade = 'F'
                        addSEETotalMarks = SEE_Total_Marks.objects.create(st_id=st_id, total_valuation_marks=total_eval_marks, grade_obtained=seegrade, valuation_type=evaluation_type, exam_qp_id=exam_qp)
                        master_detail_id = Academics_Master_Details.objects.get(st_uid=st_id, acad_cal_id_id=exam.acad_cal_id, scheme_details_id=course_id, st_branch_applied_id=department)
                        final_marks = (int(total_eval_marks/2)) +  master_detail_id.cie_marks
                        grade = GradeMapping.objects.get(MinMarks__lte=total_eval_marks, MaxMarks__gte=total_eval_marks, TotalMarks=100)   
                        
                        Exam_Results.objects.create(semester=exam.semester, acad_cal_id=exam.acad_cal_id, st_id=st_id, exam_id=exam, st_branch_id=department, scheme_details_id=course_id, exam_type=evaluation_type, see_marks=total_eval_marks, final_marks=final_marks, exam_new_grade=seegrade, exam_gp_earned=grade.GradePoints, grade_mapping_id=grade, academics_master_details_id=master_detail_id)
                        
                    elif total_eval_marks == 38:
                        total_eval_marks = 40
                        seegrade = 'E'
                        addSEETotalMarks = SEE_Total_Marks.objects.create(st_id=st_id, total_valuation_marks=total_eval_marks, grade_obtained=seegrade, valuation_type=evaluation_type, exam_qp_id=exam_qp)
                        master_detail_id = Academics_Master_Details.objects.get(st_uid=st_id, acad_cal_id_id=exam.acad_cal_id, scheme_details_id=course_id, st_branch_applied_id=department)
                        final_marks = (int(total_eval_marks/2)) +  master_detail_id.cie_marks
                        grade = GradeMapping.objects.get(MinMarks__lte=final_marks, MaxMarks__gte=final_marks, TotalMarks=100) 
                        scheme_detail=master_detail_id.scheme_details_id
                        print(scheme_detail)
                        a=Course_Equivalence.object.get(old_scheme_details_id_id=scheme_detail).new_scheme_details_id_id
                        if a :
                            print("000000000000000")
                            master_detail_id = Academics_Master_Details.objects.get(st_uid=st_id, acad_cal_id_id=exam.acad_cal_id, scheme_details_id=a, st_branch_applied_id=department)
                            print("999",master_detail_id)
                            Exam_Results.objects.get(semester=exam.semester, acad_cal_id=exam.acad_cal_id, st_id=st_id, exam_id=exam, st_branch_id=department, scheme_details_id=a, exam_type=evaluation_type, see_marks=total_eval_marks,academics_master_details_id=master_detail_id).update( final_marks=final_marks, exam_new_grade=grade.Grade, exam_gp_earned=grade.GradePoints, grade_mapping_id=grade )
                            print("llllllllllll")
                        else:

                            Exam_Results.objects.create(semester=exam.semester, acad_cal_id=exam.acad_cal_id, st_id=st_id, exam_id=exam, st_branch_id=department, scheme_details_id=course_id, exam_type=evaluation_type, see_marks=total_eval_marks, final_marks=final_marks, exam_new_grade=grade.Grade, exam_gp_earned=grade.GradePoints, grade_mapping_id=grade, academics_master_details_id=master_detail_id)
                    else:
                        grade = GradeMapping.objects.get(MinMarks__lte=total_eval_marks, MaxMarks__gte=total_eval_marks, TotalMarks=100)   
                        addSEETotalMarks = SEE_Total_Marks.objects.create(st_id=st_id, total_valuation_marks=total_eval_marks, grade_obtained=grade, valuation_type=evaluation_type, exam_qp_id=exam_qp)
                        master_detail_id = Academics_Master_Details.objects.get(st_uid=st_id, acad_cal_id_id=exam.acad_cal_id, scheme_details_id=course_id, st_branch_applied_id=department)
                        print("..............................///////////////////////////..........")
                        print(st_id,exam.acad_cal_id,course_id)
                        final_marks = (int(total_eval_marks/2)) +  master_detail_id.cie_marks
                        grade = GradeMapping.objects.get(MinMarks__lte=final_marks, MaxMarks__gte=final_marks, TotalMarks=100) 
                        scheme_detail=master_detail_id.scheme_details_id
                        print(scheme_detail)
                        try:
                            a = Course_Equivalence.objects.get(old_scheme_details_id_id=scheme_detail).new_scheme_details_id_id
                            print("New Scheme Details ID:", a)
                        except Course_Equivalence.DoesNotExist:
                            print(f"No course equivalence found for scheme detail {scheme_detail}")
                            return  # Handle missing equivalence, possibly return or skip further processing

                        if a:
                            print("Course Equivalence Found")

                            # Step 6: Update master detail ID for the new scheme
                            try:
                                master_detail_id = Academics_Master_Details.objects.get(
                                    st_uid=st_id,
                                    scheme_details_id=a,
                                    st_branch_applied_id=department
                                )
                                print("New Master Detail Found for Scheme:", master_detail_id)
                            except Academics_Master_Details.DoesNotExist:
                                print(f"Master details not found for student {st_id} with scheme {a}")
                                return  # Handle missing master details, possibly return or skip further processing

                            # Step 7: Print relevant details for debugging
                            print("Exam:", exam.semester, exam.acad_cal_id, st_id, exam, department, a, evaluation_type, master_detail_id)
                            print("Marks and Grades:", total_eval_marks, final_marks, grade.Grade, grade.GradePoints, grade)

                            # Step 8: Try to update existing exam results
                            try:
                                print("st_id",st_id)
                                exam_result = Exam_Results.objects.get(
                                   
                                    exam_type=evaluation_type,
                                    academics_master_details_id=master_detail_id,
                                    st_id=st_id,
                                    scheme_details_id=a
                                )
                                print("Existing Exam Result Found:", exam_result)

                                # Update the existing record
                                exam_result.see_marks = total_eval_marks
                                exam_result.final_marks = final_marks
                                exam_result.exam_new_grade = grade.Grade
                                exam_result.exam_gp_earned = grade.GradePoints
                                exam_result.grade_mapping_id = grade
                                exam_result.save()
                                print("Record updated successfully")

                            except Exam_Results.DoesNotExist:
                                print(f"No matching Exam_Results record found for student {st_id} and course {course_id}")
                                # Optionally, create a new exam result if none exists
                                Exam_Results.objects.create(semester=exam.semester, acad_cal_id=exam.acad_cal_id, st_id=st_id, exam_id=exam, st_branch_id=department, scheme_details_id=course_id, exam_type=evaluation_type, see_marks=total_eval_marks, final_marks=final_marks, exam_new_grade=grade.Grade, exam_gp_earned=grade.GradePoints, grade_mapping_id=grade, academics_master_details_id=master_detail_id)

                                print("New Exam Result Created")
                        # else:

                        #     Exam_Results.objects.create(semester=exam.semester, acad_cal_id=exam.acad_cal_id, st_id=st_id, exam_id=exam, st_branch_id=department, scheme_details_id=course_id, exam_type=evaluation_type, see_marks=total_eval_marks, final_marks=final_marks, exam_new_grade=grade.Grade, exam_gp_earned=grade.GradePoints, grade_mapping_id=grade, academics_master_details_id=master_detail_id)
                 
                        # print(total_eval_marks,final_marks,grade.GradePoints,evaluation_type,master_detail_id.cie_marks)  
                        # Exam_Results.objects.create(semester=exam.semester, acad_cal_id=exam.acad_cal_id, st_id=st_id, exam_id=exam, st_branch_id=department, scheme_details_id=course_id, exam_type=evaluation_type, see_marks=total_eval_marks, final_marks=final_marks, exam_new_grade=grade.Grade, exam_gp_earned=grade.GradePoints, grade_mapping_id=grade, academics_master_details_id=master_detail_id)
                
                if int(evaluation_type) == 2:
                    grade = GradeMapping.objects.get(MinMarks__lte=total_eval_marks, MaxMarks__gte=total_eval_marks, TotalMarks=100)   
                    addSEETotalMarks = SEE_Total_Marks.objects.create(st_id=st_id, total_valuation_marks=total_eval_marks, grade_obtained=grade, valuation_type=evaluation_type, exam_qp_id=exam_qp)
                    master_detail_id = Academics_Master_Details.objects.get(st_uid=st_id, acad_cal_id_id=exam.acad_cal_id, scheme_details_id=course_id, st_branch_applied_id=department)
                    final_marks = (int(total_eval_marks/2)) +  master_detail_id.cie_marks
                    grade = GradeMapping.objects.get(MinMarks__lte=final_marks, MaxMarks__gte=final_marks, TotalMarks=100)
                    rev_exam_result = Exam_Results.objects.get(semester=exam.semester, acad_cal_id=exam.acad_cal_id, st_id=st_id, exam_type=1)
                    Exam_Results.objects.create(exam_old_grade=rev_exam_result.exam_new_grade, semester=exam.semester, acad_cal_id=exam.acad_cal_id, st_id=st_id, exam_id=exam, st_branch_id=department, scheme_details_id=course_id, exam_type=evaluation_type, see_marks=total_eval_marks, final_marks=final_marks, exam_new_grade=grade.Grade, exam_gp_earned=grade.GradePoints, grade_mapping_id=grade, academics_master_details_id=master_detail_id)
                
                elif int(evaluation_type) == 3:
                    grade = GradeMapping.objects.get(MinMarks__lte=total_eval_marks, MaxMarks__gte=total_eval_marks, TotalMarks=100)   
                    addSEETotalMarks = SEE_Total_Marks.objects.create(st_id=st_id, total_valuation_marks=total_eval_marks, grade_obtained=grade, valuation_type=evaluation_type, exam_qp_id=exam_qp)
                    master_detail_id = Academics_Master_Details.objects.get(st_uid=st_id, acad_cal_id_id=exam.acad_cal_id, scheme_details_id=course_id, st_branch_applied_id=department)
                    final_marks = (int(total_eval_marks/2)) +  master_detail_id.cie_marks
                    grade = GradeMapping.objects.get(MinMarks__lte=final_marks, MaxMarks__gte=final_marks, TotalMarks=100)
                    chal_exam_result = Exam_Results.objects.get(semester=exam.semester, acad_cal_id=exam.acad_cal_id, st_id=st_id, exam_type=1)
                    Exam_Results.objects.create(exam_old_grade=chal_exam_result.exam_new_grade, semester=exam.semester, acad_cal_id=exam.acad_cal_id, st_id=st_id, exam_id=exam, st_branch_id=department, scheme_details_id=course_id, exam_type=evaluation_type, see_marks=total_eval_marks, final_marks=final_marks, exam_new_grade=grade.Grade, exam_gp_earned=grade.GradePoints, grade_mapping_id=grade, academics_master_details_id=master_detail_id)
                    
                st_list = Exam_Results.objects.filter(exam_id=exam, exam_type=evaluation_type).values('st_id').distinct()
                students_list = Exam_HallTicket.objects.filter(exam_id=exam, st_uid_id__in=st_list)
                student_results = dict()

                for student in students_list:
                    course_grades = dict()
                    total_credits = 0
                    total_points = 0
                    earned_crs = 0
                    for course in course_list:
                        try:
                            st_grade = Exam_Results.objects.get(
                                st_branch=branch, 
                                exam_id=exam, 
                                exam_type=evaluation_type, 
                                scheme_details_id=course.course_code, 
                                st_id=student.st_uid
                            )
                            # Check if the grade is not "F" before considering it for earned credits
                            if st_grade.exam_new_grade != "F":
                                earned_crs += int(st_grade.scheme_details_id.credits)
                            total_credits += int(st_grade.scheme_details_id.credits)
                            course_grades[course] = st_grade
                            total_points += (int(st_grade.scheme_details_id.credits) * int(st_grade.exam_gp_earned))
                            
                        except Exam_Results.DoesNotExist:
                            # Handle the case where no Exam_Results object is found
                            # For example, you can print a message or take other actions
                            print(f"No Exam_Results found for student {student.st_uid} and course {course.course_code}")
                            # You can choose to continue with the loop or break out of it, depending on your logic
                    
                    sgpa = total_points / total_credits
                        # Update the SGPA for the current student
                    Student_current_status.objects.filter(st_uid=master_detail_id.st_uid).update(sgpa=sgpa)

                
                messages.success(request, "Success! Marks Added Successfully")
                return render(request, "external_exam_bitwise.html", {'username': userName, 'units': units, 'department': department, 'exam': exam, 'course_name': course_name, 'evaluation_type': evaluation_type})
        return render(request, "external_exam_bitwise.html")

# def student_promotion_list(request):
#     userName=CustomUser.objects.get(id=request.user.id)
#     if request.method!="POST":
#         departments = Department.objects.all()
#         academic_year_tbl = AcademicYear.objects.all().order_by('-acayear') 
#         return render(request,"student_promotion_list.html",{'username':userName,'academic_year_tbl':academic_year_tbl,'departments':departments})
#     else:
#         departments = Department.objects.all()
#         btn_clicked = request.POST.get("btn_clicked")
#         acad_year = request.POST.get("acad_cal_acad_year")
#         acad_year = AcademicYear.objects.get(id=acad_year).acayear
#         student_year = request.POST.get("student_year")
#         print("year",student_year)
#         department = request.POST.get("department")
#         year_spilt = acad_year.split('-')
#         print(year_spilt)
#         st_year = student_year.split('-')
#         st_year_list = [int(i) for i in st_year]
#         print(st_year_list)
#         st_new_year = [x + 2 for x in st_year_list]
#         year = str(int(year_spilt[0])+1)+'-'+str(int(year_spilt[1])+1)
#         print(year)
#         sem = Academic_Calendar.objects.get(acad_cal_acad_year_id = AcademicYear.objects.get(acayear=year).id,acad_cal_sem=st_year[1]).acad_cal_sem
#         print(sem)
#         new_cal_list = list(Academic_Calendar.objects.filter(acad_cal_acad_year_id=AcademicYear.objects.get(acayear=year).id,acad_cal_sem=sem))
#         print('newcall',new_cal_list)
#         print(st_new_year)
#         cal_list = Academic_Calendar.objects.filter(acad_cal_acad_year_id=AcademicYear.objects.get(acayear=year).id,acad_cal_sem__in=st_year_list)
#         print(cal_list)
#         branch = Department.objects.get(dept_id=department).dept_id
#         print(branch)
#         print("---------------------------------------------TO be continued----------------------------------------------------------")
#         studentList = Student_Division_Allotment.objects.filter(acad_cal_id=4)
#         print(studentList)  # manually changed acad year to 4
#         print(studentList)
#         eligible_students= dict()
#         not_eligible_students= dict()

#         for student in studentList:
#             st_course_list = Exam_Results.objects.filter(st_id_id=student.st_uid).values('scheme_details_id').distinct()
#             backLogCount = 0
#             for course in st_course_list:
#                 st_marks_list = Exam_Results.objects.filter(st_id_id=student.st_uid,scheme_details_id_id=course['scheme_details_id'],exam_new_grade='F').order_by('-exam_type')[:1]
#                 if st_marks_list.exists:
#                     backLogCount = backLogCount + 1
#             studentDetails = dict()
            
#             studentDetails['backlogcount'] = backLogCount
#             print(backLogCount)
#             if backLogCount <= 3:
#                     eligible_students[Student_Details.objects.get(st_uid=student.st_uid.st_uid)] = studentDetails
#             else:
#                 not_eligible_students[Student_Details.objects.get(st_uid=student.st_uid.st_uid)] = studentDetails


#         if btn_clicked == "promot_specific_students":
#             for student, details in not_eligible_students.items():
#                 st_check = request.POST.get(str(student.st_uid)+'_promote')
#                 if st_check is not None:
#                     Student_Promotion_List.objects.create(acad_cal_id_odd=new_cal_list,acad_cal_id_even=new_cal_list,branch=branch,st_id=student)
            
#             messages.success(request, "Success! Students Promoted Sucessfully")
#             return render(request,"student_promotion_list.html",{'username':userName,'acad_year':acad_year,'department':department,'not_eligible_students': not_eligible_students,'branch':branch,'student_year':student_year})

#         if btn_clicked == "not_eligible_students":
#             return render(request,"student_promotion_list.html",{'username':userName,'acad_year':acad_year,'department':department,'not_eligible_students':not_eligible_students,'branch':branch,'student_year':student_year})
#         if btn_clicked == "eligible_students":
#             return render(request,"student_promotion_list.html",{'username':userName,'acad_year':acad_year,'department':department,'eligible_students':eligible_students,'branch':branch,'student_year':student_year})
#         if btn_clicked == "promote_students":
#             for student, details in eligible_students.items():
#                 Student_Promotion_List.objects.create(acad_cal_id_odd=new_cal_list[0],acad_cal_id_even=new_cal_list[0],st_uid=student,offered_by=Department.objects.get(dept_name = "Computer Science & Engineering"))
#             return render(request,"student_promotion_list.html",{'username':userName,'departments':departments})
def student_promotion_list(request):
    userName = CustomUser.objects.get(id=request.user.id)
    
    if request.method != "POST":
        departments = Department.objects.all()
        academic_year_tbl = AcademicYear.objects.all().order_by('-acayear')
        return render(request, "student_promotion_list.html", {'username': userName, 'academic_year_tbl': academic_year_tbl, 'departments': departments})
    else:
        departments = Department.objects.all()
        btn_clicked = request.POST.get("btn_clicked")
        acad_year_id = request.POST.get("acad_cal_acad_year")
        acad_year = AcademicYear.objects.get(id=acad_year_id)
        acad_year_str = acad_year.acayear
        student_year = request.POST.get("student_year")
        department = request.POST.get("department")
      
        
        year_split = acad_year_str.split('-')
        st_year_split = student_year.split('-')
        st_year_list = [int(i) for i in st_year_split]
        st_new_year = [x + 2 for x in st_year_list]
        next_acad_year_str = str(int(year_split[0]) + 1) + '-' + str(int(year_split[1]) + 1)
        print(st_year_split[1],st_year_split[0])
        sem = Academic_Calendar.objects.get(acad_cal_acad_year=acad_year, acad_cal_sem=st_year_split[0],acad_cal_type=1).acad_cal_sem
        sem1 = Academic_Calendar.objects.get(acad_cal_acad_year=acad_year, acad_cal_sem=st_year_split[1],acad_cal_type=1).acad_cal_sem
        acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year=acad_year,acad_cal_sem=sem1,acad_cal_type=1).acad_cal_id
        print(acad_cal_id,"cc",acad_year,sem)
        new_cal_list = list(Academic_Calendar.objects.filter(acad_cal_acad_year=acad_year, acad_cal_sem=sem,acad_cal_type=1))
        new_cal_list1 = list(Academic_Calendar.objects.filter(acad_cal_acad_year=acad_year, acad_cal_sem=sem1+1,acad_cal_type=1))
        print(new_cal_list,"new_cal_list",new_cal_list1)
        
        cal_list = Academic_Calendar.objects.filter(acad_cal_acad_year=acad_year, acad_cal_sem__in=st_year_list,acad_cal_type=1)
        branch = Department.objects.get(dept_id=department).dept_id
        print(sem)
        
        a = Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id)
        b=UG_Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id)
        
        if a:
            studentList = Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id)

        # studentList = UG_Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id)
        if b:
            studentList = UG_Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id)

       
        
        eligible_students = dict()
        not_eligible_students = dict()

        for student in studentList:
            st_course_list = Exam_Results.objects.filter(st_id_id=student.st_uid).values('scheme_details_id').distinct()
            print("student.st_uid",st_course_list,student.st_uid)
            
            
            

            backLogCount = 0
            for course in st_course_list:
                st_marks_list = Exam_Results.objects.filter(st_id_id=student.st_uid, scheme_details_id_id=course['scheme_details_id'], exam_new_grade='F').order_by('-exam_type')[:1]
                print(st_marks_list,"mm")
                if st_marks_list.exists():
                    backLogCount += 1
            studentDetails = {'backlogcount': backLogCount}
            if backLogCount <= 3:
                if st_course_list.exists():
                    eligible_students[Student_Details.objects.get(st_uid=student.st_uid.st_uid)] = studentDetails
                else:
                    not_eligible_students[Student_Details.objects.get(st_uid=student.st_uid.st_uid)] = studentDetails

        if btn_clicked == "promot_specific_students":
            for student, details in not_eligible_students.items():              
                st_check = request.POST.get(str(student.st_uid) + '_promote')
                print(new_cal_list)
                if st_check is not None:
                    Student_Promotion_List.objects.create(acad_cal_id_odd=new_cal_list, acad_cal_id_even=new_cal_list, branch=branch, st_id=student)
            messages.success(request, "Success! Students Promoted Successfully")
            return render(request, "student_promotion_list.html", {'username': userName, 'acad_year': acad_year, 'department': department, 'not_eligible_students': not_eligible_students, 'branch': branch, 'student_year': student_year})

        if btn_clicked == "not_eligible_students":
            return render(request, "student_promotion_list.html", {'username': userName, 'acad_year': acad_year, 'department': department, 'not_eligible_students': not_eligible_students, 'branch': branch, 'student_year': student_year})

        if btn_clicked == "eligible_students":
            print(eligible_students)
            return render(request, "student_promotion_list.html", {'username': userName, 'acad_year': acad_year, 'department': department, 'eligible_students': eligible_students, 'branch': branch, 'student_year': student_year})

        if btn_clicked == "promote_students":
            
            for student, details in eligible_students.items():
                Student_Promotion_List.objects.create(acad_cal_id_odd=new_cal_list1[0], acad_cal_id_even=new_cal_list[0], st_uid=student, offered_by=Department.objects.get(dept_name="Computer Science & Engineering"))
            return render(request, "student_promotion_list.html", {'username': userName, 'departments': departments})
            
def gen_barcode(request):
    if request.method!="POST":
        userName=CustomUser.objects.get(id=request.user.id)
        departments = Department.objects.all()
        course_obj = Scheme_Details.objects.all()
        # exams  = Exam_Details.objects.order_by('-acad_year')[:2]
        exams  = Exam_Details.objects.order_by('-acad_year')
        return render(request,"generateBarCode.html",{'username':userName,'departments':departments, 'course_obj':course_obj, 'exams':exams})

    else:
        btn_clicked = request.POST.get("btn_clicked")
        exam_id = request.POST.get("exam_id")
        department = request.POST.get("department")
        exam = Exam_Details.objects.get(exam_details_id=exam_id)
        if btn_clicked == "generate_qrcode_submit":
            print("---------------------")
            userName=CustomUser.objects.get(id=request.user.id)
            departments = Department.objects.all()
            studentList = Student_Details.objects.all()
            studentCount = Student_Details.objects.all().count()
            

            coursesOfExam = Exam_QP.objects.filter(exam_id=exam_id)
            coursesOfDept = coursesOfExam.filter(course_code__offered_by=department)

            for course in coursesOfDept:
                scheme_details_id = course.course_code_id

                #getting "hall_ticket_id"'s of the exam    Ex: all hall-tickets for {"2020-21 Regular SEE Exam Odd Sem(5) Dec21-Jan22"}
                halticketsOfExam = Exam_HallTicket.objects.filter(exam_id=exam_id)

                #getting halltickets of the previously retrived hall-tickets
                halticketDetailsOfExam = Exam_HallTicket_Details.objects.filter(hall_ticket_id__in = halticketsOfExam)

                #getting all "ht_details_id"'s for a particular course 
                ht_details_id = halticketDetailsOfExam.filter(academics_master_details_id__scheme_details_id = scheme_details_id)

                #getting all the student list with the "ht_details_id"'s and present for the exam
                studentsAttended = Exam_Attendance.objects.filter(ht_details_id__in = ht_details_id, attendance_Status = 'P').values('st_uid')

                # total_stds = studentsAttended.count()

                # no_of_packets = 100 + total_stds/10

                packet = 100

                std_counter = 1


                
                for student in studentsAttended :
                    schemeDetails = Scheme_Details.objects.get(scheme_details_id = scheme_details_id)
                    exam = Exam_Details.objects.get(exam_details_id=exam_id)
                    branchCode = schemeDetails.offered_by.dept_id

                    examType = exam.exam_type

                    # Ex for 2021-22 getting only 22
                    print(exam.acad_cal_id.acad_cal_acad_year)
                    ay = str(exam.acad_cal_id.acad_cal_acad_year).split("-")[1]

                    sem = exam.semester

                    #getting last 2 characters of code ex : 18UCSL603 => 03 
                    course = schemeDetails.course_code[-2:]

                    script_no = (std_counter%11)
                    std_counter+=1

                    print("std_counter")
                    print(std_counter)

                    if(script_no%11 == 0):
                        script_no = 1
                        std_counter+=1
                        packet +=1


                    # var1 = "Hello"
                    # var2 = "World"
                    # "{} {}".format(var1, var2)
                    # var3 = > Hello World
                    code = "{}{}{}{}{}{}-{}".format(branchCode, ay, examType, sem, course, packet, script_no)
                    print(".............................................")
                    print(code)
                    print("///////////////////////////////////////")

                    std = Student_Details.objects.get(st_uid = student['st_uid'])

                    # barcode_generate =  Bar_Code.objects.create(st_id=std,barcode=code,exam_id=exam)
                    # barcode_generate.save()
                   
                        # Generate a new barcode and save it
                    print("std",std)
                    barcode_generate = Bar_Code.objects.create(st_id=std, barcode=code, exam_id=exam)
                    barcode_generate.save()
                    messages.success(request,"Generated Success") 

            return HttpResponseRedirect('generate_barcode')
        if btn_clicked == "generate_qrcode_pdf":

            program = None
            
            userName=CustomUser.objects.get(id=request.user.id)
            barcodeList = Bar_Code.objects.filter(exam_id = exam)
            print(barcodeList)

            st_temp = barcodeList[0].st_id

            if "BE" in st_temp.st_uid :
                program = "BE"
            if "MTECH" in st_temp.st_uid :
                program = "MTECH"
            if "MBA" in st_temp.st_uid :
                program = "MBA"

            barcodes = dict()

            coursesOfExam = Exam_QP.objects.filter(exam_id=exam_id)
            coursesOfDept = coursesOfExam.filter(course_code__offered_by=department)
            
            examType = exam.exam_type
            # Ex for 2021-22 getting only 22
            ay = str(exam.acad_cal_id.acad_cal_acad_year).split("-")[1]
            sem = exam.semester

            for course in coursesOfDept:
                scheme_details_id = course.course_code_id
                schemeDetails = Scheme_Details.objects.get(scheme_details_id = scheme_details_id)
                course_code = schemeDetails.course_code[-2:]
                branchCode = schemeDetails.offered_by.dept_id

                code = "{}{}{}{}{}".format(branchCode, ay, examType, sem, course_code)
                print(code,"codecodecodecode",branchCode,ay,examType,sem,course_code)
                barcodeListOfCourse = barcodeList.filter(barcode__startswith=code)
         
                barcodes[schemeDetails] = barcodeListOfCourse


            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'inline; attachment; filename='+"ack_pdf_ug"+str(datetime.now())+".pdf"
            response['Content-Transfer-Encoding'] = 'binary'

            dept = Department.objects.get(dept_id = department)
            print(barcodes,"barcodes")
            html_string = render_to_string('barcode_pdf.html',{'username':userName,'barcodes':barcodes, 'exam':exam, "dept":dept, "program":program})
            html = HTML(string=html_string, base_url=request.build_absolute_uri())

            result = html.write_pdf()

            with tempfile.NamedTemporaryFile(delete=True) as output:
                output.write(result)
                output.flush()

                output=open(output.name, 'rb')
                response.write(output.read())

            return response



def gen_hallTicket(request):
    print("Method call")
    if request.method!="POST":
        userName=CustomUser.objects.get(id=request.user.id)
        departments = Department.objects.all()
        course_obj = Scheme_Details.objects.all()
        # exams  = Exam_Details.objects.order_by('-acad_year')[:2]
        exams  = Exam_Details.objects.order_by('-acad_year')
        return render(request,"gen_hallticket.html",{'username':userName,'departments':departments, 'course_obj':course_obj, 'exams':exams})
    
    else:
        print("inside else")
        btn_clicked = request.POST.get("btn_clicked")
        x=0
        exam_id = request.POST.get("exam_id")
        department = request.POST.get("department")
        print(department)
        exam = Exam_Details.objects.get(exam_details_id=exam_id)
        coursesOfExam = Exam_QP.objects.filter(exam_id=exam_id)
        print(coursesOfExam)
        coursesOfDept = coursesOfExam.filter(course_code__offered_by=department)
        print(coursesOfDept)
        acad_cal_id = exam.acad_cal_id
        print(acad_cal_id)
        coursesOfDept = coursesOfExam.filter(course_code__offered_by=department).values_list('course_code_id', flat=True).distinct()
        print(coursesOfDept,"ppppppppppppppppppppppppppppppppppp")
        print("-----------------------------")
        if btn_clicked == "generate_hallticket_submit":
            
            sequence_no=100
            
            
            if exam.exam_type==1:
                etype = 'R'
                print(acad_cal_id)
                print(coursesOfDept)
                cie_marks_list = Academics_Master_Details.objects.filter(acad_cal_id_id=acad_cal_id,scheme_details_id__in=coursesOfDept,st_branch_applied_id=2).values_list('cie_marks', flat=True).distinct()

                
                student_id_list = Academics_Master_Details.objects.filter(
                        acad_cal_id_id=acad_cal_id,
                        scheme_details_id__in=coursesOfDept,
                        st_branch_applied_id=2,
                       
                        cie_marks__gt=20
                    ).values_list('st_uid', flat=True).distinct()
                print("student_id_list",student_id_list)
            elif exam.exam_type==2:
                print("lll3")

                etype = 'M'
                student_id_list = Makeup_Exam_Registration.objects.filter(acad_cal_id_id=acad_cal_id,scheme_details_id__in=coursesOfDept,branch_id=2).values_list('st_uid', flat=True).distinct()
                print(student_id_list,"makeup")
            elif exam.exam_type==4:
                etype = 'S'
            else:  # consider other exams also
                etype = 'A'
            branchCode = Department.objects.get(dept_id=department).dept_id
            # Ex for 2021-22 getting only 22
            ayear=str(exam.acad_cal_id.acad_cal_acad_year)
            #print(ayear.split("-")[1])
            #ay = exam.acad_cal_id.acad_cal_acad_year.split("-")[1]
            ay = ayear.split("-")[1]
            sem = exam.semester
            x=[]
            for st_id in student_id_list:
                print("rntgirhet")
                print(st_id)
                print("Inside for loop")
                # "10-digit number to be generated according to following pattern:
                # 1) First digist represents UG/PG. U --> UG, P--> PG
                # 2) Next 2-digits represent Current Academic Year (Eg: AY 2022-23 --> 22)
                # 3) Next 1-char represents Exam Type (Regular-'R', Makeup-'M',STC-'S',Special Makeup-'A', STC Makeup-'B',Special Exam-'C')
                # 3) Next 2-digits represent Department (Eg: CS - 01)
                # 4) Next 1-digit represnets semseter
                # 5) Next 3-digits represents sequence number"
            
                
                student = Student_Details.objects.get(st_uid=st_id)

                #prev_created_hallticket = Exam_HallTicket.objects.get(Q(st_uid=student, exam_id__acad_cal_id__acad_cal_acad_year= exam.acad_cal_id.acad_cal_acad_year) & ~Q(exam_id=exam))

                if "BE" in student.st_uid:
                    fd = "U"
                else:
                    fd = "P"
                code = "{}{}{}{}{}{}".format(fd, ay,etype,branchCode, sem, sequence_no)
                sequence_no+=1
                #student_master_details_list = None
                try:
                    stuid = Student_Details.objects.get(st_uid=student.st_uid)
                    print(stuid)
                    #exam_hallTicket = Exam_HallTicket.objects.create(exam_id=exam, st_uid=student.st_uid, ht_application_no=code)
                    try:
                        print("exam")
                        print(exam)
                        print("kkkkkk",exam)
                        exam_hallTicket = Exam_HallTicket.objects.create(exam_id=exam, st_uid=stuid, ht_application_no=code)

                    # except IntegrityError:
                    #     messages.error(request,"line 2096 - already generated the hallticket")
                    except Exception as e:
                        messages.error(request, e)
                    
                    try:
                        student_master_details_list = Academics_Master_Details.objects.filter(st_uid=student.st_uid,acad_cal_id_id=acad_cal_id,scheme_details_id__in=coursesOfDept)
                    except Exception:
                        print("exc-2")
                except IntegrityError:
                    print("line 2105 - already generated the hallticket")
                except Exception as e:
                    messages.error(request, e)
                    print("Exception occur")
                    pass
             
                for smd in student_master_details_list:

                    try:
                        print(exam_hallTicket,smd,"pppppppppppo")
                        x=Exam_HallTicket_Details.objects.create(hall_ticket_id=exam_hallTicket, academics_master_details_id=smd)
                        print("ppp")

                        x=x.hall_ticket_id
                    except Exception as e:
                        print("Exception occur")
                        pass
                    print(x,"ppppppppp")
                    hall_ticket_list = Exam_HallTicket_Details.objects.filter(hall_ticket_id=x)
                    print("/////////////////////////////////////////////////")
                    print(hall_ticket_list,"hall_ticket_list")
                for  hall_ticket in hall_ticket_list:
                        
                    master_detail_id = Academics_Master_Details.objects.get(academics_master_details_id=hall_ticket.academics_master_details_id_id)
                    print(master_detail_id,"master_detail_id")
                    hallticket_details_obj = Exam_HallTicket_Details.objects.get(hall_ticket_id=hall_ticket.hall_ticket_id,academics_master_details_id=master_detail_id)
                    print(hallticket_details_obj,Student_Details.objects.get(st_id=(Exam_HallTicket.objects.get(hall_ticket_id=hall_ticket.hall_ticket_id_id)).st_uid_id),"p")
                    see_attendance_obj = Exam_Attendance.objects.create(ht_details_id=hallticket_details_obj,st_uid=Student_Details.objects.get(st_id=(Exam_HallTicket.objects.get(hall_ticket_id=hall_ticket.hall_ticket_id_id)).st_uid_id),attendance_Status='P')
                    print(see_attendance_obj)
                    see_attendance_obj.save()
                    print("/////////////////////////////////////////////////")

            userName=CustomUser.objects.get(id=request.user.id)
            departments = Department.objects.all()
            course_obj = Scheme_Details.objects.all()
            # exams  = Exam_Details.objects.order_by('-acad_year')[:2]
            exams  = Exam_Details.objects.order_by('-acad_year')

            return render(request,"gen_hallticket.html",{'username':userName,'departments':departments, 'course_obj':course_obj, 'exams':exams})

        if btn_clicked == "generate_hallticket_pdf":

            program = None
            acad_cal_id = exam.acad_cal_id

            branchCode = Department.objects.get(dept_id=department).dept_id

            exam_qps_of_branch = Exam_QP.objects.filter(exam_id=exam)
            print(exam_qps_of_branch)
            course_reg_for_exam_by_branch = exam_qps_of_branch.filter(course_code__offered_by=department).values_list('course_code_id', flat=True).distinct()

            hall_tickets_details_of_exam_of_dept = Exam_HallTicket_Details.objects.filter(hall_ticket_id__exam_id = exam, academics_master_details_id__scheme_details_id__in = course_reg_for_exam_by_branch)
            hall_tickets_of_exam_of_dept_list = hall_tickets_details_of_exam_of_dept.values_list('hall_ticket_id', flat=True).distinct()
            print(hall_tickets_of_exam_of_dept_list)
            hall_tickets_of_exam_of_dept_list = Exam_HallTicket.objects.filter(hall_ticket_id__in = hall_tickets_of_exam_of_dept_list).order_by('st_uid')[:30]
            print(hall_tickets_of_exam_of_dept_list)
            st_temp = hall_tickets_of_exam_of_dept_list[0].st_uid
            print(st_temp)
            if "BE" in st_temp.st_uid :
                program = "BE"
            if "MTECH" in st_temp.st_uid :
                program = "MTECH"
            if "MBA" in st_temp.st_uid :
                program = "MBA"
            

            ht_list = dict()
            for hallTicket in hall_tickets_of_exam_of_dept_list:
                ht_details = dict()
                student = hallTicket.st_uid
                usn = student.st_uid
                courses_reg_for_exam_by_student = hallTicket.hallTicketDetails.values_list('academics_master_details_id__scheme_details_id', flat=True).distinct()
                scheme_details_reg_for_exam_by_student = Scheme_Details.objects.filter(scheme_details_id__in = courses_reg_for_exam_by_student)
                courses = dict()
                for index, course in enumerate(scheme_details_reg_for_exam_by_student):
                    courses[index]=course
                ht_details["hall_ticket"] = hallTicket
                ht_details["student"] = student

               
                    
                ht_details["courses"] = courses
                ht_list[usn] = ht_details


            

            dept = Department.objects.get(dept_id = department)

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'inline; attachment; filename='+"hallticket"+str(datetime.now())+".pdf"
            response['Content-Transfer-Encoding'] = 'binary'

            userName=CustomUser.objects.get(id=request.user.id)
            
            html_string = render_to_string('gen_hallticket_pdf.html',{'username':userName, 'ht_list': ht_list, "exam":exam, "dept":dept, "program":program})
            html = HTML(string=html_string, base_url=request.build_absolute_uri())

            result = html.write_pdf()

            with tempfile.NamedTemporaryFile(delete=True) as output:
                output.write(result)
                output.flush()

                output=open(output.name, 'rb')
                response.write(output.read())

            return response

            



def gen_result(request):
    userName=CustomUser.objects.get(id=request.user.id)
    if request.method!="POST":
        departments = Department.objects.all()
        # exams  = Exam_Details.objects.order_by('-acad_year')[:2]
        exams  = Exam_Details.objects.order_by('-acad_year')
        return render(request,"gen_result.html",{'username':userName,'departments':departments, 'exams':exams})
    
    else:
        evaluation_type = request.POST.get("evaluation_type")
        if (evaluation_type == "1"):
            exam_id = request.POST.get("exam_id")
            department = request.POST.get("department")
            evaluation_type = request.POST.get("evaluation_type")

        
            exam = Exam_Details.objects.get(exam_details_id=exam_id)
          
            program = None
            acad_cal_id = exam.acad_cal_id
            branch = Department.objects.get(dept_id=department)
            course_list = Exam_QP.objects.filter(exam_id=exam)
        
            st_list = Exam_Results.objects.filter(exam_id = exam, exam_type = evaluation_type).values('st_id').distinct()

            students_list = Exam_HallTicket.objects.filter(exam_id = exam,st_uid_id__in=st_list)

            # for st in st_list:
            #     print(st['st_id'])
            #     students_list = Exam_HallTicket.objects.filter(exam_id = exam,st_uid_id=st['st_id'])
           

            student_results = dict()

            for student in students_list:

                student_grades = dict()

                course_grades = dict()

                total_credits = 0

                total_points = 0

                earned_crs = 0


                for course in course_list:
                    
                    st_grade = Exam_Results.objects.filter(st_branch = branch, exam_id = exam, exam_type = evaluation_type,scheme_details_id = course.course_code, st_id = student.st_uid)
                    print(st_grade)
                    if st_grade:
                        for st_grade in st_grade:
                            if st_grade.exam_new_grade != "F":
                                earned_crs += int(st_grade.scheme_details_id.credits)
                            if st_grade.exam_new_grade == "F":
                                st_grade.scheme_details_id.credits=0
                        total_credits += int(st_grade.scheme_details_id.credits)
                        course_grades[course] = st_grade

                        total_points += (int(st_grade.scheme_details_id.credits) * int(st_grade.exam_gp_earned))
                    else :
                        pass

                if total_credits != 0:
                    result = total_points / total_credits
                    rounded_result = round(result, 2) 
                    student_grades["course_grade"] = course_grades
                    student_grades["sgpa"] = rounded_result
                    student_grades["total_crs"] = total_credits
                    student_grades["earned_crs"] = earned_crs
                    student_grades["cgpa"] = 0
                else:
                    # Handle the case where total_credits is zero, such as setting result to None or raising an error
                    result = None  #
                    student_grades["course_grade"] = course_grades
                    student_grades["sgpa"] = 0
                    student_grades["total_crs"] = total_credits
                    student_grades["earned_crs"] = earned_crs
                    student_grades["cgpa"] = 0
                

                student_results[student] = student_grades
            # return render(request,"gen_results_pdf.html",{'username':userName, "exam":exam, "program":program, "dept": branch, "course_list": course_list, "student_results": student_results})


            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'inline; attachment; filename='+"Exam Results"+str(datetime.now())+".pdf"
            response['Content-Transfer-Encoding'] = 'binary'

            userName=CustomUser.objects.get(id=request.user.id)
            html_string = render_to_string('gen_results_pdf.html',{'username':userName, "exam":exam, "program":program, "dept": branch, "course_list": course_list, "student_results": student_results})
            html = HTML(string=html_string, base_url=request.build_absolute_uri())

            result = html.write_pdf()

            with tempfile.NamedTemporaryFile(delete=True) as output:
                output.write(result)
                output.flush()

                output=open(output.name, 'rb')
                response.write(output.read())

            return response
    
        elif evaluation_type == "2":

            exam_id = request.POST.get("exam_id")
            department = request.POST.get("department")
            evaluation_type = request.POST.get("evaluation_type")

            print(exam_id)
            exam = Exam_Details.objects.get(exam_details_id=exam_id)
            print("----------------------")
            print(exam)
            program = None
            #acad_cal_id = exam.acad_cal_id
            branch = Department.objects.get(dept_id=department)


            

            
            course_list = Exam_QP.objects.filter(exam_id=exam)
            print("course")
            print(course_list)
            st_list = Exam_Results.objects.filter(exam_id = exam, exam_type = evaluation_type).values('st_id').distinct()

            students_list = Exam_HallTicket.objects.filter(exam_id = exam,st_uid_id__in=st_list)

            # for st in st_list:
            #     print(st['st_id'])
            #     students_list = Exam_HallTicket.objects.filter(exam_id = exam,st_uid_id=st['st_id'])

            #     print(students_list)

            student_results = dict()
            print("-----------------------")
            print(students_list)
            print("-----------------------")
            st_grade = dict()

            for student in students_list:

                #student_grades = dict()

                # course_grades = dict()

                # total_credits = 0

                # total_points = 0

                # earned_crs = 0

                st_grade = Exam_Results.objects.get( exam_id = exam, exam_type = evaluation_type,st_id = student.st_uid)
                print("hello")
                print(evaluation_type)
                print(st_grade)
                print(st_grade.exam_old_grade)
                print(st_grade.exam_new_grade)

            
            # return render(request,"gen_results_pdf.html",{'username':userName, "exam":exam, "program":program, "dept": branch, "course_list": course_list, "student_results": student_results})


            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'inline; attachment; filename='+"Revaluation Results"+str(datetime.now())+".pdf"
            response['Content-Transfer-Encoding'] = 'binary'

            userName=CustomUser.objects.get(id=request.user.id)
            html_string = render_to_string('gen_results_pdf_revaluation.html',{'username':userName, "exam":exam, "program":program, "dept": branch, "course_list": course_list, "students_list": students_list,"st_grade":st_grade})
            html = HTML(string=html_string, base_url=request.build_absolute_uri())

            result = html.write_pdf()

            with tempfile.NamedTemporaryFile(delete=True) as output:
                output.write(result)
                output.flush()

                output=open(output.name, 'rb')
                response.write(output.read())

            return response
        elif evaluation_type == "3":

            exam_id = request.POST.get("exam_id")
            department = request.POST.get("department")
            evaluation_type = request.POST.get("evaluation_type")

            print(exam_id)
            exam = Exam_Details.objects.get(exam_details_id=exam_id)
            print("----------------------")
            print(exam)
            program = None
            #acad_cal_id = exam.acad_cal_id
            branch = Department.objects.get(dept_id=department)


            

            
            course_list = Exam_QP.objects.filter(exam_id=exam)
        
            st_list = Exam_Results.objects.filter(exam_id = exam, exam_type = evaluation_type).values('st_id').distinct()

            students_list = Exam_HallTicket.objects.filter(exam_id = exam,st_uid_id__in=st_list)

            # for st in st_list:
            #     print(st['st_id'])
            #     students_list = Exam_HallTicket.objects.filter(exam_id = exam,st_uid_id=st['st_id'])

            #     print(students_list)

            student_results = dict()
            print("-----------------------")
            print(students_list)
            print("-----------------------")
            st_grade = dict()
            for student in students_list:

                #student_grades = dict()

                # course_grades = dict()

                # total_credits = 0

                # total_points = 0

                # earned_crs = 0

                st_grade = Exam_Results.objects.get( exam_id = exam, exam_type = evaluation_type,st_id = student.st_uid)
                print("hello")
                print(evaluation_type)
                print(st_grade)
                print(st_grade.exam_old_grade)
                print(st_grade.exam_new_grade)

            
            # return render(request,"gen_results_pdf.html",{'username':userName, "exam":exam, "program":program, "dept": branch, "course_list": course_list, "student_results": student_results})


            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'inline; attachment; filename='+"Revaluation Results"+str(datetime.now())+".pdf"
            response['Content-Transfer-Encoding'] = 'binary'

            userName=CustomUser.objects.get(id=request.user.id)
            html_string = render_to_string('gen makeup result.html',{'username':userName, "exam":exam, "program":program, "dept": branch, "course_list": course_list, "students_list": students_list,"st_grade":st_grade})
            html = HTML(string=html_string, base_url=request.build_absolute_uri())

            result = html.write_pdf()

            with tempfile.NamedTemporaryFile(delete=True) as output:
                output.write(result)
                output.flush()

                output=open(output.name, 'rb')
                response.write(output.read())

            return response
def provisional(request):
    # usn=request.post.get("exam_id")
    # stu=Student_Details.objects.get()
    exam_id = request.POST.get("exam_id")
    exam = Exam_Details.objects.all()
    print(exam)
    if request.method!="POST":
        departments = Department.objects.all()
        return render(request,"PROVISIONAL.html",{'departments':departments,'exams':exam})
# def pro(request):
#             exam_id = request.POST.get("exam_id")
#             exam = Exam_Details.objects.get(exam_details_id=exam_id)
#             decr=str(exam.description)
#             decro=(decr[22:26])
#             print("exam",decro)
#             stu=student=request.POST.get("usn")
#             print(student)
#             student=Student_Details.objects.get(st_uid=stu)
#             print(student)
#             hello=student.st_id
#             print("hello",hello)
#             name=student.st_name
#             branch=student.st_branch_applied_id
#             departments = Department.objects.get(dept_id=branch)
#             print(departments)
#             print(name)
#             course_list = Exam_QP.objects.filter(exam_id=exam)
#             print(course_list)
#             count=0
#             sgpatemp=0
#             name=[]
#             grade=[]
#             credits=[]
#             gradepoint=[]
#             creditsearned=[]
#             creditsearnedo=[]
#             creditso=[]
#             gradepointo=[]
#             cgpatemp=0
#             cgpa=0
#             counter=[]
#             for i in course_list:
#                 course_id=i.course_code_id
#                 name.append((Scheme_Details.objects.get(scheme_details_id=course_id).course_title))
#                 students_list = Exam_Results.objects.filter(st_id_id=hello).aggregate(max_value=Max('exam_type'))['max_value']
#                 print("sumanth:",students_list)
#                 student_lists = Exam_Results.objects.get(st_id_id=hello,exam_type=students_list,exam_id_id=exam_id)
#                 grade.append(student_lists.exam_new_grade)
#                 hello1=Scheme_Details.objects.get(scheme_details_id=course_id)
#                 credits.append(hello1.credits)
#                 gradepoint.append(student_lists.exam_gp_earned)
#                 print(gradepoint)
#                 if student_lists.exam_new_grade=='F':
#                     creditsearned.append("0")
#                 else:
#                     creditsearned.append(hello1.credits)
#                 totalgradepoints=sum(creditsearned)
#                 totalcredits=sum(credits)
#                 sgpatemp+=(creditsearned[count]*gradepoint[count])
#                 sgpa=sgpatemp/totalcredits
#                 counter.append(count+1)
#                 print("count",counter)
#                 count=count+1
                
#             counto=0
#             print('sumanth',int(exam_id))
#             for j in range (0,int(exam_id)):
#                 for i in course_list:
                    
#                     exam_ido=j+1
#                     print()
#                     course_id=i.course_code_id
#                     students_list = Exam_Results.objects.filter(st_id_id=hello).aggregate(max_value=Max('exam_type'))['max_value']
#                     print("he;llo",students_list)
#                     student_listso = Exam_Results.objects.get(st_id_id=hello,exam_type=students_list,exam_id_id=exam_ido)
#                     hello1=Scheme_Details.objects.get(scheme_details_id=course_id)
#                     creditso.append(hello1.credits)
#                     gradepointo.append(student_listso.exam_gp_earned)
#                     if student_listso.exam_new_grade=='F':
#                         creditsearnedo.append("0")
#                     else:
#                         creditsearnedo.append(hello1.credits)
#                     totalgradepoints=sum(creditsearnedo)
#                     totalcredits=sum(creditso)
#                     cgpatemp+=(creditsearnedo[counto]*gradepointo[counto])
#                     cgpa=cgpatemp/totalcredits
#                     # print("cgpa",totalgradepoints,totalcredits)
                    
#                     counto=count+1
#             response = HttpResponse(content_type='application/pdf')
#             response['Content-Disposition'] =  'inline; attachment; filename='+"PROVISIONAL Results"+str(datetime.now())+".pdf"
#             response['C+ontent-Transfer-Encoding'] = 'binary'

#             userName=CustomUser.objects.get(id=request.user.id)
#             html_string = render_to_string('pro.html',{"student":student,"branch":departments,"exam":exam,'course_list':course_list,'grade':grade,'credits':credits,'name':name,'gradep':gradepoint,'creditse':creditsearned,'totalcre':totalgradepoints,'totalcredits':totalcredits,'sgpa':sgpa,'cgpa':cgpa,'counter':counter,'sem':decro})
#             html = HTML(string=html_string, base_url=request.build_absolute_uri())

#             result = html.write_pdf()
#             with tempfile.NamedTemporaryFile(delete=True) as output:
#                 output.write(result)
#                 output.flush()

#                 output=open(output.name, 'rb')
#                 response.write(output.read())
#             return response
def pro(request):
            exam_id = request.POST.get("exam_id")
            exam = Exam_Details.objects.get(exam_details_id=exam_id)
            decr=str(exam.description)
            decro=(decr[22:26])
            print("exam",decro)
            stu=student=request.POST.get("usn")
            print(student)
            student=Student_Details.objects.get(st_uid=stu)
            print(student)
            hello=student.st_id
            print("hello",hello)
            name=student.st_name
            branch=student.st_branch_applied_id
            departments = Department.objects.get(dept_id=branch)
            print(departments)
            print(name)
            course_list = Exam_QP.objects.filter(exam_id=exam)
            print(course_list)
            count=0
            sgpatemp=0
            name=[]
            grade=[]
            credits=[]
            gradepoint=[]
            creditsearned=[]
            creditsearnedo=[]
            creditso=[]
            gradepointo=[]
            cgpatemp=0
            cgpa=0
            counter=[]
            for i in course_list:
                course_id = i.course_code_id
                name.append((Scheme_Details.objects.get(scheme_details_id=course_id).course_title))
                students_list = Exam_Results.objects.filter(st_id_id=hello).aggregate(max_value=Max('exam_type'))['max_value']
                print("sumanth:", students_list)
                student_lists = Exam_Results.objects.filter(st_id_id=hello, exam_type=students_list, exam_id_id=exam_id)
                
                # Iterate over each student_list for the current course
                for student_list in student_lists:
                    grade.append(student_list.exam_new_grade)
                    hello1 = Scheme_Details.objects.get(scheme_details_id=course_id)
                    credits.append(hello1.credits)
                    gradepoint.append(student_list.exam_gp_earned)
                    print(gradepoint)
                    if student_list.exam_new_grade == 'F':
                        creditsearned.append("0")
                    else:
                        creditsearned.append(hello1.credits)
                    totalgradepoints = sum(creditsearned)
                    totalcredits = sum(credits)
                    sgpatemp += (creditsearned[count] * gradepoint[count])
                    sgpa = sgpatemp / totalcredits
                    counter.append(count + 1)
                    print("count", counter)
                    count += 1
            counto=0
            for j in range (0,int(exam_id)):
                print(exam_id,"exam_idexam_idexam_id")
                for i in course_list:
                    
                    exam_ido=j+1
                    print()
                    course_id=i.course_code_id
                    students_list = Exam_Results.objects.filter(st_id_id=hello).aggregate(max_value=Max('exam_type'))['max_value']
                    print("he;llo",students_list)
                    student_listso = Exam_Results.objects.filter(st_id_id=hello, exam_type=students_list, exam_id_id=exam_ido)

                    # Check if any objects are returned
                    if student_listso.exists():
                        for student_list in student_listso:
                            hello1 = Scheme_Details.objects.get(scheme_details_id=course_id)
                            creditso.append(hello1.credits)
                            gradepointo.append(student_list.exam_gp_earned)
                            if student_list.exam_new_grade == 'F':
                                creditsearnedo.append(0)
                            else:
                                creditsearnedo.append(hello1.credits)
                            
                            totalgradepoints = sum(creditsearnedo)
                            totalcredits = sum(creditso)
                            cgpatemp += (creditsearnedo[counto] * gradepointo[counto])
                            cgpa = cgpatemp / totalcredits
                            counto += 1

                        response = HttpResponse(content_type='application/pdf')
                        response['Content-Disposition'] = 'inline; attachment; filename=' + "PROVISIONAL Results" + str(datetime.now()) + ".pdf"
                        response['C+ontent-Transfer-Encoding'] = 'binary'
                        print("sgpa")
                        print(sgpa)
                        print(cgpa)

                        userName = CustomUser.objects.get(id=request.user.id)
                        html_string = render_to_string('pro.html', {"student": student, "branch": departments, "exam": exam,
                                                                    'course_list': course_list, 'grade': grade, 'credits': credits,
                                                                    'name': name, 'gradep': gradepoint, 'creditse': creditsearned,
                                                                    'totalcre': totalgradepoints, 'totalcredits': totalcredits,
                                                                    'sgpa': sgpa, 'cgpa': cgpa, 'counter': counter, 'sem': decro})
                        html = HTML(string=html_string, base_url=request.build_absolute_uri())

                        result = html.write_pdf()
                        with tempfile.NamedTemporaryFile(delete=True) as output:
                            output.write(result)
                            output.flush()

                            output = open(output.name, 'rb')
                            response.write(output.read())
                        return response

def fetch_exam_details_seetitable(request):
    academic_year_id = request.GET.get('academic_year')
    semester = request.GET.get('semester')
    # exam_id = request.GET.get('exam_descr')
    # print(academic_year_id)
    # print(exam_id)
    # if 'regular' in exam_id.lower():
    #     acad_cal_type = 1
    # elif 'stc' in exam_id.lower():
    #     acad_cal_type = 2
    # print(acad_cal_type,"pp")
    
    
    try:
        acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id=academic_year_id, acad_cal_sem=semester,acad_cal_type=1)
        # acadcal_id = Academic_Calendar.objects.get(acad_cal_acad_year=acadyear,acad_cal_sem=sem,acad_cal_type=acad_cal_type)
        print(acad_cal_id)
        exams = Exam_Details.objects.filter(
            acad_cal_id=acad_cal_id,
            semester=semester
        ).values('description')
    except Academic_Calendar.DoesNotExist:
        exams = []

    return JsonResponse({'exams': list(exams)})

def exam_schedule_view(request):
    userName = CustomUser.objects.get(id=request.user.id)
    departments = Department.objects.all()
    
    current_date = timezone.now().strftime('%d-%m-%Y')
    current_year = timezone.now().year

    if request.method != "POST":
        academic_years = AcademicYear.objects.all()
        context = {
            'username': userName,
            'departments': departments,
            'academic_years': academic_years,
            'current_date': current_date,
            'current_year': current_year,
        }
        return render(request, "exam_schedule.html", context)
    
    else:
        academic_year_id = request.POST.get('academic_year')
        semester = request.POST.get('semester')
        exam_desc = request.POST.get('exam_descr')
        if 'regular' in exam_desc.lower():
            acad_cal_type = 1
        elif 'stc' in exam_desc.lower():
            acad_cal_type = 2
        print(acad_cal_type,"pp")

        try:
            acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id=academic_year_id, acad_cal_sem=semester,acad_cal_type=acad_cal_type)
            exams = Exam_Details.objects.filter(acad_cal_id=acad_cal_id).order_by('semester')
        except Academic_Calendar.DoesNotExist:
            exams = []
            acad_cal_id = None
        
        schedule_data = []
        if exam_desc and semester:
            try:
                exam_details = Exam_Details.objects.get(description=exam_desc, semester=semester, acad_cal_id=acad_cal_id)
                schedule_data = SEE_timetable.objects.filter(exam_id=exam_details).order_by('exam_date')
            except Exam_Details.DoesNotExist:
                schedule_data = []

        detailed_schedule_data = []
        branches = set()
        for schedule in schedule_data:
            course_code = schedule.scheme_details_id.course_code if schedule.scheme_details_id else 'N/A'
            course_title = schedule.scheme_details_id.course_title if schedule.scheme_details_id else 'N/A'

            data_row = {
                'exam_date': schedule.exam_date.strftime('%d-%m-%Y') if schedule.exam_date else 'N/A',
                'timing': schedule.timing if hasattr(schedule, 'timing') else '-',
                'course_code': course_code,
                'course_title': course_title,
                'CH': course_code if 'CH' in course_code.upper() else '',
                'CS': course_code if 'CS' in course_code.upper() else '',
                'CV': course_code if 'CV' in course_code.upper() else '',
                'EC': course_code if 'EC' in course_code.upper() else '',
                'EE': course_code if 'EE' in course_code.upper() else '',
                'IS': course_code if 'IS' in course_code.upper() else '',
                'ME': course_code if 'ME' in course_code.upper() else '',
            }
            detailed_schedule_data.append(data_row)
            
            if 'CH' in course_code.upper():
                branches.add('Chemical Engineering')
            elif 'CS' in course_code.upper():
                branches.add('Computer Science Engineering')
            elif 'CV' in course_code.upper():
                branches.add('Civil Engineering')
            elif 'EC' in course_code.upper():
                branches.add('Electronics & Communication Engineering')
            elif 'EE' in course_code.upper():
                branches.add('Electrical Engineering')
            elif 'IS' in course_code.upper():
                branches.add('Information Science Engineering')
            elif 'ME' in course_code.upper():
                branches.add('Mechanical Engineering')

        context = {
            'username': userName,
            'departments': departments,
            'exams': exams,
            'schedule_data': detailed_schedule_data,
            'branches': sorted(branches),
            'academic_years': AcademicYear.objects.all(),
            'selected_academic_year': academic_year_id,
            'selected_semester': semester,
            'exam_desc': exam_desc,
            'current_date': current_date,
            'current_year': current_year,
        }

        return render(request, "see_timetable.html", context)



def order(request):
    if request.method!="POST":
        exam = Exam_Details.objects.all()
        departments = Department.objects.all()
        return render(request,"qporder.html",{'departments':departments,'exams':exam,'scheme':Scheme_Details.objects.all()})
    else:
        print("hello")
        examid=request.POST.get("exam_id")
        exam = Exam_Details.objects.get(exam_details_id=examid).semester
        desc=str(Exam_Details.objects.get(exam_details_id=examid).description)
        print(desc)
        sub=request.POST.get("sub")
        subname=Scheme_Details.objects.get(course_code=sub).course_title
        marks=Scheme_Details.objects.get(course_code=sub).max_see_marks
        credit=Scheme_Details.objects.get(course_code=sub).credits
        dept=Department.objects.get(dept_name=Scheme_Details.objects.get(course_code=sub).offered_by).dept_abbr
        if(credit<3):
            time=2
        else:
            time=3
        
        departments = Department.objects.all()
        faculty=Faculty_Course_Allotment.objects.filter(course_code=sub)
        print(faculty)
        print(examid,sub,subname)

        now = datetime.now()
        day = now.strftime("%a")  # Short weekday name, e.g., "Wed"
        month = now.month  # Numeric month, e.g., 7
        date = now.day  # Day of the month, e.g., 26
        year = now.year  # Full year, e.g., 2023
        hours = now.hour  # Hour in 24-hour format
        minutes = now.strftime("%M")  # Zero-padded minute, e.g., "14"
        ampm = now.strftime("%p")  # AM/PM
    
        hours12 = hours % 12 or 12  # Convert to 12-hour format, handle midnight (0)
    
        date_time_string = f"{day} {month}/{date}/{year} {hours12}:{minutes} {ampm}"

        teacher_name=[]
        designation=[]
        teacher_dept=[]
        hello=request.POST.getlist("faculty_ids")
        print("///////////////////////////////")
        print(hello)
        count=[]
        print(date_time_string)
        for i in hello:
            teacher_name.append(Employee_Details.objects.get(employee_emp_id=i).employee_name)
            designation.append(Employee_Details.objects.get(employee_emp_id=i).employee_designation)
            teacher_dept.append(Department.objects.get(dept_name=Employee_Details.objects.get(employee_emp_id=i).employee_dept_id))
        teacher_data=[]
        for teacher in range(len(hello)):
                teacher_data.append({
                'name': teacher_name[teacher],
                'designation': designation[teacher],
                'department': teacher_dept[teacher]  # Assuming teacher_dept is a ForeignKey
            })

        


        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; attachment; filename=' + "Results.pdf"
        response['C+ontent-Transfer-Encoding'] = 'binary'
        html_string = render_to_string('printordercopy.html',{"now": date_time_string,"name":hello,"subname":subname,"exam":exam,"marks":marks,"time":time,"sub":sub,"dept":dept,"teacher_name":teacher_name,"teacher_data":teacher_data,"designation":designation,"teacher_dept":teacher_dept,"des":desc})
        html = HTML(string=html_string, base_url=request.build_absolute_uri())

        result = html.write_pdf()
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()

            output = open(output.name, 'rb')
            response.write(output.read())
        return response
def fetch_exam_details(request):
    if request.method == "GET":
        exam_id = request.GET.get('exam_id')
        print(exam_id,"exam_id")
        
        if not exam_id:
            return JsonResponse({'error': 'No exam_id provided'}, status=400)
        
        try:
            # Retrieve course codes from Exam_QP
            exam_qps = Exam_QP.objects.filter(exam_id=exam_id).values_list('course_code', flat=True)
            print("Course Codes from Exam QP:", list(exam_qps))
            
            # Convert course_codes to integers if needed
            course_codes = [int(code) for code in exam_qps]
            print("Converted Course Codes:", course_codes)
            
            # Retrieve course titles from Scheme_Details based on course codes
            courses = Scheme_Details.objects.filter(scheme_details_id__in=course_codes).values('course_code', 'course_title')
            print("Courses Found:", list(courses))
            
            # Construct the list of subjects
            subjects = list(courses)
            
            return JsonResponse({'subjects': subjects})
        
        except Scheme_Details.DoesNotExist:
            return JsonResponse({'error': 'Courses not found'}, status=404)
        
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def fetch_faculty_by_course(request):
    course_code = request.GET.get('course_code')
    
    if course_code:
        # Retrieve unique faculty IDs for the selected course code
        unique_faculty_ids = Faculty_Course_Allotment.objects.filter(course_code__course_code=course_code).values_list('employee_emp_id', flat=True).distinct()
        
        # Fetch full details of the unique faculties
        faculty_list = Employee_Details.objects.filter(employee_emp_id__in=unique_faculty_ids)

        # Prepare data for JSON response
        faculty_data = [
            {
                'faculty_id': faculty.employee_emp_id,
                'name': faculty.employee_name,
                'course_code': course_code  # Assuming course_code is the same for all entries
            }
            for faculty in faculty_list
        ]
        
        return JsonResponse({'faculty': faculty_data})
    
    return JsonResponse({'error': 'Course code not provided'}, status=400)
    
def valuator(request):
    if request.method == "POST":
        # Retrieve form data
        exam_id1 = request.POST.get('exam_id')
        department_id = request.POST.get('department_id')
        subject_code = request.POST.get('sub')
        reporting_date = request.POST.get('reportingDate')
        reporting_time = request.POST.get('reportingTime')
        num_scripts = request.POST.get('numScripts')
        complete_within = request.POST.get('completeWithin')
        num_valuators = request.POST.get('numValuators')
        faculty_ids = request.POST.getlist('faculty_ids')
        semester = request.POST.get('semester')
        hall_id=[]
        hall_details=[]
        hello=Exam_HallTicket.objects.filter(exam_id=exam_id1)
        for i in hello:
            hall_id.append(i.hall_ticket_id)


        for i in hall_id:
            hall_details.append(Exam_HallTicket_Details.objects.filter(hall_ticket_id_id=int(i)))
        course_id = Scheme_Details.objects.get(course_code=subject_code).scheme_details_id
        count=0
        print("/////////////")
        print(hall_details)
        unique_faculty_ids = Faculty_Course_Allotment.objects.filter(course_code=subject_code).values_list('employee_emp_id', flat=True).distinct()
        print(unique_faculty_ids.count())
        for i in hall_details:
            if i :
                for j in i:
                    if(Academics_Master_Details.objects.get(academics_master_details_id=j.academics_master_details_id_id,scheme_details_id=course_id)):
                        count += 1

        print(count)
        total_count=count
        total=int(unique_faculty_ids.count())
        num_of_papers=[]
        time=[]
        for i in range (0,total):
            if i == total-1:
                num_of_papers.append(total_count-count)
            else:
                num_of_papers.append(math.floor(count/total))
                count=count-(math.floor(count/total))
        print("/////////////////////////")
        print(num_of_papers)
        for i in num_of_papers:
            time.append(math.ceil(i/25))
        




        # Fetch additional data if needed
        faculty_list = []
        employee_name=[]
        department_name=[]
        for faculty_id in faculty_ids:
            employee_name.append(Employee_Details.objects.get(employee_emp_id=faculty_id).employee_name)
            department_name.append(Employee_Details.objects.get(employee_emp_id=faculty_id).employee_dept_id)




        for i in range(0,total):

            faculty_list.append({
                'name': employee_name[i],
                'department': department_name[i],
                'num_scripts': num_of_papers[i],
                'complete_within': time[i]
            })
        desc = Exam_Details.objects.get(exam_details_id=exam_id1).description
        semester = Exam_Details.objects.get(exam_details_id=exam_id1).semester
        course_title = Scheme_Details.objects.get(course_code=subject_code).course_title

        # Prepare context for the report
        context = {
            'semester': semester,
            'desc': desc,
            'course_title': course_title,
            'exam': exam_id1,
            'subject': subject_code,
            'reporting_date': reporting_date,
            'reporting_time': reporting_time,
            'num_valuators': str(total),
            'faculty_list': faculty_list,
            'department_id': department_id

        }

        # Render the report template with the context
        
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; attachment; filename=' + "Results.pdf"
        response['C+ontent-Transfer-Encoding'] = 'binary'
        html_string = render_to_string('valuationAnswerScript.html', context)               
        html = HTML(string=html_string, base_url=request.build_absolute_uri())

        result = html.write_pdf()
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()

            output = open(output.name, 'rb')
            response.write(output.read())
        return response
        

    else:
        exams = Exam_Details.objects.all()
        departments = Department.objects.all()
        
        return render(request, "report_valuator.html", {'exams': exams,'departments':departments})

def load_courses_for_exam(request):
    department = request.GET.get('department')
    exam_id = request.GET.get('exam_id')
    print(department,exam_id)
    print("ppppppppppppppp")
    acad_cal_id=Exam_Details.objects.get(exam_details_id=exam_id).acad_cal_id
    semester=Exam_Details.objects.get(exam_details_id=exam_id).semester
    series = Scheme_Allotment.objects.get(acad_cal_id=acad_cal_id,course_sem=semester).scheme_series
    print(acad_cal_id,series)
    courselist = Scheme_Details.objects.filter(sem_allotted=semester, scheme_series=series, offered_by=department).order_by('course_code')
    print(courselist,"ppppppppppp")
    course_list_html = render_to_string('course_code_dropdown.html', {'courselist': courselist})
    print(course_list_html)
 
    return JsonResponse({'html': course_list_html})

        
    
    
    