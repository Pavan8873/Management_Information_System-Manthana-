from operator import truediv
from ssl import AlertDescription
from stat import ST_UID
from venv import create
from webbrowser import get
from django.db import IntegrityError
from django.shortcuts import render
from academics.models import *
import secrets
from PIL import Image
import base64
import io
import requests
import json
from django.core.files.base import ContentFile
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.conf import settings
import tempfile
from django.db.models.aggregates import Count
#from django.utils.http import urlquote
from admission.EmailBackEnd import EmailBackEnd
from django.urls.base import reverse
from django.template.loader import render_to_string
from admission.models import CustomUser
from weasyprint import HTML
from django.db.models import Sum
from admission.models import Student_Details
from master_mgmt.models import AcademicYear, Department
from hr.models import Employee_Details
from django.db.models import Q
from django.db.models import Exists  #11 Apr
from django.db import DatabaseError, transaction
#from .EmailBackEnd import EmailBackEnd
#from django.utils.http import urlquote
import csv
from django.http import JsonResponse
from master_mgmt.models import * 
from academics.session_attendance import check_students,student_present,student_absent,edit_student_present,edit_student_absent
from datetime import datetime
import itertools
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
def ug_acad_calender(request):
    acad_year_tbl = AcademicYear.objects.all().order_by('-acayear')
    return render(request, "ug_acad_calender.html" ,{'acad_year_tbl':acad_year_tbl})

def faculty_course_allotment(request):
    dept = Department.objects.all()
    academic_year = AcademicYear.objects.all()
    div_tbl = Division.objects.all().order_by('division')
    return render(request, "faculty_course_allotment.html", {'dept': dept, 'academic_year':academic_year,'div_tbl':div_tbl})

def load_faculty(request):
    dept_id = request.GET.get('offered_by')
    dept_faculty_list = Employee_Details.objects.filter(employee_dept_id_id=dept_id).order_by('employee_emp_id')
    return render(request, "faculty_id_dropdown_list.html", {'dept_faculty_list': dept_faculty_list})

# def load_courses(request):
#     courselist = None
#     try:t
#         acad_cal_id = None
#         acad_year = request.GET.get('acad_year')
#         print(acad_year)
#         print("into load courses")
#         # aca_year=AcademicYear.objects.get(acayear=acad_year)
#         sem = request.GET.get('sem')
#         print(sem)
#         acad_cal_type=request.GET.get('acad_cal_type')
#         acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year,acad_cal_sem=sem,acad_cal_type=acad_cal_type)
#     # acad_cal_cnt = Academic_Calendar.objects.filter(acad_cal_acad_year= acad_year,acad_cal_sem=sem).count()
#     # if acad_cal_cnt == 0:
#         # messages.error(request, "Please check Academic Year and retry")
#         # dept = Department.objects.all()
#         # academic_year = AcademicYear.objects.all()
#         # return render(request, "faculty_course_allotment.html", {'dept': dept, 'academic_year':academic_year})
#         # return HttpResponseRedirect(reverse("FacultyCourseAllot"))
        
#     except Academic_Calendar.DoesNotExist:
#         return JsonResponse({"error":"Please check Academic Year and retry"},status=500)
#     # print("exc thrown")
#     # messages.error(request, "Please check Academic Year and retry")
#     # return faculty_course_allotment(request)
#     # dept = Department.objects.all()
#     # academic_year = AcademicYear.objects.all()
#     # return render(request, "faculty_course_allotment.html", {'dept': dept, 'academic_year':academic_year})
#         # return HttpResponseRedirect('FacultyCourseAllot')

#     try:
#         series = Scheme_Allotment.objects.get(acad_cal_id=acad_cal_id,course_sem=sem).scheme_series
#         dept_id = request.GET.get('offered_by')
#         courselist = Scheme_Details.objects.filter(sem_allotted=sem, scheme_series=series, offered_by=dept_id).order_by('course_code')
#         print(courselist)
#     except Scheme_Allotment.DoesNotExist:
#         return JsonResponse({"error":"Scheme is NOT allotted for the AY"},status=500)
    
#     if courselist is None:
#         return JsonResponse({"error":"No courses offered by this dept in this sem."},status=500)

#     # messages.error(request, "No courses offered by this dept in this sem. Enter correct data")
#     # return render(request, "faculty_course_allotment.html")
#     print(courselist,"courselistcourselist")
#     return render(request, "course_code_dropdown.html", {'courselist': courselist})

def load_UG_courses(request):
    dept_id = request.GET.get('offered_by') # changed from batch to offered_by
    sem = request.GET.get('sem')
    acad_year = request.GET.get('acad_year')
    acad_year_id = AcademicYear.objects.get(acayear=acad_year).id
    acad_cal_id = None
    courselist = None
    series = None
    print("kkk")
    try:
        acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year_id,acad_cal_sem=sem)
    except Exception:
        messages.error(request,"Please select correct AY and Sem")
        return UGCourseRegistration(request)
    try:
        print(acad_cal_id)
        print(sem)
        series = Scheme_Allotment.objects.get(acad_cal_id=acad_cal_id,course_sem=sem).scheme_series
        print(series)
    except Scheme_Allotment.DoesNotExist:
        messages.error(request,"Scheme is NOT yet allotted for the AY")
        return UGCourseRegistration(request)
    try:
        print(series)
        courselist = Scheme_Details.objects.filter(sem_allotted=sem, scheme_series=series, offered_by_id=dept_id).order_by('course_code')
    except Scheme_Details.DoesNotExist:
        messages.error(request,"No subjects found to register!")
        return UGCourseRegistration(request)
    
    return render(request, "UG_course_code_dropdown.html", {'courselist': courselist})

def load_sem(request):
    dept_id = request.GET.get('offered_by')
    sem_id = Scheme_Details.objects.filter(offered_by_id=dept_id).order_by('sem_allotted')
    return render(request, "sem_dropdown.html", {'sem_id': sem_id})

def SchemeAllotment(request):
    acad_year_tbl = AcademicYear.objects.all().order_by('-acayear')
    return render(request, "SchemeAllotment.html" ,{'acad_year_tbl':acad_year_tbl})

def AddSchemeDetails(request):
    return render(request,"addSchemeDetails.html",{'department': Department.objects.all})

# def Student_Attendance(request):
#     return render(request,"student_attendance.html",{'div_tbl':Division.objects.all(),'calender': Academic_Calendar.objects.all(),'scheme_detail':Scheme_Details.objects.all()})

def load_student(request):
    st_list = None
    try:
        acadyear= request.GET.get('academic_year')
       
        sem = int(request.GET.get('course_sem'))
        dep = request.GET.get('dep')
        acad_cal_type = request.GET.get("acad_cal_type")
        # acadcal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_yr,acad_cal_sem=sem,)
        acadcal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id=acadyear,acad_cal_sem=sem,acad_cal_type=acad_cal_type)
        print(acadyear,sem,dep,acadcal_id,"lllll")

        #Working code 
        # st_list = Student_Details.objects.filter(st_acad_year=acadyear).order_by('st_uid')
        
        # for st in st_list:
        #     #uid = st.uid
        #     #To check if a student is already allotted a division
        #     allotted_st_list = Student_Division_Allotment.objects.filter(acad_cal_id=acadcal_id,st_uid=st.st_uid)
        #     st_uid_values = allotted_st_list.values('st_uid')
        #     #print(str(allotted_st_list))
        #     for allot_st in allotted_st_list:
        #         st_list = st_list.exclude(st_uid__in = st_uid_values)
        #     print(st_list)
        
        #Alternate approach without loops
        st_list = Student_Details.objects.filter(st_acad_year=acadyear,st_branch_applied_id=dep).order_by('st_uid')
       
        st_list_uid_vals = st_list.values('st_uid')
        st_div_allotted_uid_values = Student_Division_Allotment.objects.filter(acad_cal_id=acadcal_id,st_uid__in=st_list_uid_vals).values('st_uid')

        st_list = st_list.exclude(st_uid__in = st_div_allotted_uid_values)
        # paginator = Paginator(st_list, 10) # Show 10 students per page
        # page_number = request.GET.get('page') # Get the current page number from request
        # page_obj = paginator.get_page(page_number) # Get the page object for the current page


        

    except Exception as e:
        print(e)
        return JsonResponse({"error":e},status=500)
    return render(request, "loadstudent.html",{'st_list':st_list})

#To load students while allotting division to them
def ugload_student(request):
    st_list = None
    st_div_allotted_uid_values = None
    try:
        acadyear= request.GET.get('academic_year')
        sem = int(request.GET.get('course_sem'))
        dept_id = request.GET.get('offered_by')
        print(acadyear,sem,dept_id)
        acadcal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id=acadyear,acad_cal_sem=sem)
        print("////////////////////")
        print(acadcal_id,"acadcal_id")
        
        # st_list = Student_Promotion_List.objects.filter(acad_cal_id=acadcal_id,offered_by=dept_id,semester=sem).order_by('st_uid')
        # for st in st_list:
        #     #uid = st.uid
        #     allotted_st_list = UG_Student_Division_Allotment.objects.filter(acad_cal_id=acadcal_id,st_uid=st.st_uid).values('st_uid')
        #     st_uid_vales = allotted_st_list.values('st_uid')
        #     print(str(allotted_st_list))
        #     for allot_st in allotted_st_list:
        #         st_list = st_list.exclude(st_uid__in = st_uid_vales)
        #     print(st_list)

        #Alternate approach without loops
        st_list = Student_Promotion_List.objects.filter(acad_cal_id_odd=acadcal_id,offered_by=dept_id).values('st_uid','st_name')
        if st_list:
            print("st list for div allot")
            print(st_list)
            # To avoid duplicate entry in UG_Student_Division_Allotment
            st_list_uid_vals = st_list.values('st_uid')
            st_div_allotted_uid_values = UG_Student_Division_Allotment.objects.filter(acad_cal_id=acadcal_id,st_uid__in=st_list_uid_vals).values('st_uid')
            print("already allotted list")
            print(st_div_allotted_uid_values)
            st_list = st_list.exclude(st_uid__in = st_div_allotted_uid_values)
            print("2024-07-042024-07-042024-07-04",st_list)
        else:
            print("bbb",acadcal_id,sem-1)
            acadcal_id1 = Academic_Calendar.objects.get(acad_cal_acad_year_id=acadyear,acad_cal_sem=sem-1)
            print("bbb",acadcal_id1)
            st_list = Student_Promotion_List.objects.filter(acad_cal_id_odd=acadcal_id1,offered_by=dept_id).values('st_uid','st_name')
            print(st_list,"st_list")
    except Academic_Calendar.DoesNotExist:
        return JsonResponse({"error":"Please check AY and re-enter"},status=500)
    return render(request, "ugloadstudents.html",{'st_list':st_list})



def First_year_StudentDivisionAllotment(request):

    std = Student_Details.objects.all()
    dv = Cycle_Division_allotment.objects.all()
    academic_year = AcademicYear.objects.all()
    div_tbl = Division.objects.all().order_by('division')
    return render(request,"First_year_StudentDivisionAllotment.html",{'std':std,'dv':dv,'academic_year':academic_year,'div_tbl':div_tbl,'dep':Department.objects.all()})

def UGStudentDivisionAllotment(request):
    dept = Department.objects.all()
    acad_year_tbl = AcademicYear.objects.all().order_by('-acayear') # desc order
    div_tbl = Division.objects.all().order_by('division')[:2]
    # acad_year_tbl = AcademicYear.objects.all().order_by('-acayear')[:2]
    return render(request,"UG_Student_Division_Allotment.html",{'dept': dept, 'acad_year_tbl':acad_year_tbl,'div_tbl':div_tbl})

def CycleDivisionAllotment(request):
    cyd = Department.objects.all()
    academic_year = AcademicYear.objects.all()
    div_tbl = Division.objects.all().order_by('division')
    return render(request,"CycleDivisionAllotment.html",{'calender': Academic_Calendar.objects.values('acad_cal_acad_year').distinct(),'cd':cyd, 'academic_year':academic_year,'div_tbl':div_tbl})
def Edit_CycleDivisionAllotment(request, cycle_div_allot_id, acad_cal_id):
    cyde = Cycle_Division_allotment.objects.get(cycle_div_allot_id = cycle_div_allot_id)
    cyd = Cycle_Division_allotment.objects.all()
    acad_obj = Academic_Calendar.objects.get(acad_cal_id = acad_cal_id)
    # messages.success(request, "Division allotment Updated Successfully")    
    return render(request,"CycleDivisionAllotment.html",{'calender': Academic_Calendar.objects.values('acad_cal_acad_year').distinct(),'cde':cyde,'cd':cyd,'acd':acad_obj})

def FirstYearCourseDetails(request):
    return render(request,"FirstYearCourseDetails.html")

def view_calender(request):
    acad_cal_obj = Academic_Calendar.objects.all()
    acad_year_tbl = AcademicYear.objects.all().order_by('-acayear')
    return render(request,"view_academic_calender.html",{'acad_cal_obj':acad_cal_obj, 'acad_year_tbl':acad_year_tbl})


def edit_calender(request, acad_cal_id):
    acad_cal_obj = Academic_Calendar.objects.get(acad_cal_id = acad_cal_id)
    print("acad_cal_obj",acad_cal_obj.acad_cal_id)
    acad_year_tbl = AcademicYear.objects.all().order_by('-acayear')
    return render(request,"ug_acad_calender.html",{'acad_cal_obj':acad_cal_obj, 'acad_year_tbl':acad_year_tbl})
def print_calender(request,acad_cal_id):
    acad_cal_obj = Academic_Calendar.objects.get(acad_cal_id = acad_cal_id)
    acad_year_tbl = AcademicYear.objects.all().order_by('-acayear')
    return render(request,"Printacdcal.html",{'acad_cal_obj':acad_cal_obj, 'acad_year_tbl':acad_year_tbl})

def addcalender(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        cal_acad_year = None
        cal_sem = None
        cal_induction_program_from = None
        cal_induction_program_to = None
        cal_teaching_commences = None
        cal_reg_date_from = None
        cal_reg_date_to = None
        cal_reg_last_date_fee = None
        cal_att_display_ia_1 = None
        cal_ia_1_from = None
        cal_ia_1_to = None
        cal_commn_to_parent_ia_1 = None
        cal_drop_course = None
        cal_att_display_ia_2 = None
        cal_ia_2_from = None
        cal_ia_2_to = None
        cal_commn_to_parent_ia_2 = None
        cal_withdraw_course = None
        cal_parents_meet = None
        cal_st_feedback_from = None
        cal_st_feedback_to = None
        cal_ia_3_from = None
        cal_ia_3_to = None
        cal_last_day_teaching = None
        cal_see_lab_from = None
        cal_see_lab_to = None
        cal_cie_marks_display = None
        cal_attendance_display = None
        cal_commn_to_parent_cie = None
        cal_see_theory_from = None
        cal_see_theory_to = None
        cal_intersem_recess_from = None
        cal_intersem_recess_to = None
        cal_results_declaration = None
        cal_makeup_from = None
        cal_makeup_to = None
        acad_cal_type=None

        try:
            cal_acad_year = request.POST.get("acad_cal_acad_year")
            print(cal_acad_year)
            acad_cal_type = request.POST.get("acad_cal_type")
            print(acad_cal_type,"kk")
            cal_sem = int(request.POST.get("acad_cal_sem"))
            cal_induction_program_from = request.POST.get("acad_cal_induction_program_from")
            cal_induction_program_to = request.POST.get("acad_cal_induction_program_to")
            cal_teaching_commences = request.POST.get("acad_cal_teaching_commences")
            cal_reg_date_from = request.POST.get("acad_cal_reg_date_from")
            cal_reg_date_to = request.POST.get("acad_cal_reg_date_to")
            cal_reg_last_date_fee = request.POST.get("acad_cal_reg_last_date_fee")
            cal_att_display_ia_1 = request.POST.get("acad_cal_att_display_ia_1")
            cal_ia_1_from = request.POST.get("acad_cal_ia_1_from")
            cal_ia_1_to = request.POST.get("acad_cal_ia_1_to")
            cal_commn_to_parent_ia_1 = request.POST.get("acad_cal_commn_to_parent_ia_1")
            cal_drop_course = request.POST.get("acad_cal_drop_course")
            cal_att_display_ia_2 = request.POST.get("acad_cal_att_display_ia_2")
            cal_ia_2_from = request.POST.get("acad_cal_ia_2_from")
            cal_ia_2_to = request.POST.get("acad_cal_ia_2_to")
            cal_commn_to_parent_ia_2 = request.POST.get("acad_cal_commn_to_parent_ia_2")
            cal_withdraw_course = request.POST.get("acad_cal_withdraw_course")
            cal_parents_meet = request.POST.get("acad_cal_parents_meet")
            cal_st_feedback_from = request.POST.get("acad_cal_st_feedback_from")
            cal_st_feedback_to = request.POST.get("acad_cal_st_feedback_to")
            cal_ia_3_from = request.POST.get("acad_cal_ia_3_from")
            cal_ia_3_to = request.POST.get("acad_cal_ia_3_to")
            cal_last_day_teaching = request.POST.get("acad_cal_last_day_teaching")
            cal_see_lab_from = request.POST.get("acad_cal_see_lab_from")
            cal_see_lab_to = request.POST.get("acad_cal_see_lab_to")
            cal_cie_marks_display = request.POST.get("acad_cal_cie_marks_display")
            cal_attendance_display = request.POST.get("acad_cal_attendance_display")
            cal_commn_to_parent_cie = request.POST.get("acad_cal_commn_to_parent_cie")
            cal_see_theory_from = request.POST.get("acad_cal_see_theory_from")
            cal_see_theory_to = request.POST.get("acad_cal_see_theory_to")
            cal_intersem_recess_from = request.POST.get("acad_cal_intersem_recess_from")
            cal_intersem_recess_to = request.POST.get("acad_cal_intersem_recess_to")
            cal_results_declaration = request.POST.get("acad_cal_results_declaration")
            cal_makeup_from = request.POST.get("acad_cal_makeup_from")
            cal_makeup_to = request.POST.get("acad_cal_makeup_to")
            print("ll")

        except:
            pass

        btn_value = request.POST["btn_acad_cal"]
        print(btn_value,"p")
        if btn_value == "register":
            print("po")
            try:
                if Academic_Calendar.objects.filter(acad_cal_acad_year=AcademicYear.objects.get(id=cal_acad_year),acad_cal_sem=cal_sem,acad_cal_type=acad_cal_type).exists():
                    messages.error(request, "An academic calendar entry for this year and semester already exists.")
                else:
                    acad_cal_obj = Academic_Calendar.objects.create(acad_cal_acad_year=AcademicYear.objects.get(id=cal_acad_year), acad_cal_sem=cal_sem,
                                                                    acad_cal_induction_program_from=cal_induction_program_from, acad_cal_induction_program_to=cal_induction_program_to, acad_cal_teaching_commences=cal_teaching_commences,
                                                                    acad_cal_reg_date_from=cal_reg_date_from, acad_cal_reg_date_to=cal_reg_date_to, acad_cal_reg_last_date_fee=cal_reg_last_date_fee,
                                                                    acad_cal_att_display_ia_1=cal_att_display_ia_1, acad_cal_ia_1_from=cal_ia_1_from, acad_cal_ia_1_to=cal_ia_1_to,
                                                                    acad_cal_commn_to_parent_ia_1=cal_commn_to_parent_ia_1, acad_cal_drop_course=cal_drop_course, acad_cal_att_display_ia_2=cal_att_display_ia_2,
                                                                    acad_cal_ia_2_from=cal_ia_2_from, acad_cal_ia_2_to=cal_ia_2_to, acad_cal_commn_to_parent_ia_2=cal_commn_to_parent_ia_2, acad_cal_withdraw_course=cal_withdraw_course,
                                                                    acad_cal_parents_meet=cal_parents_meet, acad_cal_st_feedback_from=cal_st_feedback_from, acad_cal_st_feedback_to=cal_st_feedback_to, acad_cal_ia_3_from=cal_ia_3_from,
                                                                    acad_cal_ia_3_to=cal_ia_3_to, acad_cal_last_day_teaching=cal_last_day_teaching, acad_cal_see_lab_from=cal_see_lab_from, acad_cal_see_lab_to=cal_see_lab_to, acad_cal_cie_marks_display=cal_cie_marks_display,
                                                                    acad_cal_attendance_display=cal_attendance_display, acad_cal_commn_to_parent_cie=cal_commn_to_parent_cie, acad_cal_see_theory_from=cal_see_theory_from, acad_cal_see_theory_to=cal_see_theory_to,
                                                                    acad_cal_intersem_recess_from=cal_intersem_recess_from, acad_cal_intersem_recess_to=cal_intersem_recess_to, acad_cal_results_declaration=cal_results_declaration, acad_cal_makeup_from=cal_makeup_from,
                                                                    acad_cal_makeup_to=cal_makeup_to,acad_cal_type=acad_cal_type)

                    messages.success(request, "Academic Calender Created Successfully")
            except IntegrityError:
            # Handle the case where an integrity error occurs (e.g., unique constraint violation)
                messages.error(request, "Error! A record with these details already exists.")

        elif btn_value == "update":
            acad_cal_id = request.POST.get('acad_cal_id')
            print(acad_cal_id)
            acad_cal_obj = Academic_Calendar.objects.get(acad_cal_id = acad_cal_id)
            print(cal_acad_year)
            print(AcademicYear.objects.get(id=cal_acad_year),"ji")
            acad_cal_obj.acad_cal_acad_year = AcademicYear.objects.get(id=cal_acad_year)
            acad_cal_obj.acad_cal_sem = cal_sem
            acad_cal_obj.acad_cal_induction_program_from = cal_induction_program_from
            acad_cal_obj.acad_cal_induction_program_to = cal_induction_program_to
            acad_cal_obj.acad_cal_teaching_commences = cal_teaching_commences
            acad_cal_obj.acad_cal_reg_date_from = cal_reg_date_from
            acad_cal_obj.acad_cal_reg_date_to = cal_reg_date_to
            acad_cal_obj.acad_cal_reg_last_date_fee = cal_reg_last_date_fee
            acad_cal_obj.acad_cal_att_display_ia_1 = cal_att_display_ia_1
            acad_cal_obj.acad_cal_ia_1_from = cal_ia_1_from
            acad_cal_obj.acad_cal_ia_1_to = cal_ia_1_to
            acad_cal_obj.acad_cal_commn_to_parent_ia_1 = cal_commn_to_parent_ia_1
            acad_cal_obj.acad_cal_drop_course = cal_drop_course
            acad_cal_obj.acad_cal_att_display_ia_2 = cal_att_display_ia_2
            acad_cal_obj.acad_cal_ia_2_from = cal_ia_2_from
            acad_cal_obj.acad_cal_ia_2_to = cal_ia_2_to
            acad_cal_obj.acad_cal_commn_to_parent_ia_2 = cal_commn_to_parent_ia_2
            acad_cal_obj.acad_cal_withdraw_course = cal_withdraw_course
            acad_cal_obj.acad_cal_parents_meet = cal_parents_meet
            acad_cal_obj.acad_cal_st_feedback_from = cal_st_feedback_from
            acad_cal_obj.acad_cal_st_feedback_to = cal_st_feedback_to
            acad_cal_obj.acad_cal_ia_3_from = cal_ia_3_from
            acad_cal_obj.acad_cal_ia_3_to = cal_ia_3_to
            acad_cal_obj.acad_cal_last_day_teaching = cal_last_day_teaching
            acad_cal_obj.acad_cal_see_lab_from = cal_see_lab_from
            acad_cal_obj.acad_cal_see_lab_to = cal_see_lab_to
            acad_cal_obj.acad_cal_cie_marks_display = cal_cie_marks_display
            acad_cal_obj.acad_cal_attendance_display = cal_attendance_display
            acad_cal_obj.acad_cal_commn_to_parent_cie = cal_commn_to_parent_cie
            acad_cal_obj.acad_cal_see_theory_from = cal_see_theory_from
            acad_cal_obj.acad_cal_see_theory_to = cal_see_theory_to
            acad_cal_obj.acad_cal_intersem_recess_from = cal_intersem_recess_from
            acad_cal_obj.acad_cal_intersem_recess_to = cal_intersem_recess_to
            acad_cal_obj.acad_cal_results_declaration = cal_results_declaration
            acad_cal_obj.acad_cal_makeup_from = cal_makeup_from
            acad_cal_obj.acad_cal_makeup_to = cal_makeup_to
            acad_cal_obj.acad_cal_type=acad_cal_type
            acad_cal_obj.save()

            messages.success(request, "Calender Updated Successfully")
    
    return render(request,"view_academic_calender.html")

def allotScheme(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        sem = None
        series = None
        acad_yr = None
        acadcal_id = None
        #Scheme_id = None
        try:
            sem = int(request.POST.get("course_sem"))
            series = int(request.POST.get("scheme_series"))
            acad_yr = request.POST.get("acad_cal_acad_year")
            acad_cal_type = request.POST.get("acad_cal_type")
            acadcal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_yr,acad_cal_sem=sem,acad_cal_type=acad_cal_type)
            print(acadcal_id)
        except Academic_Calendar.DoesNotExist:
            messages.error(request, "Please check Academic Year and enter")
            return render(request,"SchemeAllotment.html") 
        except Exception as e:
            print(e)
            messages.error(request, "Scheme could not be allotted")
            return render(request,"SchemeAllotment.html") 

        try:
            btn_value = request.POST["btn_clicked"]
            if btn_value == "register":    
                scheme_allot = Scheme_Allotment.objects.create(acad_cal_id=acadcal_id,course_sem=sem,scheme_series=series)
                scheme_allot.save()
                messages.success(request, "Allotted Scheme for the Year")
                return render(request,"SchemeAllotment.html")
        except IntegrityError:
            messages.warning(request, "Scheme already exists for Sem-"+str(sem)+" in the AY "+acad_yr)
            return render(request,"SchemeAllotment.html")

def addschemedetails(request):
    if request.method!="POST":
        return render(request,"addSchemeDetails.html",{'department':Department.objects.all()})
    else:
        btn_value = request.POST["btn_clicked"]
        course_code = None
        course_title = None
        sem_allotted = None
        credits = None
        ltps = None
        course_type = None
        is_credit = None
        scheme_series = None
        dept = None
        max_cie_marks = None
        min_cie_marks = None
        max_see_marks = None
        min_see_marks = None
        min_total_pass_marks = None
        max_total_marks = None
        deduct = 0
        program=0
        program_select=None
        open=0
        open_select=None
        
        try:
            course_code = request.POST.get("course_code")
            course_title = request.POST.get("course_title")
            sem_allotted = int(request.POST.get("sem_allotted"))
            is_credit = request.POST.get("is_credit")
            credits = int(request.POST.get("credits"))
            
        except:
            if credits is None:
                credits = 0
        try:
            ltps = request.POST.get("ltps")
            course_type = request.POST.get("course_type")
            branch = request.POST.get("offered_by")
            dept_id = Department.objects.get(dept_id=branch)
            scheme_series = int(request.POST.get("scheme_series"))
            max_cie_marks = int(request.POST.get("max_cie_marks"))
            min_cie_marks = int(request.POST.get("min_cie_marks"))
            max_see_marks = int(request.POST.get("max_see_marks"))
            min_see_marks = int(request.POST.get("min_see_marks"))
        except:
            if max_see_marks is None:
                max_see_marks = 0
            if min_see_marks is None:
                min_see_marks = 0
                
        try:
            deduct = request.POST.get("deduction") 
        except:
            pass
        program_select = (request.POST.get("myDropdown"))
        open_select = (request.POST.get("myDropdown1"))    
        max_total_marks = max_cie_marks + max_see_marks
        min_total_pass_marks = min_cie_marks + min_see_marks

        btn_value = request.POST["btn_clicked"]

        print("button value:",program_select,open_select)
        scho=Scheme_Details.objects.filter(sem_allotted=sem_allotted,offered_by=branch)
        if btn_value == "register":
            try:
                scheme_details = Scheme_Details.objects.create(course_code=course_code,course_title=course_title,
                sem_allotted=sem_allotted,credits=credits,ltps=ltps,course_type=course_type,is_credit=is_credit,
                scheme_series=scheme_series,offered_by=dept_id,max_cie_marks=max_cie_marks,min_cie_marks=min_cie_marks,
                max_see_marks=max_see_marks,min_see_marks=min_see_marks,max_total_marks=max_total_marks,min_total_pass_marks=min_total_pass_marks,deduction=deduct,open=open_select,program=program_select)
                scheme_details.save()

                messages.success(request, "Success! Added Details for the Subject" + scheme_details.course_code)
                
                #return addSchemeDetails.html CHECK html name
                
                return render(request,"addSchemeDetails.html",{'scho':scho,'department':Department.objects.all()})
            except IntegrityError:
                # Handle the case where a duplicate entry is attempted
                messages.error(request, "Error! A record with this course code already exists.")
                return render(request,"addSchemeDetails.html",{'scho':scho,'department':Department.objects.all()})
        
        elif btn_value == "update":
            print("sumanthaaaa")
            print("Inside update")
            dirty = 0
            scheme=request.POST.get('course_code')
            print(scheme)

            hello=Scheme_Details.objects.get(course_code=scheme)
            hello.course_code=course_code
            hello.course_title=course_title
            hello.sem_allotted=sem_allotted
            hello.is_credit=is_credit
            hello.credits=credits
            hello.ltps=ltps
            hello.course_type=course_type
            hello.branch=branch
            hello.dept_id=dept_id
            hello.scheme_series=scheme_series
            hello.max_cie_marks=max_cie_marks
            hello.min_cie_marks=min_cie_marks
            hello.max_see_marks=max_see_marks   
            hello.min_see_marks=min_see_marks
            hello.save()
            # with transaction.atomic():
            #     if hello.is_dirty():
            #         dirty = 1
            #         dirty_fields = hello.get_dirty_fields().keys()
            #         hello.save(update_fields=dirty_fields)
            # if dirty : 
            #     messages.success(request, "Student Updated Successfully with UID")
            # else:
            #     messages.success(request, "No changes were made with UID")
            
            return render(request,"addSchemeDetails.html")

# def allotCourseToFaculty(request):
#     if request.method!="POST":
#         return HttpResponse("<h2>Method Not Allowed</h2>")
#     else:
#         acad_year = None
#         sem = None
#         division = None
#         gui_fac_id = None
#         gui_course_code = None
#         batch = None
#         try:
#             batch = request.POST.get("batch")
#             acad_year = request.POST.get("academic_yr")
           
#             sem = int(request.POST.get("academic_sem"))
#             gui_fac_id = request.POST.get("employee_emp_id") #fetched via GUI
#             acad_cal_type = request.POST.get('acad_cal_type')
#             acad_ob = Academic_Calendar.objects.get(acad_cal_acad_year_id = acad_year,acad_cal_sem=sem,acad_cal_type=acad_cal_type)
#             acad_cal_id = acad_ob.acad_cal_id
#             print(acad_cal_id)
#             '''
#             if .faculty_emp_id is not mentioned then by default auto_id of the table on RHS is fetched
#             faculty_emp_id = (Faculty_Details.objects.get(faculty_emp_id=gui_fac_id)).faculty_emp_id 
#             NOT useful while creating object IF foreign key is not primary key
#             '''
#             division = request.POST.get("division")
#             gui_course_code = request.POST.get("courselist") #fetched via GUI

#         except:
#             messages.error(request, "Could NOT allot the subject!")
#             return faculty_course_allotment(request)

#         try:
#             btn_value = request.POST["btn_clicked"]
#             if btn_value == "register":
#                 schem_ob = Scheme_Details.objects.get(course_code = gui_course_code )
#                 schem_id = schem_ob.scheme_details_id
#                 dept = schem_ob.offered_by
#                 course_type = schem_ob.course_type
#                 course_type = int(course_type)


#                 #===============Only for Theory=====================
#                 if course_type == 1:
#                     batch = 'B0'
#                     if sem == 1 or sem == 2:
#                         st_list = Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id, division=division).order_by('st_uid')
#                     elif sem >= 3 and sem <= 8:
#                         print("allotCourseToFaculty")
#                         print(acad_cal_id)
#                         print(division)
#                         st_list = UG_Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id, ug_division_id=division).order_by('st_uid')
#                         print(st_list)
                    
#                     l = len(st_list)
#                     print("hello", st_list)
#                     st_list_uid_vals = st_list.values('st_uid')

#                     st_list = [entry for entry in st_list_uid_vals]  
                    
#                     sid = []
                    
#                     for i in range(0, l):
#                         sid.append(st_list[i]['st_uid'])

#                     div_id = Division.objects.get(id=division)
                    
#                     for st in sid:
#                         st_uid = st
#                         print("uid", st_uid)
                        
#                         try:
#                             stud_attd = student_attendance.objects.create(
#                                 acad_cal_id=Academic_Calendar.objects.get(acad_cal_acad_year=acad_year, acad_cal_sem=sem, acad_cal_type=acad_cal_type),
#                                 scheme_details_id=Scheme_Details.objects.get(course_code=gui_course_code),
#                                 division=division,
#                                 faculty_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
#                                 st_uid=Student_Details.objects.get(st_uid=st_uid),
#                                 status="0",
#                                 batch_no='B0'
#                             )
#                             stud_attd.save()
#                             print("Attendance record created for student", st_uid)
                        
#                         except IntegrityError as e:
#                             print(f"Duplicate entry for student attendance record for student {st_uid}: {e}")
#                             messages.error(request, f"Attendance record for student {st_uid} already exists.")
                        
#                         except Exception as e:
#                             print(f"Error creating student attendance record for student {st_uid}: {e}")
#                             messages.error(request, f"Error creating attendance record for student {st_uid}")

#                     try:
#                         faculty_course_allotment_obj = Faculty_Course_Allotment.objects.create(
#                             session_count=0,
#                             batch_no='B0',
#                             employee_emp_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
#                             acad_year_id=acad_year,
#                             sem=sem,
#                             division=div_id,
#                             course_code=Scheme_Details.objects.get(course_code=gui_course_code)
#                         )
#                         faculty_course_allotment_obj.save()
#                         print("Faculty course allotment record created")
#                         messages.success(request, "Allotted " + gui_course_code + " to the faculty member " + gui_fac_id)
                    
#                     except IntegrityError as e:
#                         print(f"Duplicate entry for faculty course allotment record: {e}")
#                         messages.error(request, "Course " + gui_course_code + " is already allotted to the faculty member " + gui_fac_id)
                    
#                     except Exception as e:
#                         print(f"Error creating faculty course allotment record: {e}")
#                         messages.error(request, "Error allotting course " + gui_course_code + " to faculty member " + gui_fac_id)

#                 #===============Only for Lab=====================
#                 sid = []
#                 st_list = []
#                 if course_type == 2:
#                     print("____Attendance for lab______")

#                     if sem == 1 or sem == 2:
#                         st_list = Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id, division=division).order_by('st_uid')
#                     elif sem >= 3 and sem <= 8:
#                         st_list = UG_Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id, ug_division=division).order_by('st_uid')
                    
#                     print(st_list)
#                     l = len(st_list)
#                     st_list_uid_vals = st_list.values('st_uid')

#                     st_list = [entry for entry in st_list_uid_vals]  

#                     sid = [entry['st_uid'] for entry in st_list]

#                     for i in range(l):
#                         print(sid[i])

#                     print(acad_cal_id)
#                     print(schem_id)
#                     print(batch)
#                     print(sem)
#                     if sem == 1 or sem == 2:
#                         batch_student_id = First_Year_Student_Course_Registration_Details.objects.filter(acad_cal_id=acad_cal_id, scheme_details_id=schem_id, semester=sem).order_by('st_uid')
#                     else:
#                         batch_student_id = UG_Student_Course_Registration_Details.objects.filter(acad_cal_id=acad_cal_id, scheme_details_id=schem_id, batch_no=batch, semester=sem).order_by('st_uid')

#                     print(batch_student_id)

#                     l = len(batch_student_id)
#                     batch_student_id_vals = batch_student_id.values('st_uid')

#                     batch_st_list = [entry for entry in batch_student_id_vals]  

#                     batch_sid = [entry['st_uid'] for entry in batch_st_list]

#                     final_selected_students = [value for value in sid if value in batch_sid] 

#                     print(final_selected_students)
#                     print(type(final_selected_students))

#                     for st in final_selected_students:
#                         st_uid = st
#                         try:
#                             stud_attd = student_attendance.objects.create(
#                                 acad_cal_id=Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year, acad_cal_sem=sem, acad_cal_type=acad_cal_type),
#                                 scheme_details_id=Scheme_Details.objects.get(course_code=gui_course_code),
#                                 division=division,
#                                 faculty_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
#                                 st_uid=Student_Details.objects.get(st_uid=st_uid),
#                                 status="0",
#                                 batch_no=batch
#                             )
#                             stud_attd.save()
#                         except IntegrityError as e:
#                             print("kkkkkk")
#                             print(f"Duplicate entry error for student attendance record: {e}")
#                             messages.error(request, f"Duplicate entry error for student attendance record: {e}")
#                         except Exception as e:
#                             print(f"Error creating student attendance record: {e}")
#                             messages.error(request, f"Error creating student attendance record: {e}")

#                     print(batch)
#                     try:
#                         faculty_course_allotment_obj = Faculty_Course_Allotment.objects.create(
#                             batch_no=batch,
#                             employee_emp_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
#                             acad_year_id=acad_year,
#                             sem=sem,
#                             division_id=division,
#                             course_code=Scheme_Details.objects.get(course_code=gui_course_code),
#                             session_count=0
#                         )
#                         faculty_course_allotment_obj.save()
#                     except IntegrityError as e:
#                         print(f"Duplicate entry error for faculty course allotment record: {e}")
#                         messages.error(request, f"Duplicate entry error for faculty course allotment record: {e}")
#                     except Exception as e:
#                         print(f"Error creating faculty course allotment record: {e}")
#                         messages.error(request, f"Error creating faculty course allotment record: {e}")

#                     messages.success(request, "Allotted " + gui_course_code + " to the faculty member " + gui_fac_id)
                    
#                 return render(request, "faculty_course_allotment.html")
#         except IntegrityError:
#             messages.error(request, "Subject is already allotted to the faculty.")
#             '''
            
#             dept = Department.objects.all()
#             return render(request, "faculty_course_allotment.html", {'dept': dept, })
#             '''
#             return faculty_course_allotment(request) # replaces the above 3 lines to load a fresh page
#         except Exception as e:
#             print(e)
#             return faculty_course_allotment(request)
#         #         st_list = Student_Division_Allotment.objects.filter(acad_cal_id = acad_cal_id,division = division).order_by('st_uid')
#         #         l = len(st_list)
#         #         st_list_uid_vals = st_list.values('st_uid')

#         #         st_list = [entry for entry in st_list_uid_vals]  
               
#         #         sid = []
                
#         #         for i in range(0,l):
#         #             sid.append(st_list[i]['st_uid'])

#         #         for st in sid:
#         #             st_uid = st
#         #             stud_attd = student_attendance.objects.create(acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id = acad_year,acad_cal_sem=sem),scheme_details_id = Scheme_Details.objects.get(course_code = gui_course_code ),division = division ,faculty_id = Employee_Details.objects.get(employee_emp_id = gui_fac_id),st_uid=Student_Details.objects.get(st_uid=st_uid),status="0")
#         #             stud_attd.save()

#         #         faculty_course_allotment_obj = Faculty_Course_Allotment.objects.create(faculty_emp_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),acad_year=acad_year,
#         #         sem=sem,division=Division.objects.get(id=division),course_code=Scheme_Details.objects.get(course_code=gui_course_code))
#         #         #faculty_course_allotment_obj = Faculty_Course_Allotment.objects.create(faculty_emp_id=faculty_emp_id,acad_year=acad_year,
#         #         #sem=sem,division=division,course_code=course_code)  #err: "cannot assign, it must be an instance"
#         #         faculty_course_allotment_obj.save()
#         #         messages.success(request, "Allotted "+gui_course_code+" to the faculty member "+gui_fac_id)
#         #         return render(request,"faculty_course_allotment.html")
#         # except IntegrityError:
#         #     messages.error(request, "Subject is already allotted to the faculty.")
#         #     '''
            
#         #     dept = Department.objects.all()
#         #     return render(request, "faculty_course_allotment.html", {'dept': dept, })
#         #     '''
#         #     return faculty_course_allotment(request) # replaces the above 3 lines to load a fresh page
#         # except Exception as e:
#         #     print(e)
#         #     return faculty_course_allotment(request)
def allotCourseToFaculty(request):
    if request.method != "POST":
        dept = Department.objects.all()
        academic_year = AcademicYear.objects.all()
        div_tbl = Division.objects.all().order_by('division')
        return render(request, "faculty_course_allotment.html", {'dept': dept, 'academic_year':academic_year,'div_tbl':div_tbl})
    else:
        acad_year = None
        sem = None
        division = None
        gui_fac_id = None
        gui_course_code = None
        batch = None
        try:
            batch = request.POST.get("batch")
            acad_year = request.POST.get("academic_yr")
            sem = int(request.POST.get("academic_sem"))
            gui_fac_id = request.POST.get("employee_emp_id")  # fetched via GUI
            acad_cal_type = request.POST.get('acad_cal_type')
            acad_ob = Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year, acad_cal_sem=sem, acad_cal_type=acad_cal_type)
            acad_cal_id = acad_ob.acad_cal_id
            division = request.POST.get("division")
            gui_course_code = request.POST.get("courselist")  # fetched via GUI
        except Exception as e:
            messages.error(request, "Could NOT allot the subject!")
            print(f"Error in retrieving form data: {e}")
            return faculty_course_allotment(request)

        try:
            btn_value = request.POST["btn_clicked"]
            if btn_value == "register":
                schem_ob = Scheme_Details.objects.get(course_code=gui_course_code)
                schem_id = schem_ob.scheme_details_id
                course_type = int(schem_ob.course_type)

                if course_type == 1:  # Theory
                    print("attenacd for 1")
                    batch = 'B0'
                    if sem == 1 or sem == 2:
                        st_list = Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id, division=division).order_by('st_uid')
                    elif 3 >= sem <= 8:
                        st_list = UG_Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id, ug_division_id=division).order_by('st_uid')

                    sid = [entry['st_uid'] for entry in st_list.values('st_uid')]
                    
                    div_id = Division.objects.get(id=division)
                    
                    for st_uid in sid:
                        existing_attd = student_attendance.objects.filter(
                            acad_cal_id=Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year, acad_cal_sem=sem, acad_cal_type=acad_cal_type),
                            scheme_details_id=Scheme_Details.objects.get(course_code=gui_course_code),
                            division=division,
                            faculty_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
                            st_uid=Student_Details.objects.get(st_uid=st_uid),
                            batch_no='B0'
                        ).exists()

                        if not existing_attd:
                            try:
                                stud_attd = student_attendance.objects.create(
                                    acad_cal_id=Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year, acad_cal_sem=sem, acad_cal_type=acad_cal_type),
                                    scheme_details_id=Scheme_Details.objects.get(course_code=gui_course_code),
                                    division=division,
                                    faculty_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
                                    st_uid=Student_Details.objects.get(st_uid=st_uid),
                                    status="0",
                                    batch_no='B0'
                                )
                                stud_attd.save()
                                messages.success(request, f"Allotted {gui_course_code} to the faculty member {gui_fac_id}")
                                print("Attendance record created for student", st_uid)
                            except IntegrityError:
                                print(f"Duplicate entry for student attendance record for student {st_uid}")
                                messages.error(request, f"Attendance record for student {st_uid} already exists.")
                            except Exception as e:
                                print(f"Error creating student attendance record for student {st_uid}: {e}")
                                messages.error(request, f"Error creating attendance record for student {st_uid}")
                        else:
                            print(f"Attendance record already exists for student {st_uid}")

                    try:
                        faculty_course_allotment_obj = Faculty_Course_Allotment.objects.create(
                            session_count=0,
                            batch_no='B0',
                            employee_emp_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
                            acad_year_id=acad_year,
                            sem=sem,
                            division=div_id,
                            course_code=Scheme_Details.objects.get(course_code=gui_course_code),
                            acad_cal_type=acad_cal_type
                        )
                        faculty_course_allotment_obj.save()
                        print("Faculty course allotment record created")
                        
                    except IntegrityError:
                        print(f"Duplicate entry for faculty course allotment record")
                        messages.error(request, f"Course {gui_course_code} is already allotted to the faculty member {gui_fac_id}")
                    except Exception as e:
                        print(f"Error creating faculty course allotment record: {e}")
                        messages.error(request, f"Error allotting course {gui_course_code} to faculty member {gui_fac_id}")

                elif course_type == 2:  # Lab
                    print("____Attendance for lab______")

                    if sem == 1 or sem == 2:
                        st_list = Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id, division=division).order_by('st_uid')
                    elif 3 <= sem <= 8:
                        st_list = UG_Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id, ug_division=division).order_by('st_uid')

                    sid = [entry['st_uid'] for entry in st_list.values('st_uid')]
                    print(sid, "sidsidsid")

                    # Depending on the semester, fetch the corresponding registration details
                    if sem == 1 or sem == 2:
                        # Fetch registration details for first-year students
                        batch_student_id = First_Year_Student_Course_Registration_Details.objects.filter(
                            acad_cal_id=acad_cal_id,
                            scheme_details_id=schem_id,
                            batch_no=batch,
                            semester=sem
                        ).order_by('st_uid')
                    else:
                        # Fetch registration details for UG students
                        batch_student_id = UG_Student_Course_Registration_Details.objects.filter(
                            acad_cal_id=acad_cal_id,
                            scheme_details_id=schem_id,
                            batch_no=batch,
                            semester=sem
                        ).order_by('st_uid')

                    # Extracting student IDs from the registration details
                    print(batch_student_id)
                    batch_sid = [entry['st_uid'] for entry in batch_student_id.values('st_uid')]

                    # Filtering `sid` to get only those which are present in `batch_sid`
                    final_selected_students = [value for value in sid if value in batch_sid]
                    print(final_selected_students, "final_selected_students")

                    for st_uid in final_selected_students:
                        existing_attd = student_attendance.objects.filter(
                            acad_cal_id=Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year, acad_cal_sem=sem, acad_cal_type=acad_cal_type),
                            scheme_details_id=Scheme_Details.objects.get(course_code=gui_course_code),
                            division=division,
                            faculty_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
                            st_uid=Student_Details.objects.get(st_uid=st_uid),
                            batch_no=batch
                        ).exists()
                        print("existing_attdexisting_attdexisting_attdexisting_attd",existing_attd)

                        if not existing_attd:
                            try:
                                print("lll",acad_cal_id," ",schem_id," ",division," ",Employee_Details.objects.get(employee_emp_id=gui_fac_id)," ",Student_Details.objects.get(st_uid=st_uid)," ",batch)
                                stud_attd = student_attendance.objects.create(
                                    acad_cal_id=Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year, acad_cal_sem=sem, acad_cal_type=acad_cal_type),
                                    scheme_details_id=Scheme_Details.objects.get(course_code=gui_course_code),
                                    division=division,
                                    faculty_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
                                    st_uid=Student_Details.objects.get(st_uid=st_uid),
                                    status="0",
                                    batch_no=batch
                                )
                                stud_attd.save()
                                messages.success(request, f"Allotted {gui_course_code} to the faculty member {gui_fac_id}")
                               
                            except IntegrityError:
                                print(f"Duplicate entry error for student attendance record: {st_uid}")
                                messages.error(request, f"Duplicate entry error for student attendance record: {st_uid}")
                            
                        else:
                            print(f"Attendance record already exists for student {st_uid}")

                    try:
                        faculty_course_allotment_obj = Faculty_Course_Allotment.objects.create(
                            batch_no=batch,
                            employee_emp_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
                            acad_year_id=acad_year,
                            sem=sem,
                            division_id=division,
                            course_code=Scheme_Details.objects.get(course_code=gui_course_code),
                            session_count=0,
                            acad_cal_type=acad_cal_type
                        )
                        faculty_course_allotment_obj.save()
                        
                    except IntegrityError:
                        print(f"Duplicate entry error for faculty course allotment record")
                        messages.error(request, f"Duplicate entry error for faculty course allotment record")
                    except Exception as e:
                        print(f"Error creating faculty course allotment record: {e}")
                        messages.error(request, f"Error creating faculty course allotment record: {e}")
                elif course_type == 3:  # Theory
                    print("attenacd for 3")
                    batch = 'B0'
                    if sem == 1 or sem == 2:
                        st_list = Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id, division=division).order_by('st_uid')
                    elif 3 >= sem <= 8:
                        st_list = UG_Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id, ug_division_id=division).order_by('st_uid')

                    sid = [entry['st_uid'] for entry in st_list.values('st_uid')]
                    
                    div_id = Division.objects.get(id=division)
                    
                    for st_uid in sid:
                        existing_attd = student_attendance.objects.filter(
                            acad_cal_id=Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year, acad_cal_sem=sem, acad_cal_type=acad_cal_type),
                            scheme_details_id=Scheme_Details.objects.get(course_code=gui_course_code),
                            division=division,
                            faculty_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
                            st_uid=Student_Details.objects.get(st_uid=st_uid),
                            batch_no='B0'
                        ).exists()

                        if not existing_attd:
                            try:
                                stud_attd = student_attendance.objects.create(
                                    acad_cal_id=Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year, acad_cal_sem=sem, acad_cal_type=acad_cal_type),
                                    scheme_details_id=Scheme_Details.objects.get(course_code=gui_course_code),
                                    division=division,
                                    faculty_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
                                    st_uid=Student_Details.objects.get(st_uid=st_uid),
                                    status="0",
                                    batch_no='B0'
                                )
                                stud_attd.save()
                                messages.success(request, f"Allotted {gui_course_code} to the faculty member {gui_fac_id}")
                                print("Attendance record created for student", st_uid)
                            except IntegrityError:
                                print(f"Duplicate entry for student attendance record for student {st_uid}")
                                messages.error(request, f"Attendance record for student {st_uid} already exists.")
                            except Exception as e:
                                print(f"Error creating student attendance record for student {st_uid}: {e}")
                                messages.error(request, f"Error creating attendance record for student {st_uid}")
                        else:
                            print(f"Attendance record already exists for student {st_uid}")

                    try:
                        faculty_course_allotment_obj = Faculty_Course_Allotment.objects.create(
                            session_count=0,
                            batch_no='B0',
                            employee_emp_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
                            acad_year_id=acad_year,
                            sem=sem,
                            division=div_id,
                            course_code=Scheme_Details.objects.get(course_code=gui_course_code),
                            acad_cal_type=acad_cal_type
                        )
                        faculty_course_allotment_obj.save()
                        print("Faculty course allotment record created")
                        
                    except IntegrityError:
                        print(f"Duplicate entry for faculty course allotment record")
                        messages.error(request, f"Course {gui_course_code} is already allotted to the faculty member {gui_fac_id}")
                    except Exception as e:
                        print(f"Error creating faculty course allotment record: {e}")
                        messages.error(request, f"Error allotting course {gui_course_code} to faculty member {gui_fac_id}")
                elif course_type == 4:  # Theory
                    print("attenacd for 4")
                    batch = 'B0'
                    if sem == 1 or sem == 2:
                        st_list = Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id, division=division).order_by('st_uid')
                    elif 3 >= sem <= 8:
                        st_list = UG_Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id, ug_division_id=division).order_by('st_uid')

                    sid = [entry['st_uid'] for entry in st_list.values('st_uid')]
                    
                    div_id = Division.objects.get(id=division)
                    
                    for st_uid in sid:
                        existing_attd = student_attendance.objects.filter(
                            acad_cal_id=Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year, acad_cal_sem=sem, acad_cal_type=acad_cal_type),
                            scheme_details_id=Scheme_Details.objects.get(course_code=gui_course_code),
                            division=division,
                            faculty_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
                            st_uid=Student_Details.objects.get(st_uid=st_uid),
                            batch_no='B0'
                        ).exists()

                        if not existing_attd:
                            try:
                                stud_attd = student_attendance.objects.create(
                                    acad_cal_id=Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year, acad_cal_sem=sem, acad_cal_type=acad_cal_type),
                                    scheme_details_id=Scheme_Details.objects.get(course_code=gui_course_code),
                                    division=division,
                                    faculty_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
                                    st_uid=Student_Details.objects.get(st_uid=st_uid),
                                    status="0",
                                    batch_no='B0'
                                )
                                stud_attd.save()
                                messages.success(request, f"Allotted {gui_course_code} to the faculty member {gui_fac_id}")
                                print("Attendance record created for student", st_uid)
                            except IntegrityError:
                                print(f"Duplicate entry for student attendance record for student {st_uid}")
                                messages.error(request, f"Attendance record for student {st_uid} already exists.")
                            except Exception as e:
                                print(f"Error creating student attendance record for student {st_uid}: {e}")
                                messages.error(request, f"Error creating attendance record for student {st_uid}")
                        else:
                            print(f"Attendance record already exists for student {st_uid}")

                    try:
                        faculty_course_allotment_obj = Faculty_Course_Allotment.objects.create(
                            session_count=0,
                            batch_no='B0',
                            employee_emp_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
                            acad_year_id=acad_year,
                            sem=sem,
                            division=div_id,
                            course_code=Scheme_Details.objects.get(course_code=gui_course_code),
                            acad_cal_type=acad_cal_type

                        )
                        faculty_course_allotment_obj.save()
                        print("Faculty course allotment record created")
                        
                    except IntegrityError:
                        print(f"Duplicate entry for faculty course allotment record")
                        messages.error(request, f"Course {gui_course_code} is already allotted to the faculty member {gui_fac_id}")
                    except Exception as e:
                        print(f"Error creating faculty course allotment record: {e}")
                        messages.error(request, f"Error allotting course {gui_course_code} to faculty member {gui_fac_id}")
                elif course_type == 5:  # Theory
                    print("attenacd for 5")
                    batch = 'B0'
                    if sem == 1 or sem == 2:
                        st_list = Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id, division=division).order_by('st_uid')
                    elif 3 >= sem <= 8:
                        st_list = UG_Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id, ug_division_id=division).order_by('st_uid')

                    sid = [entry['st_uid'] for entry in st_list.values('st_uid')]
                    
                    div_id = Division.objects.get(id=division)
                    
                    for st_uid in sid:
                        existing_attd = student_attendance.objects.filter(
                            acad_cal_id=Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year, acad_cal_sem=sem, acad_cal_type=acad_cal_type),
                            scheme_details_id=Scheme_Details.objects.get(course_code=gui_course_code),
                            division=division,
                            faculty_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
                            st_uid=Student_Details.objects.get(st_uid=st_uid),
                            batch_no='B0'
                        ).exists()

                        if not existing_attd:
                            try:
                                stud_attd = student_attendance.objects.create(
                                    acad_cal_id=Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year, acad_cal_sem=sem, acad_cal_type=acad_cal_type),
                                    scheme_details_id=Scheme_Details.objects.get(course_code=gui_course_code),
                                    division=division,
                                    faculty_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
                                    st_uid=Student_Details.objects.get(st_uid=st_uid),
                                    status="0",
                                    batch_no='B0'
                                )
                                stud_attd.save()
                                messages.success(request, f"Allotted {gui_course_code} to the faculty member {gui_fac_id}")
                                print("Attendance record created for student", st_uid)
                            except IntegrityError:
                                print(f"Duplicate entry for student attendance record for student {st_uid}")
                                messages.error(request, f"Attendance record for student {st_uid} already exists.")
                            except Exception as e:
                                print(f"Error creating student attendance record for student {st_uid}: {e}")
                                messages.error(request, f"Error creating attendance record for student {st_uid}")
                        else:
                            print(f"Attendance record already exists for student {st_uid}")

                    try:
                        faculty_course_allotment_obj = Faculty_Course_Allotment.objects.create(
                            session_count=0,
                            batch_no='B0',
                            employee_emp_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
                            acad_year_id=acad_year,
                            sem=sem,
                            division=div_id,
                            course_code=Scheme_Details.objects.get(course_code=gui_course_code),
                            acad_cal_type=acad_cal_type
                        )
                        faculty_course_allotment_obj.save()
                        print("Faculty course allotment record created")
                        
                    except IntegrityError:
                        print(f"Duplicate entry for faculty course allotment record")
                        messages.error(request, f"Course {gui_course_code} is already allotted to the faculty member {gui_fac_id}")
                    except Exception as e:
                        print(f"Error creating faculty course allotment record: {e}")
                        messages.error(request, f"Error allotting course {gui_course_code} to faculty member {gui_fac_id}")
                elif course_type == 6:  # Theory
                    print("attenacd for 6")
                    batch = 'B0'
                    if sem == 1 or sem == 2:
                        st_list = Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id, division=division).order_by('st_uid')
                    elif 3 <= sem <= 8:
                        st_list = UG_Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id, ug_division=division).order_by('st_uid')

                    sid = [entry['st_uid'] for entry in st_list.values('st_uid')]
                    print(sid, "sidsidsid")

                    # Depending on the semester, fetch the corresponding registration details
                    if sem == 1 or sem == 2:
                        # Fetch registration details for first-year students
                        batch_student_id = First_Year_Student_Course_Registration_Details.objects.filter(
                            acad_cal_id=acad_cal_id,
                            scheme_details_id=schem_id,
                            batch_no=batch,
                            semester=sem
                        ).order_by('st_uid')
                    else:
                        # Fetch registration details for UG students
                        batch_student_id = UG_Student_Course_Registration_Details.objects.filter(
                            acad_cal_id=acad_cal_id,
                            scheme_details_id=schem_id,
                            batch_no=batch,
                            semester=sem
                        ).order_by('st_uid')

                    # Extracting student IDs from the registration details
                    print(batch_student_id)
                    batch_sid = [entry['st_uid'] for entry in batch_student_id.values('st_uid')]

                    # Filtering `sid` to get only those which are present in `batch_sid`
                    final_selected_students = [value for value in sid if value in batch_sid]
                    print(final_selected_students, "final_selected_students")
                    div_id = Division.objects.get(id=division)

                    for st_uid in final_selected_students:
                        existing_attd = student_attendance.objects.filter(
                            acad_cal_id=Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year, acad_cal_sem=sem, acad_cal_type=acad_cal_type),
                            scheme_details_id=Scheme_Details.objects.get(course_code=gui_course_code),
                            division=division,
                            faculty_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
                            st_uid=Student_Details.objects.get(st_uid=st_uid),
                            batch_no='B0'
                        ).exists()

                        if not existing_attd:
                            try:
                                stud_attd = student_attendance.objects.create(
                                    acad_cal_id=Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year, acad_cal_sem=sem, acad_cal_type=acad_cal_type),
                                    scheme_details_id=Scheme_Details.objects.get(course_code=gui_course_code),
                                    division=division,
                                    faculty_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
                                    st_uid=Student_Details.objects.get(st_uid=st_uid),
                                    status="0",
                                    batch_no='B0'
                                )
                                stud_attd.save()
                                messages.success(request, f"Allotted {gui_course_code} to the faculty member {gui_fac_id}")
                                print("Attendance record created for student", st_uid)
                            except IntegrityError:
                                print(f"Duplicate entry for student attendance record for student {st_uid}")
                                messages.error(request, f"Attendance record for student {st_uid} already exists.")
                            except Exception as e:
                                print(f"Error creating student attendance record for student {st_uid}: {e}")
                                messages.error(request, f"Error creating attendance record for student {st_uid}")
                        else:
                            print(f"Attendance record already exists for student {st_uid}")

                    try:
                        faculty_course_allotment_obj = Faculty_Course_Allotment.objects.create(
                            session_count=0,
                            batch_no='B0',
                            employee_emp_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
                            acad_year_id=acad_year,
                            sem=sem,
                            division=div_id,
                            course_code=Scheme_Details.objects.get(course_code=gui_course_code),
                            acad_cal_type=acad_cal_type
                        )
                        faculty_course_allotment_obj.save()
                        print("Faculty course allotment record created")
                        
                    except IntegrityError:
                        print(f"Duplicate entry for faculty course allotment record")
                        messages.error(request, f"Course {gui_course_code} is already allotted to the faculty member {gui_fac_id}")
                    except Exception as e:
                        print(f"Error creating faculty course allotment record: {e}")
                        messages.error(request, f"Error allotting course {gui_course_code} to faculty member {gui_fac_id}") 
                elif course_type == 7:  # Theory
                    print("attenacd for 7")
                    batch = 'B0'
                    if sem == 1 or sem == 2:
                        st_list = Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id, division=division).order_by('st_uid')
                    elif 3 >= sem <= 8:
                        st_list = UG_Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id, ug_division_id=division).order_by('st_uid')

                    sid = [entry['st_uid'] for entry in st_list.values('st_uid')]
                    
                    div_id = Division.objects.get(id=division)
                    
                    for st_uid in sid:
                        existing_attd = student_attendance.objects.filter(
                            acad_cal_id=Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year, acad_cal_sem=sem, acad_cal_type=acad_cal_type),
                            scheme_details_id=Scheme_Details.objects.get(course_code=gui_course_code),
                            division=division,
                            faculty_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
                            st_uid=Student_Details.objects.get(st_uid=st_uid),
                            batch_no='B0'
                        ).exists()

                        if not existing_attd:
                            try:
                                stud_attd = student_attendance.objects.create(
                                    acad_cal_id=Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year, acad_cal_sem=sem, acad_cal_type=acad_cal_type),
                                    scheme_details_id=Scheme_Details.objects.get(course_code=gui_course_code),
                                    division=division,
                                    faculty_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
                                    st_uid=Student_Details.objects.get(st_uid=st_uid),
                                    status="0",
                                    batch_no='B0'
                                )
                                stud_attd.save()
                                messages.success(request, f"Allotted {gui_course_code} to the faculty member {gui_fac_id}")
                                print("Attendance record created for student", st_uid)
                            except IntegrityError:
                                print(f"Duplicate entry for student attendance record for student {st_uid}")
                                messages.error(request, f"Attendance record for student {st_uid} already exists.")
                            except Exception as e:
                                print(f"Error creating student attendance record for student {st_uid}: {e}")
                                messages.error(request, f"Error creating attendance record for student {st_uid}")
                        else:
                            print(f"Attendance record already exists for student {st_uid}")

                    try:
                        faculty_course_allotment_obj = Faculty_Course_Allotment.objects.create(
                            session_count=0,
                            batch_no='B0',
                            employee_emp_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
                            acad_year_id=acad_year,
                            sem=sem,
                            division=div_id,
                            course_code=Scheme_Details.objects.get(course_code=gui_course_code),
                            acad_cal_type=acad_cal_type
                        )
                        faculty_course_allotment_obj.save()
                        print("Faculty course allotment record created")
                        
                    except IntegrityError:
                        print(f"Duplicate entry for faculty course allotment record")
                        messages.error(request, f"Course {gui_course_code} is already allotted to the faculty member {gui_fac_id}")
                    except Exception as e:
                        print(f"Error creating faculty course allotment record: {e}")
                        messages.error(request, f"Error allotting course {gui_course_code} to faculty member {gui_fac_id}")
                elif course_type == 8:  # Theory
                    print("attenacd for 8")
                    batch = 'B0'
                    if sem == 1 or sem == 2:
                        st_list = Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id, division=division).order_by('st_uid')
                    elif 3 >= sem <= 8:
                        st_list = UG_Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id, ug_division_id=division).order_by('st_uid')

                    sid = [entry['st_uid'] for entry in st_list.values('st_uid')]
                    
                    div_id = Division.objects.get(id=division)
                    
                    for st_uid in sid:
                        existing_attd = student_attendance.objects.filter(
                            acad_cal_id=Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year, acad_cal_sem=sem, acad_cal_type=acad_cal_type),
                            scheme_details_id=Scheme_Details.objects.get(course_code=gui_course_code),
                            division=division,
                            faculty_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
                            st_uid=Student_Details.objects.get(st_uid=st_uid),
                            batch_no='B0'
                        ).exists()

                        if not existing_attd:
                            try:
                                stud_attd = student_attendance.objects.create(
                                    acad_cal_id=Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year, acad_cal_sem=sem, acad_cal_type=acad_cal_type),
                                    scheme_details_id=Scheme_Details.objects.get(course_code=gui_course_code),
                                    division=division,
                                    faculty_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
                                    st_uid=Student_Details.objects.get(st_uid=st_uid),
                                    status="0",
                                    batch_no='B0'
                                )
                                stud_attd.save()
                                messages.success(request, f"Allotted {gui_course_code} to the faculty member {gui_fac_id}")
                                print("Attendance record created for student", st_uid)
                            except IntegrityError:
                                print(f"Duplicate entry for student attendance record for student {st_uid}")
                                messages.error(request, f"Attendance record for student {st_uid} already exists.")
                            except Exception as e:
                                print(f"Error creating student attendance record for student {st_uid}: {e}")
                                messages.error(request, f"Error creating attendance record for student {st_uid}")
                        else:
                            print(f"Attendance record already exists for student {st_uid}")

                    try:
                        faculty_course_allotment_obj = Faculty_Course_Allotment.objects.create(
                            session_count=0,
                            batch_no='B0',
                            employee_emp_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),
                            acad_year_id=acad_year,
                            sem=sem,
                            division=div_id,
                            course_code=Scheme_Details.objects.get(course_code=gui_course_code),
                            acad_cal_type=acad_cal_type
                        )
                        faculty_course_allotment_obj.save()
                        print("Faculty course allotment record created")
                        
                    except IntegrityError:
                        print(f"Duplicate entry for faculty course allotment record")
                        messages.error(request, f"Course {gui_course_code} is already allotted to the faculty member {gui_fac_id}")
                    except Exception as e:
                        print(f"Error creating faculty course allotment record: {e}")
                        messages.error(request, f"Error allotting course {gui_course_code} to faculty member {gui_fac_id}")   
                
                return render(request, "faculty_course_allotment.html")
        except IntegrityError:
            messages.error(request, "Subject is already allotted to the faculty.")
            return faculty_course_allotment(request)  # Reload the page to handle the error
        except Exception as e:
            print(e)
            return faculty_course_allotment(request)

# def allotCourseToFaculty(request):
#     if request.method!="POST":
#         return HttpResponse("<h2>Method Not Allowed</h2>")
#     else:
#         acad_year = None
#         sem = None
#         division = None
#         gui_fac_id = None
#         gui_course_code = None
#         batch = None
#         try:
#             batch = request.POST.get("batch")
#             acad_year = request.POST.get("academic_yr")
#             print(acad_year)
#             sem = int(request.POST.get("academic_sem"))
#             gui_fac_id = request.POST.get("employee_emp_id") #fetched via GUI
#             acad_cal_type = request.POST.get('acad_cal_type')
#             acad_ob = Academic_Calendar.objects.get(acad_cal_acad_year_id = acad_year,acad_cal_sem=sem,acad_cal_type=acad_cal_type)
#             acad_cal_id = acad_ob.acad_cal_id
#             print(acad_cal_id)
#             '''
#             if .faculty_emp_id is not mentioned then by default auto_id of the table on RHS is fetched
#             faculty_emp_id = (Faculty_Details.objects.get(faculty_emp_id=gui_fac_id)).faculty_emp_id 
#             NOT useful while creating object IF foreign key is not primary key
#             '''
#             division = request.POST.get("division")
#             gui_course_code = request.POST.get("courselist") #fetched via GUI

#         except:
#             messages.error(request, "Could NOT allot the subject!")
#             return faculty_course_allotment(request)

#         try:
#             btn_value = request.POST["btn_clicked"]
#             if btn_value == "register":
#                 schem_ob = Scheme_Details.objects.get(course_code = gui_course_code )
#                 schem_id = schem_ob.scheme_details_id
#                 dept = schem_ob.offered_by
#                 course_type = schem_ob.course_type
#                 course_type = int(course_type)


#                 #===============Only for Theory=====================
#                 if course_type ==  1:
#                         batch = 'B0'
#                         if sem==1 or sem==2:
#                             st_list = Student_Division_Allotment.objects.filter(acad_cal_id = acad_cal_id,division = division).order_by('st_uid')
#                         elif sem>=3 and sem<=8:
#                             print("allotCourseToFaculty")
#                             print(acad_cal_id)
#                             print(division)
#                             st_list = UG_Student_Division_Allotment.objects.filter(acad_cal_id = acad_cal_id,ug_division_id = division).order_by('st_uid')
#                             print(st_list)
#                         l = len(st_list)
#                         print("hello",st_list)
#                         st_list_uid_vals = st_list.values('st_uid')

#                         st_list = [entry for entry in st_list_uid_vals]  
                        
#                         sid = []
                        
#                         for i in range(0,l):
#                             sid.append(st_list[i]['st_uid'])

#                         div_id = Division.objects.get(id=division)
#                         for st in sid:
#                             st_uid = st
#                             print("uid",st_uid)

#                             stud_attd = student_attendance.objects.create(acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year = acad_year,acad_cal_sem=sem,acad_cal_type=acad_cal_type),scheme_details_id = Scheme_Details.objects.get(course_code = gui_course_code ),division = division ,faculty_id = Employee_Details.objects.get(employee_emp_id = gui_fac_id),st_uid=Student_Details.objects.get(st_uid=st_uid),status="0",batch_no='B0')
#                             stud_attd.save()
                        
                            
#                             print("helllo academics finally done")
#                         faculty_course_allotment_obj = Faculty_Course_Allotment.objects.create(session_count=0,batch_no='B0',employee_emp_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),acad_year_id=acad_year,sem=sem,division=div_id,course_code=Scheme_Details.objects.get(course_code=gui_course_code))
#                         #faculty_course_allotment_obj = Faculty_Course_Allotment.objects.create(faculty_emp_id=faculty_emp_id,acad_year=acad_year,
#                         #sem=sem,division=division,course_code=course_code)  #err: "cannot assign, it must be an instance"
#                         faculty_course_allotment_obj.save()
#                         messages.success(request, "Allotted "+gui_course_code+" to the faculty member "+gui_fac_id)

#                 #===============Only for Lab=====================
#                 sid = []
#                 st_list = []
#                 if course_type ==  2:
#                     print("____Attendance for lab______")

#                     if sem==1 or sem==2:
#                         st_list = Student_Division_Allotment.objects.filter(acad_cal_id = acad_cal_id,division = division).order_by('st_uid')
#                     elif sem>=3 and sem<=8:
#                         st_list = UG_Student_Division_Allotment.objects.filter(acad_cal_id = acad_cal_id,ug_division = division).order_by('st_uid')
#                     print(st_list)
#                     l = len(st_list)
#                     st_list_uid_vals = st_list.values('st_uid')

#                     st_list = [entry for entry in st_list_uid_vals]  
                    
#                     sid = []
                    
#                     for i in range(0,l):
#                         sid.append(st_list[i]['st_uid'])
                    
#                     for i in range(0,l):
#                         print(sid[i])
                    
#                     print(acad_cal_id)
#                     print(schem_id)
#                     print(batch)
#                     print(sem)
#                     if sem==1 or sem==2:
#                         # batch_student_id = First_Year_Student_Course_Registration_Details.objects.filter(acad_cal_id = acad_cal_id,scheme_details_id = schem_id,batch_no=batch,semester=sem).order_by('st_uid')
#                         batch_student_id = First_Year_Student_Course_Registration_Details.objects.filter(acad_cal_id = acad_cal_id,scheme_details_id = schem_id,semester=sem).order_by('st_uid')
#                     else:
#                         batch_student_id = UG_Student_Course_Registration_Details.objects.filter(acad_cal_id = acad_cal_id,scheme_details_id = schem_id,batch_no=batch,semester=sem).order_by('st_uid')
                    
#                     print(batch_student_id)

#                     l = len(batch_student_id)
#                     batch_student_id_vals = batch_student_id.values('st_uid')

#                     batch_st_list = [entry for entry in batch_student_id_vals]  
                    

#                     batch_sid = []
                    
#                     for i in range(0,l):
#                         batch_sid.append(batch_st_list[i]['st_uid'])
                    
                    
#                     final_selected_students = [value for value in sid if value in batch_sid] 

#                     print(final_selected_students)
#                     print(type(final_selected_students))

#                     for st in final_selected_students:
#                         st_uid = st
#                         stud_attd = student_attendance.objects.create(acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id = acad_year,acad_cal_sem=sem,acad_cal_type=acad_cal_type),scheme_details_id = Scheme_Details.objects.get(course_code = gui_course_code ),division = division ,faculty_id= Employee_Details.objects.get(employee_emp_id = gui_fac_id),st_uid=Student_Details.objects.get(st_uid=st_uid),status="0",batch_no = batch)
#                         stud_attd.save()
         

#                     print(batch)
#                     faculty_course_allotment_obj = Faculty_Course_Allotment.objects.create(batch_no=batch,employee_emp_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),acad_year_id=acad_year,sem=sem,division_id=division,course_code=Scheme_Details.objects.get(course_code=gui_course_code),session_count=0)
                    
#                     faculty_course_allotment_obj.save()
#                     messages.success(request, "Allotted "+gui_course_code+" to the faculty member "+gui_fac_id)
                        
#                 return render(request,"faculty_course_allotment.html")
#         except IntegrityError:
#             messages.error(request, "Subject is already allotted to the faculty.")
#             '''
            
#             dept = Department.objects.all()
#             return render(request, "faculty_course_allotment.html", {'dept': dept, })
#             '''
#             return faculty_course_allotment(request) # replaces the above 3 lines to load a fresh page
#         except Exception as e:
#             print(e)
#             return faculty_course_allotment(request)
#         #         st_list = Student_Division_Allotment.objects.filter(acad_cal_id = acad_cal_id,division = division).order_by('st_uid')
#         #         l = len(st_list)
#         #         st_list_uid_vals = st_list.values('st_uid')

#         #         st_list = [entry for entry in st_list_uid_vals]  
               
#         #         sid = []
                
#         #         for i in range(0,l):
#         #             sid.append(st_list[i]['st_uid'])

#         #         for st in sid:
#         #             st_uid = st
#         #             stud_attd = student_attendance.objects.create(acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id = acad_year,acad_cal_sem=sem),scheme_details_id = Scheme_Details.objects.get(course_code = gui_course_code ),division = division ,faculty_id = Employee_Details.objects.get(employee_emp_id = gui_fac_id),st_uid=Student_Details.objects.get(st_uid=st_uid),status="0")
#         #             stud_attd.save()

#         #         faculty_course_allotment_obj = Faculty_Course_Allotment.objects.create(faculty_emp_id=Employee_Details.objects.get(employee_emp_id=gui_fac_id),acad_year=acad_year,
#         #         sem=sem,division=Division.objects.get(id=division),course_code=Scheme_Details.objects.get(course_code=gui_course_code))
#         #         #faculty_course_allotment_obj = Faculty_Course_Allotment.objects.create(faculty_emp_id=faculty_emp_id,acad_year=acad_year,
#         #         #sem=sem,division=division,course_code=course_code)  #err: "cannot assign, it must be an instance"
#         #         faculty_course_allotment_obj.save()
#         #         messages.success(request, "Allotted "+gui_course_code+" to the faculty member "+gui_fac_id)
#         #         return render(request,"faculty_course_allotment.html")
#         # except IntegrityError:
#         #     messages.error(request, "Subject is already allotted to the faculty.")
#         #     '''
            
#         #     dept = Department.objects.all()
#         #     return render(request, "faculty_course_allotment.html", {'dept': dept, })
#         #     '''
#         #     return faculty_course_allotment(request) # replaces the above 3 lines to load a fresh page
#         # except Exception as e:
#         #     print(e)
#         #     return faculty_course_allotment(request)

def student_attendance_det(request):
    academic_year = AcademicYear.objects.all().order_by('-acayear').distinct()
    userName=CustomUser.objects.get(id=request.user.id)
    fac_id = Employee_Details.objects.get(employee_emp_id=userName)
    acad_year = Faculty_Course_Allotment.objects.filter(employee_emp_id=fac_id).values('acad_year').distinct()
    #calender = Academic_Calendar.objects.all()
    calender = Academic_Calendar.objects.all().order_by('-acad_cal_acad_year').values('acad_cal_acad_year').distinct()
    #Code to get unique AY list
    dep=Department.objects.all()
    ay = []
    for c in calender:
        a = AcademicYear.objects.get(id=c['acad_cal_acad_year']) # model returns AY string(acacyear)
        ay.append(a)

    return render(request,"student_attendance.html",{'div_tbl':Division.objects.all(),'academic_year':academic_year,'calender': ay,'scheme_detail':Scheme_Details.objects.all(),'acad_year':acad_year,'dep':dep})

def studenteachclassattendance(request):
    userName=CustomUser.objects.get(id=request.user.id)
    # if request.method!="POST":
    #     return HttpResponse("<h2>Method Not Allowed</h2>")
    # else:
    #     # try:
    #     print(Employee_Details.objects.get(employee_emp_id=userName))
    #     faculty_id = Faculty_Course_Allotment.objects.filter(employee_emp_id_id=Employee_Details.objects.get(employee_emp_id=userName))
    #     print(faculty_id)
    #     print("+++++++++")
    #     print("==========")
    #     acad_year = Faculty_Course_Allotment.objects.filter(faculty_id=faculty_id).values('acad_year')
    #     course_code= faculty_id.course_code 
    #     attend_date = request.POST['attend_date']
    #     numberofclasses = request.POST['numberofclasses']
    #     division = faculty_id.division_id
    #     # div_tbl=Division.objects.get(division=division)

    #     scheme_obj = Scheme_Details.objects.get(scheme_details_id = course_code )
    #     all_student_obj =  Student_Details.objects.all()

    #     course_id = Scheme_Details.objects.get(scheme_details_id=course_code)
    #     course_code = course_id.course_code
    #     sem = course_id.sem_allotted
        
    #     faculty_obj = Faculty_Course_Allotment.objects.filter(division=division,acad_year=acad_year,course_code=course_code)
    #     if not faculty_obj.exists():
    #         messages.error(request,"Details Not Found")
    #         return render(request,"student_attendance.html",{'division':division,'acad_year':acad_year,'course_code':course_code})
        
    #     faculty_obj = Faculty_Course_Allotment.objects.get(division=division,acad_year=acad_year,course_code =course_code)
    #     faculty_id = faculty_obj.faculty_emp_id.employee_emp_id
    #     print(faculty_obj)
    #     print("==========")
    #     print(faculty_id)
    #     session_count = faculty_obj.session_count
    #     print(session_count)
    
    #     acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id= acad_year,acad_cal_sem=sem)

    #     #-------------If attendance is already taken-----------------------
    #     student_attendace_assigned_date = student_Attendance_date.objects.filter(acad_cal_id_id=acad_cal_id,division = division,faculty_id = Employee_Details.objects.get(employee_emp_id = faculty_id),scheme_details_id_id = Scheme_Details.objects.get(course_code = course_code),attendance_date = attend_date)
    #     checkifalreadyexists = len(student_attendace_assigned_date)

    #     if checkifalreadyexists == 0:
    #         pass
    #     else :
    #         messages.error(request,"You have already took the attendance on "+attend_date)
    #         return render(request,"student_attendance.html",{'div_tbl':Division.objects.all(),'calender': Academic_Calendar.objects.all(),'scheme_detail':Scheme_Details.objects.all()})
    #     #----------------------------------

    #     student_obj = student_attendance.objects.filter(acad_cal_id=acad_cal_id,division = division).order_by('st_uid')
        
    #     if(numberofclasses == 1):
    #         session1 = int(session_count) +1
    #         session2 = 0
    #     else:
    #         session1 = int(session_count) +1
    #         session2 = int(session_count) +2

    #     btn_value = request.POST["btn_clicked"]
    #     if btn_value == "register":    
    #         edit_permission = "no"
    #         return render(request,"attendance_list.html",{'calender': Academic_Calendar.objects.values('acad_cal_acad_year_id').distinct(),'scheme_detail':scheme_obj,'attend_date':attend_date,'student_obj':student_obj,'numberofclasses':numberofclasses,'acad_year':acad_year,'division':division,'all_student_obj':all_student_obj,'session1':session1,'session2':session2,'edit_permission':edit_permission})
    #     else:
    #         return render(request,"student_attendance.html",{'div_tbl':Division.objects.all(),'calender': Academic_Calendar.objects.values('acad_cal_acad_year_id').distinct(),'scheme_detail':Scheme_Details.objects.all()})
        # except Exception as e:
        #     print(e)

    if request.POST:
        acad_year = request.POST['academic_year']
        print(acad_year)
        #scheme_details_id = request.POST['subject']
        sub_code = request.POST['subject']
        print(sub_code)
        attend_date = request.POST['attend_date']
        numberofclasses = request.POST['numberofclasses']
        acad_cal_type = request.POST['acad_cal_type']
        division = request.POST['div']
        print(division)
        # div_tbl=Division.objects.get(division=division)
        CourseType = Scheme_Details.objects.get(course_code=sub_code).course_type
        print(CourseType)
        if CourseType=='1':
            batch = 'B0'
        else:
            batch = request.POST['batch']
        
        scheme_obj = Scheme_Details.objects.get(course_code = sub_code )
        all_student_obj =  Student_Details.objects.all()
        

        #course_id = Scheme_Details.objects.get(scheme_details_id=scheme_details_id)
        course_id = Scheme_Details.objects.get(scheme_details_id=scheme_obj.scheme_details_id)
        course_code = course_id.course_code
        print("views course code 752")
        print(course_code)
        print(batch)
        sem = course_id.sem_allotted
        faculty_obj = Faculty_Course_Allotment.objects.filter(division=division,acad_year=acad_year,course_code=course_code,batch_no=batch,acad_cal_type=acad_cal_type)
        if not faculty_obj.exists():
            messages.error(request,"Details Not Found")
            return render(request,"student_attendance.html",{'div_tbl':Division.objects.all(),'calender': Academic_Calendar.objects.all(),'scheme_detail':Scheme_Details.objects.all()})
        
        faculty_obj = Faculty_Course_Allotment.objects.get(division=division,acad_year=acad_year,course_code =course_code,batch_no=batch,acad_cal_type=acad_cal_type)
        faculty_id = faculty_obj.employee_emp_id.employee_emp_id
        print(faculty_obj)
        print(faculty_id)
        session_count = faculty_obj.session_count
        print(session_count)
    
        acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id= acad_year,acad_cal_sem=sem,acad_cal_type=acad_cal_type)

        #-------------If attendance is already taken-----------------------
        student_attendace_assigned_date = student_Attendance_date.objects.filter(acad_cal_id_id=acad_cal_id,division = division,faculty_id = Employee_Details.objects.get(employee_emp_id = faculty_id),scheme_details_id_id = Scheme_Details.objects.get(course_code = course_code),attendance_date = attend_date)
        checkifalreadyexists = len(student_attendace_assigned_date)
        

        if checkifalreadyexists == 0:
            pass
        else :
            messages.error(request,"You have already took the attendance on "+attend_date)
            return render(request,"student_attendance.html",{'div_tbl':Division.objects.all(),'calender': Academic_Calendar.objects.all(),'scheme_detail':Scheme_Details.objects.all()})
        #----------------------------------

        #scheme_details_id added in the condition
        student_obj = student_attendance.objects.filter(acad_cal_id=acad_cal_id,division = division,batch_no=batch,scheme_details_id=scheme_obj.scheme_details_id).order_by('st_uid')
        print("testing attendance")

        print(student_obj)
        if(numberofclasses == 1):
            session1 = int(session_count) +1
            session2 = 0
        else:
            session1 = int(session_count) +1
            session2 = int(session_count) +2
        print("Checking scheme object")
        print(scheme_obj)

        batch_student_id = None
        if sem==1 or sem==2:
            print("first year lab att")
            print(batch,acad_cal_id,course_id,sem)
            batch_student_id = First_Year_Student_Course_Registration_Details.objects.filter(acad_cal_id = acad_cal_id,scheme_details_id = course_id,first_year_cycle=division,batch_no=batch,semester=sem).order_by('st_uid')
            print(batch_student_id)
        else:
            print("higher sem lab att")
            batch_student_id = UG_Student_Course_Registration_Details.objects.filter(acad_cal_id = acad_cal_id,scheme_details_id = course_id,division=division,batch_no=batch,semester=sem).order_by('st_uid')
        print('ooooo')       
        print(batch_student_id)
    
        btn_value = request.POST["btn_clicked"]
        print("button value")
        print(btn_value)
        if btn_value == "register": 
            print("inside if register") 
            edit_permission = "no"
            # To fetch division value A, B, C --- Display purpose
            div = Division.objects.get(id=division) 
            # To fetch acad_year value 2022-23 --- Display purpose
            acad_year_string = AcademicYear.objects.get(id=acad_year).acayear
            print("lllllllllll000w")
            student_attendance_queryset = student_attendance.objects.all()
            print(student_attendance_queryset)

            # Loop through the queryset and print the student UID
            print(batch,"batchbatchbatchbatchbatchbatchbatchbatchbatchbatchbatchbatchbatchbatchbatchbatch")
            



                      
                      
            return render(request,"attendance_list.html",{'calender': Academic_Calendar.objects.values('acad_cal_acad_year_id').distinct(),'scheme_detail':scheme_obj,'attend_date':attend_date,'student_obj':student_obj,'numberofclasses':numberofclasses,'acad_year':acad_year,'division':division,'all_student_obj':all_student_obj,'session1':session1,'session2':session2,'edit_permission':edit_permission,'div_html':div,'acad_cal_type':acad_cal_type,'batch_no':batch,'acad_year_html':acad_year_string,'batch_student_id':batch_student_id})
    else:
        academic_year = AcademicYear.objects.all().order_by('-acayear').distinct()
        userName=CustomUser.objects.get(id=request.user.id)
        fac_id = Employee_Details.objects.get(employee_emp_id=userName)
        acad_year = Faculty_Course_Allotment.objects.filter(employee_emp_id=fac_id).values('acad_year').distinct()
        #calender = Academic_Calendar.objects.all()
        calender = Academic_Calendar.objects.all().order_by('-acad_cal_acad_year').values('acad_cal_acad_year').distinct()
        #Code to get unique AY list
        dep=Department.objects.all()
        ay = []
        for c in calender:
            a = AcademicYear.objects.get(id=c['acad_cal_acad_year']) # model returns AY string(acacyear)
            ay.append(a)

        return render(request,"student_attendance.html",{'div_tbl':Division.objects.all(),'academic_year':academic_year,'calender': ay,'scheme_detail':Scheme_Details.objects.all(),'acad_year':acad_year,'dep':dep})
        # return render(request,"student_attendance.html",{'div_tbl':Division.objects.all(),'calender': Academic_Calendar.objects.values('acad_cal_acad_year_id').distinct(),'scheme_detail':Scheme_Details.objects.all()})

#def student_attendance_list(request,attend_date,numberofclasses,course_code,division,acad_year,session1,session2,): #removed comma
def student_attendance_list(request,attend_date,numberofclasses,course_code,division,acad_year,session1,session2,acad_cal_type,batch_no):  
    print(" function student_att_list")
    userName=CustomUser.objects.get(id=request.user.id)
    if request.method!="POST":
        academic_year = AcademicYear.objects.all().order_by('-acayear').distinct()
        userName=CustomUser.objects.get(id=request.user.id)
        fac_id = Employee_Details.objects.get(employee_emp_id=userName)
        acad_year = Faculty_Course_Allotment.objects.filter(employee_emp_id=fac_id).values('acad_year').distinct()
        #calender = Academic_Calendar.objects.all()
        calender = Academic_Calendar.objects.all().order_by('-acad_cal_acad_year').values('acad_cal_acad_year').distinct()
        #Code to get unique AY list
        dep=Department.objects.all()
        ay = []
        for c in calender:
            a = AcademicYear.objects.get(id=c['acad_cal_acad_year']) # model returns AY string(acacyear)
            ay.append(a)

        return render(request,"student_attendance.html",{'div_tbl':Division.objects.all(),'academic_year':academic_year,'calender': ay,'scheme_detail':Scheme_Details.objects.all(),'acad_year':acad_year,'dep':dep})
    else:
        acad_cal_year = None
        subj_course_code = None
        div = None
        faculty_id = None
        attendance_date = None

        st_list_1 = None
        st_list_2 = None

        number_of_classes = 0
        total_session = 0
        session_id_1 = 0
        session_id_2 = 0

        sid = []

        absentee_count_s1 = 0
        absentee_count_s2 = 0
        
        try:    
            subj_course_code = course_code
           
            #scheme_details_id = Scheme_Details.objects.get(course_code = subj_course_code)
            scheme_details_obj = Scheme_Details.objects.get(course_code = subj_course_code)
            scheme_details_id = Scheme_Details.objects.get(course_code = subj_course_code).scheme_details_id
            semester = scheme_details_obj.sem_allotted
            div = division

            acad_cal_year = acad_year

            print("printing acad cal id -- pre get")
            print(batch_no)
            acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id= acad_year,acad_cal_sem = semester,acad_cal_type=acad_cal_type)
            print("printing acad cal id")
            print(acad_cal_id)
            faculty_obj = Faculty_Course_Allotment.objects.get(division=div,acad_year=acad_cal_year,course_code =course_code,batch_no=batch_no,acad_cal_type=acad_cal_type)
            faculty_id = faculty_obj.employee_emp_id.employee_emp_id
           
            attendance_date = attend_date
            
            number_of_classes = numberofclasses
                       
            faculty_obj = Faculty_Course_Allotment.objects.get(division=division,acad_year=acad_year,course_code =course_code,batch_no=batch_no,acad_cal_type=acad_cal_type)
            count = faculty_obj.session_count
            print(count,"countcount")
           

            student_obj = student_attendance.objects.filter(acad_cal_id=acad_cal_id,division = div).order_by('st_uid')
            
            if number_of_classes == '1':
                total_session = int(count) + int(number_of_classes)
                st_list_1 = request.POST.getlist("checked_allot_1")   
                
            else :
                total_session = int(count) + int(number_of_classes)
                st_list_1 = request.POST.getlist("checked_allot_1")     
                st_list_2 = request.POST.getlist("checked_allot_2")      

            #st_list = Student_Division_Allotment.objects.filter(acad_cal_id = acad_cal_id,division_id = div).order_by('st_uid') - - - this fetches all students
            st_list = student_attendance.objects.filter(acad_cal_id=acad_cal_id,division = div, scheme_details_id=scheme_details_id,batch_no=batch_no).order_by('st_uid') 
            l = len(st_list)
            print(l)
            st_list_uid_vals = st_list.values('st_uid')
            print(st_list_uid_vals)
            
            st_list = [entry for entry in st_list_uid_vals] 
            print(st_list) 
                  
            for i in range(0,l):
                print(i)
                sid.append(st_list[i]['st_uid'])
                print(sid)
                     
        except Academic_Calendar.DoesNotExist:
            messages.error(request, "Please check Academic Year and enter")
            userName=CustomUser.objects.get(id=request.user.id)
            context={'username':userName}
            return render(request,"attendance_list.html",context=context) 

        try:
            print("ifff")
            btn_value = request.POST["btn_clicked"]
            if btn_value == "register":
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print(current_time)

                faculty_obj = Faculty_Course_Allotment.objects.get(division=div,acad_year=acad_year,course_code =course_code,batch_no=batch_no,acad_cal_type=acad_cal_type)
                faculty_obj.session_count = total_session
                faculty_obj.save()
                print("no of classes")
                print(number_of_classes)
                if number_of_classes == '1':
                    print("compare - true", sid)
                    for st in sid:
                        try:
                            if check_students(st_list_1, st):
                                print(st, scheme_details_id, student_present)
                                student_present(st, scheme_details_id,acad_cal_id)
                                print("inside present block")
                            else:
                                student_absent(st, scheme_details_id,acad_cal_id)
                                print(st)
                                absentee_count_s1 += 1
                            print("/////////////////")
                        except Exception as e:
                            print(f"Error checking or updating student attendance for student {st}: {e}")
                    
                    print(acad_cal_type, "acad_cal_typeacad_cal_typeacad_cal_type")
                    acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year, acad_cal_sem=semester, acad_cal_type=acad_cal_type).acad_cal_id
                    
                    try:
                        stud_attd_date = student_Attendance_date.objects.create(
                            acad_cal_id_id=acad_cal_id,
                            scheme_details_id_id=scheme_details_id,
                            division=div,
                            faculty_id=Employee_Details.objects.get(employee_emp_id=faculty_id),
                            session_index=total_session,
                            attendance_date=attendance_date,
                            attendance_time=current_time,
                            absentees_count=absentee_count_s1,
                            batch_no=batch_no
                        )
                        stud_attd_date.save()
                        print("printing att date")
                        print(stud_attd_date)
                    
                    except IntegrityError as e:
                        print(f"Duplicate entry error for student attendance date record: {e}")
                        messages.error(request, "A record for the student attendance date already exists.")
                    
                    except Exception as e:
                        print(f"Error creating student attendance date record: {e}")
                        messages.error(request, "Error creating student attendance date record.")
                    
                else:
                    for st in sid:
                        try:
                            if check_students(st_list_1, st):
                                # student_present(st)
                                student_present(st, scheme_details_id,acad_cal_id)
                            else:
                                # student_absent(st)
                                student_absent(st, scheme_details_id,acad_cal_id)
                                absentee_count_s1 += 1
                        except Exception as e:
                            print(f"Error processing student {st} in first check: {e}")

                    for st in sid:
                        try:
                            if check_students(st_list_2, st):
                                # student_present(st)
                                student_present(st, scheme_details_id,acad_cal_id)
                            else:
                                # student_absent(st)
                                student_absent(st, scheme_details_id,acad_cal_id)
                                absentee_count_s2 += 1
                        except Exception as e:
                            print(f"Error processing student {st} in second check: {e}")

                    try:
                        stud_attd_date = student_Attendance_date.objects.create(
                            acad_cal_id_id=Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_cal_year, acad_cal_sem=semester, acad_cal_type=acad_cal_type),
                            scheme_details_id_id=Scheme_Details.objects.get(course_code=subj_course_code),
                            division=div,
                            faculty_id=Employee_Details.objects.get(employee_emp_id=faculty_id),
                            session_index=int(total_session) - 1,
                            attendance_date=attendance_date,
                            attendance_time=current_time,
                            absentees_count=absentee_count_s1,
                            batch_no=batch_no
                        )
                        stud_attd_date.save()

                        # stud_attd_date = student_Attendance_date.objects.create(
                        #     acad_cal_id_id=Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_cal_year, acad_cal_sem=semester, acad_cal_type=acad_cal_type),
                        #     scheme_details_id_id=Scheme_Details.objects.get(course_code=subj_course_code),
                        #     division=div,
                        #     faculty_id=Employee_Details.objects.get(employee_emp_id=faculty_id),
                        #     session_index=int(total_session),
                        #     attendance_date=attendance_date,
                        #     attendance_time=current_time,
                        #     absentees_count=absentee_count_s2,
                        #     batch_no=batch_no
                        # )
                        # stud_attd_date.save()

                        div_value = Division.objects.get(id=div).division
                        messages.success(request, f"Attendance Submitted Successfully for {div_value}-division")

                    except IntegrityError as e:
                        print(f"Duplicate entry error for student attendance date record: {e}")
                        messages.error(request, "A record for the student attendance date already exists.")
                    
                    except Exception as e:
                        print(f"Error creating student attendance date record: {e}")
                        messages.error(request, "Error creating student attendance date record.")

            else:
                print("print("")")
                scheme_details_id = Scheme_Details.objects.get(course_code = subj_course_code).scheme_details_id
                student_attendace_assigned_date = student_Attendance_date.objects.filter(acad_cal_id_id=acad_cal_id,division = division,faculty_id = Employee_Details.objects.get(employee_emp_id = faculty_id),scheme_details_id_id = Scheme_Details.objects.get(course_code = course_code),attendance_date = attend_date)
                print(student_attendace_assigned_date,"student_attendace_assigned_date")
                absentee_count_s1 = 0
                absentee_count_s2 = 0
                
                if number_of_classes == '1':
                    for st in sid:
                        if check_students(st_list_1,st):
                            print(st_list_1,"st_list_1",st,session1)
                            edit_student_present(st,int(session1),batch_no,scheme_details_id,acad_cal_id)
                        else:
                            edit_student_absent(st,int(session1),batch_no,scheme_details_id,acad_cal_id)
                            absentee_count_s1 = absentee_count_s1 + 1
                    
                    for stud_obj in student_attendace_assigned_date:
                        print(absentee_count_s1)
                        stud_obj.absentees_count = absentee_count_s1
                    stud_obj.save()

                else:
                    batch_no = "B0"
                    for st in sid:
                        if check_students(st_list_1,st):
                            edit_student_present(st,int(session1),batch_no,scheme_details_id,acad_cal_id)
                        else:
                            edit_student_absent(st,int(session1),batch_no,scheme_details_id,acad_cal_id)
                            absentee_count_s1 = absentee_count_s1 + 1
                    
                    for st in sid:
                        if check_students(st_list_2,st):
                            edit_student_present(st,int(session2),batch_no,scheme_details_id,acad_cal_id)
                        else:
                            edit_student_absent(st,int(session2),batch_no,scheme_details_id,acad_cal_id)
                            absentee_count_s2 = absentee_count_s2 + 1
                    
                    i = 1
                    for stud_obj in student_attendace_assigned_date:
                        if i == 1:
                            stud_obj.absentees_count = absentee_count_s1
                            i = i+1
                            stud_obj.save()
                        else:
                            stud_obj.absentees_count = absentee_count_s2
                            stud_obj.save()
                div_value = Division.objects.get(id=div).division
                messages.success(request, "Attendance Updated Successfully "+div_value+"-div")

        except IntegrityError:
          messages.warning(request, "You have already took the attendance"+div+"-div")
        except Exception as e:
            print(e)
        userName=CustomUser.objects.get(id=request.user.id)
        context={'username':userName}
        return render(request,"student_attendance.html",{'username':userName,'div_tbl':Division.objects.all(),'calender': Academic_Calendar.objects.values('acad_cal_acad_year_id').distinct(),'scheme_detail':Scheme_Details.objects.all()})

#------------------------------Edit Student Attendance-----------------------------------------------------
def edit_student_attendance(request):
    userName=CustomUser.objects.get(id=request.user.id)
    if request.POST:
        acad_year = request.POST['acad_year']
        scheme_details_id = request.POST['subject']
        attend_date = request.POST['attend_date']
        division = request.POST['div']
        acad_cal_type = request.POST['acad_cal_type']
        batch_no = request.POST['batch']
        print(scheme_details_id)
        scheme_details_id=Scheme_Details.objects.get(course_code = scheme_details_id ).scheme_details_id
        absentee_count_s1 = 0
        absentee_count_s2 = 0

        scheme_obj = Scheme_Details.objects.get(scheme_details_id = scheme_details_id )
        semester = scheme_obj.sem_allotted
        course_id = Scheme_Details.objects.get(scheme_details_id=scheme_details_id)
        course_code = course_id.course_code
        
        faculty_obj = Faculty_Course_Allotment.objects.filter(division=division,acad_year=acad_year,course_code =course_code,batch_no=batch_no,acad_cal_type=acad_cal_type)
        if not faculty_obj.exists():
            messages.error(request,"Details Not Found")
            return render(request,"student_attendance.html",{'div_tbl':Division.objects.all(),'calender': Academic_Calendar.objects.all(),'scheme_detail':Scheme_Details.objects.all()})
            
        faculty_obj = Faculty_Course_Allotment.objects.get(division=division,acad_year=acad_year,course_code =course_code,batch_no=batch_no,acad_cal_type=acad_cal_type)
        faculty_id = faculty_obj.employee_emp_id.employee_emp_id
     

        acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id= acad_year,acad_cal_sem = semester,acad_cal_type=acad_cal_type)
       
        student_obj = student_attendance.objects.filter(acad_cal_id=acad_cal_id,division = division,scheme_details_id_id=scheme_details_id,batch_no=batch_no).order_by('st_uid')
        
        for st in student_obj:
            print(st.st_uid.st_uid)

        student_attendace_assigned_date = student_Attendance_date.objects.filter(acad_cal_id_id=acad_cal_id,division = division,faculty_id = Employee_Details.objects.get(employee_emp_id = faculty_id),scheme_details_id_id = Scheme_Details.objects.get(course_code = course_code),attendance_date = attend_date,batch_no=batch_no)

        numberofclasses = len(student_attendace_assigned_date)
       
        if numberofclasses == 0:
            messages.error(request,"You have not yet took Attendance on "+attend_date)
            return render(request,"Edit_student_attendance.html",{'div_tbl':Division.objects.all(),'calender': Academic_Calendar.objects.all(),'scheme_detail':Scheme_Details.objects.all()})
       
        i = 1
        i = int(i)
        session1 = 0
        session2 = 0
        for date_obj in student_attendace_assigned_date:
            if numberofclasses == 1:
                session1 = date_obj.session_index
                session2 = 0
                absentee_count_s1 = date_obj.absentees_count
                break
            else:
                if i == 1:
                    session1 = date_obj.session_index
                    absentee_count_s1 = date_obj.absentees_count
                    i = i+1
                else :
                    session2 = date_obj.session_index
                    absentee_count_s2 = date_obj.absentees_count
                    break
       

        edit_status_session1 = []

        edit_status_session2 = []
      
        for stu_obj in student_obj:
            if numberofclasses == 1:
               
                edit_status_session1.append(stu_obj.status[session1-1])
                edit_status_session2.append(stu_obj.status[session1-1])  
               
            else:
                print(stu_obj.status[session1-1])
                print(stu_obj.status[session2-1])
                edit_status_session1.append(stu_obj.status[session1-1])
                edit_status_session2.append(stu_obj.status[session2-1])  
               
        old_attendance = zip(student_obj,edit_status_session1,edit_status_session2)

        edit_permission = None
        btn_value = request.POST["btn_clicked"]
        if btn_value == "register":  
            print("acad year to attendance list function")
            print(acad_year) 
            div = Division.objects.get(id=division) 
            print("hhhhhhhh")
            print(old_attendance)
            print(batch_no)
            return render(request,"attendance_list.html",{'div_tbl':Division.objects.all(),'calender': Academic_Calendar.objects.values('acad_cal_acad_year_id').distinct(),'scheme_detail':scheme_obj,'attend_date':attend_date,'numberofclasses':numberofclasses,'acad_year':acad_year,'division':division,'session1':session1,'session2':session2,'edit_permission':edit_permission,'edit_status_session1':edit_status_session1,'edit_status_session2':edit_status_session2,'old_attendance':old_attendance,'absentee_count_s1':absentee_count_s1,'absentee_count_s2':absentee_count_s2,'div_html':div,'acad_cal_type':acad_cal_type,'batch_no':batch_no})
    else:
        # return render(request,"Edit_student_attendance.html",{'div_tbl':Division.objects.all(),'calender': Academic_Calendar.objects.values('acad_cal_acad_year_id').distinct(),'scheme_detail':Scheme_Details.objects.all()})
        return render(request,"Edit_student_attendance.html",{'div_tbl':Division.objects.all(),'calender' :AcademicYear.objects.all().order_by('-acayear'),'dep':Department.objects.all(),'scheme_detail':Scheme_Details.objects.all()})

def allotCycle(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        sem = None
        acadcal_id = None
        div = None
        cycle = None
        acad_yr = None
        #Scheme_id = None
        try:
            sem = int(request.POST.get("sem"))
            cycle = request.POST.get("cycle")
            div = request.POST.get("div")
            acad_yr = request.POST.get("acad_year")
            acad_id = AcademicYear.objects.get(id=acad_yr).id
            
            acad_cal_type = request.POST.get("acad_cal_type")
            acadcal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_id,acad_cal_sem=sem,acad_cal_type=acad_cal_type)
            #scheme_details_id NOT added
            print(acadcal_id)
        except Academic_Calendar.DoesNotExist:
            messages.error(request, "Please check Academic Year and enter")
            return render(request,"CycleDivisionAllotment.html",{'calender': Academic_Calendar.objects.values('acad_cal_acad_year_id').distinct()}) 

        try:
            btn_value = request.POST["btn_clicked"]
            if btn_value == "register":    
                cycle_allot = Cycle_Division_allotment.objects.create(acad_cal_id=acadcal_id,sem=sem,div=div,cycle=cycle)
                cycle_allot.save()
                messages.success(request, "Success! Allotted Department for the "+div+"-div")
            if btn_value == "Update":    
                cycle_div_allot_id = request.POST.get('cycle_div_allot_id')
                Cycle_cal_obj = Cycle_Division_allotment.objects.get(cycle_div_allot_id = cycle_div_allot_id)
                Cycle_cal_obj.acad_cal_id = acadcal_id
                Cycle_cal_obj.sem = sem
                Cycle_cal_obj.div = div
                Cycle_cal_obj.cycle = cycle
                Cycle_cal_obj.save()
                messages.success(request, "Success! Updated Cycle for the "+div+"-div")
        except IntegrityError:
            messages.warning(request, "Cycle already allotted for the "+div+"-div")
            return render(request,"CycleDivisionAllotment.html",{'calender': Academic_Calendar.objects.values('acad_cal_acad_year').distinct()})
        except Exception as e:
            print(e)
       
        return render(request,"CycleDivisionAllotment.html")


def Searchdiv(request):
    if request.POST:
        cycle_cal = request.POST['cycle_cal']
        if cycle_cal == "0":
            messages.error(request, "Please select year to Search")
        else:
            SearchParm = Cycle_Division_allotment.objects.filter(acad_cal_id = int(cycle_cal))
            if not SearchParm.exists():
                messages.error(request,"Details Not Found")
            return render(request,"Edit_cycle_division_allotment.html",{'cd':SearchParm,'calender': Academic_Calendar.objects.all()})
        return render(request,"Edit_cycle_division_allotment.html",{'calender': Academic_Calendar.objects.all()})
    else:
         return render(request,"Edit_cycle_division_allotment.html",{'calender': Academic_Calendar.objects.all()})

#First year division allotment
def allotDivision(request):
    if request.method!="POST":
        std = Student_Details.objects.all()
        dv = Cycle_Division_allotment.objects.all()
        academic_year = AcademicYear.objects.all()
        div_tbl = Division.objects.all().order_by('division')
        return render(request,"First_year_StudentDivisionAllotment.html",{'std':std,'dv':dv,'academic_year':academic_year,'div_tbl':div_tbl,'dep':Department.objects.all()})
    else:
        sem = None
        acad_yr = None
        acadcal_id = None
        div = None
        st_list = None
        tbl = None
        #Scheme_id = None
        try:
            acad_yr = request.POST.get("academic_year")
            sem = int(request.POST.get("course_sem"))
            div = request.POST.get("div")
            dept=request.POST.get("dep")
            acad_cal_type = request.POST.get("acad_cal_type")
        
            st_list = request.POST.getlist("checked_allot")

            #count = 0
            #for x in st_uid:
            acadcal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_yr,acad_cal_sem=sem,acad_cal_type=acad_cal_type)

        except Academic_Calendar.DoesNotExist:
            messages.error(request, "Please check Academic Year and Semester")
            return render(request,"First_year_StudentDivisionAllotment.html") 
        except Exception as e:
            print(e)
            messages.error(request, "Division Allotment failed. Retry!")
            return render(request,"First_year_StudentDivisionAllotment.html")  
        
        try:
            btn_value = request.POST["btn_clicked"]
            print(btn_value,"............................................")
            if btn_value == "register":   
                count = 0
                for st in st_list:
                    st_uid = st
                    div_allot = Student_Division_Allotment.objects.create(acad_cal_id=acadcal_id,division=Division.objects.get(id=div),st_uid=Student_Details.objects.get(st_uid=st_uid),dept_id=dept)
                    div_allot.save()
                    count = count+1
                if count>0:
                    division = Division.objects.get(id=div).division
                    messages.success(request, "Allotted "+division+"-Division for "+str(count)+" students!")
                else:
                    messages.error(request,"Division Allotment failed!")
                return First_year_StudentDivisionAllotment(request)  
            if btn_value == "getlist":
                context = {}
                print(acadcal_id)

                # Filter Student_Division_Allotment by provided parameters
                allotments = Student_Division_Allotment.objects.filter(
                    acad_cal_id=acadcal_id,
                    division=Division.objects.get(id=div),
                    dept=dept
                ).select_related('st_uid')  # Use select_related to optimize database access

                # Prepare the student list with the necessary details
                student_list = [
                    {
                        'st_uid': allotment.st_uid.st_uid,
                        'st_name': allotment.st_uid.st_name,
                        'division': allotment.division.division,
                        'sem':sem
                    }
                    for allotment in allotments
                ]

                context['student_list'] = student_list
                return render(request, "First_year_StudentDivisionAllotment.html", context)
        except IntegrityError:
            messages.error(request, "Error! Division already allotted for the student"+str(st_uid))
            return First_year_StudentDivisionAllotment(request)
        except Exception as e:
            print(e)                     
            return First_year_StudentDivisionAllotment(request)

#Higher semester division allotment
def ugAllotDivision(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        sem = None
        acad_yr = None
        acadcal_id = None
        div = None
        st_list = None
        dept_id = None
        try:
            acad_yr = request.POST.get("academic_year")
            sem = int(request.POST.get("course_sem"))
            div = request.POST.get("div")
            branch = request.POST.get("offered_by")
            acad_cal_type = request.POST.get("acad_cal_type")
            dept_id = Department.objects.get(dept_id=branch)
            st_list = request.POST.getlist("checked_allot")
            acadcal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_yr,acad_cal_sem=sem,acad_cal_type=acad_cal_type)
        except Academic_Calendar.DoesNotExist:
            messages.error(request, "Please check Academic Year and Semester")
            return UGStudentDivisionAllotment(request) 
        except Exception as e:
            print(e)
            messages.error(request, "Division Allotment failed. Retry!")
            return UGStudentDivisionAllotment(request)  
        
        try:
            btn_value = request.POST["btn_clicked"]
            if btn_value == "register":   
                count = 0
                for st in st_list:
                    # div_allot = UG_Student_Division_Allotment.objects.create(acad_cal_id=acadcal_id,offered_by=dept_id,division=div,st_uid=Student_Promotion_List.objects.get(st_uid=st_uid))
                    div_allot = UG_Student_Division_Allotment.objects.create(acad_cal_id=acadcal_id,offered_by=dept_id,ug_division=Division.objects.get(id=div),st_uid=Student_Details.objects.get(st_uid=st))
                    div_allot.save()
                    count = count+1
                if count>0:
                    messages.success(request, "Allotted "+div+"-Division for "+str(count)+" students!")
                else:
                    messages.error(request,"Division Allotment failed!")
                return UGStudentDivisionAllotment(request)  
        except IntegrityError:
            messages.error(request, "Error! Division already allotted for the student"+str(st))
            return UGStudentDivisionAllotment(request)
        except Exception as e:
            print(e)    
            return UGStudentDivisionAllotment(request)

def declareAssessment(request):
    department = Department.objects.all()
    course_obj = Scheme_Details.objects.all()
    # course_name = None
    print("kkkkkkkkkkkk")
    academic_year_obj = AcademicYear.objects.all().order_by('-acayear')

    sem = None
    branch = None
    acad_year_tble = AcademicYear.objects.all()
    print("vv")
    return render(request,"declareAssessment.html",{'academic_year_obj':academic_year_obj,'sem':sem,'branch':branch,'department':department, 'course_obj':course_obj, 'acad_year_tble':acad_year_tble})

def getAssessment(request):
    if request.method!="POST":
        return HttpResponseRedirect('DeclareAssessment') 
    else:
        academic_year_obj = AcademicYear.objects.all().order_by('-acayear')
        branch = request.POST.get("branch")
        print(branch)
        department = Department.objects.all()
        course_obj = Scheme_Details.objects.all()
     
        btn_value = request.POST["btn_clicked"]
        

        if btn_value == "getAssessment":
            academic_year = request.POST.get("academic_year")
            acad_year_id = AcademicYear.objects.get(acayear=academic_year) # Fetch acad_year_id
            course_name = request.POST.get("course_name")
            sem = request.POST.get("course_sem")
            acad_cal_type = request.POST.get("acad_cal_type")
            print("pppp",acad_cal_type,course_name)
            try:
               
                
               
                course_id = Scheme_Details.objects.get(course_code = course_name,sem_allotted=sem,offered_by_id=branch)
                print(course_id)
                          
                # course_id = Scheme_Details.objects.get(course_title = course_title,course_code = course_code,sem_allotted=sem,offered_by_id=branch)
                # print(course_id,"////////////")
                acad_year_obj = Academic_Calendar.objects.get(acad_cal_acad_year_id = acad_year_id,acad_cal_sem=sem,acad_cal_type=acad_cal_type)
                print(acad_year_obj)
                assessments = Declare_Assessment.objects.all().filter(acad_cal_id_id = acad_year_obj.acad_cal_id,scheme_details_id_id = course_id.scheme_details_id,sem = sem)
                print(acad_cal_type,"00000000000000000")
                return render(request,"declareAssessment.html",{'course_name':course_name,'academic_year':academic_year,'academic_year_obj':academic_year_obj,'sem':sem,'branch':branch,'department':department, 'course_obj':course_obj,'assessments':assessments,'acad_cal_type':acad_cal_type})
            except Exception as e:
                #messages.error(request, "Error! Please enter the details correctly")
                messages.error(request,e)
                context={'department':department, 'course_obj':course_obj}
                return render(request,"declareAssessment.html",context=context) 

        elif btn_value == "addAssessment":
            try:
                academic_year = request.POST.get("acadYear")
                print("-------------------")
                print(academic_year)
                acad_year_id = AcademicYear.objects.get(acayear=academic_year) # Fetch acad_year_id
                course_name = request.POST.get("course")
                sem = request.POST.get("sem")
                assessmentType = request.POST.get("assessmentType")
                date = request.POST.get("date")
                max_marks = request.POST.get("max_marks")
                acad_cal_type = request.POST.get("acad_cal_type")
                print("///////",course_name)
                # print(sem,acad_cal_type,max_marks,"//////////////////////////")
                # course = course_name.split("-")
                course_id = Scheme_Details.objects.get(course_code = course_name,offered_by=branch,sem_allotted=sem)
                print("lll")
                acad_year_obj = Academic_Calendar.objects.get(acad_cal_sem = sem,acad_cal_acad_year_id= acad_year_id,acad_cal_type=acad_cal_type)
                print(acad_year_obj)
                try:
                    add_assessment = Declare_Assessment.objects.create(acad_cal_id_id = acad_year_obj.acad_cal_id,sem = sem,assessment_type=assessmentType,date=date,max_marks=max_marks,scheme_details_id_id = course_id.scheme_details_id)
                    add_assessment.save()
                except IntegrityError: 
                    messages.error(request, "Error! Duplicate entry not possible")

                assessments = Declare_Assessment.objects.all().filter(acad_cal_id_id = acad_year_obj.acad_cal_id,scheme_details_id_id = course_id.scheme_details_id,sem = sem)
                return render(request,"declareAssessment.html",{'course_name':course_name,'academic_year':academic_year,'academic_year_obj':academic_year_obj,'sem':sem,'branch':branch,'department':department, 'course_obj':course_obj,'assessments':assessments,'acad_cal_type':acad_cal_type})

            except:
                messages.error(request, "Error! Course details not found")
                return HttpResponseRedirect('DeclareAssessment') 

        elif btn_value == "editAssessment":
            id = request.POST.get("btn_ass_id")
            print("in edit assmnt")
            academic_year = request.POST.get("acadYear")
            print("aca year in edit")
            print(academic_year)
            course_name = request.POST.get("course")
            sem = request.POST.get("sem")
            assessment = Declare_Assessment.objects.get(declare_assessment_id = id)
            return render(request,"declareAssessment.html",{'id':id,'course_name':course_name,'academic_year':academic_year,'academic_year_obj':academic_year_obj,'sem':sem,'branch':branch,'department':department, 'course_obj':course_obj,'assessment':assessment})

        
        elif btn_value == "deleteAssessment":
            id = request.POST.get("btn_ass_id")
            academic_year = request.POST.get("acadYear")
            acad_year_id = AcademicYear.objects.get(acayear=academic_year).id
            course_name = request.POST.get("course")
            sem = request.POST.get("sem")
            print(course_name,"course_namecourse_name")
            
            acad_cal_type = request.POST.get("acad_cal_type")
            try:
                update_assessment = Declare_Assessment.objects.get(declare_assessment_id = id)
                update_assessment.delete()
            except:
                messages.error(request, "Error! Cannot delete the assessment")

            course_id = Scheme_Details.objects.get(course_code = course_name,offered_by_id=branch)
            acad_year_obj = Academic_Calendar.objects.get(acad_cal_acad_year_id = acad_year_id,acad_cal_sem=sem,acad_cal_type=acad_cal_type)
            assessments = Declare_Assessment.objects.all().filter(acad_cal_id_id = acad_year_obj.acad_cal_id,scheme_details_id_id = course_id.scheme_details_id,sem = sem)
            messages.success(request, "Success! Assessment deleted successfully")
            return render(request,"declareAssessment.html",{'course_name':course_name,'academic_year':academic_year,'academic_year_obj':academic_year_obj,'sem':sem,'branch':branch,'department':department, 'course_obj':course_obj,'assessments':assessments,'acad_cal_type':acad_cal_type})

        elif btn_value == "addMarks":
            pritn("mmmmmmmmmmmmmmmmmm")
            return HttpResponseRedirect('bitWiseMarks')

        elif btn_value == "updateAssessment":
            id = request.POST.get("btn_ass_id")
            academic_year = request.POST.get("acadYear")
            acad_year_id = AcademicYear.objects.get(acayear=academic_year) # Fetch acad_year_id

            course_name = request.POST.get("course")
            sem = request.POST.get("sem")
            assessmentType = request.POST.get("assessmentType")
            date = request.POST.get("date")
            max_marks = request.POST.get("max_marks")
            course = course_name.split("-")
            acad_cal_type = request.POST.get("acad_cal_type") 
            print("ppp",acad_cal_type,"pppu")
            course_id = Scheme_Details.objects.get(course_title = course[0].strip(),course_code = course[1].strip(),offered_by_id=branch)
            try:
                update_assessment = Declare_Assessment.objects.get(declare_assessment_id = id)
                update_assessment.assessment_type = assessmentType
                update_assessment.date = date
                update_assessment.max_marks = max_marks
                update_assessment.save()
            except:
                messages.error(request, "Error! Cannot update the assessment")
            acad_year_obj = Academic_Calendar.objects.get(acad_cal_acad_year_id = acad_year_id,acad_cal_sem=sem,acad_cal_type=acad_cal_type)
            assessments = Declare_Assessment.objects.all().filter(acad_cal_id_id = acad_year_obj.acad_cal_id,scheme_details_id_id = course_id.scheme_details_id,sem = sem)
            return render(request,"declareAssessment.html",{'course_name':course_name,'academic_year':academic_year,'academic_year_obj':academic_year_obj,'sem':sem,'branch':branch,'department':department, 'course_obj':course_obj,'assessments':assessments})

def assessment_pattern(request):
    if request.method!="POST":
        userName=CustomUser.objects.get(id=request.user.id)

        cos = Course_Outcome.objects.all() # All Course_Outcome object for displaying in UI
        sd = Scheme_Details.objects.all()  # All Scheme_Details object for displaying in UI
        return render(request,"assessment_pattern.html",{'username':userName, 'cos': cos, 'sd':sd})
    else:

        no_of_questions = request.POST.get('no-of-question')
        no_of_questions_to_be_answered = request.POST.get('no-of-question-to-be-answered')
        declare_assessment_id_val = request.POST.get('assessment_id')


        assessment = Declare_Assessment.objects.get(declare_assessment_id=declare_assessment_id_val)

        no_of_cos = Course_Outcome.objects.all().count()


        print('no_of_questions:' + str(no_of_questions))

        with transaction.atomic():
            for i in range(1,int(no_of_questions)+1):
                no_of_sub_questions = request.POST.get('q-'+str(i)+'-sub-q')
                max_marks = request.POST.get('q-'+str(i)+'-max-marks')
                is_compulsory = request.POST.get('q-'+str(i)+'-is-compulsory')
                if is_compulsory is None:
                    is_compulsory=0

                assessment_pattern_q = Assessment_Pattern_Question.objects.create(qnum=str(i), is_compulsory=is_compulsory, max_marks=max_marks, declare_assessment_id=assessment )
                for j in range(1, int(no_of_sub_questions)+1):
                    subqmarks = request.POST.get('q-'+str(i)+'-sub-q-'+chr(97+j-1)+'-marks')
                    


                    co_list = []
                    for k in range(1, int(no_of_cos)+1):
                        coi ='q-'+str(i)+'-sub-q-'+chr(97+j-1)+'-cos-input-'+str(k)
                        co = request.POST.get(coi)

                        if co is not None:
                            co_list.append(co)

                    try:
                        
                        assessment_pattern = Assessment_Pattern_Sub_Question.objects.create(assessment_pattern_qnum_id=assessment_pattern_q, subqnum=chr(97+j-1), max_marks=subqmarks)
                        assessment.ans_q = no_of_questions_to_be_answered
                        assessment.save()
                        assessment_pattern.co.set(Course_Outcome.objects.filter(co_num__in=co_list))
                    except IntegrityError: 
                        messages.error(request, "Error! Duplicate entry not possible")
                    
            messages.success(request, "Success! Assessment Pattern Added Sucessfully")

        cos = Course_Outcome.objects.all() # All Course_Outcome object for displaying in UI
        sd = Scheme_Details.objects.all()  # All Scheme_Details object for displaying in UI
        userName=CustomUser.objects.get(id=request.user.id)


        assessments = Declare_Assessment.objects.all().filter(acad_cal_id = assessment.acad_cal_id, scheme_details_id = assessment.scheme_details_id ,sem = assessment.sem)
        return render(request,"declareAssessment.html",{'course_name':assessment.scheme_details_id.course_title,'academic_year':assessment.acad_cal_id.acad_cal_acad_year_id,'sem':assessment.scheme_details_id.sem_allotted,'assessments':assessments,'acad_acal_type':assessment.acad_cal_id.acad_cal_type, 'username':userName})

def add_assessment_pattern(request, id):
    assessment = Declare_Assessment.objects.get(declare_assessment_id=id)
    userName=CustomUser.objects.get(id=request.user.id)
    academic_year = AcademicYear.objects.all()
    cos = Course_Outcome.objects.all() # All Course_Outcome object for displaying in UI
    return render(request,"assessment_pattern.html",{'username':userName,'cos': cos,'assessment': assessment,'calender': Academic_Calendar.objects.values('acad_cal_acad_year').distinct(), 'academic_year':academic_year})


def edit_assessment_pattern(request, id):
    if request.method!= "POST":
        cos = Course_Outcome.objects.all() # All Course_Outcome object for displaying in UI
        assessment = Declare_Assessment.objects.get(declare_assessment_id=id)
        userName=CustomUser.objects.get(id=request.user.id)

        details = dict()
        qlist = dict()
        no_of_questions = assessment.questions.all().values('qnum').distinct().count()
        no_of_questions_to_be_answered = assessment.ans_q

        details['assessment'] = assessment
        details['no_of_questions'] = no_of_questions
        details['no_of_questions_to_be_answered'] = no_of_questions_to_be_answered

        for i in range(1, int(no_of_questions)+1):
            question = assessment.questions.get(qnum=i)
            qnum = dict()
            qnum['compulsory'] = question.is_compulsory
            qnum['max_marks'] =  question.max_marks

            
            no_of_sub_questions = question.subquestion.count()
            sub_q_list = dict()
            qnum['no_of_sub_questions'] = no_of_sub_questions
            for j in range(1, int(no_of_sub_questions)+1):
                max_marks = question.subquestion.get(subqnum=chr(97+j-1)).max_marks
                co = question.subquestion.get(subqnum=chr(97+j-1)).co.all().values('co_num')
                sub_q = dict()

                sub_q['max_marks'] = max_marks
                sub_q['co'] = co
                sub_q_list[chr(97+j-1)] = sub_q
            qnum['sub_q_list'] = sub_q_list
            
            qlist[i] = qnum

        return render(request,"edit_assessment_pattern.html",{'username':userName, 'cos': cos, 'assessment': assessment , 'details': details, 'qlist': qlist})
    else :
        assessment = Declare_Assessment.objects.get(declare_assessment_id=id)
        with transaction.atomic():
            try:
                assessment.questions.all().delete()
            except Exception as e:
                print(e)
                messages.error(request, "Error! Cannot delete the assessment")

            
            no_of_questions = request.POST.get('no-of-question')
            no_of_questions_to_be_answered = request.POST.get('no-of-question-to-be-answered')
            declare_assessment_id_val = request.POST.get('assessment_id')

            assessment = Declare_Assessment.objects.get(declare_assessment_id=declare_assessment_id_val)

            # Getting how many course outcomes are there in the data_base
            no_of_cos = Course_Outcome.objects.all().count()

            print('no_of_questions:' + str(no_of_questions))

            for i in range(1,int(no_of_questions)+1):
                no_of_sub_questions = request.POST.get('q-'+str(i)+'-sub-q')
                max_marks = request.POST.get('q-'+str(i)+'-max-marks')
                is_compulsory = request.POST.get('q-'+str(i)+'-is-compulsory')
                if is_compulsory is None:
                    is_compulsory=0

                assessment_pattern_q = Assessment_Pattern_Question.objects.create(qnum=str(i), is_compulsory=is_compulsory, max_marks=max_marks, declare_assessment_id=assessment )
                for j in range(1, int(no_of_sub_questions)+1):
                    subqmarks = request.POST.get('q-'+str(i)+'-sub-q-'+chr(97+j-1)+'-marks')

                    co_list = []
                    for k in range(1, int(no_of_cos)+1):
                        coi ='q-'+str(i)+'-sub-q-'+chr(97+j-1)+'-cos-input-'+str(k)
                        co = request.POST.get(coi)

                        if co is not None:
                            co_list.append(co)

                    try:
                        
                        assessment_pattern = Assessment_Pattern_Sub_Question.objects.create(assessment_pattern_qnum_id=assessment_pattern_q, subqnum=chr(97+j-1), max_marks=subqmarks)
                        assessment.ans_q = no_of_questions_to_be_answered
                        assessment.save()
                        assessment_pattern.co.set(Course_Outcome.objects.filter(co_num__in=co_list))
                    except IntegrityError: 
                        messages.error(request, "Error! Duplicate entry not possible")
                
        messages.success(request, "Success! Assessment Pattern Modified Sucessfully")

        cos = Course_Outcome.objects.all() # All Course_Outcome object for displaying in UI
        sd = Scheme_Details.objects.all()  # All Scheme_Details object for displaying in UI
        userName=CustomUser.objects.get(id=request.user.id)
        composite_course_name = assessment.scheme_details_id.course_title+"-"+assessment.scheme_details_id.course_code
        academic_year = assessment.acad_cal_id.acad_cal_acad_year
        assessments = Declare_Assessment.objects.all().filter(acad_cal_id = assessment.acad_cal_id, scheme_details_id = assessment.scheme_details_id ,sem = assessment.sem)
        return render(request,"declareAssessment.html",{'course_name':composite_course_name,'academic_year':academic_year,'sem':assessment.scheme_details_id.sem_allotted,'assessments':assessments, 'username':userName})

def bitWiseMarks(request):

    if request.method!="POST":
        return HttpResponseRedirect('DeclareAssessment') 
    else:
        userName=CustomUser.objects.get(id=request.user.id)
      
        id = request.POST.get("btn_ass_id")
        academic_year = request.POST.get("acadYear")
        print(academic_year)
        acad_cal_type = request.POST.get("acad_cal_type")
        print(acad_cal_type,"//////////////")

        
        academic_year_id = AcademicYear.objects.get(acayear = academic_year).id
    
        
        # academic_year_id = AcademicYear.objects.get(id = academic_year)
        course_name = request.POST.get("course")
        print(course_name)

        sem = int(request.POST.get("sem"))
       
        course = course_name.split("-")
      
        # print(userName.username)
        # employee = Employee_Details.objects.get(emp_login=userName.username)
        # print(employee)
        faculty_course_details = Faculty_Course_Allotment.objects.filter(acad_year=academic_year_id,sem=sem,course_code=course_name,employee_emp_id=Employee_Details.objects.get(employee_emp_id=userName),acad_cal_type=acad_cal_type)
       
        scheme_details_id = Scheme_Details.objects.get(course_code = course_name)

        btn_clicked = request.POST.get("btn_clicked")
        
        students = None

        if sem == 1:
            print("Fetching students for semester 1")
            print(acad_cal_type)
            academic_calendar = Academic_Calendar.objects.get(acad_cal_acad_year_id=academic_year_id, acad_cal_sem=sem,acad_cal_type=acad_cal_type)
            students = First_Year_Student_Course_Registration_Details.objects.filter(acad_cal_id=academic_calendar, semester=sem, scheme_details_id=scheme_details_id)
            print(students)
        elif sem == 2:
            print("Fetching students for semester 2")
            academic_calendar = Academic_Calendar.objects.get(acad_cal_acad_year_id=academic_year_id, acad_cal_sem=sem,acad_cal_type=acad_cal_type)
            students = First_Year_Student_Course_Registration_Details.objects.filter(acad_cal_id=academic_calendar, semester=sem, scheme_details_id=scheme_details_id)
            print(students)
        else:
            print("Fetching students for other semesters")
            academic_calendar = Academic_Calendar.objects.get(acad_cal_acad_year_id=academic_year_id, acad_cal_sem=sem,acad_cal_type=acad_cal_type)
            students = UG_Student_Course_Registration_Details.objects.filter(acad_cal_id=academic_calendar, semester=sem, scheme_details_id=scheme_details_id)
            print(students)
        # Getting only assessments that have pattern declared
        declared_asessments = Declare_Assessment.objects.all().filter(scheme_details_id = scheme_details_id,acad_cal_id=Academic_Calendar.objects.get(acad_cal_acad_year_id=academic_year_id,acad_cal_sem=sem,acad_cal_type=acad_cal_type))
        #print(declared_asessments)
        asessments = []
        for asessment in declared_asessments : 
            if asessment.questions.count() > 0 :
                asessments.append(asessment)
        


        if btn_clicked == "save":
            print("pppppppppppppppppppppppppppppppppppppppppppppppp")
            uid = request.POST.get("uid")
            print(uid)
            assessment_id = request.POST.get("assessment_id")
            print(assessment_id)
            id = request.POST.get("btn_ass_id")
            academic_year = request.POST.get("acadYear")
            course_name = request.POST.get("course")
            acad_cal_type = request.POST.get("acad_cal_type")
            print("course name")
            print(course_name)
            sem = request.POST.get("sem")
            academic_calendar = Academic_Calendar.objects.get(acad_cal_acad_year_id=academic_year_id, acad_cal_sem=sem,acad_cal_type=acad_cal_type)

            qnums = Assessment_Pattern_Question.objects.all().filter(declare_assessment_id_id=assessment_id)
            declareAssessment = Declare_Assessment.objects.get(declare_assessment_id=assessment_id)
            student = Student_Details.objects.get(st_uid=uid)
            print(student)
            ia1_marks = 0
            ia2_marks = 0
            ia3_marks = 0
            cta_marks = 0
            cie_marks = 0
            min_ia_marks = 0
            all_ia_marks_sum = 0
            cie_marks = 0
            grade = 'A'
            if declareAssessment.assessment_type =='IA-1':
                ques = dict()
                for que in qnums:
                    subqnums = Assessment_Pattern_Sub_Question.objects.filter(assessment_pattern_qnum_id=que)
                    ques[que] = subqnums

                total_qns_marks = dict()
                total_cmp_marks = dict()
                for que, subques in ques.items():
                    
                    total_marks = 0

                    for subque in subques:
                        marks = request.POST.get(str(que.qnum)+"_"+subque.subqnum)
                        print(str(que.qnum)+"_"+subque.subqnum)

                        # try:
                        
                        total_marks += int(marks)
                        if marks == '':
                            marks = 0
                        assessment_pattern = Assessment_Pattern_Question.objects.get(declare_assessment_id_id = assessment_id,qnum=que.qnum)
                
                        st_details = BitWise_Marks.objects.all().filter(st_uid=student,qnum=que.qnum,subqnum=subque.subqnum,assessment_pattern_id=assessment_pattern)
                        if st_details.exists():
                            updateBitWiseMarks = BitWise_Marks.objects.get(st_uid=student,qnum=que.qnum,subqnum=subque.subqnum,assessment_pattern_id=assessment_pattern)
                            updateBitWiseMarks.obtained_marks = marks
                            updateBitWiseMarks.save()
                        else:
                            addBitWiseMarks = BitWise_Marks.objects.create(st_uid=student,qnum=que.qnum,subqnum=subque.subqnum,obtained_marks=marks,assessment_pattern_id=assessment_pattern)
                            addBitWiseMarks.save()
                        # except:
                        #     messages.error(request, "Error! Cannot update the assessment")
                st_total_marks = request.POST.get("st_total_marks")
                ia1_marks = int(st_total_marks)
                print('hello sumanth')
                print(st_total_marks)
                # Sumanth=Academics_Master_Details.objects.create(scheme_details_id = scheme_details_id,st_uid_id=student,st_branch_applied_id=9)
                # Sumanth.save()
                Academics_Master_Details.objects.filter(scheme_details_id = scheme_details_id,st_uid=student,acad_cal_id=academic_calendar).update(ia1_marks = ia1_marks)            

                        #IA1_marks.save()  
            elif declareAssessment.assessment_type =='IA-2':
                ques = dict()
                for que in qnums:
                    subqnums = Assessment_Pattern_Sub_Question.objects.filter(assessment_pattern_qnum_id=que)
                    ques[que] = subqnums

                total_qns_marks = dict()
                total_cmp_marks = dict()
                for que, subques in ques.items():
                    
                    total_marks = 0

                    for subque in subques:
                        marks = request.POST.get(str(que.qnum)+"_"+subque.subqnum)

                        # try:
                        total_marks += int(marks)
                        if marks == '':
                            marks = 0
                        assessment_pattern = Assessment_Pattern_Question.objects.get(declare_assessment_id_id = assessment_id,qnum=que.qnum)
                
                        st_details = BitWise_Marks.objects.all().filter(st_uid=student,qnum=que.qnum,subqnum=subque.subqnum,assessment_pattern_id=assessment_pattern)
                        if st_details.exists():
                            updateBitWiseMarks = BitWise_Marks.objects.get(st_uid=student,qnum=que.qnum,subqnum=subque.subqnum,assessment_pattern_id=assessment_pattern)
                            updateBitWiseMarks.obtained_marks = marks
                            updateBitWiseMarks.save()
                        else:
                            addBitWiseMarks = BitWise_Marks.objects.create(st_uid=student,qnum=que.qnum,subqnum=subque.subqnum,obtained_marks=marks,assessment_pattern_id=assessment_pattern)
                            addBitWiseMarks.save()
            
                if(que.is_compulsory == 0):
                    total_qns_marks[que.qnum] = total_marks
                else:
                    total_cmp_marks[que.qnum] = total_marks

                st_total_marks = request.POST.get("st_total_marks")

                ia2_marks = int(st_total_marks)
                Academics_Master_Details.objects.filter(scheme_details_id = scheme_details_id,st_uid=student,acad_cal_id=academic_calendar).update(ia2_marks = ia2_marks)

            elif declareAssessment.assessment_type =='IA-3':
                ques = dict()
                for que in qnums:
                    subqnums = Assessment_Pattern_Sub_Question.objects.filter(assessment_pattern_qnum_id=que)
                    ques[que] = subqnums

                total_qns_marks = dict()
                total_cmp_marks = dict()
                for que, subques in ques.items():
                    
                    total_marks = 0

                    for subque in subques:
                        marks = request.POST.get(str(que.qnum)+"_"+subque.subqnum)

                        # try:
                        total_marks += int(marks)
                        if marks == '':
                            marks = 0
                        assessment_pattern = Assessment_Pattern_Question.objects.get(declare_assessment_id_id = assessment_id,qnum=que.qnum)
                
                        st_details = BitWise_Marks.objects.all().filter(st_uid=student,qnum=que.qnum,subqnum=subque.subqnum,assessment_pattern_id=assessment_pattern)
                        if st_details.exists():
                            updateBitWiseMarks = BitWise_Marks.objects.get(st_uid=student,qnum=que.qnum,subqnum=subque.subqnum,assessment_pattern_id=assessment_pattern)
                            updateBitWiseMarks.obtained_marks = marks
                            updateBitWiseMarks.save()
                        else:
                            addBitWiseMarks = BitWise_Marks.objects.create(st_uid=student,qnum=que.qnum,subqnum=subque.subqnum,obtained_marks=marks,assessment_pattern_id=assessment_pattern)
                            addBitWiseMarks.save()
                        # except:
                        #     messages.error(request, "Error! Cannot update the assessment")
                st_total_marks = request.POST.get("st_total_marks")
                print(st_total_marks)
                ia3_marks = int(st_total_marks)
                Academics_Master_Details.objects.filter(scheme_details_id = scheme_details_id,st_uid=student,acad_cal_id=academic_calendar).update(ia3_marks = ia3_marks)            

            elif declareAssessment.assessment_type =='CTA':
                ques = dict()
                for que in qnums:
                    subqnums = Assessment_Pattern_Sub_Question.objects.filter(assessment_pattern_qnum_id=que)
                    ques[que] = subqnums

                total_qns_marks = dict()
                total_cmp_marks = dict()
                for que, subques in ques.items():
                    
                    total_marks = 0

                    for subque in subques:
                        marks = request.POST.get(str(que.qnum)+"_"+subque.subqnum)

                        # try:
                        total_marks += int(marks)
                        if marks == '':
                            marks = 0
                        assessment_pattern = Assessment_Pattern_Question.objects.get(declare_assessment_id_id = assessment_id,qnum=que.qnum)
                
                        st_details = BitWise_Marks.objects.all().filter(st_uid=student,qnum=que.qnum,subqnum=subque.subqnum,assessment_pattern_id=assessment_pattern)
                        if st_details.exists():
                            updateBitWiseMarks = BitWise_Marks.objects.get(st_uid=student,qnum=que.qnum,subqnum=subque.subqnum,assessment_pattern_id=assessment_pattern)
                            updateBitWiseMarks.obtained_marks = marks
                            updateBitWiseMarks.save()
                        else:
                            addBitWiseMarks = BitWise_Marks.objects.create(st_uid=student,qnum=que.qnum,subqnum=subque.subqnum,obtained_marks=marks,assessment_pattern_id=assessment_pattern)
                            addBitWiseMarks.save()
                        # except:
                        #     messages.error(request, "Error! Cannot update the assessment")
                st_total_marks = request.POST.get("st_total_marks")
                cta_marks = int(st_total_marks)
                Academics_Master_Details.objects.filter(scheme_details_id = scheme_details_id,st_uid=student,acad_cal_id=academic_calendar).update(cta_marks = cta_marks)
                
                # CIE = request.POST.get(str(student.st_uid)+"_CIE")
                # print("+++++++++++++++")
                # print(str(student.st_uid)+"_CIE")
            #total_marks = request.POST.get(str(student.st_uid)+"_CIE")
            print(str(student.st_uid)+"_CIE")
            print(st_total_marks)

           
            ia1_marks = Academics_Master_Details.objects.get(scheme_details_id = scheme_details_id,st_uid=student,acad_cal_id=academic_calendar).ia1_marks
            ia2_marks = Academics_Master_Details.objects.get(scheme_details_id = scheme_details_id,st_uid=student,acad_cal_id=academic_calendar).ia2_marks
            ia3_marks = Academics_Master_Details.objects.get(scheme_details_id = scheme_details_id,st_uid=student,acad_cal_id=academic_calendar).ia3_marks
            cta_marks = Academics_Master_Details.objects.get(scheme_details_id = scheme_details_id,st_uid=student,acad_cal_id=academic_calendar).cta_marks

            # Best 2 out of 3 IA-marks + CTA
            min_ia_marks = min(ia1_marks,ia2_marks,ia3_marks)
            all_ia_marks_sum = ia1_marks+ia2_marks+ia3_marks
            cie_marks = all_ia_marks_sum-min_ia_marks+cta_marks

            if cie_marks>=20:
                Academics_Master_Details.objects.filter(scheme_details_id = scheme_details_id,st_uid=student,acad_cal_id=academic_calendar).update(final_cie_eligibility_status = 1)
            
            # Grade Calculation
            if cie_marks>=45 :
                grade = 'S'
            elif cie_marks>=40 :
                grade = 'A'
            elif cie_marks>=35 :
                grade = 'B'
            elif cie_marks>=30 :
                grade = 'C'
            elif cie_marks>=25 :
                grade = 'D'
            elif cie_marks>=20 :
                grade = 'E'
            else:
                grade = 'F'
            #02-06-2023 Cie marks taken as a latest entry in the row
            Academics_Master_Details.objects.filter(scheme_details_id = scheme_details_id,st_uid=student,acad_cal_id=academic_calendar).update(cie_marks = cie_marks,cie_grade=grade)

        studentList = dict()
        for st in students:

            iaType = dict()
            for ia in asessments:
                qnums = Assessment_Pattern_Question.objects.all().filter(declare_assessment_id_id=ia.declare_assessment_id)
                st_qnums = BitWise_Marks.objects.all().filter(st_uid_id=st.st_uid,assessment_pattern_id__in=qnums)
                
                st_que_list = dict()
                if st_qnums.exists():
                    for que in qnums:
                        subqnums = BitWise_Marks.objects.all().filter(qnum=que.qnum,st_uid_id=st.st_uid,assessment_pattern_id__in=qnums)
                        # for sub in subqnums:
                        #     print(sub.assessment_pattern_id.subquestion.get(subqnum=sub.subqnum).max_marks)
                        st_que_list[que] = subqnums
            
                else:
                    for que in qnums:
                        subqnums = Assessment_Pattern_Sub_Question.objects.filter(assessment_pattern_qnum_id=que)
                        
                        st_que_list[que] = subqnums 
                iaType[ia] = st_que_list
            
            
            studentList[Student_Details.objects.get(st_uid=st.st_uid.st_uid)] = iaType
        #print(studentList)
        studentMarksList = dict()
        for st in students:
            iaMarks = dict()
            for ia in asessments:
                print("what is ia")
                try:
                    iamarks = Academics_Master_Details.objects.get(st_uid=st.st_uid,scheme_details_id = scheme_details_id,acad_cal_id=academic_calendar)
                    print(iamarks)
                    print(ia.assessment_type)
                    if ia.assessment_type == 'IA-1':
                        iaMarks[ia] = iamarks.ia1_marks
                        print(iaMarks[ia])
                    elif ia.assessment_type == 'IA-2':
                        iaMarks[ia] = iamarks.ia2_marks
                        print(iaMarks[ia])
                    elif ia.assessment_type == 'IA-3':
                        iaMarks[ia] = iamarks.ia3_marks
                        print(iaMarks[ia])
                    elif ia.assessment_type == 'CTA':
                        iaMarks[ia] = iamarks.cta_marks
                        print(iaMarks[ia])

                except:
                    iaMarks[ia] = 0
            
            #final_cie_marks = max(iaMarks)
            studentMarksList[Student_Details.objects.get(st_uid=st.st_uid.st_uid)] = iaMarks


            # print(iaMarks[])    
            # Academics_Master_Details.objects.filter(scheme_details_id_id = scheme_details_id,st_uid=student).update(cie_marks = iaMarks)

        return render(request,"bitWiseMarks.html",{'username':userName,'students':students,'studentList':studentList,'asessments':asessments,'course_name':course_name,'academic_year':academic_year,'sem':sem,'studentMarksList':studentMarksList,'acad_cal_type':acad_cal_type})

def load_first_year_course(request):
    acad_year_tbl = AcademicYear.objects.all().order_by('-acayear')
    cyd = Department.objects.all()
    return render(request,"FirstYearCourseDetails.html",{'acad_year_tbl':acad_year_tbl,'cd':cyd})

def load_first_year_subjects(request):
    course_list = None
    print("hello")

    try:
        acad_year = request.GET.get('acad_year')
        sem = int(request.GET.get('first_year_sem'))
        cycle = request.GET.get('first_year_cycle')
        
        acad_cal_type = request.GET.get('acad_cal_type')
        
        print(acad_year,cycle)
        acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id= acad_year,acad_cal_sem=sem,acad_cal_type=acad_cal_type)
        print(acad_cal_id,sem)
        try:
            print("---------------")
            series = Scheme_Allotment.objects.get(acad_cal_id=acad_cal_id,course_sem=sem).scheme_series
            print(series,"sem_allottedsem_allottedsem_allottedsem_allotted")
        except Scheme_Allotment.DoesNotExist:
            messages.error(request,"Please select correct Scheme_Allotment ")
      
        course_list = Scheme_Details.objects.filter(scheme_series=series,offered_by=cycle,sem_allotted=sem)
        print("hello1")
        print(course_list)
        
        

    except Academic_Calendar.DoesNotExist:
        messages.error(request,"Please select correct Academic Year")
        return render(request,"FirstYearCourseDetails.html")
    except Exception as e:
        return render(request,"FirstYearCourseDetails.html")
    return render(request, "first_year_subjects_dropdown.html", {'course_list': course_list})
def load_first_year_subjects_for_declare_assement(request):
    course_list = None
    print("hello")

    try:
        acad_year = request.GET.get('acad_year')
        print(acad_year,"acad_yearacad_yearacad_year")
        acad_year=AcademicYear.objects.get(acayear=acad_year)
        sem = int(request.GET.get('first_year_sem'))
        cycle = request.GET.get('first_year_cycle')
        
        acad_cal_type = request.GET.get('acad_cal_type')
        
        print(acad_year,cycle)
        acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id= acad_year,acad_cal_sem=sem,acad_cal_type=acad_cal_type)
        print(acad_cal_id)
        series = Scheme_Allotment.objects.get(acad_cal_id=acad_cal_id,course_sem=sem).scheme_series
      
        course_list = Scheme_Details.objects.filter(scheme_series=series,offered_by=cycle,sem_allotted=sem)
        print("hello1")
        print(course_list)
        for i in course_list:
            print(i.course_code)
        
        

    except Academic_Calendar.DoesNotExist:
        messages.error(request,"Please select correct Academic Year")
        return render(request,"FirstYearCourseDetails.html")
    except Exception as e:
        return render(request,"FirstYearCourseDetails.html")
    return render(request, "course_code_dropdown_declare_aasement.html", {'courselist': course_list})

def addFirstYearCourses(request):
    if request.method!="POST":
        acad_year_tbl = AcademicYear.objects.all().order_by('-acayear')
        cyd = Department.objects.all()
        return render(request,"FirstYearCourseDetails.html",{'acad_year_tbl':acad_year_tbl,'cd':cyd})
    else:
        acad_year = None
        sem = None
        cycle = None
        course_code = None
        try:
            acad_year = request.POST.get("academic_year")
            sem = request.POST.get("first_year_sem")
            cycle = request.POST.get("cycle")
            course_code = request.POST.getlist("courseList")
            acad_cal_type = request.POST.get('acad_cal_type')
            print(course_code,acad_cal_type,"acad_cal_typeacad_cal_type")
            count = 0
            for sub in course_code:
                first_year_course_details_obj = First_Year_Course_Details.objects.create(first_year_sem=sem,first_year_cycle=cycle,scheme_details_id=Scheme_Details.objects.get(course_code=sub),acad_cal_id=Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year,acad_cal_sem=sem,acad_cal_type=acad_cal_type))
                first_year_course_details_obj.save()
                count = count+1
            messages.success(request,"Added "+str(count)+" courses in "+str(cycle)+"-Department for the AY-"+acad_year+"!") 
        except IntegrityError:
            messages.warning(request,"Duplicate entry not allowed!")
        except Academic_Calendar.DoesNotExist:
            messages.warning(request,"Enter correct Academic Year & Semester!")
        except Exception as e:
            messages.warning(request,e)
            print(e)
        return render(request,"FirstYearCourseDetails.html") 

def UGCourseRegistration(request):
    dept = Department.objects.all()
    scheme_details = Scheme_Details.objects.all()
    acad_year_tbl = AcademicYear.objects.all().order_by('-acayear')
    return render(request,"UGStudentCourseRegistrationsBulk.html",{'dept':dept,'scheme_details':scheme_details, 'acad_year_tbl':acad_year_tbl})

def bulkRegisterUGStudentCourses(request):
    if request.method!="POST":
        dept = Department.objects.all()
        scheme_details = Scheme_Details.objects.all()
        acad_year_tbl = AcademicYear.objects.all().order_by('-acayear')
        return render(request,"UGStudentCourseRegistrationsBulk.html",{'dept':dept,'scheme_details':scheme_details, 'acad_year_tbl':acad_year_tbl})
    else:
        acad_year = request.POST.get("academic_year")
        acad_year_id = AcademicYear.objects.get(acayear=acad_year).id
        sem = request.POST.get("academic_sem")
        branch = request.POST.get("offered_by")
        acad_cal_type = request.POST.get("acad_cal_type")
        try:
            acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year_id,acad_cal_sem=sem,acad_cal_type=acad_cal_type)
            series = Scheme_Allotment.objects.get(acad_cal_id=acad_cal_id).scheme_series
            scheme_ids = Scheme_Details.objects.filter(scheme_series=series,offered_by=branch,sem_allotted=sem)
            print(scheme_ids)
            student_uid_list = UG_Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id,offered_by=branch)
            print(student_uid_list)
            print(student_uid_list.count())
            count = 0
            totalCount = (student_uid_list.count())*(scheme_ids.count())
            for st in student_uid_list:
                uid = st.st_uid.st_uid # why st.st_uid.st_uid ?
                branch_id = Student_Details.objects.get(st_uid=uid).st_branch_applied_id
                st_branch = Department.objects.get(dept_id=branch_id)
                division=UG_Student_Division_Allotment.objects.get(acad_cal_id=acad_cal_id,offered_by=st_branch,st_uid=uid).ug_division
                for id in scheme_ids:
                    batch = 'B0'
                    '''
                    if(id.course_type=='2'):
                        batch = 'B1'
                        print("inside if batch")
                        print(batch)
                    print("outside if batch")
                    print(batch)
                    '''
                    ug_st_course_registr_obj = UG_Student_Course_Registration_Details.objects.create(semester=sem, acad_cal_id=acad_cal_id, st_uid=Student_Details.objects.get(st_uid=uid),scheme_details_id=Scheme_Details.objects.get(scheme_details_id=id.scheme_details_id),division=division,st_branch=st_branch,batch_no=batch)
                    ug_st_course_registr_obj.save()
                    count = count+1
                    print(count)
                print(count)
            if count == totalCount:
                 messages.success(request,"Bulk Registration is successful!")
            else:
                messages.error(request,"Bulk Registration failed!")
        except Exception as e:
            messages.error(request,e)
            return UGCourseRegistration(request)
        return UGCourseRegistration(request)

def load_first_year_student_course_reg_page(request):
    acad_year_tbl = AcademicYear.objects.all().order_by('-acayear')
    dv = Department.objects.all()
    print(dv)
    return render(request,"FirstYearStudentCourseRegistrationsBulk.html",{'acad_year_tbl':acad_year_tbl,'cd':dv})
#code to handle ajax request
def load_first_year_st_reg_subjects(request):
    course_list = None
    try:
        acad_year = request.GET.get('acad_year')
        sem = int(request.GET.get('first_year_sem'))
        cycle = request.GET.get('first_year_cycle')
        acad_cal_type = request.GET.get('acad_cal_type')
        
        print(cycle,"cyclecycle")
        acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year,acad_cal_sem=sem,acad_cal_type=acad_cal_type)
        course_list_values = First_Year_Course_Details.objects.filter(acad_cal_id=acad_cal_id,first_year_sem=sem,first_year_cycle=cycle).values('scheme_details_id')   
        course_list = Scheme_Details.objects.filter(scheme_details_id__in = course_list_values)
    except Academic_Calendar.DoesNotExist:
        messages.error(request,"Please select correct Academic Year")
    except Exception as e:
        print(e)
    return render(request, "student_reg_course_code_dropdown.html", {'course_list': course_list})

def bulkRegisterFirstYearStudentCourses(request):
    if request.method!="POST":
        acad_year_tbl = AcademicYear.objects.all().order_by('-acayear')
        dv = Department.objects.all()
        print(dv)
        return render(request,"FirstYearStudentCourseRegistrationsBulk.html",{'acad_year_tbl':acad_year_tbl,'cd':dv})
    else:
        try:
            acad_year = request.POST.get("academic_year")
           
            sem = request.POST.get("first_year_sem")
            cycle = request.POST.get("cycle")
            acad_cal_type = request.POST.get('acad_cal_type')
            acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year,acad_cal_sem=sem,acad_cal_type=acad_cal_type) 
              
            first_year_scheme_ids = First_Year_Course_Details.objects.filter(acad_cal_id=acad_cal_id,first_year_sem=sem,first_year_cycle=cycle)
            print(acad_cal_id,"pppp",cycle)
            division_values = Cycle_Division_allotment.objects.filter(acad_cal_id=acad_cal_id,cycle=cycle).values('div')
            print(division_values)
            student_uid_list = Student_Division_Allotment.objects.filter(acad_cal_id=acad_cal_id,division__in = division_values)
            print(student_uid_list)
            st_branch = None
            count = 0
            totalCount = student_uid_list.count()*first_year_scheme_ids.count()
            print(totalCount)
            for st in student_uid_list:
                print((st.st_uid).st_uid)
                st_branch = Student_Details.objects.get(st_uid=(st.st_uid).st_uid).st_branch_applied_id
                print(st_branch)
                for id in first_year_scheme_ids:
                    print("SUMANTH", Student_Details.objects.get(st_uid=(st.st_uid).st_uid))
                    
                    # Extract necessary objects for filters
                    student = Student_Details.objects.get(st_uid=(st.st_uid).st_uid)
                    department = Department.objects.get(dept_id=st_branch)
                    scheme_details = Scheme_Details.objects.get(scheme_details_id=id.scheme_details_id_id)
                    div=Student_Division_Allotment.objects.get(acad_cal_id=acad_cal_id,st_uid=(st.st_uid).st_uid).division
               
                    div=Division.objects.get(division=div).id
                    print("//////////////")
                    print(div)
                    # Construct the filters dictionary
                    filters = {
                        'acad_cal_id': acad_cal_id,
                        'semester': sem,
                        'first_year_cycle': div,
                        'st_uid': student,
                        'st_branch': department,
                        'scheme_details_id': scheme_details,
                    }
                    
                    # Use filter to create a queryset
                    queryset = First_Year_Student_Course_Registration_Details.objects.filter(**filters)
                    
                    # Check if the queryset exists
                    if not queryset.exists():
                        # Object does not exist, create a new one
                        first_year_st_course_registr_obj = First_Year_Student_Course_Registration_Details.objects.create(
                            acad_cal_id=acad_cal_id,
                            semester=sem,
                            first_year_cycle=div,
                            st_uid=student,
                            st_branch=department,
                            scheme_details_id=scheme_details
                        )
                        print(first_year_st_course_registr_obj)
                        first_year_st_course_registr_obj.save()
                        count = count + 1
                        print(count)
                    else:
                        print(f"Record already exists for scheme_details_id: {id.scheme_details_id_id}")
            if count == totalCount:
                print(count,totalCount)
                messages.success(request,"Bulk Registration Successful!")
                return load_first_year_student_course_reg_page(request)
            else:
                messages.error(request,"Bulk Registration Failed")
                return load_first_year_student_course_reg_page(request)
        except Exception as e:
            messages.error(request,"Bulk Registration Failed")
            print(e)

        return load_first_year_student_course_reg_page(request)

def UGProgramElective(request):
   dept = Department.objects.all()
   scheme_details = Scheme_Details.objects.all()
   acad_year_tbl = AcademicYear.objects.all().order_by('-acayear')
   div_tbl = Division.objects.all().order_by('division')[:2]
   return render(request,"ug_program_elective_bulk.html",{'dept':dept,'scheme_details':scheme_details, 'acad_year_tbl':acad_year_tbl,'div_tbl':div_tbl})

def CourseEquivalence(request):
    dept = Department.objects.all()
    scheme_details = Scheme_Details.objects.all()
    acad_year_tbl = AcademicYear.objects.all().order_by('-acayear')
    return render(request,"CourseEquivalence.html",{'dept':dept,'scheme_details':scheme_details, 'acad_year_tbl':acad_year_tbl,'ce':None})

def load_courseslist(request):
    try:
        acad_year = request.GET.get('acad_year')
        sem = request.GET.get('sem')
        acad_cal_type = request.GET.get('acad_cal_type')
        acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year,acad_cal_sem=sem,acad_cal_type=acad_cal_type)
        print("kkkkkkkkkkkkk",acad_cal_id)
    except Academic_Calendar.DoesNotExist:
        messages.error(request, "Please check Academic Year and retry")
        return render(request, "CourseEquivalence.html")
    try:
        series = Scheme_Allotment.objects.get(acad_cal_id=acad_cal_id,course_sem=sem).scheme_series
        dept_id = request.GET.get('branch')
        print(sem,series,dept_id)
        old_courselist = Scheme_Details.objects.filter(sem_allotted=sem, scheme_series=series, offered_by_id=dept_id)
        print(old_courselist,series)
        old_scheme_details_id_list = Course_Equivalence.objects.values('old_scheme_details_id')
        pending_course_list = old_courselist.exclude(scheme_details_id__in=old_scheme_details_id_list).order_by('course_code')
    except Scheme_Allotment.DoesNotExist:
        messages.error(request, "No courses offered by this dept in this sem. Enter correct data")
        return render(request, "CourseEquivalence.html")
    return render(request, "course_code_dropdown.html", {'courselist': pending_course_list})


# def load_newcourseslist(request):
#     try:
#         acad_year = request.GET.get('acad_year')
#         semester = request.GET.get('equi_sem')
#         acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id= acad_year,acad_cal_sem=semester)
#     except Academic_Calendar.DoesNotExist:
#         messages.error(request, "Please check Academic Year")
#         return render(request, "CourseEquivalence.html")
#     try:
#         series = Scheme_Allotment.objects.get(acad_cal_id=acad_cal_id,course_sem=semester).scheme_series
#         dept_id = request.GET.get('branch')
#         courselist = Scheme_Details.objects.filter(sem_allotted=semester, scheme_series=series, offered_by_id=dept_id)
#         new_scheme_details_id_list = Course_Equivalence.objects.values('new_scheme_details_id')
#         pending_course_list = courselist.exclude(scheme_details_id__in=new_scheme_details_id_list).order_by('course_code')
    
#     except Scheme_Allotment.DoesNotExist:
#         messages.error(request, "No courses offered by this dept in this sem. Enter correct data")
#         return render(request, "CourseEquivalence.html")
#     return render(request, "course_code_dropdown.html", {'courselist': pending_course_list})
def load_newcourseslist(request):
    try:
        semester = request.GET.get('equi_sem')
        dept_id = request.GET.get('branch')

        print("nnnnn")
        print(semester)
        print(dept_id)
        
       
        
        # Fetch courses based on semester and department
        if dept_id and not dept_id.isdigit():
        
            dept_obj = Department.objects.get(dept_name=dept_id)
            courselist = Scheme_Details.objects.filter(sem_allotted=semester, offered_by=dept_obj)
            
        else:
            # Skip further execution if dept_id is numeric or empty
            courselist = Scheme_Details.objects.filter(sem_allotted=semester, offered_by=dept_id)
        
       
    
    except :
        messages.error(request, "Error: Please check your input data.")
        return render(request, "CourseEquivalence.html")
    
    return render(request, "course_code_dropdown.html", {'courselist': courselist})


def addCourseEquivalent(request):
    if request.method!="POST":
        dept = Department.objects.all()
        scheme_details = Scheme_Details.objects.all()
        acad_year_tbl = AcademicYear.objects.all().order_by('-acayear')
        return render(request,"CourseEquivalence.html",{'dept':dept,'scheme_details':scheme_details, 'acad_year_tbl':acad_year_tbl,'ce':None})
    else:
        oldcoursecode = None
        newcoursecode = None
        acad_year = None
        acad_cal_id = None
        series = None
        sem = None
        old_scheme_id = None
        new_scheme_id = None
        prev_sem = None

        try:
            oldcoursecode = request.POST.get("select_sub")
            sem = request.POST.get("equi_sem")
            acad_year = request.POST.get("acad_cal_acad_year")
            acad_cal_type = request.POST.get("acad_cal_type")
        except Academic_Calendar.DoesNotExist:
            messages.error(request, "Please check Academic Year and enter")
            username = CustomUser.objects.get(id=request.user.id)
            context = {'username':username,'ce':Course_Equivalence.objects.all(),'branch':Department.objects.all()}
            return render(request,"CourseEquivalence.html",context=context)
        
        try:
            print("kkkkkkkk")
            print(acad_year)
            prev_sem = request.POST.get("sem")
            print(sem)
            print(acad_year)
            print(prev_sem)
            acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year,acad_cal_sem=sem,acad_cal_type=acad_cal_type)
            
            series = Scheme_Allotment.objects.get(course_sem=sem,acad_cal_id=acad_cal_id).scheme_series
        
        except Scheme_Allotment.DoesNotExist:
            messages.error(request, "No courses offered by this dept in this sem. Enter correct data")
            return render(request, "CourseEquivalence.html")  
        
        except Exception as e:
            print(e)

        try:
            newcoursecode = request.POST.get("equi_subject")
            new_scheme_id = Scheme_Details.objects.get(course_code=newcoursecode)
        except Exception as e:
            print(e)

        try:
            btn_value = request.POST["btn_equi_course"]
            if btn_value == "register":
                print("nn")
                print(series)
                print(oldcoursecode)
                print(newcoursecode)
                print(old_scheme_id)
                print(new_scheme_id)
                old_scheme_id = Scheme_Details.objects.get(scheme_series=series,course_code=oldcoursecode)
                course_equivalence = Course_Equivalence.objects.create(old_course_code=oldcoursecode,new_course_code=newcoursecode,old_scheme_details_id=old_scheme_id,new_scheme_details_id=new_scheme_id)
                course_equivalence.save()
                messages.success(request,"Success! Alloted Equivalent Course for "+oldcoursecode)
            if btn_value == "update":
                course_equi_id = request.POST.get('course_equivalence_id')
                print(course_equi_id,"bbbbbb")
                course_equi_obj = Course_Equivalence.objects.get(course_equivalence_id=course_equi_id)
                course_equi_obj.old_course_code = oldcoursecode
                course_equi_obj.new_course_code = newcoursecode
                print(series,oldcoursecode,"ppppppppppppppppppppp")
                course_equi_obj.old_scheme_details_id = Scheme_Details.objects.get(scheme_series=series,course_code=oldcoursecode)
                course_equi_obj.new_scheme_details_id = new_scheme_id
                course_equi_obj.save()
                messages.success(request,"Success! Updated Successfully for "+oldcoursecode)
        except IntegrityError:
            messages.warning(request,"Equivalent Course already alloted for "+oldcoursecode)   
        except Exception as e:
            print(e)
        username = CustomUser.objects.get(id=request.user.id)
        context = {'username':username,'ce':Course_Equivalence.objects.all(),'branch':Department.objects.all()}
        return render(request,"CourseEquivalence.html",context=context)    

def displaylist(request):
    try:
        print(";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;999")
        acad_year = request.GET.get('acad_year')
        sem = request.GET.get('sem')
        acad_cal_type = request.GET.get('acad_cal_type')
        acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id= acad_year,acad_cal_sem=sem,acad_cal_type=acad_cal_type)
    except Academic_Calendar.DoesNotExist:
        messages.error(request, "Please check Academic Year and retry")
        return render(request, "CourseEquivalence.html")
    try:
        series = Scheme_Allotment.objects.get(acad_cal_id=acad_cal_id,course_sem=sem).scheme_series
        dept_id = request.GET.get('branch')
        old_courselist = Scheme_Details.objects.filter(sem_allotted=sem, scheme_series=series, offered_by_id=dept_id).order_by('course_code')
        old_course_codelist = Scheme_Details.objects.filter(sem_allotted=sem, scheme_series=series, offered_by_id=dept_id).values('course_code')
        print("ppppppp")
        old_courselist_course_equi = Course_Equivalence.objects.filter(old_scheme_details_id__in=old_courselist)
        print(old_courselist_course_equi)
        course_details = []
        for course_equi in old_courselist_course_equi:
            print("ppiiiiiiiiiiiiiiiiiiiiiii")
            print(course_equi.old_scheme_details_id_id)
            old_course = Scheme_Details.objects.get(scheme_details_id=course_equi.old_scheme_details_id_id)
            new_course = Scheme_Details.objects.get(scheme_details_id=course_equi.new_scheme_details_id_id)

            course_details.append({
                'old_course_code': old_course.course_code,
                'old_course_title': old_course.course_title,
                'new_course_code': new_course.course_code,
                'new_course_title': new_course.course_title,
                'course_equivalence_id': course_equi.course_equivalence_id
            })

    except Scheme_Allotment.DoesNotExist:
        messages.error(request, "No courses offered by this dept in this sem. Enter correct data")
        return render(request, "CourseEquivalence.html")
    return render(request, "display_mapped_courses.html", {'courselist': course_details})

def edit_course_equivalence(request, course_equivalence_id):
    print(course_equivalence_id)
    userName=CustomUser.objects.get(id=request.user.id)
    course_equi_obj = Course_Equivalence.objects.get(course_equivalence_id = course_equivalence_id)
    acad_year_tbl = AcademicYear.objects.all().order_by('-acayear')
    
    # Display old and new course title which is selected to edit

    old_course_title = Scheme_Details.objects.get(course_code=course_equi_obj.old_course_code).course_title
    new_course_title = Scheme_Details.objects.get(course_code=course_equi_obj.new_course_code).course_title

    # display pending courses which has to be mapped of the selected sem(equivalent sem)
    
    equi_sem = Scheme_Details.objects.get(course_code=course_equi_obj.new_course_code).sem_allotted
    branch = Scheme_Details.objects.get(course_code=course_equi_obj.old_course_code).offered_by_id
    print(branch)
    branch_id = Department.objects.get(dept_id=branch)
    
    old_course_dept = Scheme_Details.objects.get(course_code=course_equi_obj.old_course_code).offered_by
    new_course_series = Scheme_Details.objects.get(course_code=course_equi_obj.new_course_code).scheme_series
    scheme_details_obj = Scheme_Details.objects.filter(sem_allotted=equi_sem, scheme_series=new_course_series, offered_by_id=old_course_dept)
    
    new_mapped_course_list = Course_Equivalence.objects.values('new_scheme_details_id')
    print(new_mapped_course_list,"new_mapped_course_list")
    pending_new_course_list = scheme_details_obj.exclude(scheme_details_id__in=new_mapped_course_list)
    print(course_equi_obj,"course_equi_obj")
    print(old_course_title,"old_course_title")
    print(new_course_title,"new_course_title")
    print(pending_new_course_list,"pending_new_course_list")
    
    return render(request,"CourseEquivalence.html",{'username':userName,'branch':Department.objects.all(),'acad_year_tbl':acad_year_tbl,'course_equi_obj':course_equi_obj,'old_course_title':old_course_title,'new_course_title':new_course_title,'equi_sem':equi_sem,'new_courselist':pending_new_course_list,'branch_id':branch_id})

# def ugload_student_elective_reg(request):
#     st_list = None
#     # try:
#     acadyear= request.GET.get('academic_year')
#     sem = int(request.GET.get('course_sem'))
#     dept_id = request.GET.get('offered_by')
#     div = request.GET.get('div')
#     elective_course_code = request.GET.get('elective_course_code')
#     acad_cal_type = request.GET.get('acad_cal_type')
#     print("jjj")
#     acadcal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id=acadyear,acad_cal_sem=sem,acad_cal_type=acad_cal_type)
#     print(acadcal_id,"lllllllllllll")

#     st_uid_list = UG_Student_Division_Allotment.objects.filter(acad_cal_id=acadcal_id,offered_by=dept_id,ug_division=div).values('st_uid')
#     print(st_uid_list)
#     ele_reg_st_uid_values = UG_Student_Course_Registration_Details.objects.filter(acad_cal_id=acadcal_id,scheme_details_id=Scheme_Details.objects.get(course_code=elective_course_code)).values('st_uid')
    
#     st_uid_list = st_uid_list.exclude(st_uid__in=ele_reg_st_uid_values)
#     st_uid_list = Student_Details.objects.filter(st_uid__in=st_uid_list).values('st_uid', 'st_name')
       
 
#     return render(request,"ugloadelestudents.html",{'st_list':st_uid_list})
def ugload_student_elective_reg(request):
    st_list = None
    acadyear = request.GET.get('academic_year')
    sem = int(request.GET.get('course_sem'))
    dept_id = request.GET.get('offered_by')
    div = request.GET.get('div')
    elective_course_code = request.GET.get('elective_course_code')
    acad_cal_type = request.GET.get('acad_cal_type')
    
    try:
        # Get the academic calendar ID
        acadcal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id=acadyear, acad_cal_sem=sem, acad_cal_type=acad_cal_type)
        
        # Get the list of students allotted to the division
        st_uid_list = UG_Student_Division_Allotment.objects.filter(
            acad_cal_id=acadcal_id, offered_by=dept_id, ug_division=div
        ).values_list('st_uid', flat=True)
        print(st_uid_list)
        print("..........................")

        # Get the students who have already registered for any elective course (not just the current elective_course_code)
        ele_reg_st_uid_values = UG_Student_Course_Registration_Details.objects.filter(
            acad_cal_id=acadcal_id,
            st_uid__in=st_uid_list  # Filtering for students in the division
        ).values_list('st_uid', flat=True)  # Get the list of students who have already registered for any elective course

        print("//////////////////////////")
        print(ele_reg_st_uid_values)

        # Exclude the students who have already registered for any elective course
        st_uid_list = st_uid_list.exclude(st_uid__in=ele_reg_st_uid_values)
        print("Updated student list after excluding already registered students:", st_uid_list)
        
        # Get the student details
        st_list = Student_Details.objects.filter(st_uid__in=st_uid_list).values('st_uid', 'st_name')
    
    except Academic_Calendar.DoesNotExist:
        # Handle the case where the academic calendar does not exist
        st_list = []

    return render(request, "ugloadelestudents.html", {'st_list': st_list})


def loadElectives(request):
        acad_cal_id = None
        courselist = None
        acad_year = None
        sem = None
        offered_by = None
        elective_type = None
        try:
            acad_year = request.GET.get('academic_year')
            sem = request.GET.get('course_sem')
            offered_by = request.GET.get('offered_by')
            elective_type = request.GET.get('elective_type')
            print("pppppppppppppppppppppppppppppppppppp")
            acad_cal_type = request.GET.get('acad_cal_type')
            print("Academic Year:", acad_year)
            print("Semester:", sem)
            print("Offered By:", offered_by)
            print("Elective Type:", elective_type)
            print("Academic Calendar Type:", acad_cal_type)
            acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year,acad_cal_sem=sem,acad_cal_type=acad_cal_type) 
            print(acad_cal_id)
        except Academic_Calendar.DoesNotExist: 
            messages.error(request, "Please check Academic Year and retry") 
            return UGProgramElective(request)
        try:
            print("ppp")
            series = Scheme_Allotment.objects.get(acad_cal_id=acad_cal_id,course_sem=sem).scheme_series 
            print(series)
        except Scheme_Allotment.DoesNotExist:
            messages.error(request,"Scheme series is NOT yet allotted!") 
            return UGProgramElective(request)
        if(elective_type=='5'):
            try:
                print("hhh")
                courselist = Scheme_Details.objects.filter(sem_allotted=sem, scheme_series=series, offered_by_id=offered_by,course_type=elective_type).order_by('course_code') 
                print(courselist)
            except Scheme_Details.DoesNotExist:
                messages.error(request, "No electives offered by this dept in this sem!") 
                return UGProgramElective(request)
        elif(elective_type=='6'):
            print("iiiiiiiiiiii")
            try:
                courselist = Scheme_Details.objects.filter(sem_allotted=sem, scheme_series=series, offered_by_id=offered_by,course_type=elective_type).order_by('course_code') 
                print(courselist)
            except Scheme_Details.DoesNotExist:
                messages.error(request, "No electives offered by this dept in this sem!") 
                return UGProgramElective(request)
        return render(request, "course_code_dropdown.html", {'courselist': courselist})

def bulkRegisterElectives(request):
    if request.method!="POST":
        dept = Department.objects.all()
        scheme_details = Scheme_Details.objects.all()
        acad_year_tbl = AcademicYear.objects.all().order_by('-acayear')
        div_tbl = Division.objects.all().order_by('division')[:2]
        return render(request,"ug_program_elective_bulk.html",{'dept':dept,'scheme_details':scheme_details, 'acad_year_tbl':acad_year_tbl,'div_tbl':div_tbl})
    else:
        acad_year = request.POST.get("hidden_academic_year")     
        sem = int(request.POST.get("hidden_course_sem"))
        branch = request.POST.get("hidden_offered_by")
        st_branch = Department.objects.get(dept_id=branch)
        elective_course_code = request.POST.get("courselist")
        acad_cal_type = request.POST.get('acad_cal_type')
        div = request.POST.get('div')
        acad_cal_id = Academic_Calendar.objects.get(acad_cal_acad_year_id=acad_year,acad_cal_sem=sem,acad_cal_type=acad_cal_type)

        student_uid_list = request.POST.getlist("checked_allot")
        totalCount = len(student_uid_list)
        regCount = 0
        try:
            for st_uid in student_uid_list:
                ug_elective_registr_obj = UG_Student_Course_Registration_Details.objects.create(acad_cal_id=acad_cal_id,semester=sem,st_uid=Student_Details.objects.get(st_uid=st_uid),st_branch=st_branch,scheme_details_id=Scheme_Details.objects.get(course_code=elective_course_code),division=div)
                ug_elective_registr_obj.save()
                regCount = regCount+1
            if regCount==totalCount:
                messages.success(request,"Successfully registered "+str(regCount)+" student(s) for "+elective_course_code)
        except IntegrityError:
            messages.error(request,"Student "+st_uid+" has already registered for "+elective_course_code)
            return UGProgramElective(request)
        except Exception as e:
            print(e)
            return UGProgramElective(request)
        return UGProgramElective(request)

def addFeedbackQue(request):
    if request.method!="POST":        
        return HttpResponseRedirect('AddQuestionnaire')
    else:
        count = request.POST.get("row_count")
        for i in range(1,int(count)+1):
                    feedback_que_no = request.POST.get("Question_number"+str(i))
                    feedback_que_desc = request.POST.get("description"+str(i))
                    feedback_course_type = request.POST.get("course_type"+str(i))
                    print(feedback_que_no)
                    print(feedback_que_desc)
                    print(feedback_course_type)

                    feedback_que = Feedback_Questionnaire.objects.create(feedback_que_no= feedback_que_no,feedback_que_desc = feedback_que_desc,feedback_course_type= feedback_course_type)
                    feedback_que.save()
                
    messages.success(request, "Success! Added the Questions")      
    return render(request,"Feedback_Questionnarie.html")
                           
def add_feedback_questionnaire(request):
    return render(request,"Feedback_Questionnarie.html")

# function to load the page
def UGStudentBatchAllotment(request):
    dept = Department.objects.all()
    acad_year_tbl = AcademicYear.objects.all().order_by('-acayear') # desc order
    div_tbl = Division.objects.all().order_by('division')[:2]
    # acad_year_tbl = AcademicYear.objects.all().order_by('-acayear')[:2] #to be used in production
    return render(request,"UG_Student_Lab_Batch_Allotment.html",{'dept': dept, 'acad_year_tbl':acad_year_tbl,'div_tbl':div_tbl})

# function to handle ajax request
def ug_load_students_batch_allot(request):
    try:
        print("ajax fn")
        acadyear= request.GET.get('academic_year')
        sem = int(request.GET.get('course_sem'))
        dept_id = request.GET.get('offered_by')
        div = request.GET.get('div')
        
        acad_cal_type = request.GET.get('acad_cal_type')
        print(acad_cal_type)

        acadcal_id = Academic_Calendar.objects.get(acad_cal_acad_year=acadyear,acad_cal_sem=sem,acad_cal_type=acad_cal_type)

        #div_st_list = UG_Student_Division_Allotment.objects.filter(acad_cal_id=acadcal_id,offered_by=dept_id,ug_division=div,st_uid__in=div_st_list).values('st_uid')
        
        series = Scheme_Allotment.objects.get(acad_cal_id=acadcal_id).scheme_series 
        scheme_det_ids = Scheme_Details.objects.filter(sem_allotted=sem,offered_by=dept_id,scheme_series=series,course_type=2)
        print(dept_id)
        print(sem)
        print(series)
        print(scheme_det_ids)
        #st_list = UG_Student_Course_Registration_Details.objects.filter(acad_cal_id=acadcal_id,batch=0,scheme_details_id__in=scheme_det_ids).values('st_uid')
        if sem>2:
            print(";;;;;;;;;;")
            div_st_list = UG_Student_Division_Allotment.objects.filter(acad_cal_id=acadcal_id,offered_by=dept_id,ug_division=div).values('st_uid') #st_uid__in=div_st_list removed
            print(div_st_list,scheme_det_ids)
            st_list = UG_Student_Course_Registration_Details.objects.filter(acad_cal_id=acadcal_id,batch_no='B0',scheme_details_id__in=scheme_det_ids,st_uid__in=div_st_list).values('st_uid')
            print(st_list)
            '''
            if st_list.exists():
                st_batch_allotted_uid_values = UG_Student_Course_Registration_Details.objects.filter(acad_cal_id=acadcal_id,batch_no='B1',st_branch_id=dept_id,semester=sem).values('st_uid')
                st_list = st_list.exclude(st_uid__in = st_batch_allotted_uid_values)
            else:
                return JsonResponse({"error":"No students left for batch allotment"},status=500)
            '''
        else:
            print("jjjjj")
            div_st_list = Student_Division_Allotment.objects.filter(acad_cal_id=acadcal_id,division=div).values('st_uid') #st_uid__in=div_st_list removed
            print(div_st_list)
            print(acadcal_id)
            print(scheme_det_ids)
            
            st_list = First_Year_Student_Course_Registration_Details.objects.filter(acad_cal_id=acadcal_id,batch_no='B0',scheme_details_id__in=scheme_det_ids,st_uid__in=div_st_list).values('st_uid')
            print(st_list)
        # st_list = st_list.exclude(st_uid__in = st_list)
        student_names = Student_Details.objects.filter(st_uid__in=st_list).values('st_uid', 'st_name')
        
        if not st_list.exists():
            return JsonResponse({"error":"No students left for batch allotment"},status=500)
    except Academic_Calendar.DoesNotExist:
        return JsonResponse({"error":"Please check AY and re-enter"},status=500)
    return render(request, "ugloadstudents.html",{'st_list':student_names})

#function to allot batch to the selected students
def ugAllotBatch(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        sem = None
        acad_yr = None
        acadcal_id = None
        batch = None
        st_list = None
        dept_id = None
        try:
            acad_yr = request.POST.get("academic_year")
            sem = int(request.POST.get("course_sem"))
            batch = request.POST.get("batch")
            branch = request.POST.get("offered_by")
            dept_id = Department.objects.get(dept_id=branch)
            acad_cal_type = request.POST.get("acad_cal_type")
            
            
            st_list = request.POST.getlist("checked_allot")
            acadcal_id = Academic_Calendar.objects.get(acad_cal_acad_year=acad_yr,acad_cal_sem=sem,acad_cal_type=acad_cal_type)
        except Academic_Calendar.DoesNotExist:
            messages.error(request, "Please check Academic Year and Semester")
            return UGStudentBatchAllotment(request) 
        except Exception as e:
            messages.error(request, "Batch Allotment failed. Retry!")
            return UGStudentBatchAllotment(request)  
        try:
            btn_value = request.POST["btn_clicked"]
            series = Scheme_Allotment.objects.get(acad_cal_id=acadcal_id,course_sem=sem).scheme_series
            scheme_det_ids = Scheme_Details.objects.filter(sem_allotted=sem,offered_by=branch,scheme_series=series,course_type='2')
            if btn_value == "register":   
                print("PPP")
                count = 0
                for st in st_list:
                   
                    print(".......")
                    if sem==1 or sem ==2:
                        a=First_Year_Student_Course_Registration_Details.objects.filter(acad_cal_id=acadcal_id,st_uid=Student_Details.objects.get(st_uid=st),scheme_details_id__in=scheme_det_ids).update(batch_no=batch)
                    if sem >2  :
                        print("jjjjjjjj",acadcal_id,Student_Details.objects.get(st_uid=st),scheme_det_ids,batch)
                        a=UG_Student_Course_Registration_Details.objects.filter(acad_cal_id=acadcal_id,st_uid=Student_Details.objects.get(st_uid=st),scheme_details_id__in=scheme_det_ids).update(batch_no=batch)
                   
                    count = count+1
                if count>0:
                    messages.success(request, "Allotted "+batch+"-Batch for "+str(count)+" students!")
                else:
                    messages.error(request,"Batch Allotment failed!")
                return UGStudentBatchAllotment(request)  
        except IntegrityError:
            messages.error(request, "Error! Batch already allotted for the student"+str(st))
            return UGStudentBatchAllotment(request)
        except Exception as e:
            messages.error(request,e)
            return UGStudentBatchAllotment(request)



def edit_scheme(request):
    a=request.POST.get("subject")
    print(a)
    return render(request,"edit_scheme.html",{'scheme_detail':Scheme_Details.objects.all()})

def SearchSCHEME(request):
    department = Department.objects.all()
    rel_tbl = Religion.objects.all()
    if request.POST:
        scheme = request.POST['subject']
        print(scheme)

        SearchParm = Scheme_Details.objects.filter(scheme_details_id=scheme)

        if not SearchParm.exists():
            messages.error(request,"Student Details Not Found")
        return render(request,"edit_scheme.html",{'hello':SearchParm})
    return render(request,"edit_scheme.html",{'department':department,'rel_tbl':rel_tbl})

def editSCHEME(request,scheme_details_id):
    try:
        hello=scheme_details_id
        print(hello)
        scheme = Scheme_Details.objects.get(scheme_details_id=hello)
        print("ppp")
    except Exception as e:
        print(e)
        scheme = None
    

    return render(request,"addSchemeDetails.html",{'department': Department.objects.all(),'scheme':scheme})


def edit_schemeallot(request):
    a=request.POST.get("subject")
    print(a)
    return render(request,"edit_scheme.html",{'scheme_detail':Scheme_Details.objects.all()})






def view_scheme(request):
    if request.method!="POST":
        return render(request,"Scheme&Syllabus.html",{'departments':Department.objects.all(),'academic_year_tbl': AcademicYear.objects.all().order_by('-acayear')})
    
    else :

        sem = request.POST.get("Scheme_id")
        Dep=request.POST.get("department")
        acad_year=request.POST.get("academic_year")
        acad_cal_type=request.POST.get("acad_cal_type")
        
        acadcal_id = Academic_Calendar.objects.get(acad_cal_acad_year=acad_year,acad_cal_sem=sem,acad_cal_type=acad_cal_type)
        series = Scheme_Allotment.objects.get(acad_cal_id=acadcal_id,course_sem=sem).scheme_series
        total_credits=0
        dur_lab=[]
        dur_see=[]
        course_code=[]
        course_cat=[]
        course_title=[]
        ltp=[]
        credits=[]
        ciemax_marks=[]
        seemax_marks=[]
        durationsee=[]
        total_cie=0
        practicalmaxmarks=[]
        durationpractical=[]
        total_see=0
        total_par=0
        type=[]
        type1=0
        to=0
        len1=0
        len2=0
        len3=0
        wi1=0
        scheme_detail1=Scheme_Details.objects.filter(sem_allotted=sem,offered_by=Dep,scheme_series=series)
        wi=int(len(scheme_detail1))
        print("pro",wi)
        exists = (scheme_detail1.filter(open=1)).exists()
        exists1=(scheme_detail1.filter(program=1)).exists()
        scheme_detail=Scheme_Details.objects.filter(sem_allotted=sem,offered_by=Dep,open=None,program=None)
        wi1 = int(len(scheme_detail))
        wi1=wi-wi1
        openex  = list(Scheme_Details.objects.filter(open='1',sem_allotted=sem,offered_by=Dep,scheme_series=series))
        openex2 = list(Scheme_Details.objects.filter(open='2',sem_allotted=sem,offered_by=Dep,scheme_series=series))
        prog = list(Scheme_Details.objects.filter(program='1',sem_allotted=sem,offered_by=Dep,scheme_series=series))
        prog1 = list(Scheme_Details.objects.filter(program='2',sem_allotted=sem,offered_by=Dep,scheme_series=series))
        len1=len(openex)
        len2=len(openex2)
        len3=len(prog)
        len4=len(prog1)
        print("-------------------------------------")
        print("vopenexopenexopenexopenexopenexopenex",openex)
        print("vopenexopenexopenexopenexopenexopenex",openex2)
        print("vopenexopenexopenexopenexopenexopenex",prog)
        print("vopenexopenexopenexopenexopenexopenex",prog1)
        pro1 = [[0 for _ in range(1)] for _ in range(1)]
        pro2 = [[0 for _ in range(1)] for _ in range(1)]
        pro3 = [[0 for _ in range(1)] for _ in range(1)]
        pro4 = [[0 for _ in range(1)] for _ in range(1)]

        count=0
        name=Department.objects.get(dept_id=Dep)
        pro = [[0 for _ in range(12)] for _ in range(wi)]
        for i in scheme_detail1:
            type1=i.course_type
            if(type1=="1"):
                type.append("PC")
            elif(type1=="2"):
                type.append("LA")
            elif(type1=="3"):
                type.append("PO")
            elif(type1=="6"):
                type.append("PE")
            elif(type1=="5"):
                type.append("OE")
            else:
                type.append("NA")
            course_code.append(i.course_code)
            course_title.append(i.course_title)
            ciemax_marks.append(i.max_cie_marks)
            ltp.append(i.ltps)
            print(scheme_detail,"scheme_detail")
            print(course_code,"course_code")
            if i.credits=='0':
                credits.append("-")
            else:
                credits.append(i.credits)
            if(i.course_type=='2'):
                practicalmaxmarks.append(i.max_see_marks)
                seemax_marks.append('-')
                dur_lab.append('3')
                dur_see.append('-')
            else:
                seemax_marks.append(i.max_see_marks)
                practicalmaxmarks.append('-')
            if int(i.credits)>2 and i.course_type!='2':
                dur_lab.append('-')
                dur_see.append('3')
            if int(i.credits)<=2 and i.course_type!='2':
                dur_lab.append('-')
                dur_see.append('2')
            count=count+1
        
        print("counter",count)
        
        if(len1):    
                    print('openo',openex)
                    count=0
                    pro1 = [[0 for _ in range(12)] for _ in range(len1)]
                    course_code.append((openex[0].course_code)[0:-2])
                    course_title.append('Open Elective'+" "+str(openex[0].open))
                    ciemax_marks.append(openex[0].max_cie_marks)
                    ltp.append(openex[0].ltps)
                    if openex[0].credits=='0':
                        credits.append("-")
                    else:
                        credits.append(openex[0].credits)
                    if int(openex[0].credits)>2 and openex[0].course_type!='2':
                        dur_lab.append('-')
                        dur_see.append('3')
                    if int(openex[0].credits)<=2 and openex[0].course_type!='2':
                        dur_lab.append('-')
                        dur_see.append('2')
                    seemax_marks.append(openex[0].max_see_marks)
                    practicalmaxmarks.append("-")
                    type.append("OE")
                    for i in openex:
                        type1=i.course_type
                        if(type1=="1"):
                            type1="PC"
                        elif(type1=="2"):
                            type1="LA"
                        elif(type1=="3"):
                            type1="PO"
                        elif(type1=="6"):
                            type1="PE"
                        elif(type1=="5"):
                            type1="OE"
                        else:
                            type1="NA"
                        pro1[count][0]=i.course_code
                        pro1[count][1]=type1
                        pro1[count][2]=i.course_title
                        pro1[count][3]=i.ltps
                        pro1[count][4]=i.credits
                        pro1[count][5]=i.max_see_marks
                        pro1[count][6]="-"
                        pro1[count][7]="-"
                        if int(i.credits)>2 and i.course_type!='2':
                            pro1[count][11]='3'
                        if int(i.credits)<=2 and i.course_type!='2':
                            pro1[count][11]='2'
                        pro1[count][9]=i.max_cie_marks
                        pro1[count][10]="-"     
                        count+=1
        if(len2):    
                    count=0
                    pro2 = [[0 for _ in range(12)] for _ in range(len2)]
                    course_code.append((openex2[0].course_code)[0:-2])
                    course_title.append('Open Elective'+" "+str(openex2[0].open))
                    ciemax_marks.append(openex2[0].max_cie_marks)
                    ltp.append(openex2[0].ltps)
                    if openex2[0].credits=='0':
                        credits.append("-")
                    else:
                        credits.append(openex2[0].credits)
                    if int(openex2[0].credits)>2 and openex2[0].course_type!='2':
                        dur_lab.append('-')
                        dur_see.append('3')
                    if int(openex2[0].credits)<=2 and openex2[0].course_type!='2':
                        dur_lab.append('-')
                        dur_see.append('2')
                    seemax_marks.append(openex2[0].max_see_marks)
                    practicalmaxmarks.append("-")
                    type.append("OE")
                    for i in openex2:
                        type1=i.course_type
                        if(type1=="1"):
                            type1="PC"
                        elif(type1=="2"):
                            type1="LA"
                        elif(type1=="3"):
                            type1="PO"
                        elif(type1=="6"):
                            type1="PE"
                        elif(type1=="5"):
                            type1="OE"
                        else:
                            type1="NA"
                        pro2[count][0]=i.course_code
                        pro2[count][1]=type1
                        pro2[count][2]=i.course_title
                        pro2[count][3]=i.ltps
                        pro2[count][4]=i.credits
                        pro2[count][5]=i.max_see_marks
                        pro2[count][6]="-"
                        pro2[count][7]=practicalmaxmarks[count]
                        if int(i.credits)>2 and i.course_type!='2':
                            pro2[count][11]='3'
                        if int(i.credits)<=2 and i.course_type!='2':
                            pro2[count][11]='2'
                        pro2[count][9]=i.max_cie_marks
                        pro2[count][10]="-" 
                        count+=1 
        if(len3): 
                    count=0
                    pro3 = [[0 for _ in range(12)] for _ in range(len3)]
                    course_code.append((prog[0].course_code)[0:-2])
                    course_title.append('Program Elective'+" "+str(prog[0].program))
                    ciemax_marks.append(prog[0].max_cie_marks)
                    ltp.append(prog[0].ltps)
                    if prog[0].credits=='0':
                        credits.append("-")
                    else:
                        credits.append(prog[0].credits)
                    if int(prog[0].credits)>2 and prog[0].course_type!='2':
                        dur_lab.append('-')
                        dur_see.append('3')
                    if int(prog[0].credits)<=2 and prog[0].course_type!='2':
                        dur_lab.append('-')
                        dur_see.append('2')
                    seemax_marks.append(prog[0].max_see_marks)
                    practicalmaxmarks.append("-")
                    type.append("PE")
                    for i in prog:
                        type1=i.course_type
                        if(type1=="1"):
                            type1="PC"
                        elif(type1=="2"):
                            type1="LA"
                        elif(type1=="3"):
                            type1="PO"
                        elif(type1=="6"):
                            type1="PE"
                        elif(type1=="5"):
                            type1="OE"
                        else:
                            type1="NA"
                        pro3[count][0]=i.course_code
                        pro3[count][1]=type1
                        pro3[count][2]=i.course_title
                        pro3[count][3]=i.ltps
                        pro3[count][4]=i.credits
                        pro3[count][5]=i.max_see_marks
                        pro3[count][6]="-"
                        pro3[count][7]="-"
                        if int(i.credits)>2 and i.course_type!='2':
                            pro3[count][11]='3'
                        if int(i.credits)<=2 and i.course_type!='2':
                            pro3[count][11]='2'
                        pro3[count][9]=i.max_cie_marks
                        pro3[count][10]="-"  
                        count+=1     
        if(len4):  
                    count=0
                    pro4 = [[0 for _ in range(12)] for _ in range(len2)]
                    course_code.append((openex2[0].course_code)[0:-2])
                    course_title.append('Program Elective'+" "+str(prog1[0].program))
                    ciemax_marks.append(openex2[0].max_cie_marks)
                    ltp.append(openex2[0].ltps)
                    if openex2[0].credits=='0':
                        credits.append("-")
                    else:
                        credits.append(openex2[0].credits)
                    if int(openex2[0].credits)>2 and openex2[0].course_type!='2':
                        dur_lab.append('-')
                        dur_see.append('3')
                    if int(openex2[0].credits)<=2 and openex2[0].course_type!='2':
                        dur_lab.append('-')
                        dur_see.append('2')
                    seemax_marks.append(openex2[0].max_see_marks)
                    practicalmaxmarks.append("-")
                    type.append("PE")
                    for i in prog1:
                        type1=i.course_type
                        if(type1=="1"):
                            type1="PC"
                        elif(type1=="2"):
                            type1="LA"
                        elif(type1=="3"):
                            type1="PO"
                        elif(type1=="6"):
                            type1="PE"
                        elif(type1=="5"):
                            type1="OE"
                        else:
                            type1="NA"
                        pro4[count][0]=i.course_code
                        pro4[count][1]=type1
                        pro4[count][2]=i.course_title
                        pro4[count][3]=i.ltps
                        pro4[count][4]=i.credits
                        pro4[count][5]=i.max_see_marks
                        pro4[count][6]="-"
                        pro4[count][7]="-"
                        if int(i.credits)>2 and i.course_type!='2':
                            pro4[count][11]='3'
                        if int(i.credits)<=2 and i.course_type!='2':
                            pro4[count][11]='2'
                        pro4[count][9]=i.max_cie_marks
                        pro4[count][10]="-" 
                        count+=1   
        for start in range(0,wi):
                
                    pro[start][0]=course_code[start]
                    pro[start][1]=type[start]
                    pro[start][2]=course_title[start]
                    pro[start][3]=ltp[start]
                    pro[start][4]=credits[start]
                    pro[start][5]=seemax_marks[start]
                    pro[start][6]="-"
                    pro[start][7]=practicalmaxmarks[start]
                    pro[start][8]="-"
                    pro[start][9]=ciemax_marks[start]
                    pro[start][10]=dur_lab[start]
                    pro[start][11]=dur_see[start]   
        for num in credits:
            total_credits += int(num)
        for num in ciemax_marks:
            total_cie += int(num)
        for num in seemax_marks:
            if(num=='-'):
                continue
            else:
                total_see += int(num)
        for num in practicalmaxmarks:
            if(num=='-'):
                continue
            else:
                total_par += int(num)
    #return render(request,"SchemeTemp.html",{'scheme_detail':scheme_detail,'sem':sem,'course_code':course_code,'course_title':course_title,'ltp':ltp,'credits':credits,'practicalmaxmarks':practicalmaxmarks,'seemax_marks':seemax_marks})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'inline; attachment; filename='+"Exam Results"+".pdf"
    response['Content-Transfer-Encoding'] = 'binary'

    userName=CustomUser.objects.get(id=request.user.id)
    html_string = render_to_string('SchemeTemp.html',{'len1':len1,'len3':len3,'len2':len2,'len4':len4,'pro2':pro2,'pro3':pro3,'pro4':pro4,'pro1':pro1,'pro':pro,'total_credits':total_credits,'total_cie':total_cie,'scheme_detail':scheme_detail,'sem':sem,'course_code':course_code,'total_see':total_see,'total_par':total_par,'credits':credits,'practicalmaxmarks':practicalmaxmarks,'seemax_marks':seemax_marks,'name':name,'cie':ciemax_marks})
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    result = html.write_pdf()
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()

        output=open(output.name, 'rb')
        response.write(output.read())
    return response
# def Report_ia_Marks(request):
#     course_list = Scheme_Details.objects.all()
#     departments = Department.objects.all()
#     academic_year_tbl = AcademicYear.objects.all().order_by('-acayear')

#     if request.method == 'POST':
#         acad_cal_acad_year = request.POST.get('acad_cal_acad_year')
#         department = request.POST.get('department')
#         acad_cal_sem = request.POST.get('acad_cal_sem')
#         print(acad_cal_acad_year)
#         print(department)
#         print(acad_cal_sem)
#         acadcal_id = Academic_Calendar.objects.get(acad_cal_acad_year=acad_cal_acad_year,acad_cal_sem=acad_cal_sem)
#         print(acadcal_id)
        
        
#         # Fetch matching rows from Academics_Master_Details
#         matching_rows = Academics_Master_Details.objects.filter(
#             acad_cal_id=acadcal_id,
#             st_branch_applied=department,
#             semester=acad_cal_sem
#         )
#         print(len(matching_rows),"hi")
#         for row in matching_rows:
#             print(row.st_uid.st_uid)
            
         
           
#             scheme_detail = Scheme_Details.objects.get(scheme_details_id=row.scheme_details_id.scheme_details_id)
#             row.scheme_name = scheme_detail.course_title  
#             student_details = Student_Details.objects.get(st_uid=row.st_uid.st_uid).st_name
#             row.stname = student_details
            
            
       

#         return render(request, 'IAmarksreport.html', {
#             'matching_rows': matching_rows,
            
#         })

#     # If it's a GET request or no matching rows found, render the initial form
#     context = {
#         'departments': departments,
#         'academic_year_tbl': academic_year_tbl,
#         'acad_cal_obj': None,
#         'course_obj':course_list
#     }
#     return render(request, 'IAmarksreport.html', context)



from django.shortcuts import render
from .models import Department, AcademicYear, Scheme_Details, Academic_Calendar, student_attendance, Student_Details, Division, Academics_Master_Details

# def Report_ia_Marks(request):
#     departments = Department.objects.all()
#     academic_year_tbl = AcademicYear.objects.all().order_by('-acayear')
#     course_list = Scheme_Details.objects.all()
#     div_tbl = Division.objects.all().order_by('division')

#     if request.method == 'POST':
#         acad_cal_acad_year = request.POST.get('acad_cal_acad_year')
#         department = request.POST.get('department')
#         acad_cal_sem = request.POST.get('acad_cal_sem')
#         course_name = request.POST.get('course_name')
#         div = request.POST.get('div')
        
#         if btn_clicked == "report":
#             try:
#                 course_title, course_code = course_name.split(" - ")
#                 course_obj = Scheme_Details.objects.get(course_title=course_title, course_code=course_code)
#                 acad_cal_obj = Academic_Calendar.objects.get(acad_cal_acad_year=acad_cal_acad_year, acad_cal_sem=acad_cal_sem)
                
#                 matching_rows = Academics_Master_Details.objects.filter(
#                     acad_cal_id=acad_cal_obj,
#                     st_branch_applied_id=department,
#                     semester=int(acad_cal_sem),
#                     scheme_details_id=course_obj,
#                     division=div
#                 )
                
#                 for row in matching_rows:
#                     student_details = Student_Details.objects.get(st_uid=row.st_uid.st_uid)
#                     row.stname = student_details.st_name

#                 return render(request, 'IAmarksreport.html', {
#                     'matching_rows': matching_rows,
#                     'departments': departments,
#                     'academic_year_tbl': academic_year_tbl,
#                     'acad_cal_obj': {
#                         'acad_cal_acad_year': acad_cal_acad_year,
#                         'acad_cal_sem': acad_cal_sem
#                     },
#                     'course_list': course_list
#                 })
            
#             except Scheme_Details.DoesNotExist:
#                 error_message = "Selected course details not found."
            
#             except Academic_Calendar.DoesNotExist:
#                 error_message = "Selected academic calendar details not found."
            
#             except Exception as e:
#                 error_message = str(e)

#             return render(request, 'IAmarksreport.html', {
#                 'error_message': error_message,
#                 'departments': departments,
#                 'academic_year_tbl': academic_year_tbl,
#                 'acad_cal_obj': {
#                     'acad_cal_acad_year': acad_cal_acad_year,
#                     'acad_cal_sem': acad_cal_sem
#                 },
#                 'course_list': course_list
#             })
        
#         elif btn_clicked == "Mark":
#             try:
#                 course_title, course_code = course_name.split(" - ")
#                 course_obj = Scheme_Details.objects.get(course_title=course_title, course_code=course_code)
#                 acad_cal_obj = Academic_Calendar.objects.get(acad_cal_acad_year=acad_cal_acad_year, acad_cal_sem=acad_cal_sem)
                
#                 cie_less_than_20 = Academics_Master_Details.objects.filter(
#                     acad_cal_id=acad_cal_obj,
#                     st_branch_applied_id=department,
#                     semester=int(acad_cal_sem),
#                     scheme_details_id=course_obj,
#                     cie_marks__lt=20
#                 )
                
#                 for row in cie_less_than_20:
#                     student_details = Student_Details.objects.get(st_uid=row.st_uid.st_uid)
#                     row.stname = student_details.st_name

#                 return render(request, 'IAmarksreport.html', {
#                     'cie_less_than_20': cie_less_than_20,
#                     'departments': departments,
#                     'academic_year_tbl': academic_year_tbl,
#                     'acad_cal_obj': {
#                         'acad_cal_acad_year': acad_cal_acad_year,
#                         'acad_cal_sem': acad_cal_sem
#                     },
#                     'course_list': course_list
#                 })
            
#             except Scheme_Details.DoesNotExist:
#                 error_message = "Selected course details not found."
            
#             except Academic_Calendar.DoesNotExist:
#                 error_message = "Selected academic calendar details not found."
            
#             except Exception as e:
#                 error_message = str(e)

#             return render(request, 'IAmarksreport.html', {
#                 'error_message': error_message,
#                 'departments': departments,
#                 'academic_year_tbl': academic_year_tbl,
#                 'acad_cal_obj': {
#                     'acad_cal_acad_year': acad_cal_acad_year,
#                     'acad_cal_sem': acad_cal_sem
#                 },
#                 'course_list': course_list
#             })
        
#         elif btn_clicked == "Attendance":
#             try:
#                 course_title, course_code = course_name.split(" - ")
#                 course_obj = Scheme_Details.objects.get(course_title=course_title, course_code=course_code)
#                 acad_cal_obj = Academic_Calendar.objects.get(acad_cal_acad_year=acad_cal_acad_year, acad_cal_sem=acad_cal_sem)
                
#                 low_attendance_students = student_attendance.objects.filter(
#                     acad_cal_id=acad_cal_obj,
#                     scheme_details_id_id=course_obj,
#                     division=div,
#                     Percentage_of_attendance__lt=80.0
#                 ).select_related('st_uid')
                
#                 for row in low_attendance_students:
#                     student_details = Student_Details.objects.get(st_uid=row.st_uid.st_uid)
#                     row.stname = student_details.st_name
#                     row.st_branch_applied = student_details.st_branch_applied  # Ensure st_branch_applied is accessible
                
#                 return render(request, 'IAmarksreport.html', {
#                     'low_attendance_students': low_attendance_students,
#                     'departments': departments,
#                     'academic_year_tbl': academic_year_tbl,
#                     'acad_cal_obj': {
#                         'acad_cal_acad_year': acad_cal_acad_year,
#                         'acad_cal_sem': acad_cal_sem
#                     },
#                     'course_list': course_list
#                 })
            
#             except Scheme_Details.DoesNotExist:
#                 error_message = "Selected course details not found."
            
#             except Academic_Calendar.DoesNotExist:
#                 error_message = "Selected academic calendar details not found."
            
#             except Exception as e:
#                 error_message = str(e)

#             return render(request, 'IAmarksreport.html', {
#                 'error_message': error_message,
#                 'departments': departments,
#                 'academic_year_tbl': academic_year_tbl,
#                 'acad_cal_obj': {
#                     'acad_cal_acad_year': acad_cal_acad_year,
#                     'acad_cal_sem': acad_cal_sem
#                 },
#                 'course_list': course_list
#             })

#     # If it's a GET request or no button is clicked, render the initial form
#     context = {
#         'departments': departments,
#         'academic_year_tbl': academic_year_tbl,
#         'acad_cal_obj': None,
#         'course_list': course_list,
#         'div_tbl': div_tbl
#     }
#     return render(request, 'IAmarksreport.html', context)

from django.contrib import messages

def Report_ia_Marks(request):
    departments = Department.objects.all()
    academic_year_tbl = AcademicYear.objects.all().order_by('-acayear')
    course_list = Scheme_Details.objects.all()
    div_tbl = Division.objects.all().order_by('division')

    if request.method == 'POST':
        acad_cal_acad_year = request.POST.get('acad_cal_acad_year')
        department = request.POST.get('department')
        acad_cal_sem = request.POST.get('acad_cal_sem')
        course_name = request.POST.get('courselist')
        div = request.POST.get('div')
        btn_clicked = request.POST.get('btn_clicked')
        acad_cal_type = request.POST.get('acad_cal_type')
        attendance_slab = request.POST.get('attendance_slab')
        print(course_name,"------------------------")

        try:
           
            
            course_obj = Scheme_Details.objects.get(course_code=course_name)
            print(course_obj)
            acad_cal_obj = Academic_Calendar.objects.get(acad_cal_acad_year=acad_cal_acad_year, acad_cal_sem=acad_cal_sem,acad_cal_type=acad_cal_type)
        except Scheme_Details.DoesNotExist:
            messages.error(request, "Selected course details not found.")
            return render(request, 'IAmarksreport.html', {
                'departments': departments,
                'academic_year_tbl': academic_year_tbl,
                'acad_cal_obj': {
                    'acad_cal_acad_year': acad_cal_acad_year,
                    'acad_cal_sem': acad_cal_sem
                },
                'course_list': course_list,
                'div_tbl': div_tbl
            })
        except Academic_Calendar.DoesNotExist:
            messages.error(request, "Selected academic calendar details not found.")
            return render(request, 'IAmarksreport.html', {
                'departments': departments,
                'academic_year_tbl': academic_year_tbl,
                'acad_cal_obj': {
                    'acad_cal_acad_year': acad_cal_acad_year,
                    'acad_cal_sem': acad_cal_sem
                },
                'course_list': course_list,
                'div_tbl': div_tbl
            })
        except Exception as e:
            messages.error(request, str(e))
            return render(request, 'IAmarksreport.html', {
                'departments': departments,
                'academic_year_tbl': academic_year_tbl,
                'acad_cal_obj': {
                    'acad_cal_acad_year': acad_cal_acad_year,
                    'acad_cal_sem': acad_cal_sem
                },
                'course_list': course_list,
                'div_tbl': div_tbl
            })

        if btn_clicked == "report":
            print("ppppppppppppppppppp")
            try:
                print(acad_cal_obj,department,acad_cal_sem,course_obj,div)
                matching_rows = Academics_Master_Details.objects.filter(
                    acad_cal_id=acad_cal_obj,
                    st_branch_applied_id=department,
                    semester=int(acad_cal_sem),
                    scheme_details_id=course_obj,
                    division=div
                )
                for row in matching_rows:
                    student_details = Student_Details.objects.get(st_uid=row.st_uid.st_uid)
                    row.stname = student_details.st_name
                return render(request, 'IAmarksreport.html', {
                    'matching_rows': matching_rows,
                    'departments': departments,
                    'academic_year_tbl': academic_year_tbl,
                    'acad_cal_obj': {
                        'acad_cal_acad_year': acad_cal_acad_year,
                        'acad_cal_sem': acad_cal_sem
                    },
                    'course_list': course_list,
                    'div_tbl': div_tbl
                })
            except Student_Details.DoesNotExist:
                messages.error(request, "Student details not found.")
            except Exception as e:
                messages.error(request, str(e))
            return render(request, 'IAmarksreport.html', {
                'departments': departments,
                'academic_year_tbl': academic_year_tbl,
                'acad_cal_obj': {
                    'acad_cal_acad_year': AcademicYear.objects.all(),
                    'acad_cal_sem': Semester.objects.all()
                },
                'course_list': course_list,
                'div_tbl': div_tbl
            })

        elif btn_clicked == "Mark":
            try:
                cie_less_than_20 = Academics_Master_Details.objects.filter(
                    acad_cal_id=acad_cal_obj,
                    st_branch_applied_id=department,
                    semester=int(acad_cal_sem),
                    scheme_details_id=course_obj,
                    division=div,
                    cie_marks__lt=20
                )
                for row in cie_less_than_20:
                    student_details = Student_Details.objects.get(st_uid=row.st_uid.st_uid)
                    row.stname = student_details.st_name
                return render(request, 'IAmarksreport.html', {
                    'cie_less_than_20': cie_less_than_20,
                    'departments': departments,
                    'academic_year_tbl': academic_year_tbl,
                    'acad_cal_obj': {
                        'acad_cal_acad_year': acad_cal_acad_year,
                        'acad_cal_sem': acad_cal_sem
                    },
                    'course_list': course_list,
                    'div_tbl': div_tbl
                })
            except Student_Details.DoesNotExist:
                messages.error(request, "Student details not found.")
            except Exception as e:
                messages.error(request, str(e))
            return render(request, 'IAmarksreport.html', {
                'departments': departments,
                'academic_year_tbl': academic_year_tbl,
                'acad_cal_obj': {
                    'acad_cal_acad_year': acad_cal_acad_year,
                    'acad_cal_sem': acad_cal_sem
                },
                'course_list': course_list,
                'div_tbl': div_tbl
            })

        elif btn_clicked == "Attendance":
            try:
                if attendance_slab == "0-60%":
                    low_attendance_students = student_attendance.objects.filter(
                        acad_cal_id=acad_cal_obj,
                        scheme_details_id_id=course_obj,
                        division=div,
                        Percentage_of_attendance__lt=60.0
                    ).select_related('st_uid')
                elif attendance_slab == "60-75%":
                    low_attendance_students = student_attendance.objects.filter(
                        acad_cal_id=acad_cal_obj,
                        scheme_details_id_id=course_obj,
                        division=div,
                        Percentage_of_attendance__gte=60.0,
                        Percentage_of_attendance__lt=75.0
                    ).select_related('st_uid')
                elif attendance_slab == "75-100%":
                    low_attendance_students = student_attendance.objects.filter(
                        acad_cal_id=acad_cal_obj,
                        scheme_details_id_id=course_obj,
                        division=div,
                        Percentage_of_attendance__gte=75.0,
                        Percentage_of_attendance__lte=100.0
                    ).select_related('st_uid')
                for row in low_attendance_students:
                    student_details = Student_Details.objects.get(st_uid=row.st_uid.st_uid)
                    row.stname = student_details.st_name
                    row.st_branch_applied = student_details.st_branch_applied  # Ensure st_branch_applied is accessible
                return render(request, 'IAmarksreport.html', {
                    'low_attendance_students': low_attendance_students,
                    'departments': departments,
                    'academic_year_tbl': academic_year_tbl,
                    'acad_cal_obj': {
                        'acad_cal_acad_year': acad_cal_acad_year,
                        'acad_cal_sem': acad_cal_sem
                    },
                    'course_list': course_list,
                    'div_tbl': div_tbl,
                    'attendance_slab': attendance_slab
                })
            except Student_Details.DoesNotExist:
                messages.error(request, "Student details not found.")
            except Exception as e:
                messages.error(request, str(e))
            return render(request, 'IAmarksreport.html', {
                'departments': departments,
                'academic_year_tbl': academic_year_tbl,
                'acad_cal_obj': {
                    'acad_cal_acad_year': acad_cal_acad_year,
                    'acad_cal_sem': acad_cal_sem
                },
                'course_list': course_list,
                'div_tbl': div_tbl
            })

    # If it's a GET request or no button is clicked, render the initial form
    context = {
        'departments': departments,
        'academic_year_tbl': academic_year_tbl,
        'acad_cal_obj': None,
        'course_list': course_list,
        'div_tbl': div_tbl
    }
    return render(request, 'IAmarksreport.html', context)


def attendance_report(request):
    # For GET requests, fetch academic years and scheme details
    if request.method != 'POST':
        academic_year_tbl = AcademicYear.objects.all().order_by('-acayear')
        scheme_details = Scheme_Details.objects.all()

        context = {
            'academic_year_tbl': academic_year_tbl,
            'scheme_details': scheme_details,  # Include scheme_details in the context
        }
        
        return render(request, 'attendance_report.html', context)
    else:
        print("kk")
        acad_cal_id = request.POST.get('acad_cal_acad_year')  # Correct field name
        scheme_details_id = request.POST.get('scheme_details_id')
        attendance_date = request.POST.get('attendance_date')

        # Query to get the attendance records
        attendance_data = StudentAttendance.objects.filter(
            acad_cal_id=acad_cal_id,
            scheme_details_id=scheme_details_id,
            st_uid__in=StudentAttendanceDate.objects.filter(
                attendance_date=attendance_date
            ).values_list('faculty_id', flat=True)
        )

        # Get all scheme details to repopulate the dropdown
        scheme_details = Scheme_Details.objects.all()

        context = {
            'attendance_data': attendance_data,
            'academic_year_tbl': AcademicYear.objects.all().order_by('-acayear'),  # academic_year_tbl context
            'scheme_details': scheme_details,  # Include scheme_details in the context
            'acad_cal_id': acad_cal_id,
            'scheme_details_id': scheme_details_id,
            'attendance_date': attendance_date,
        }
        return render(request, 'attendance_report.html', context)
def course_registration_page(request):
    acad_year_tbl = AcademicYear.objects.all()
    departments = Department.objects.all()
    semesters = Semester.objects.all()
    division = Division.objects.all()
   
 
    return render(request, 'course_registration.html', {
        'acad_year_tbl': acad_year_tbl,
        'departments': departments,
        'semesters': semesters,
        'division':division,
        
    })


def fetch_failed_students(request):
    # Before POST: Render the form page
    if request.method != 'POST':
        acad_year_tbl = AcademicYear.objects.all()
        departments = Department.objects.all()
        semesters = Semester.objects.all()
        division = Division.objects.all()

        return render(request, 'failed_students.html', {
            'acad_year_tbl': acad_year_tbl,
            'departments': departments,
            'semesters': semesters,
            'division': division,
        })

    # After POST: Process the data and return the failed students
    else:
        academic_year = request.POST.get('academic_year')
        department_id = request.POST.get('department')
        semester_id = request.POST.get('semester')
        division_id = request.POST.get('division')
        

        # Fetching the failed students based on the given criteria
        failed_students = Academics_Master_Details.objects.filter(
            acad_cal_id__acad_cal_acad_year_id=academic_year,
            st_branch_applied_id=department_id,
            semester_id=semester_id,
            division_id=division_id,
            cie_grade='F'  # Assuming 'F' represents a failed grade
        )

        # Returning the failed students as a JSON response
        return JsonResponse({
            'failed_students': list(failed_students.values('st_uid__st_name', 'cie_grade'))
        })


def load_courses(request):
    academic_year_id = request.GET.get('acad_year')
    semester = request.GET.get('sem')
    department_id = request.GET.get('offered_by')
    acad_cal_type = request.GET.get('acad_cal_type')
    
    print("pppppppppppppppppp")
    print(academic_year_id,semester,department_id,acad_cal_type)
    acad_cal_id=Academic_Calendar.objects.get(acad_cal_sem=semester,acad_cal_type=acad_cal_type,acad_cal_acad_year_id=academic_year_id).acad_cal_id
    print("ll")
    print(acad_cal_id)
    series = Scheme_Allotment.objects.get(acad_cal_id=acad_cal_id,course_sem=semester).scheme_series
    print(acad_cal_id,series)
    courselist = Scheme_Details.objects.filter(sem_allotted=semester, scheme_series=series, offered_by=department_id).order_by('course_code')
    print(courselist)
   
    # course_list_html = render_to_string('course_list.html', {'courses': courselist})
    course_list_html = render_to_string('course_code_dropdown.html', {'courselist': courselist})
    print(course_list_html)
 
    return JsonResponse({'html': course_list_html})

def displaycourses(request):
    semester = request.GET.get('sem_allotted')
    department_id = request.GET.get('offered_by')
    
    if not semester or not department_id:
        return JsonResponse({'error': 'Missing parameters'}, status=400)
    
    # Filter courses based on semester and department
    courselist = Scheme_Details.objects.filter(
        sem_allotted=semester,
        offered_by=department_id
    ).order_by('course_code')
    
    # Prepare course list data for JSON response
    course_data = list(courselist.values('course_code', 'course_title'))  # Adjust fields as needed
    
    # Return JSON response with the course data
    return JsonResponse({'data': course_data})




def load_courses_select(request):
    academic_year_id = request.GET.get('acad_year')
    semester = request.GET.get('sem')
    department_id = request.GET.get('offered_by')
    acad_cal_type = request.GET.get('acad_cal_type')
    
    print("pppppppppppppppppp")
    print(academic_year_id,semester,department_id,acad_cal_type)
    acad_cal_id=Academic_Calendar.objects.get(acad_cal_sem=semester,acad_cal_type=acad_cal_type,acad_cal_acad_year_id=academic_year_id).acad_cal_id
    print("ll")
    print(acad_cal_id)
    series = Scheme_Allotment.objects.get(acad_cal_id=acad_cal_id,course_sem=semester).scheme_series
    print(acad_cal_id,series)
    courselist = Scheme_Details.objects.filter(sem_allotted=semester, scheme_series=series, offered_by=department_id).order_by('course_code')
    print(courselist)
   
    course_list_html = render_to_string('course_list.html', {'courses': courselist})
    # course_list_html = render_to_string('course_code_dropdown.html', {'courselist': courselist})
    print(course_list_html)
 
    return JsonResponse({'html': course_list_html})
def load_courses_co_po(request):
    academic_year_id = request.GET.get('acad_year')
    semester = request.GET.get('sem')
    department_id = request.GET.get('offered_by')
    acad_cal_type = request.GET.get('acad_cal_type')
    
    print("pppppppppppppppppp")
    print(academic_year_id,semester,department_id,acad_cal_type)
    acad_cal_id=Academic_Calendar.objects.get(acad_cal_sem=semester,acad_cal_type=acad_cal_type,acad_cal_acad_year_id=academic_year_id).acad_cal_id
    print("ll")
    print(acad_cal_id)
    series = Scheme_Allotment.objects.get(acad_cal_id=acad_cal_id,course_sem=semester).scheme_series
    print(acad_cal_id,series)
    courselist = Scheme_Details.objects.filter(sem_allotted=semester, scheme_series=series, offered_by=department_id).order_by('course_code')
    print(courselist)
   
    course_list_html = render_to_string('course_list_co_po.html', {'courses': courselist})
 
    return JsonResponse({'html': course_list_html})
# def register_course(request):
#     if request.method == 'POST':
#         student_id = request.POST.get('student_id')
#         academic_year = request.POST.get('acad_year')
#         department_id = request.POST.get('offered_by')
#         semester = request.POST.get('sem')
#         division_id = request.POST.get('division')
#         course_ids = request.POST.getlist('course_ids')
#         faculty = request.POST.get('faculty')
#         acad_cal_type = request.POST.get('acad_cal_type')
#         batch = request.POST.get('batch', 'B0')  # Default batch to 'B0' if not provided

#         try:
#             # Fetch the Academic Calendar
#             acad_cal_id = Academic_Calendar.objects.get(
#                 acad_cal_sem=semester, acad_cal_acad_year_id=academic_year, acad_cal_type=acad_cal_type
#             )

#             # Fetch the Student Details
#             student = Student_Details.objects.get(st_uid=student_id)

#             # Fetch the Department
#             department = Department.objects.get(dept_id=department_id).dept_id

#             # Fetch the Division
#             division = Division.objects.get(id=division_id).id

#             # Handle division allotment for the 1st and 2nd semesters
#             if semester in [1, 2]:
#                 try:
#                     division_allotment = Student_Division_Allotment.objects.get(
#                         st_uid=student, acad_cal_id=acad_cal_id
#                     )
#                 except Student_Division_Allotment.DoesNotExist:
#                     division_allotment = Student_Division_Allotment.objects.create(
#                         st_uid=student, acad_cal_id=acad_cal_id, division=division, dept=department
#                     )
#                     division_allotment.save()

#                 # Register courses
#                 for course_id in course_ids:
#                     try:
#                         course_id = int(course_id)
#                         scheme_details = Scheme_Details.objects.get(scheme_details_id=course_id)
#                         print(f"acad_cal_id: {acad_cal_id}")
#                         print(f"semester: {semester}")
#                         print(f"division: {division}")  # This will print the Division instance
#                         print(f"student: {student}")
#                         print(f"department: {department}")
#                         print(f"scheme_details: {scheme_details}")
#                         print(f"registration_status: R")
#                         print(f"batch_no: {batch}")

#                         # Create course registration
#                         First_Year_Student_Course_Registration_Details.objects.create(
#                             acad_cal_id=acad_cal_id,
#                             semester=semester,
#                             first_year_cycle=division.id,
#                             st_uid=student,
#                             st_branch=department,
#                             scheme_details_id=scheme_details,
#                             registration_status='R',  # Registered
#                             batch_no=batch
#                         )

#                         # Create student attendance
#                         student_attendance.objects.create(
#                             acad_cal_id=acad_cal_id,
#                             scheme_details_id=scheme_details,
#                             division=division.id,
#                             faculty_id=Employee_Details.objects.get(employee_emp_id=faculty),
#                             st_uid=student,
#                             status="P",  # Present (example)
#                             batch_no=batch
#                         )

#                     except Scheme_Details.DoesNotExist:
#                         messages.error(request, f"Course {course_id} does not exist.")
#                     except Exception as e:
#                         messages.error(request, f"Error registering course {course_id}: {e}")
#                         return redirect('course_registration_page')

#                 messages.success(request, "Courses successfully registered.")
#                 return redirect('course_registration_page')

#             # Handle division allotment for 3rd to 8th semesters
#             else:
#                 try:
#                     division_allotment = UG_Student_Division_Allotment.objects.get(
#                         st_uid=student, acad_cal_id=acad_cal_id
#                     )
#                 except UG_Student_Division_Allotment.DoesNotExist:
#                     division_allotment = UG_Student_Division_Allotment.objects.create(
#                         st_uid=student, acad_cal_id=acad_cal_id, ug_division=division, offered_by=department
#                     )
#                     division_allotment.save()

#                 # Register courses
#                 for course_id in course_ids:
#                     try:
#                         course_id = int(course_id)
#                         scheme_details = Scheme_Details.objects.get(scheme_details_id=course_id)
#                         print(f"acad_cal_id: {acad_cal_id}")
#                         print(f"semester: {semester}")
#                         print(f"division: {division}")  # This will print the Division instance
#                         print(f"student: {student}")
#                         print(f"department: {department}")
#                         print(f"scheme_details: {scheme_details}")
#                         print(f"registration_status: R")
#                         print(f"batch_no: {batch}")

#                         # Create course registration
#                         UG_Student_Course_Registration_Details.objects.create(
#                             acad_cal_id=acad_cal_id,
#                             semester=semester,
#                             division=division,  # Corrected to pass the Division instance
#                             st_uid=student,
#                             st_branch=department,
#                             scheme_details_id=scheme_details,
#                             registration_status='R',  # Registered
#                             batch_no=batch
#                         )

#                         # Create student attendance
#                         student_attendance.objects.create(
#                             acad_cal_id=acad_cal_id,
#                             scheme_details_id=scheme_details,
#                             division=division.id,
#                             faculty_id=Employee_Details.objects.get(employee_emp_id=faculty),
#                             st_uid=student,
#                             status="P",  # Present (example)
#                             batch_no=batch
#                         )

#                         # Create faculty course allotment
#                         faculty_course_allotment_obj = Faculty_Course_Allotment.objects.create(
#                             session_count=0,
#                             batch_no=batch,
#                             employee_emp_id=Employee_Details.objects.get(employee_emp_id=faculty),
#                             acad_year_id=academic_year,
#                             sem=semester,
#                             division=division,
#                             course_code=scheme_details.course_code
#                         )

#                     except Scheme_Details.DoesNotExist:
#                         messages.error(request, f"Course {course_id} does not exist.")
#                     except Exception as e:
#                         messages.error(request, f"Error registering course {course_id}: {e}")
#                         return redirect('course_registration_page')

#                 messages.success(request, "Courses successfully registered.")
#                 return redirect('course_registration_page')

#         except Academic_Calendar.DoesNotExist:
#             messages.error(request, "Academic calendar not found.")
#         except Student_Details.DoesNotExist:
#             messages.error(request, "Student not found.")
#         except Department.DoesNotExist:
#             messages.error(request, "Department not found.")
#         except Division.DoesNotExist:
#             messages.error(request, "Division not found.")
#         except Exception as e:
#             messages.error(request, f"An error occurred: {e}")

#         return redirect('course_registration_page')

#     return HttpResponse("Invalid request method.", status=405)



def register_course(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        academic_year = request.POST.get('acad_year')
        department_id = request.POST.get('offered_by')
        semester = request.POST.get('sem')
        division_id = request.POST.get('division')
        course_ids = request.POST.getlist('course_ids')
        faculty = request.POST.get('faculty')
        acad_cal_type = request.POST.get('acad_cal_type')
        print("semestersemester",type(semester))
        
        batch = request.POST.get('batch')
        if batch:
            batch=batch
        else:

            batch="B0"
        
        if semester == '1' or semester == '2' :
            print(";;;;;;;;;;;;;;;;;;;;;;")
            try:
                # Fetch the Academic Calendar
                print(semester,academic_year,acad_cal_type,batch)
                acad_cal_id = Academic_Calendar.objects.get(acad_cal_sem=semester, acad_cal_acad_year_id=academic_year,acad_cal_type=acad_cal_type)
                print(acad_cal_id,"acad_cal_idacad_cal_idacad_cal_idacad_cal_idacad_cal_idacad_cal_id")

                # Fetch the Student Details
                student = Student_Details.objects.get(st_uid=student_id)

                # Fetch the Department
                department = Department.objects.get(dept_id=department_id)

                # Fetch the Division
                division = Division.objects.get(id=division_id)

                # Ensure the student has a division allocated
                print(student,department,division)
               
                try:
                    division_allotment = Student_Division_Allotment.objects.get(
                        st_uid=Student_Details.objects.get(st_uid=student_id),
                        acad_cal_id=acad_cal_id
                    )
                    print("Division allocation already exists",division_allotment,student,acad_cal_id)
                except Student_Division_Allotment.DoesNotExist:
                    division_allotment = Student_Division_Allotment.objects.create(
                        st_uid= Student_Details.objects.get(st_uid=student_id),
                        acad_cal_id=acad_cal_id,
                        division=Division.objects.get(id=division_id),
                        dept=Department.objects.get(dept_id=department_id)
                    )
                    division_allotment.save()
                    


                # Process each course registration
                for course_id in course_ids:
                    try:
                        # Convert course_id to integer
                        course_id = int(course_id)

                        # Fetch the Scheme Details
                        scheme_details = Scheme_Details.objects.get(scheme_details_id=course_id)

                        # Create a registration entry
                        print(f"acad_cal_id: {acad_cal_id}")
                        print(f"semester: {semester}")
                        print(f"division: {Division.objects.get(id=division_id)}")  # Print the Division object
                        print(f"student: {Student_Details.objects.get(st_uid=student_id)}")  # Print the Student object
                        print(f"department: {Department.objects.get(dept_id=department_id)}")  # Print the Department object
                        print(f"scheme_details: {Scheme_Details.objects.get(scheme_details_id=course_id)}")
                        print(f"batch_no: {batch}")
                        try:
                            First_Year_Student_Course_Registration_Details.objects.create(
                                acad_cal_id=acad_cal_id,
                                semester=semester,
                                first_year_cycle=Division.objects.get(id=division_id).id,
                                st_uid=Student_Details.objects.get(st_uid=student_id),
                                st_branch=Department.objects.get(dept_id=department_id),
                                scheme_details_id=Scheme_Details.objects.get(scheme_details_id=course_id),
                                registration_status='R',
                                batch_no=batch
                            )
                            print("Object created successfully!")
                        except Exception as e:
                            print(f"Error: {e}")

                        try:
                            employee = Employee_Details.objects.get(employee_emp_id=faculty)
                            division = Division.objects.get(id=division_id)
                            course_details = Scheme_Details.objects.get(scheme_details_id=course_id)  # Get the full Scheme_Details object
                            academic_year = AcademicYear.objects.get(id=academic_year)

                            print(f"Employee: {employee}")
                            print(f"Division: {division}")
                            print(f"Course Details: {course_details}")
                            print(batch, semester, academic_year)

                            # Pass the entire course_details object, not just course_code
                            faculty_course_allotment_obj = Faculty_Course_Allotment.objects.create(
                                session_count=0,
                                batch_no=batch,
                                employee_emp_id=employee,
                                acad_year=academic_year,
                                sem=semester,
                                division=division,
                                course_code=course_details,  # Pass the entire Scheme_Details object,
                                acad_cal_type=acad_cal_type
                            )
                            print("Faculty_Course_Allotment object created successfully.")
                        except Exception as e:
                            print(f"Error creating Faculty_Course_Allotment object: {e}")


                        try:
                            student_attendance.objects.create(
                                acad_cal_id=acad_cal_id,  # Acad Calendar object
                                scheme_details_id=Scheme_Details.objects.get(scheme_details_id=course_id),  # Pass the Scheme_Details object
                                division=Division.objects.get(id=division_id).id,  # Pass the Division object
                                faculty_id=Employee_Details.objects.get(employee_emp_id=faculty),  # Pass the Employee_Details object
                                st_uid=Student_Details.objects.get(st_uid=student_id),  # Pass the Student object
                                status="P",  # Status value is fine
                                batch_no='B0'  # Batch number is fine
                            )
                            messages.success(request, "Courses successfully registered.")

                        except Exception as e:
                            print(f"Error creating Faculty_Course_Allotment object: {e}")
                        
                    except Scheme_Details.DoesNotExist:
                        messages.error(request, f"Course {course_id} does not exist.")
                    except Exception as e:
                        messages.error(request, f"Error registering course {course_id}: {e}")
                        return redirect('course_registration_page')

                
                return redirect('course_registration_page')  # Redirect to the registration page

            except Academic_Calendar.DoesNotExist:
                messages.error(request, "Academic calendar not found.")
            except Student_Details.DoesNotExist:
                messages.error(request, "Student not found.")
            except Department.DoesNotExist:
                messages.error(request, "Department not found.")
            except Division.DoesNotExist:
                messages.error(request, "Division not found.")
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")

            return redirect('course_registration_page')  # Redirect to the registration page if any error occurs
        else:
            try:
                print("//////////////////")
                # Fetch the Academic Calendar
                print(semester,academic_year,acad_cal_type,batch)
                acad_cal_id = Academic_Calendar.objects.get(acad_cal_sem=semester, acad_cal_acad_year_id=academic_year,acad_cal_type=acad_cal_type)
                print(acad_cal_id,"acad_cal_idacad_cal_idacad_cal_idacad_cal_idacad_cal_idacad_cal_id")

                # Fetch the Student Details
                student = Student_Details.objects.get(st_uid=student_id)

                # Fetch the Department
                department = Department.objects.get(dept_id=department_id)

                # Fetch the Division
                division = Division.objects.get(id=division_id)

                # Ensure the student has a division allocated
                print(Student_Details.objects.get(st_uid=student_id), acad_cal_id, Division.objects.get(id=division_id), department)
                try:
                    division_allotment = UG_Student_Division_Allotment.objects.get(
                        st_uid=Student_Details.objects.get(st_uid=student_id),
                        acad_cal_id=acad_cal_id
                    )
                    print("Division allocation already exists",division_allotment,student,acad_cal_id)
                except UG_Student_Division_Allotment.DoesNotExist:
                    division_allotment = UG_Student_Division_Allotment.objects.create(
                        st_uid= Student_Details.objects.get(st_uid=student_id),
                        acad_cal_id=acad_cal_id,
                        ug_division=Division.objects.get(id=division_id),
                        offered_by=Department.objects.get(dept_id=department_id)
                    )
                    division_allotment.save()
                
                # Process each course registration
                for course_id in course_ids:
                    
                        # Convert course_id to integer
                        course_id = int(course_id)

                        # Fetch the Scheme Details
                        scheme_details = Scheme_Details.objects.get(scheme_details_id=course_id)
                        print(f"acad_cal_id: {acad_cal_id}")
                        print(f"semester: {semester}")
                        print(f"division: {Division.objects.get(id=division_id)}")  # Print the Division object
                        print(f"student: {Student_Details.objects.get(st_uid=student_id)}")  # Print the Student object
                        print(f"department: {Department.objects.get(dept_id=department_id)}")  # Print the Department object
                        print(f"scheme_details: {Scheme_Details.objects.get(scheme_details_id=course_id)}")
                        print(f"batch_no: {batch}")

                     
                        UG_Student_Course_Registration_Details.objects.create(
                            acad_cal_id=acad_cal_id,  # The actual Academic Calendar object
                            semester=semester,  # Semester number
                            division=Division.objects.get(id=division_id),  # Pass the Division object, not its id
                            st_uid=Student_Details.objects.get(st_uid=student_id),  # The Student object
                            st_branch=Department.objects.get(dept_id=department_id),  # Pass the Department object, not its id
                            scheme_details_id=Scheme_Details.objects.get(scheme_details_id=course_id),  # The Scheme Details object
                            registration_status='R',  # Registration status
                            batch_no=batch  # Batch number
                        )

                        try:
                            employee = Employee_Details.objects.get(employee_emp_id=faculty)
                            division = Division.objects.get(id=division_id)
                            course_details = Scheme_Details.objects.get(scheme_details_id=course_id)  # Get the full Scheme_Details object
                            academic_year = AcademicYear.objects.get(id=academic_year)

                            print(f"Employee: {employee}")
                            print(f"Division: {division}")
                            print(f"Course Details: {course_details}")
                            print(batch, semester, academic_year)

                            # Pass the entire course_details object, not just course_code
                            faculty_course_allotment_obj = Faculty_Course_Allotment.objects.create(
                                session_count=0,
                                batch_no=batch,
                                employee_emp_id=employee,
                                acad_year=academic_year,
                                sem=semester,
                                division=division,
                                course_code=course_details,  # Pass the entire Scheme_Details object
                                acad_cal_type=acad_cal_type
                            )
                            print("Faculty_Course_Allotment object created successfully.")
                        except Exception as e:
                            print(f"Error creating Faculty_Course_Allotment object: {e}")



                        student_attendance.objects.create(
                            acad_cal_id=acad_cal_id,  # Acad Calendar object
                            scheme_details_id=Scheme_Details.objects.get(scheme_details_id=course_id),  # Pass the Scheme_Details object
                            division=Division.objects.get(id=division_id).id,  # Pass the Division object
                            faculty_id=Employee_Details.objects.get(employee_emp_id=faculty),  # Pass the Employee_Details object
                            st_uid=Student_Details.objects.get(st_uid=student_id),  # Pass the Student object
                            status="P",  # Status value is fine
                            batch_no='B0'  # Batch number is fine
                        )


                        print(f"Created registration for course {course_id}")

                    

                messages.success(request, "Courses successfully registered.")
                return redirect('course_registration_page')  # Redirect to the registration page

            except Academic_Calendar.DoesNotExist:
                messages.error(request, "Academic calendar not found.")
            except Student_Details.DoesNotExist:
                messages.error(request, "Student not found.")
            except Department.DoesNotExist:
                messages.error(request, "Department not found.")
            except Division.DoesNotExist:
                messages.error(request, "Division not found.")
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")

            return redirect('course_registration_page')  # Redirect to the registration page if any error occurs

    return HttpResponse("Invalid request method.", status=405)
# def register_course(request):
#     if request.method == 'POST':
#         student_id = request.POST.get('student_id')
#         academic_year = request.POST.get('acad_year')
#         department_id = request.POST.get('offered_by')
#         semester = request.POST.get('sem')
#         division_id = request.POST.get('division')
#         course_ids = request.POST.getlist('course_ids')
#         faculty = request.POST.get('faculty')
#         acad_cal_type = request.POST.get('acad_cal_type')
        
#         batch = request.POST.get('batch')
#         if batch:
#             batch=batch
#         else:

#             batch="B0"

#         try:
#             # Fetch the Academic Calendar
#             print(semester,academic_year,acad_cal_type,batch)
#             acad_cal_id = Academic_Calendar.objects.get(acad_cal_sem=semester, acad_cal_acad_year_id=academic_year,acad_cal_type=acad_cal_type)
#             print(acad_cal_id,"acad_cal_idacad_cal_idacad_cal_idacad_cal_idacad_cal_idacad_cal_id")

#             # Fetch the Student Details
#             student = Student_Details.objects.get(st_uid=student_id)

#             # Fetch the Department
#             department = Department.objects.get(dept_id=department_id)

#             # Fetch the Division
#             division = Division.objects.get(id=division_id)

#             # Ensure the student has a division allocated
#             print(Student_Details.objects.get(st_uid=student_id), acad_cal_id, Division.objects.get(id=division_id), department)
#             if semester == 1 or semester ==2 :
#                 try:
#                     division_allotment = Student_Division_Allotment.objects.get(
#                         st_uid=Student_Details.objects.get(st_uid=student_id),
#                         acad_cal_id=acad_cal_id
#                     )
#                     print("Division allocation already exists",division_allotment,student,acad_cal_id)
#                 except Student_Division_Allotment.DoesNotExist:
#                     division_allotment = Student_Division_Allotment.objects.create(
#                         st_uid= Student_Details.objects.get(st_uid=student_id),
#                         acad_cal_id=acad_cal_id,
#                         division=Division.objects.get(id=division_id),
#                         dept=Department.objects.get(dept_id=department_id)
#                     )
#                     division_allotment.save()
#                     print("Created new division allocation")

#                 # Process each course registration
#                 for course_id in course_ids:
#                     try:
#                         # Convert course_id to integer
#                         course_id = int(course_id)

#                         # Fetch the Scheme Details
#                         scheme_details = Scheme_Details.objects.get(scheme_details_id=course_id)

#                         # Create a registration entry
#                         First_Year_Student_Course_Registration_Details.objects.create(
#                             acad_cal_id=acad_cal_id,
#                             semester=semester,
#                             first_year_cycle=Division.objects.get(id=division_id).id,
#                             st_uid=Student_Details.objects.get(st_uid=student_id),
#                             st_branch=Department.objects.get(dept_id=department_id),
#                             scheme_details_id=scheme_details,
#                             registration_status='R',  # Assuming 'R' means registered
#                             batch_no=batch  # Default batch number
#                         )
#                         print(faculty,"facultyfacultyfaculty")
#                         student_attendance.objects.create(
#                             acad_cal_id=acad_cal_id,
#                             scheme_details_id=scheme_details,
#                             division=Division.objects.get(id=division_id).id,
#                             faculty_id=Employee_Details.objects.get(employee_emp_id=faculty),
#                             st_uid=Student_Details.objects.get(st_uid=student_id),
#                             status="P",  # Example status value
#                             batch_no='B0'  # Default batch number
#                         )

#                         print(f"Created registration for course {course_id}")

#                     except Scheme_Details.DoesNotExist:
#                         messages.error(request, f"Course {course_id} does not exist.")
#                     except Exception as e:
#                         messages.error(request, f"Error registering course {course_id}: {e}")
#                         return redirect('course_registration_page')

#                 messages.success(request, "Courses successfully registered.")
#                 return redirect('course_registration_page')  # Redirect to the registration page
#             else :
#                 try:
#                     division_allotment = UG_Student_Division_Allotment.objects.get(
#                         st_uid=Student_Details.objects.get(st_uid=student_id),
#                         acad_cal_id=acad_cal_id
#                     )
#                     print("Division allocation already exists",division_allotment,student,acad_cal_id)
#                 except UG_Student_Division_Allotment.DoesNotExist:
#                     division_allotment = UG_Student_Division_Allotment.objects.create(
#                         st_uid= Student_Details.objects.get(st_uid=student_id),
#                         acad_cal_id=acad_cal_id,
#                         ug_division=Division.objects.get(id=division_id),
#                         offered_by=Department.objects.get(dept_id=department_id)
#                     )
#                     division_allotment.save()
#                     print("Created new division allocation")

#                 # Process each course registration
#                 for course_id in course_ids:
#                     try:
#                         # Convert course_id to integer
#                         course_id = int(course_id)

#                         # Fetch the Scheme Details
#                         scheme_details = Scheme_Details.objects.get(scheme_details_id=course_id)

#                         # Create a registration entry
#                         print(".....................")
#                         print(acad_cal_id," ",semester,Division.objects.get(id=division_id).id," ",Student_Details.objects.get(st_uid=student_id)," ",Department.objects.get(dept_id=department_id)," ",scheme_details," ",batch)
#                         UG_Student_Course_Registration_Details.objects.create(
#                             acad_cal_id=acad_cal_id,
#                             semester=semester,
#                             division=Division.objects.get(id=division_id).id,
#                             st_uid=Student_Details.objects.get(st_uid=student_id),
#                             st_branch=Department.objects.get(dept_id=department_id),
#                             scheme_details_id=Scheme_Details.objects.get(scheme_details_id=course_id),
#                             registration_status='R',  # Assuming 'R' means registered
#                             batch_no=batch  # Default batch number
#                         )
#                         print(faculty,"facultyfacultyfaculty")
#                         student_attendance.objects.create(
#                             acad_cal_id=acad_cal_id,
#                             scheme_details_id=Scheme_Details.objects.get(scheme_details_id=course_id),
#                             division=Division.objects.get(id=division_id).id,
#                             faculty_id=Employee_Details.objects.get(employee_emp_id=faculty),
#                             st_uid=Student_Details.objects.get(st_uid=student_id),
#                             status="P",  # Example status value
#                             batch_no='B0'  # Default batch number
#                         )

#                         print(f"Created registration for course {course_id}")

#                     except Scheme_Details.DoesNotExist:
#                         messages.error(request, f"Course {course_id} does not exist.")
#                     except Exception as e:
#                         messages.error(request, f"Error registering course {course_id}: {e}")
#                         return redirect('course_registration_page')
#                 messages.success(request, "Courses successfully registered.")
#                 return redirect('course_registration_page')  # Redirect to the registration page
        
#         except Academic_Calendar.DoesNotExist:
#             messages.error(request, "Academic calendar not found.")
#         except Student_Details.DoesNotExist:
#             messages.error(request, "Student not found.")
#         except Department.DoesNotExist:
#             messages.error(request, "Department not found.")
#         except Division.DoesNotExist:
#             messages.error(request, "Division not found.")
#         except Exception as e:
#             messages.error(request, f"An error occurred: {e}")

#         return redirect('course_registration_page')  # Redirect to the registration page if any error occurs

#     return HttpResponse("Invalid request method.", status=405)
def ajax_load_faculty(request):
    
    department_id = request.GET.get('offered_by')
    print("kkk",department_id)
    

        # Fetch the faculty members based on department and division
    dept_faculty_list = Employee_Details.objects.filter(employee_dept_id_id=department_id).order_by('employee_emp_id')
    print(dept_faculty_list)
    course_list_html = render_to_string('faculty_dropdown_options.html', {'dept_faculty_list': dept_faculty_list})
    print(course_list_html)
    return JsonResponse({'html': course_list_html})
# def map_co_po(request):
#     if request.method == 'POST':
#         # Retrieve form data
#         academic_year_id = request.POST.get('acad_year')
#         semester = request.POST.get('first_year_sem')
#         acad_cal_type = request.POST.get('acad_cal_type')
#         scheme_details_ids = request.POST.getlist('course_ids')
#         btn_clicked = request.POST.get('btn_clicked')
#         print(btn_clicked)

#         # Debug: Print the retrieved scheme details IDs
#         print(scheme_details_ids)

#         # Retrieve academic calendar instance
#         try:
#             acad_cal = Academic_Calendar.objects.get(
#                 acad_cal_sem=semester,
#                 acad_cal_acad_year_id=academic_year_id,
#                 acad_cal_type=acad_cal_type
#             ).acad_cal_id
#             print(acad_cal)
#         except Academic_Calendar.DoesNotExist:
#             messages.error(request, "Academic Calendar not found.")
#             return redirect('some_error_url')  # Redirect to an error page

#         if btn_clicked == "register":
#             # Loop through each course ID and CO to save the mappings
#             for scheme_details_id in scheme_details_ids:
#                 try:
#                     scheme_detail = Scheme_Details.objects.get(scheme_details_id=scheme_details_id).scheme_details_id
#                 except Scheme_Details.DoesNotExist:
#                     messages.error(request, "Scheme Details not found.")
#                     continue  # Skip this course and move on to the next

#                 num_co = int(request.POST.get('num_co', 0))  # Number of COs from the form

#                 for co_id in range(1, num_co + 1):
#                     co_description = request.POST.get(f'co{co_id}_desc')
#                     print(f'CO {co_id} Description:', co_description)

#                     # Handle PO Mappings for each CO
#                     for po_id in range(1, 13):  # Assuming 12 POs
#                         for level, level_label in CourseOutcomePO.LEVEL_CHOICES:
#                             if request.POST.get(f'co{co_id}_po{po_id}_{level.lower()}'):
#                                 # Store the level as a number (3, 2, 1)
#                                 mapping_level = level

#                                 # Check if the mapping already exists
#                                 if CourseOutcomePO.objects.filter(
#                                     acad_cal_id_id=acad_cal,
#                                     scheme_details_id_id=scheme_detail,
#                                     co_id=co_id,
#                                     po_id=po_id,
#                                     mapping_level=mapping_level
#                                 ).exists():
#                                     messages.error(request, f"Mapping for CO {co_id}, PO {po_id}, Level {level} already exists.")
#                                     continue  # Skip this mapping

#                                 # Create a new mapping if it doesn't exist
#                                 try:
#                                     print("Creating mapping...")
#                                     CourseOutcomePO.objects.create(
#                                         acad_cal_id_id=acad_cal,
#                                         scheme_details_id_id=scheme_detail,
#                                         co_id=co_id,
#                                         po_id=po_id,
#                                         mapping_level=mapping_level,
#                                         co_description=co_description
#                                     )
#                                     messages.success(request, "COs and POs have been successfully mapped.")
#                                 except CourseOutcome.DoesNotExist:
#                                     messages.error(request, f"Course Outcome {co_id} not found.")
#                                     continue
#                                 except ProgramOutcome.DoesNotExist:
#                                     messages.error(request, f"Program Outcome {po_id} not found.")
#                                     continue
        
#         elif btn_clicked == "generate_report":
#             # Logic to generate the report based on CO-PO mappings
#             report_data = []
#             for scheme_details_id in scheme_details_ids:
#                 try:
#                     mappings = CourseOutcomePO.objects.filter(
#                         acad_cal_id_id=acad_cal,
#                         scheme_details_id_id=scheme_details_id
#                     )
#                     for mapping in mappings:
#                         report_data.append({
#                             'co_id': mapping.co_id,
#                             'co_description': mapping.co_description,
#                             'po_id': mapping.po_id,
#                             'mapping_level': mapping.mapping_level,
#                         })
#                 except CourseOutcomePO.DoesNotExist:
#                     messages.error(request, "No mappings found for the selected courses.")
#                     continue

#             # Pass the report data to the template
#             return render(request, 'report_template.html', {
#                 'report_data': report_data,
#                 'acad_year': academic_year_id,
#                 'semester': semester,
#                 'acad_cal_type': acad_cal_type,
#                 'departments': Department.objects.all(),
#             })

#     # Handle GET request
#     return render(request, 'map_co_po_combined.html', {
#         'form_submitted': False,
#         'po_range': range(1, 13),
#         'acad_year_tbl': AcademicYear.objects.all(),
#         'departments': Department.objects.all(),
#         'semesters': Semester.objects.all()
#     })
from collections import defaultdict  # Ensure this import is present
def map_co_po(request):
    if request.method == 'POST':
        # Retrieve form data
        academic_year_id = request.POST.get('acad_year')
        semester = request.POST.get('first_year_sem')
        acad_cal_type = request.POST.get('acad_cal_type')
        scheme_details_ids = request.POST.getlist('course_ids')
        btn_clicked = request.POST.get('btn_clicked')
        print(btn_clicked)

        # Debug: Print the retrieved scheme details IDs
        print(scheme_details_ids)

        # Retrieve academic calendar instance
        try:
            acad_cal = Academic_Calendar.objects.get(
                acad_cal_sem=semester,
                acad_cal_acad_year_id=academic_year_id,
                acad_cal_type=acad_cal_type
            ).acad_cal_id
            print(acad_cal)
        except Academic_Calendar.DoesNotExist:
            messages.error(request, "Academic Calendar not found.")
            return redirect('some_error_url')  # Redirect to an error page

        if btn_clicked == "register":
            # Loop through each course ID and CO to save the mappings
            for scheme_details_id in scheme_details_ids:
                try:
                    scheme_detail = Scheme_Details.objects.get(scheme_details_id=scheme_details_id).scheme_details_id
                except Scheme_Details.DoesNotExist:
                    messages.error(request, "Scheme Details not found.")
                    continue  # Skip this course and move on to the next

                num_co = int(request.POST.get('num_co', 0))  # Number of COs from the form

                for co_id in range(1, num_co + 1):
                    co_description = request.POST.get(f'co{co_id}_desc')
                    print(f'CO {co_id} Description:', co_description)

                    # Handle PO Mappings for each CO
                    for po_id in range(1, 13):  # Assuming 12 POs
                        for level, level_label in CourseOutcomePO.LEVEL_CHOICES:
                            if request.POST.get(f'co{co_id}_po{po_id}_{level.lower()}'):
                                # Check if the mapping already exists
                                if CourseOutcomePO.objects.filter(
                                    acad_cal_id_id=acad_cal,
                                    scheme_details_id_id=scheme_detail,
                                    co_id=co_id,
                                    po_id=po_id,
                                    mapping_level=level
                                ).exists():
                                    messages.error(request, f"Mapping for CO {co_id}, PO {po_id}, Level {level} already exists.")
                                    continue  # Skip this mapping

                                # Create a new mapping if it doesn't exist
                                try:
                                    CourseOutcomePO.objects.create(
                                        acad_cal_id_id=acad_cal,
                                        scheme_details_id_id=scheme_detail,
                                        co_id=co_id,
                                        po_id=po_id,
                                        mapping_level=level,
                                        co_description=co_description
                                    )
                                    messages.success(request, "COs and POs have been successfully mapped.")
                                except CourseOutcome.DoesNotExist:
                                    messages.error(request, f"Course Outcome {co_id} not found.")
                                    continue
                                except ProgramOutcome.DoesNotExist:
                                    messages.error(request, f"Program Outcome {po_id} not found.")
                                    continue
        
        elif btn_clicked == "generate_report":
            # Logic to generate the report based on CO-PO mappings
            report_data = CourseOutcomePO.objects.filter(
                acad_cal_id_id=acad_cal,
                scheme_details_id_id__in=scheme_details_ids
            ).values('co_id', 'co_description', 'po_id', 'mapping_level')

            # Prepare the grouped data
            grouped_data = defaultdict(list)
            for entry in report_data:
                grouped_data[entry['co_id']].append(entry)

            # Pass the grouped data to the template
            return render(request, 'report_template.html', {
                'grouped_data': dict(grouped_data),
                'acad_year': academic_year_id,
                'semester': semester,
                'acad_cal_type': acad_cal_type,
                'departments': Department.objects.all(),
            })

    # Handle GET request
    return render(request, 'map_co_po_combined.html', {
        'form_submitted': False,
        'po_range': range(1, 13),
        'acad_year_tbl': AcademicYear.objects.all(),
        'departments': Department.objects.all(),
        'semesters': Semester.objects.all()
    })