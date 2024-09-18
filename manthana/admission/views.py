from datetime import date
from doctest import master
from gettext import translation
from itertools import count
from queue import Empty
from sre_parse import State
from tkinter import E

from academics.models import Academic_Calendar, Student_Promotion_List
from admission.models import *
import secrets 
from PIL import Image
import base64
import io
import requests
import json
from django.db import IntegrityError, transaction
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
from weasyprint import HTML
from django.db.models import Sum
from .EmailBackEnd import EmailBackEnd
from django.db.models import Q
from .forms import CaptchaForm
from master_mgmt.models import *

import xlwt
import csv

def error_500(request):
    return render(request, "error_500.html")
    
# Create your views here.
def loginPage(request):
    form = CaptchaForm()
    return render(request,"login.html",{"form": form})

def serverDown(request):
    return render(request,"server_down.html")

def index(request):
    return render(request,"index.html")

def admin_home(request):
    return render(request,"admin_home.html")

def staff_home(request):
    return render(request,"staff_home.html")

def student_home(request):
    return render(request,"student_home.html")

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] =  'attachment; filename='+"student"+str(datetime.datetime.now())+".csv"
    
    writer = csv.writer(response)
    writer.writerow(['Student ID', 'Mobile Number', 'Email ID'])
    student = Student_Details.objects.all()

    for st in student:
        writer.writerow([st.st_id, st.st_mobile_no, st.st_email_id])
    
    return response

def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] =  'attachment; filename='+"student"+str(datetime.datetime.now())+".xls"
    wb = xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Student Views')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Student ID', 'Mobile Number', 'Email ID']
    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()
    rows = Student_Details.objects.all().values_list('st_id','st_mobile_no','st_email_id')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]),font_style)

    wb.save(response)
    return response

def pdf_students(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'inline; attachment; filename='+"student"+str(datetime.datetime.now())+".pdf"
    response['Content-Transfer-Encoding'] = 'binary'

    student = Student_Details.objects.all()
    sum = student.aggregate(Count('st_id'))
    html_string = render_to_string('pdf_detail.html',{'student':student,'sum':sum['st_id__count']})
    html = HTML(string=html_string, base_url=request.build_absolute_uri())

    result = html.write_pdf()
    
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()

        output=open(output.name, 'rb')
        response.write(output.read())

    return response

def id_card_students(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'inline; attachment; filename='+"st_id_card"+str(datetime.datetime.now())+".pdf"
    response['Content-Transfer-Encoding'] = 'binary'

    student = Student_Details.objects.all()
    sum = student.aggregate(Count('st_id'))
    html_string = render_to_string('gen_id_card.html',{'student':student,'sum':sum['st_id__count']})
    html = HTML(string=html_string, base_url=request.build_absolute_uri())

    result = html.write_pdf()
    
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()

        output=open(output.name, 'rb')
        response.write(output.read())

    return response

def ackPdf_ug(request,st_id):
    student = None
    pacad_10th  = None
    pacad_12th = None
    cet_admission_ug = None
    comedk_admission_ug = None
    mgmt_admission_ug = None
    doc_details = None
    academic_year = None
    bld_grp_tbl = None
    state_tbl = None
    rel_tbl = None
    quota_tbl = None
    months_tbl = None
    category_tbl = None
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] =  'inline; attachment; filename='+"student_Acknowledgement"+str(datetime.datetime.now())+".pdf"
    response['Content-Disposition'] =  'inline; attachment; filename=%s' % ('student_Acknowledgement.pdf')
    response['Content-Transfer-Encoding'] = 'binary'

    try:
        student = Student_Details.objects.get(st_id = st_id)
    except Exception as e:
        print(e)
        student = None

    try:
        pacad_10th = Previous_10th_Academic_Details.objects.get(sslc_uid = student.st_id)
    except Exception as e:
        print(e)
        pacad_10th = None

    try:
        pacad_12th = Previous_12th_Academic_Details.objects.get(puc_uid = student.st_id)
    except Exception as e:
        print(e)
        pacad_12th = None
    
    try:
        cet_admission_ug = CET_Admission_Details_UG.objects.get(cet_uid = student.st_id)
    except Exception as e:
        print(e)
        cet_admission_ug = None

    try:
        comedk_admission_ug = COMEDK_Admission_Details_UG.objects.get(comedk_uid = student.st_id)
    except Exception as e:
        print(e)
        comedk_admission_ug = None

    try:
        mgmt_admission_ug = MGMT_Admission_Details_UG.objects.get(mgmt_uid = student.st_id)
    except Exception as e:
        print(e)
        mgmt_admission_ug = None

    try:
        doc_details = Document_Details.objects.get(doc_uid = student.st_id)
    except Exception as e:
        print(e)
        doc_details = None

    try:
        bld_grp_tbl = BloodGroup.objects.all().order_by('name')
    except Exception as e:
        print(e)
        bld_grp_tbl = None

    try:
        state_tbl = States.objects.all()
    except Exception as e:
        print(e)
        state_tbl = None    
        
    try:
        rel_tbl = Religion.objects.all()
    except Exception as e:
        print(e)
        rel_tbl = None

    try:
        quota_tbl = Admission_Quota.objects.all().order_by('name')
    except Exception as e:
        print(e)
        quota_tbl = None

    try:
        months_tbl = Months.objects.all()
    except Exception as e:
        print(e)
        months_tbl = None

    try:
        category_tbl = Category.objects.all().order_by('name')
    except Exception as e:
        print(e)
        category_tbl = None

    st_img = student.st_profile_pic
    print("inside st ack pdf gen")
    print(student.st_profile_pic)

    html_string = render_to_string('ack_pdf_ug.html', { 'student':student, 'pacad_10th':pacad_10th, 
    'pacad_12th':pacad_12th, 'cet_admission_ug':cet_admission_ug, 'comedk_admission_ug':comedk_admission_ug, 
    'mgmt_admission_ug':mgmt_admission_ug,'doc_details':doc_details, 'id': st_id, 
    'rel_tbl':rel_tbl,'bld_grp_tbl':bld_grp_tbl, 'state_tbl':state_tbl,
    'months_tbl':months_tbl,'quota_tbl':quota_tbl,'category_tbl':category_tbl, 'st_img' : st_img })

    html = HTML(string=html_string, base_url=request.build_absolute_uri())

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()

        output=open(output.name, 'rb')
        response.write(output.read())

    return response


def ackPdf_lat(request,st_id):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'inline; attachment; filename='+"st_id_card"+str(datetime.datetime.now())+".pdf"
    response['Content-Transfer-Encoding'] = 'binary'

    student = Student_Details.objects.get(st_id = st_id)
    pacad_10th = Previous_10th_Academic_Details.objects.get(sslc_uid = student.st_id)
    pacad_12th = Previous_12th_Academic_Details.objects.get(puc_uid = student.st_id)
    pacad_dip = Previous_dip_Academic_Details.objects.get(dip_uid = student.st_id)
    lateral_admission_ug = Lateralentry_Admission_Details_UG.objects.get(dip_uid = student.st_id)
    mgmt_admission_ug = MGMT_Admission_Details_UG.objects.get(mgmt_uid = student.st_id)
    doc_details = Document_Details.objects.get(doc_uid = student.st_id)
    
    bld_grp_tbl = None
    rel_tbl = None
    quota_tbl = None
    category_tbl = None

    try:
        bld_grp_tbl = BloodGroup.objects.all().order_by('name')
    except Exception as e:
        print(e)
        bld_grp_tbl = None

    try:
        rel_tbl = Religion.objects.all()
    except Exception as e:
        print(e)
        rel_tbl = None
    
    try:
        quota_tbl = Admission_Quota.objects.all().order_by('name')
    except Exception as e:
        print(e)
        quota_tbl = None


    try:
        category_tbl = Category.objects.all().order_by('name')
    except Exception as e:
        print(e)
        category_tbl = None

    html_string = render_to_string('ack_pdf_lat.html',{'bld_grp_tbl':bld_grp_tbl,'rel_tbl':rel_tbl,'quota_tbl':quota_tbl,'category_tbl':category_tbl,'student':student,'student':student, 'pacad_10th':pacad_10th, 'pacad_12th':pacad_12th, 'pacad_dip':pacad_dip, 'lateral_admission_ug':lateral_admission_ug, 'mgmt_admission_ug':mgmt_admission_ug,'doc_details':doc_details, 'id': st_id, 'a_id':pacad_dip.dip_uid, 'lateral_id':lateral_admission_ug.dip_uid, 'mgmt_id':mgmt_admission_ug.mgmt_uid,'doc_id':doc_details.doc_uid})
    html = HTML(string=html_string, base_url=request.build_absolute_uri())

    result = html.write_pdf()
    
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()

        output=open(output.name, 'rb')
        response.write(output.read())

    return response

def ackPdf_pg(request,st_id):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'inline; attachment; filename='+"st_id_card"+str(datetime.datetime.now())+".pdf"
    response['Content-Transfer-Encoding'] = 'binary'

    student = Student_Details.objects.get(st_id = st_id)
    pacad_pg = Previous_Academic_Details_PG.objects.get(pg_uid = student.st_id)
    pgcet_admission_pg = PGCET_Admission_Details_PG.objects.get(pgcet_uid = student.st_id)
    mgmt_admission_pg = MGMT_Admission_Details_PG.objects.get(mgmt_pg_uid = student.st_id)
    doc_details = Document_Details.objects.get(doc_uid = student.st_id)
    
    bld_grp_tbl = None
    rel_tbl = None
    quota_tbl = None
    category_tbl = None

    try:
        bld_grp_tbl = BloodGroup.objects.all().order_by('name')
    except Exception as e:
        print(e)
        bld_grp_tbl = None

    try:
        rel_tbl = Religion.objects.all()
    except Exception as e:
        print(e)
        rel_tbl = None
    
    try:
        quota_tbl = Admission_Quota.objects.all().order_by('name')
    except Exception as e:
        print(e)
        quota_tbl = None


    try:
        category_tbl = Category.objects.all().order_by('name')
    except Exception as e:
        print(e)
        category_tbl = None
    
    html_string = render_to_string('ack_pdf_pg.html',{'bld_grp_tbl':bld_grp_tbl,'rel_tbl':rel_tbl,'quota_tbl':quota_tbl,'category_tbl':category_tbl,'student':student,'pacad_pg':pacad_pg,'pgcet_admission_pg':pgcet_admission_pg,'mgmt_admission_pg':mgmt_admission_pg,'doc_details':doc_details,'id': st_id,'b_id':pacad_pg.pg_uid,'pgcet_id':pgcet_admission_pg.pgcet_uid,'pgmgmt_id':mgmt_admission_pg.mgmt_pg_uid,'doc_id':doc_details.doc_uid})
    html = HTML(string=html_string, base_url=request.build_absolute_uri())

    result = html.write_pdf()
    
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()

        output=open(output.name, 'rb')
        response.write(output.read())

    return response

def ackPdf_tr(request,st_id):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'inline; attachment; filename='+"st_id_card"+str(datetime.datetime.now())+".pdf"
    response['Content-Transfer-Encoding'] = 'binary'

    academic_year = None
    bld_grp_tbl = None
    state_tbl = None
    rel_tbl = None
    quota_tbl = None
    months_tbl = None
    category_tbl = None
    clg_trns_under_cet = None
    pacad_10th = None 
    pacad_12th = None 
    dip_ug = None
    mgmt_admission_ug = None
    prv_clgtrns_details = None
    comedk_clgtrns = None
    doc_details = None
    dip_admission_ug = None
    try:
        academic_year = AcademicYear.objects.all()
    except Exception as e:
        print(e)
        academic_year = None
    try:
        bld_grp_tbl = BloodGroup.objects.all().order_by('name')
    except Exception as e:
        print(e)
        bld_grp_tbl = None
    try:
        state_tbl = States.objects.all().order_by('name')
    except Exception as e:
        print(e)
        state_tbl = None
        
    try:
        rel_tbl = Religion.objects.all()
    except Exception as e:
        print(e)
        rel_tbl = None
    try:
        quota_tbl = Admission_Quota.objects.all().order_by('name')
    except Exception as e:
        print(e)
        quota_tbl = None

    try:
        months_tbl = Months.objects.all().order_by('id')
    except Exception as e:
        print(e)
        months_tbl = None
    try:
        category_tbl = Category.objects.all().order_by('name')
    except Exception as e:
        print(e)
        category_tbl = None
    student = Student_Details.objects.get(st_id = st_id)
    try:
        clg_trns_under_cet = CET_Admission_Details_UG.objects.get(cet_uid_id = student.st_id)
    except:
        if clg_trns_under_cet is None:
            clg_trns_under_cet = ""
        
    try:
        dip_ug = Previous_dip_Academic_Details.objects.get(dip_uid_id = student.st_id)
    except:
        if dip_ug is None:  
            dip_ug = None
    try:
        pacad_10th = Previous_10th_Academic_Details.objects.get(sslc_uid_id = student.st_id)
    except:
        if pacad_10th is None:
            pacad_10th = None
    try:  
        pacad_12th = Previous_12th_Academic_Details.objects.get(puc_uid_id = student.st_id)
    except:
        if pacad_12th is None:
            pacad_12th = None  
    try:
        dip_admission_ug = Lateralentry_Admission_Details_UG.objects.get(dip_uid = student.st_id)
    except:
        if dip_admission_ug is None:
            dip_admission_ug = None
    try:
        mgmt_admission_ug = MGMT_Admission_Details_UG.objects.get(mgmt_uid = student.st_id)
    except:
        if mgmt_admission_ug is None:
            pass
    try:
        prv_clgtrns_details = Previous_Transfer_College_Details.objects.get(clgtrns_st_uid = student.st_id)
    except Exception as e:
        print(e)
        if prv_clgtrns_details is None:
            pass
    try:        
        comedk_clgtrns = COMEDK_Admission_Details_UG.objects.get(comedk_uid_id = student.st_id)
    except:
        if comedk_clgtrns is None:
            comedk_clgtrns = None
    try:
        doc_details = Document_Details.objects.get(doc_uid = student.st_id)
    except:
        if doc_details is None:
            doc_details = None

    html_string = render_to_string('ack_pdf_clgtrns.html',{'department':Department.objects.all(),'state_tbl' : state_tbl,'student':student,
   'clg_trns_under_cet':clg_trns_under_cet,'dip_ug':dip_ug,'pacad_10th':pacad_10th,'doc_details':doc_details,'id': st_id,'quota_tbl':quota_tbl,'months_tbl':months_tbl,'category_tbl':category_tbl,
   'rel_tbl':rel_tbl, 'state_tbl':state_tbl, 'bld_grp_tbl':bld_grp_tbl, 'academic_year':academic_year,'pacad_12th':pacad_12th,'dip_admission_ug':dip_admission_ug,'mgmt_admission_ug':mgmt_admission_ug,'prv_clgtrns_details':prv_clgtrns_details,'comedk_clgtrns':comedk_clgtrns,'doc_details':doc_details})
    
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    result = html.write_pdf()
 
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output=open(output.name, 'rb')
        response.write(output.read())
        
    return response

def view_ug(request,st_id):
    # student = Student_Details.objects.get(st_id = st_id)
    # pacad_ug = Previous_Academic_Details_UG.objects.get(ug_uid = student.st_id)
    # cet_admission_ug = CET_Admission_Details_UG.objects.get(cet_uid = student.st_id)
    # comedk_admission_ug = COMEDK_Admission_Details_UG.objects.get(comedk_uid = student.st_id)
    # mgmt_admission_ug = MGMT_Admission_Details_UG.objects.get(mgmt_uid = student.st_id)
    # doc_details = Document_Details.objects.get(doc_uid = student.st_id)
    # state_tbl = States.objects.all()
    # return render(request, "view_ug.html",{ 'department':Department.objects.all(),'state_tbl':state_tbl, 'student':student, 'pacad_ug':pacad_ug, 'cet_admission_ug':cet_admission_ug, 'comedk_admission_ug':comedk_admission_ug, 'mgmt_admission_ug':mgmt_admission_ug,'doc_details':doc_details, 'id': st_id, 'a_id':pacad_ug.ug_uid, 'cet_id':cet_admission_ug.cet_uid, 'comedk_id':comedk_admission_ug.comedk_uid,'mgmt_id':mgmt_admission_ug.mgmt_uid,'doc_id':doc_details.doc_uid})
    student = None
    pacad_ug = None
    cet_admission_ug = None
    comedk_admission_ug = None
    mgmt_admission_ug = None
    doc_details = None
    academic_year = None
    bld_grp_tbl = None
    state_tbl = None
    rel_tbl = None
    quota_tbl = None
    months_tbl = None
    category_tbl = None
    try:
        student = Student_Details.objects.get(st_id = st_id)
    except Exception as e:
        print(e)
        student = None

    try:
        pacad_10th = Previous_10th_Academic_Details.objects.get(sslc_uid = student.st_id)
    except Exception as e:
        print(e)
        pacad_10th = None
    
    try:
        pacad_12th = Previous_12th_Academic_Details.objects.get(puc_uid = student.st_id)
    except Exception as e:
        print(e)
        pacad_12th = None

   
    try:
        cet_admission_ug = CET_Admission_Details_UG.objects.get(cet_uid = student.st_id)
    except Exception as e:
        print(e)
        cet_admission_ug = None

    try:
        comedk_admission_ug = COMEDK_Admission_Details_UG.objects.get(comedk_uid = student.st_id)
    except Exception as e:
        print(e)
        comedk_admission_ug = None

    try:
        mgmt_admission_ug = MGMT_Admission_Details_UG.objects.get(mgmt_uid = student.st_id)
    except Exception as e:
        print(e)
        mgmt_admission_ug = None

    try:
        doc_details = Document_Details.objects.get(doc_uid = student.st_id)
    except Exception as e:
        print(e)
        doc_details = None
    
    try:
        academic_year = AcademicYear.objects.all()
    except Exception as e:
        print(e)
        academic_year = None

    try:
        bld_grp_tbl = BloodGroup.objects.all().order_by('name')
    except Exception as e:
        print(e)
        bld_grp_tbl = None

    try:
        state_tbl = States.objects.all()
    except Exception as e:
        print(e)
        state_tbl = None    
        
    try:
        rel_tbl = Religion.objects.all()
    except Exception as e:
        print(e)
        rel_tbl = None

    try:
        quota_tbl = Admission_Quota.objects.all().order_by('name')
    except Exception as e:
        print(e)
        quota_tbl = None

    try:
        months_tbl = Months.objects.all()
    except Exception as e:
        print(e)
        months_tbl = None

    try:
        category_tbl = Category.objects.all().order_by('name')
    except Exception as e:
        print(e)
        category_tbl = None

    return render(request, "view_ug.html",{ 'department':Department.objects.all(),'rel_tbl':rel_tbl, 
    'bld_grp_tbl':bld_grp_tbl, 'state_tbl':state_tbl, 'student':student, 'pacad_10th':pacad_10th, 
    'pacad_12th':pacad_12th, 'cet_admission_ug':cet_admission_ug, 'comedk_admission_ug':comedk_admission_ug, 
    'mgmt_admission_ug':mgmt_admission_ug,'doc_details':doc_details, 'id': st_id, 'academic_year' : academic_year,
    'bld_grp_tbl':bld_grp_tbl, 'rel_tbl':rel_tbl,'months_tbl':months_tbl,'quota_tbl':quota_tbl,'category_tbl':category_tbl})

def view_lat(request,st_id):
    # student = Student_Details.objects.get(st_id = st_id)
    # pacad_ug = Previous_Academic_Details_UG.objects.get(ug_uid = student.st_id)
    # lateral_admission_ug = Lateralentry_Admission_Details_UG.objects.get(dip_uid = student.st_id)
    # mgmt_admission_ug = MGMT_Admission_Details_UG.objects.get(mgmt_uid = student.st_id)
    # doc_details = Document_Details.objects.get(doc_uid = student.st_id)
    # return render(request, "view_lat.html",{ 'department':Department.objects.all(),'student':student, 'pacad_ug':pacad_ug, 'lateral_admission_ug':lateral_admission_ug, 'mgmt_admission_ug':mgmt_admission_ug,'doc_details':doc_details, 'id': st_id, 'a_id':pacad_ug.ug_uid, 'lateral_id':lateral_admission_ug.dip_uid, 'mgmt_id':mgmt_admission_ug.mgmt_uid,'doc_id':doc_details.doc_uid})
    student = None
    pacad_ug = None
    lateral_admission_ug = None
    mgmt_admission_ug = None
    doc_details = None
    academic_year = None
    bld_grp_tbl = None
    state_tbl = None
    rel_tbl = None
    quota_tbl = None
    months_tbl = None
    category_tbl = None

    try:
        student = Student_Details.objects.get(st_id = st_id)
    except Exception as e:
        print(e)
        student = None

    try:
        pacad_10th = Previous_10th_Academic_Details.objects.get(sslc_uid = student.st_id)
    except Exception as e:
        print(e)
        pacad_10th = None
    
    try:
        pacad_12th = Previous_12th_Academic_Details.objects.get(puc_uid = student.st_id)
    except Exception as e:
        print(e)
        pacad_12th = None

    try:
        pacad_dip = Previous_dip_Academic_Details.objects.get(dip_uid = student.st_id)
    except Exception as e:
        print(e)
        pacad_dip = None


    try:
        lateral_admission_ug = Lateralentry_Admission_Details_UG.objects.get(dip_uid = student.st_id)
        print(lateral_admission_ug)
    except Exception as e:
        print(e)
        lateral_admission_ug = None

    try:
        mgmt_admission_ug = MGMT_Admission_Details_UG.objects.get(mgmt_uid = student.st_id)
    except Exception as e:
        print(e)
        mgmt_admission_ug = None

    try:
        doc_details = Document_Details.objects.get(doc_uid = student.st_id)
    except Exception as e:
        print(e)
        doc_details = None

    try:
        academic_year = AcademicYear.objects.all()
    except Exception as e:
        print(e)
        academic_year = None

    try:
        bld_grp_tbl = BloodGroup.objects.all().order_by('name')
    except Exception as e:
        print(e)
        bld_grp_tbl = None

    try:
        state_tbl = States.objects.all().order_by('name')
    except Exception as e:
        print(e)
        state_tbl = None
    
    try:
        rel_tbl = Religion.objects.all()
    except Exception as e:
        print(e)
        rel_tbl = None

    try:
        quota_tbl = Admission_Quota.objects.all().order_by('name')
    except Exception as e:
        print(e)
        quota_tbl = None

    try:
        months_tbl = Months.objects.all().order_by('id')
    except Exception as e:
        print(e)
        months_tbl = None

    try:
        category_tbl = Category.objects.all().order_by('name')
    except Exception as e:
        print(e)
        category_tbl = None

    return render(request, "view_lat.html",{ 'department':Department.objects.all(),'student':student, 
    'pacad_10th':pacad_10th, 'pacad_12th':pacad_12th, 'pacad_dip':pacad_dip, 'lateral_admission_ug':lateral_admission_ug, 
    'mgmt_admission_ug':mgmt_admission_ug,'doc_details':doc_details, 'id': st_id, 'quota_tbl':quota_tbl,'months_tbl':months_tbl,'category_tbl':category_tbl,
    'rel_tbl':rel_tbl, 'state_tbl':state_tbl, 'bld_grp_tbl':bld_grp_tbl, 'academic_year':academic_year})

def view_pg(request,st_id):
    academic_year = None
    bld_grp_tbl = None
    state_tbl = None
    rel_tbl = None
    quota_tbl = None
    months_tbl = None
    category_tbl = None
    try:
        academic_year = AcademicYear.objects.all()
    except Exception as e:
        print(e)
        academic_year = None
    try:
        bld_grp_tbl = BloodGroup.objects.all().order_by('name')
    except Exception as e:
        print(e)
        bld_grp_tbl = None
    try:
        state_tbl = States.objects.all().order_by('name')
    except Exception as e:
        print(e)
        state_tbl = None
    
    try:
        rel_tbl = Religion.objects.all()
    except Exception as e:
        print(e)
        rel_tbl = None
    try:
        quota_tbl = Admission_Quota.objects.all().order_by('name')
    except Exception as e:
        print(e)
        quota_tbl = None
    try:
        months_tbl = Months.objects.all().order_by('id')
    except Exception as e:
        print(e)
        months_tbl = None
    try:
        category_tbl = Category.objects.all().order_by('name')
    except Exception as e:
        print(e)
        category_tbl = None
    student = Student_Details.objects.get(st_id = st_id)
    pacad_pg = Previous_Academic_Details_PG.objects.get(pg_uid = student.st_id)
    pgcet_admission_pg = PGCET_Admission_Details_PG.objects.get(pgcet_uid = student.st_id)
    mgmt_admission_pg = MGMT_Admission_Details_PG.objects.get(mgmt_pg_uid = student.st_id)
    doc_details = Document_Details.objects.get(doc_uid = student.st_id)
    return render(request, "view_pg.html",{ 'department':Department.objects.all(),'state_tbl' : state_tbl,'student':student,
    'pacad_pg':pacad_pg,'pgcet_admission_pg':pgcet_admission_pg,'mgmt_admission_pg':mgmt_admission_pg,'doc_details':doc_details,'id': st_id,'quota_tbl':quota_tbl,'months_tbl':months_tbl,'category_tbl':category_tbl,
    'rel_tbl':rel_tbl, 'state_tbl':state_tbl, 'bld_grp_tbl':bld_grp_tbl, 'academic_year':academic_year})
def view_clgtrns(request,st_id):
    academic_year = None
    bld_grp_tbl = None
    state_tbl = None
    rel_tbl = None
    quota_tbl = None
    months_tbl = None
    category_tbl = None
    clg_trns_under_cet = None
    pacad_10th = None 
    pacad_12th = None 
    dip_ug = None
    mgmt_admission_ug = None
    prv_clgtrns_details = None
    comedk_clgtrns = None
    doc_details = None
    dip_admission_ug = None


    try:
        academic_year = AcademicYear.objects.all()
    except Exception as e:
        print(e)
        academic_year = None

    try:
        bld_grp_tbl = BloodGroup.objects.all().order_by('name')
    except Exception as e:
        print(e)
        bld_grp_tbl = None

    try:
        state_tbl = States.objects.all().order_by('name')
    except Exception as e:
        print(e)
        state_tbl = None
    
    try:
        rel_tbl = Religion.objects.all()
    except Exception as e:
        print(e)
        rel_tbl = None

    try:
        quota_tbl = Admission_Quota.objects.all().order_by('name')
    except Exception as e:
        print(e)
        quota_tbl = None

    try:
        months_tbl = Months.objects.all().order_by('id')
    except Exception as e:
        print(e)
        months_tbl = None

    try:
        category_tbl = Category.objects.all().order_by('name')
    except Exception as e:
        print(e)
        category_tbl = None
    student = Student_Details.objects.get(st_id = st_id)
    try:
        clg_trns_under_cet = CET_Admission_Details_UG.objects.get(cet_uid_id = student.st_id)
    except:
        if clg_trns_under_cet is None:
            clg_trns_under_cet = ""
    
    try:
        dip_ug = Previous_dip_Academic_Details.objects.get(dip_uid_id = student.st_id)
    except:
        if dip_ug is None:  
            dip_ug = None

    try:
        pacad_10th = Previous_10th_Academic_Details.objects.get(sslc_uid_id = student.st_id)
    except:
        if pacad_10th is None:
            pacad_10th = None

    try:  
        pacad_12th = Previous_12th_Academic_Details.objects.get(puc_uid_id = student.st_id)
    except:
        if pacad_12th is None:
            pacad_12th = None  
    try:
        dip_admission_ug = Lateralentry_Admission_Details_UG.objects.get(dip_uid = student.st_id)
    except:
        if dip_admission_ug is None:
            dip_admission_ug = None
    try:
        mgmt_admission_ug = MGMT_Admission_Details_UG.objects.get(mgmt_uid = student.st_id)
    except:
        if mgmt_admission_ug is None:
            pass
    try:
        prv_clgtrns_details = Previous_Transfer_College_Details.objects.get(clgtrns_st_uid = student.st_id)
    except Exception as e:
        print(e)
        if prv_clgtrns_details is None:
            pass
    try:        
        comedk_clgtrns = COMEDK_Admission_Details_UG.objects.get(comedk_uid_id = student.st_id)
    except:
        if comedk_clgtrns is None:
            comedk_clgtrns = None
    try:
        doc_details = Document_Details.objects.get(doc_uid = student.st_id)
    except:
        if doc_details is None:
            doc_details = None
    return render(request, "view_clgtrns.html",{ 'department':Department.objects.all(),'state_tbl' : state_tbl,'student':student,
    'clg_trns_under_cet':clg_trns_under_cet,'dip_ug':dip_ug,'pacad_10th':pacad_10th,'doc_details':doc_details,'id': st_id,'quota_tbl':quota_tbl,'months_tbl':months_tbl,'category_tbl':category_tbl,
    'rel_tbl':rel_tbl, 'state_tbl':state_tbl, 'bld_grp_tbl':bld_grp_tbl, 'academic_year':academic_year,'pacad_12th':pacad_12th,'dip_admission_ug':dip_admission_ug,'mgmt_admission_ug':mgmt_admission_ug,'prv_clgtrns_details':prv_clgtrns_details,'comedk_clgtrns':comedk_clgtrns,'doc_details':doc_details})

# methods to handle admission statistics and admission reports

# def admission_stat(request):
#     academic_year = AcademicYear.objects.all().order_by('-acayear')
#     return render(request,"AdmissionStat.html",{'academic_year':academic_year})

def admissionStat(request):
    userName=CustomUser.objects.get(id=request.user.id)
    context={'username':userName}
    if request.POST:
        ac_year = request.POST['ac_year']
        ad_type = request.POST['ad_type']
    
        if ac_year == "0" or  ad_type == "0" :
            messages.error(request, "Please Enter Both Field to Generate Stat")
            return render(request,"AdmissionStat.html", context)
        else:
            academic_year = AcademicYear.objects.all().order_by('-acayear')
            if ad_type == "1":
                print("--------------------")
                q = Student_Details.objects.filter(Q(st_acad_year_id = ac_year) & Q(st_uid__icontains = "BE"))
                print(q)
                stat = q.values('st_branch_applied_id__dept_name').annotate(CET=Count('st_adm_quota',filter=Q(st_adm_quota=1)), COMEDK=Count('st_adm_quota',filter=Q(st_adm_quota=2)), MGMT=Count('st_adm_quota',filter=Q(st_adm_quota=3)), SNQ=Count('st_adm_quota',filter=Q(st_adm_quota=4)), Total_Student=Count('st_id'))
                context={'username':userName, "ac_year":ac_year, "ad_type":ad_type, "stat": stat,'academic_year':academic_year}
                return render(request,"AdmissionStat.html", context)
            if ad_type == "2":
                q = Student_Details.objects.filter(Q(st_acad_year = ac_year) & Q(st_uid__icontains = "DP"))
                stat = q.values('st_branch_applied_id__dept_name').annotate(DCET=Count('st_adm_quota',filter=Q(st_adm_quota=1)), MGMT=Count('st_adm_quota',filter=Q(st_adm_quota=2)), Total_Student=Count('st_id'))
                context={'username':userName,"ac_year":ac_year, "ad_type":ad_type, "stat": stat,'academic_year':academic_year}
                return render(request,"AdmissionStat.html", context)
            if ad_type == "3":
                q = Student_Details.objects.filter(Q(st_acad_year = ac_year) & (Q(st_uid__icontains = "MT") | Q(st_uid__icontains = "MB"))  )
                stat = q.values('st_branch_applied_id__dept_name').annotate(PGCET=Count('st_adm_quota',filter=Q(st_adm_quota=5)), MGMT=Count('st_adm_quota',filter=Q(st_adm_quota=4)), Total_Student=Count('st_id'))
                context={'username':userName, "ac_year":ac_year, "ad_type":ad_type, "stat": stat,'academic_year':academic_year}
                return render(request,"AdmissionStat.html", context)
    else:       
        academic_year = AcademicYear.objects.all().order_by('-acayear')
        return render(request,"AdmissionStat.html",{'academic_year':academic_year})

def admissionStatReport(request, ad_type, ac_year):
    if ad_type == "1":
        q = Student_Details.objects.filter(Q(st_acad_year_id = ac_year) & Q(st_uid__icontains = "BE"))
        stat = q.values('st_branch_applied_id__dept_name').annotate(CET=Count('st_adm_quota',filter=Q(st_adm_quota=1)), SNQ=Count('st_adm_quota',filter=Q(st_adm_quota=2)), COMEDK=Count('st_adm_quota',filter=Q(st_adm_quota=3)), MGMT=Count('st_adm_quota',filter=Q(st_adm_quota=4)), Total_Student=Count('st_id'))
    if ad_type == "2":
        q = Student_Details.objects.filter(Q(st_acad_year_id = ac_year) & Q(st_uid__icontains = "DP"))
        stat = q.values('st_branch_applied_id__dept_name').annotate(DCET=Count('st_adm_quota',filter=Q(st_adm_quota=1)), MGMT=Count('st_adm_quota',filter=Q(st_adm_quota=2)), Total_Student=Count('st_id'))
    if ad_type == "3":
        q = Student_Details.objects.filter(Q(st_acad_year_id = ac_year) & (Q(st_uid__icontains = "MT") | Q(st_uid__icontains = "MB"))  )
        stat = q.values('st_branch_applied_id__dept_name').annotate(PGCET=Count('st_adm_quota',filter=Q(st_adm_quota=5)), MGMT=Count('st_adm_quota',filter=Q(st_adm_quota=4)), Total_Student=Count('st_id'))
    ac_year=AcademicYear.objects.get(id=ac_year)
    context={"ac_year":ac_year.acayear, "ad_type":ad_type, "stat": stat}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'inline; attachment; filename='+"AdmissionStatReport"+str(datetime.datetime.now())+".pdf"
    response['Content-Transfer-Encoding'] = 'binary'

    html_string = render_to_string("AdmStatReport.html", context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())

    result = html.write_pdf()
    
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()

        output=open(output.name, 'rb')
        response.write(output.read())

    return response

def gen_ack(request):
    department = Department.objects.all()

    if request.POST:
        Branch = request.POST['st_branch']
        Uid = request.POST['st_uid']
        Name = request.POST['st_name']
        Usn = request.POST['st_usn']
        if Branch == "0" and Uid == "" and Name == "" and Usn == "":
            messages.error(request, "Please Enter Atleast One Field to Search")
        else:
            SearchParm1 = Student_Details.objects.filter(Q(st_name__icontains = Name) & Q(st_uid__icontains = Uid))
            SearchParm2 = Student_Details.objects.filter(st_branch_applied_id = int(Branch))
            if Name == '':
                c1 = ~Q(st_name__icontains = Name)
            else:
                c1 = Q(st_name__icontains = Name)
            
            if Uid == '':
                c2 = ~Q(st_uid__icontains = Uid)
            else:
                c2 = Q(st_uid__icontains = Uid)    

            c3 = Q(st_branch_applied_id = int(Branch))

            SearchParm = Student_Details.objects.filter(c1 | c2 | c3)
            if not SearchParm.exists():
                messages.error(request,"Student Details Not Found")
            return render(request,"gen_ack.html",{'student':SearchParm,'department':department})

        return render(request,"gen_ack.html",{'department':department})
        
    else:
        return render(request,"gen_ack.html",{'department':department})

def edit_student(request,st_id):
    student = None
    pacad_ug = None
    cet_admission_ug = None
    comedk_admission_ug = None
    mgmt_admission_ug = None
    doc_details = None
    academic_year = None
    bld_grp_tbl = None
    state_tbl = None
    rel_tbl = None
    quota_tbl = None
    months_tbl = None
    category_tbl = None

    try:
        student = Student_Details.objects.get(st_id = st_id)
    except Exception as e:
        print(e)
        student = None

    try:
        pacad_10th = Previous_10th_Academic_Details.objects.get(sslc_uid = student.st_id)
    except Exception as e:
        print(e)
        pacad_10th = None

    try:
        pacad_12th =  Previous_12th_Academic_Details.objects.get(puc_uid = student.st_id)
    except Exception as e:
        print(e)
        pacad_12th = None

    try:
        cet_admission_ug = CET_Admission_Details_UG.objects.get(cet_uid = student.st_id)
    except Exception as e:
        print(e)
        cet_admission_ug = None

    try:
        comedk_admission_ug = COMEDK_Admission_Details_UG.objects.get(comedk_uid = student.st_id)
    except Exception as e:
        print(e)
        comedk_admission_ug = None
 
    try:
        mgmt_admission_ug = MGMT_Admission_Details_UG.objects.get(mgmt_uid = student.st_id)
    except Exception as e:
        print(e)
        mgmt_admission_ug = None

    try:
        doc_details = Document_Details.objects.get(doc_uid = student.st_id)
    except Exception as e:
        print(e)
        doc_details = None
    try:
        academic_year = AcademicYear.objects.all()
    except Exception as e:
        print(e)
        academic_year = None
    
    try:
        bld_grp_tbl = BloodGroup.objects.all().order_by('name')
    except Exception as e:
        print(e)
        bld_grp_tbl = None
    
    try:
        state_tbl = States.objects.all()
    except Exception as e:
        print(e)
        state_tbl = None
    
    try:
        rel_tbl = Religion.objects.all()
    except Exception as e:
        print(e)
        rel_tbl = None

    try:
        quota_tbl = Admission_Quota.objects.all().order_by('name')
    except Exception as e:
        print(e)
        quota_tbl = None
    
    try:
        months_tbl = Months.objects.all()
    except Exception as e:
        print(e)
        months_tbl = None
    
    try:
        category_tbl = Category.objects.all().order_by('name')
    except Exception as e:
        print(e)
        category_tbl = None

    return render(request, "add_student.html",{ 'department':Department.objects.all(),'state_tbl':state_tbl,'student':student, 'pacad_10th':pacad_10th, 'pacad_12th':pacad_12th,'cet_admission_ug':cet_admission_ug, 'comedk_admission_ug':comedk_admission_ug, 
    'mgmt_admission_ug':mgmt_admission_ug,'doc_details':doc_details, 'id': st_id,'academic_year' : academic_year,'bld_grp_tbl':bld_grp_tbl, 'rel_tbl':rel_tbl,'months_tbl':months_tbl,'quota_tbl':quota_tbl,'category_tbl':category_tbl})

def edit_lateral(request,st_id):
    student = None
    pacad_ug = None
    pacad_10th = None
    lateral_admission_ug = None
    mgmt_admission_ug = None
    doc_details = None
    academic_year = None
    bld_grp_tbl = None
    state_tbl = None
    rel_tbl = None
    quota_tbl = None
    months_tbl = None
    category_tbl = None

    try:
        student = Student_Details.objects.get(st_id = st_id)
    except Exception as e:
        print(e)
        student = None
    
    try:
        pacad_dip = Previous_dip_Academic_Details.objects.get(dip_uid = student.st_id)
    except Exception as e:
        print(e)
        pacad_dip = None

    try:
        pacad_10th = Previous_10th_Academic_Details.objects.get(sslc_uid_id = student.st_id)
    except Exception as e:
        print(e)
        pacad_10th = None

    try:
        lateral_admission_ug = Lateralentry_Admission_Details_UG.objects.get(dip_uid_id = student.st_id)
        print(lateral_admission_ug)
    except Exception as e:
        print(e)
        lateral_admission_ug = None

    try:
        mgmt_admission_ug = MGMT_Admission_Details_UG.objects.get(mgmt_uid = student.st_id)
    except Exception as e:
        print(e)
        mgmt_admission_ug = None
    
    try:
        doc_details = Document_Details.objects.get(doc_uid = student.st_id)
    except Exception as e:
        print(e)
        doc_details = None

    try:
        academic_year = AcademicYear.objects.all()
    except Exception as e:
        print(e)
        academic_year = None
    
    try:
        bld_grp_tbl = BloodGroup.objects.all().order_by('name')
    except Exception as e:
        print(e)
        bld_grp_tbl = None
    
    try:
        state_tbl = States.objects.all().order_by('name')
    except Exception as e:
        print(e)
        state_tbl = None
    
    try:
        rel_tbl = Religion.objects.all()
    except Exception as e:
        print(e)
        rel_tbl = None

    try:
        quota_tbl = Admission_Quota.objects.all().order_by('name')
    except Exception as e:
        print(e)
        quota_tbl = None

    try:
        months_tbl = Months.objects.all().order_by('id')
    except Exception as e:
        print(e)
        months_tbl = None

    try:
        category_tbl = Category.objects.all().order_by('name')
    except Exception as e:
        print(e)
        category_tbl = None

    return render(request, "add_lateral.html",{ 'department':Department.objects.all(),'student':student,
    'pacad_dip':pacad_dip, 'mgmt_admission_ug':mgmt_admission_ug,'doc_details':doc_details, 
    'id': st_id,'quota_tbl':quota_tbl,'months_tbl':months_tbl,'category_tbl':category_tbl,'lateral_admission_ug':lateral_admission_ug ,
    'rel_tbl':rel_tbl, 'state_tbl':state_tbl, 'bld_grp_tbl':bld_grp_tbl, 'academic_year':academic_year,'pacad_10th':pacad_10th})

def edit_transferofcollege(request,st_id):
    clg_trns_under_cet = None; pacad_ug = None; dip_admission_ug = None; mgmt_admission_ug = None; 
    prv_clgtrns_details = None; comedk_clgtrns = None; doc_details = None; quota_tbl = None;
    months_tbl = None; category_tbl = None;  academic_year = None; bld_grp_tbl = None; rel_tbl = None;
    state_tbl = None;pacad_10th = None; pacad_12th = None; dip_ug = None;  
    student = Student_Details.objects.get(st_id = st_id)
    try:
        clg_trns_under_cet = CET_Admission_Details_UG.objects.get(cet_uid = student.st_id)
    except:
        if clg_trns_under_cet is None:
            clg_trns_under_cet = ""
    
    try:
        dip_ug = Previous_dip_Academic_Details.objects.get(dip_uid_id = student.st_id)
    except:
        if dip_ug is None:  
            dip_ug = None

    try:
        pacad_10th = Previous_10th_Academic_Details.objects.get(sslc_uid_id = student.st_id)
    except:
        if pacad_10th is None:
            pacad_10th = None

    try:  
        pacad_12th = Previous_12th_Academic_Details.objects.get(puc_uid_id = student.st_id)
    except:
        if pacad_12th is None:
            pacad_12th = None  
    try:
        dip_admission_ug = Lateralentry_Admission_Details_UG.objects.get(dip_uid = student.st_id)
    except:
        if dip_admission_ug is None:
            dip_admission_ug = None
    try:
        mgmt_admission_ug = MGMT_Admission_Details_UG.objects.get(mgmt_uid = student.st_id)
    except:
        if mgmt_admission_ug is None:
            pass
    try:
        prv_clgtrns_details = Previous_Transfer_College_Details.objects.get(clgtrns_st_uid = student.st_id)
    except Exception as e:
        print(e)
        if prv_clgtrns_details is None:
            pass
    try:        
        comedk_clgtrns = COMEDK_Admission_Details_UG.objects.get(comedk_uid = student.st_id)
    except:
        if comedk_clgtrns is None:
            comedk_clgtrns = None
    try:
        doc_details = Document_Details.objects.get(doc_uid = student.st_id)
    except:
        if doc_details is None:
            doc_details = None
    quota_tbl = Admission_Quota.objects.all().order_by('name')
    months_tbl = Months.objects.all()
    category_tbl = Category.objects.all()
    academic_year = AcademicYear.objects.all()
    bld_grp_tbl = BloodGroup.objects.all().order_by('name')
    rel_tbl = Religion.objects.all().order_by('name')
    state_tbl = States.objects.all().order_by('name')
    return render(request, "add_transfercollege.html",{ 'department':Department.objects.all(),'student':student, 'clg_trns_under_cet':clg_trns_under_cet, 
    'pacad_ug':pacad_ug, 'dip_admission_ug':dip_admission_ug,'mgmt_admission_ug':mgmt_admission_ug,'doc_details':doc_details,
    'id': st_id, 'comedk_clgtrns':comedk_clgtrns,'prv_clgtrns_details':prv_clgtrns_details,'quota_tbl':quota_tbl,'months_tbl':months_tbl,'category_tbl':category_tbl,'academic_year':academic_year,'bld_grp_tbl':bld_grp_tbl,'rel_tbl':rel_tbl,'months_tbl':months_tbl,'state_tbl':state_tbl,
    'pacad_10th':pacad_10th,'pacad_12th':pacad_12th,'dip_ug':dip_ug})

def edit_studentpg(request,st_id):

    student = None
    pacad_pg = None
    pgcet_admission_pg = None
    mgmt_admission_pg = None
    doc_details = None
    academic_year = None
    bld_grp_tbl = None
    state_tbl = None
    rel_tbl = None
    quota_tbl = None
    months_tbl = None
    category_tbl = None

    try:
        student = Student_Details.objects.get(st_id = st_id)
    except Exception as e:
        print(e)
        student = None

    try:
        pacad_pg =  Previous_Academic_Details_PG.objects.get(pg_uid_id = student.st_id)
    except Exception as e:
        print(e)
        pacad_pg = None

    try:
        pgcet_admission_pg = PGCET_Admission_Details_PG.objects.get(pgcet_uid_id = student.st_id)
    except Exception as e:
        print(e)
        pgcet_admission_pg = None
        
    try:
        mgmt_admission_pg = MGMT_Admission_Details_PG.objects.get(mgmt_pg_uid_id = student.st_id)
    except Exception as e:
        print(e)
        mgmt_admission_pg = None

    try:
        doc_details = Document_Details.objects.get(doc_uid = student.st_id)
    except Exception as e:
        print(e)
        doc_details = None
    try:
        academic_year = AcademicYear.objects.all()
    except Exception as e:
        print(e)
        academic_year = None
    
    try:
        bld_grp_tbl = BloodGroup.objects.all().order_by('name')
    except Exception as e:
        print(e)
        bld_grp_tbl = None
    
    try:
        state_tbl = States.objects.all()
    except Exception as e:
        print(e)
        state_tbl = None
    
    try:
        rel_tbl = Religion.objects.all()
    except Exception as e:
        print(e)
        rel_tbl = None

    try:
        quota_tbl = Admission_Quota.objects.all().order_by('name')
    except Exception as e:
        print(e)
        quota_tbl = None
    
    try:
        months_tbl = Months.objects.all()
    except Exception as e:
        print(e)
        months_tbl = None
    
    try:
        category_tbl = Category.objects.all().order_by('name')
    except Exception as e:
        print(e)
        category_tbl = None

    return render(request, "add_pg.html",{ 'department':Department.objects.all(),'state_tbl':state_tbl,'student':student, 'pacad_pg':pacad_pg, 'pgcet_admission_pg':pgcet_admission_pg, 
    'mgmt_admission_pg':mgmt_admission_pg,'doc_details':doc_details, 'id': st_id,'academic_year' : academic_year,'bld_grp_tbl':bld_grp_tbl, 'rel_tbl':rel_tbl,'months_tbl':months_tbl,'quota_tbl':quota_tbl,'category_tbl':category_tbl})


def add_student(request):
    academic_year = AcademicYear.objects.all().order_by('-acayear')
    department = Department.objects.all().order_by('dept_name')
    bld_grp_tbl = BloodGroup.objects.all().order_by('name')
    rel_tbl = Religion.objects.all().order_by('name')
    state_tbl = States.objects.all().order_by('name')
    months_tbl = Months.objects.all().order_by('id')
    quota_tbl = Admission_Quota.objects.all().order_by('name')
    category_tbl = Category.objects.all().order_by('name')
    return render(request,"add_student.html",{'department': Department.objects.all(), 'state_tbl':state_tbl,
    'academic_year':academic_year,'bld_grp_tbl':bld_grp_tbl,'rel_tbl':rel_tbl,'months_tbl':months_tbl,'quota_tbl':quota_tbl,'category_tbl':category_tbl})

def add_pg(request):
    academic_year = AcademicYear.objects.all()
    bld_grp_tbl = BloodGroup.objects.all().order_by('name')
    rel_tbl = Religion.objects.all()
    state_tbl = States.objects.all()
    months_tbl = Months.objects.all()
    quota_tbl = Admission_Quota.objects.all().order_by('name')
    category_tbl = Category.objects.all()
    return render(request,"add_pg.html",{'department': Department.objects.all(), 'state_tbl':state_tbl,'academic_year':academic_year,'bld_grp_tbl':bld_grp_tbl,'rel_tbl':rel_tbl,'months_tbl':months_tbl,'quota_tbl':quota_tbl,'category_tbl':category_tbl})

def add_lateral(request):
    academic_year = AcademicYear.objects.all().order_by('-acayear')
    bld_grp_tbl = BloodGroup.objects.all().order_by('name')
    rel_tbl = Religion.objects.all().order_by('name')
    state_tbl = States.objects.all().order_by('name')
    months_tbl = Months.objects.all().order_by('id')
    quota_tbl = Admission_Quota.objects.all().order_by('name')
    category_tbl = Category.objects.all().order_by('name')
    return render(request,"add_lateral.html",{'department': Department.objects.all(), 'state_tbl':state_tbl,'academic_year':academic_year,'bld_grp_tbl':bld_grp_tbl,'rel_tbl':rel_tbl,'months_tbl':months_tbl,'quota_tbl':quota_tbl,'category_tbl':category_tbl})

def add_transferofcollege(request):
    academic_year = AcademicYear.objects.all().order_by('-acayear')
    bld_grp_tbl = BloodGroup.objects.all().order_by('name')
    rel_tbl = Religion.objects.all()
    state_tbl = States.objects.all().order_by('name')
    months_tbl = Months.objects.all()
    quota_tbl = Admission_Quota.objects.all().order_by('name')
    category_tbl = Category.objects.all()
    return render(request,"add_transfercollege.html",{'department': Department.objects.all(), 'state_tbl':state_tbl,'academic_year':academic_year,'bld_grp_tbl':bld_grp_tbl,'rel_tbl':rel_tbl,'months_tbl':months_tbl,'quota_tbl':quota_tbl,'category_tbl':category_tbl})

def view_student(request):
    department = Department.objects.all()
    student_obj = Student_Details.objects.all()
    return render(request,"view_student.html",{'department':department, 'student_obj':student_obj})

def Admission_Higher_Semester_Details_view(request):
    academic_year = AcademicYear.objects.all()
    userName=CustomUser.objects.get(id=request.user.id)
    dept = Department.objects.all()
    student_obj = Student_Details.objects.all()
    return render(request,"Admission_Higher_Semester_Details.html",{'academic_year':academic_year,'dept':dept, 'student_obj':student_obj,'username':userName})

def admitStudent_higher(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:  
        admit_year = request.POST.get("acad_year")
        # sem_type = request.POST.get("semester-type")
        sem = request.POST.get("semester-select")
        branch = request.POST.get("offered_by")
        st_uid = request.POST.get("uid")

        dept = Department.objects.all().get(dept_id=branch) 
        dept_name=dept.dept_name
        print(dept.dept_name)
        st_uid = request.POST.get("uid")
 
        print(st_uid) 
        higher_fees = request.POST.get("feepaid") 
        challan_no = request.POST.get("challanid") 
        flag=0
        try:
            student= Student_Details.objects.all().get(st_uid=st_uid)
        except:
            messages.error(request,"Student not present in the promotion list")
            return HttpResponseRedirect('Admission_Higher_Semester_Details_view')

        try:
            acad_cal_id_odd = Academic_Calendar.objects.get(acad_cal_acad_year=admit_year,acad_cal_sem=sem).acad_cal_id

            print(acad_cal_id_odd)
            even_sem = int(sem)+1
            print(even_sem)
            acad_cal_id_even = Academic_Calendar.objects.get(acad_cal_acad_year=admit_year,acad_cal_sem=even_sem).acad_cal_id
            print(acad_cal_id_even)
            promotion_id = Student_Promotion_List.objects.filter(st_uid=st_uid,acad_cal_id_odd=acad_cal_id_odd).values('st_uid')
            print(promotion_id)
            for st in promotion_id:
                print(st['st_uid'])
                flag=1
            
        except Exception as e:
            messages.error(request,e)

        btn_value = request.POST["btn_clicked"]
        if btn_value == "search":
            context={'admit_year':admit_year,'sem':sem,'branch':branch,'dept_name':dept_name,'st_uid':st_uid,'flag':flag}
            return render(request,"Admission_Higher_Semester_Details.html",context=context)

        btn_value = request.POST["btn_clicked"]    
        if btn_value=="submit":
            admit_year = request.POST.get("acad_year")
            print(admit_year)
            try:
                admit_higher_sem_obj = Admission_Higher_Semester_Details.objects.create(acad_cal_odd=acad_cal_id_odd,acad_cal_even=acad_cal_id_even,semester=sem,dept_id=dept,st_uid=student,admit_higher_fees=higher_fees,admit_higher_challan_no=challan_no)
                admit_higher_sem_obj.save()
            except IntegrityError:
                print('duplicate')
                messages.error(request,'Duplicate entry!!Student already exists')
                return HttpResponseRedirect('Admission_Higher_Semester_Details_view')

            messages.success(request, "Success! Admitted")
            #return Admission_Higher_Semester_Details(request)
            return HttpResponseRedirect('Admission_Higher_Semester_Details_view')

def student_report(request):
    pass

def delete_student(request):
    pass

def get_image_from_data_url( data_url, resize=False, base_width=600 ):
    # getting the file format and the necessary dataURl for the file
    _format, _dataurl = data_url.split(';base64,')
    # file name and extension
    _filename, _extension   = secrets.token_hex(20), _format.split('/')[-1]

    # generating the contents of the file
    file = ContentFile( base64.b64decode(_dataurl), name=f"{_filename}.{_extension}")

    # resizing the image, reducing quality and size
    if resize:

        # opening the file with the pillow
        image = Image.open(file)
        # using BytesIO to rewrite the new content without using the filesystem
        image_io = io.BytesIO()

        # save resized image
        image.save(image_io, format=_extension)

        # generating the content of the new image
        file = ContentFile( image_io.getvalue(), name=f"{_filename}.{_extension}" ) 

    # file and filename
    # return file, ( _filename, _extension )
    return file

#@transaction.atomic
def admitStudent_lat(request):
    if request.method!="POST":
        return HttpResponseRedirect('AddLateralStudent')
    else:
        parent_income = None
        mother_income = None
        admit_year = None
       # pg_course = None
        admis_date = None
        admis_allot = None
        name = None
        course = None
        branch = None
        dept = None
        quota = None
        dob = None
        medium = None
        gender = None
        locality = None
        bld_grp = None
        BirthPlace = None
        Mothertongue = None
        Nationality = None
        religion = None
        Caste = None
        SubCaste = None
        ActualCategory = None
        StudentMobileNo = None
        StudentMailID = None
        aadhar_no = None
        st_eactivity = None
        father_name = None
        mother_name = None
        fatherjob = None
        motherjob = None
        parent_mobile_no = None
        mother_mobile_no = None
        parent_pan = None
        mother_pan = None
        parent_email = None
        mother_email =None
        pmtaddress = None
        pmtaddress_city = None
        pmtaddress_district = None
        pmtaddress_state = None
        pmtaddress_pincode = None
        postaladdress = None
        postaladdress_city = None
        postaladdress_district = None
        postaladdress_state = None
        postaladdress_pincode =None
        st_gaddress = None
        st_gmobno = None
        st_healthissues = None
        st_gemail = None
        x_board = None
        x_schoolname = None
        x_pass_month = None
        x_pass_year = None
        x_state = None
        x_medium = None
        x_regno = None
        x_marks = None
        x_percentage = None
        xii_board = None
        xii_school_name = None
        xii_month =None
        xii_passyr = None
        xii_pass_state = None
        xii_medium = None
        xii_regno = None
        xii_marks = None
        xii_percentage = None
        xii_pmarks = None
        xii_cmarks = None
        xii_mmarks = None
        xii_biocsmarks = None
        xii_pcmmakrs = None
        xii_pcmpercentage = None
        TotalFeePaid = None
        RtChallanNo = None
        RtChallanDate = None

        dip_board = None
        dip_school_name = None
        dip_month =None
        dip_passyr = None
        dip_pass_state = None
        dip_medium = None
        dip_regno = None
        dip_5marks = None
        dip_6marks = None
        dip_tmarks = None
        dip_tpercentage = None

        dip_admorder = None
        dip_dcetno = None
        diprank = None
        dipcatclaim = None
        dipcatallot = None
        dip_allotdate = None
        dip_feespaid = None 
        dip_collfeepaid = None
        dip_tfeespaid = None 
        dip_cdate = None
        dip_cno = None

        MGMTRank = None
        MGMTcet = None
        MGMTcomedk = None
        MGMTCollegeFeedPaid = None
        MGMTChallandate = None
        MGMTChallanNo = None
        ptm = None
        AllotmentOrdCopy = None
        x_MarksCardCopy = None
        xii_MarksCardCopy = None
        dip_MarksCardCopy = None
        deg_certCopy = None
        StudyCertificate = None
        IncomeCertificate = None
        LinguisticCertificate = None
        Eligcertificate = None
        Migcertificate = None
        TransferCertificate = None
        AadharCard = None
        PanCard = None
        rlg=None
        pmtstate=None
        actualCategory=None
        take_photo = None
        StudentID = None
        StudentUID = None
        poststate=None
        mg_ug=0
        tenSTATE = None
        admyear=None
        mg_pg=0
        try:   
            # Student details (add_student.html)
            take_photo = request.POST.get("take-photo")
            # # Generating Student UID code
            name = request.POST.get("st_name") 
            admit_year = request.POST.get("st_acad_year")
            branch = request.POST.get("st_branch_applied")
            dept = Department.objects.get(dept_id=branch)  
            # # Generating Student UID code
            #admit_year = "2020-21"
            admis_allot = request.POST.get("st_adm_applied")
            st_similar_uid_set_count = 0
            acadyr = AcademicYear.objects.get(id=admit_year).acayear
            Slice_year = acadyr[2:4]
            course = request.POST.get("st_course")
            with transaction.atomic():
                #StudentSet = Student_Details.objects.select_for_update().filter(st_uid__contains=Slice_year + course).order_by('-st_id')[0]
                StudentSet = Student_Details.objects.filter(st_uid__contains=Slice_year + course).order_by('-st_id')[0]
            
            st_uid_sl_no = int(StudentSet.st_uid[4:])+1
                #st_uid_sl_no must be converted to string type else it cannot be concatenated
            if(st_uid_sl_no < 10):
                st_uid = Slice_year+course+'000'+str(st_uid_sl_no)
            elif(st_uid_sl_no > 9 and st_uid_sl_no <100):
                st_uid = Slice_year+course+'00'+str(st_uid_sl_no)
            elif(st_uid_sl_no > 99 and st_uid_sl_no <1000):
                st_uid = Slice_year+course+'0'+str(st_uid_sl_no)
            elif(st_uid_sl_no > 999 and st_uid_sl_no <10000):
                    st_uid = Slice_year+course+str(st_uid_sl_no)
            StudentUID = st_uid   
            
        except IndexError:
            st_uid = Slice_year+course+'0001'
            StudentUID = st_uid

        #Compulsory HTML fields are validated from fron-end itself
        #Hence no need of individual try-catch blocks for such fields
        try:
            RtChallanDate = request.POST.get("st_adm_date")  
            admis_date = request.POST.get("adm_date")
            quota = int(request.POST.get("st_adm_quota"))
            dob = request.POST.get("st_dob")
            medium = int(request.POST.get("medium"))
            gender = int(request.POST.get("st_gender"))
            locality = int(request.POST.get("st_locality"))
            #Religion static table instance
            StudentMobileNo = request.POST.get("st_mobile_no")
            religion = int(request.POST.get("st_religion"))      
            Caste = request.POST.get("st_caste")
            ActualCategory = int(request.POST.get("st_category"))
            StudentMailID = request.POST.get("st_email_id")
            st_eactivity = request.POST.get("st_extracurr_activity")
            father_name = request.POST.get("st_father_name")
            mother_name = request.POST.get("st_mother_name")
            parent_income = request.POST.get("st_father_income")
            parent_mobile_no = request.POST.get("st_father_mobile_no")
            pmtaddress = request.POST.get("st_parent_address")
            pmtaddress_city = request.POST.get("st_parent_address_city")
            pmtaddress_district= request.POST.get("st_parent_address_district")
            pmtaddress_state = int(request.POST.get("st_parent_address_state"))
            pmtaddress_pincode = request.POST.get("st_parent_address_pincode")
            postaladdress = request.POST.get("st_postal_address")
            postaladdress_city = request.POST.get("st_postal_address_city")
            postaladdress_district= request.POST.get("st_postal_address_district")
            postaladdress_state = int(request.POST.get("st_postal_address_state"))
            postaladdress_pincode = request.POST.get("st_postal_address_pincode")
            TotalFeePaid = int(request.POST.get("st_total_fees"))
            RtChallanNo = int(request.POST.get("st_rt_no"))
            st_gaddress = request.POST.get("st_local_guardian_addr")
            st_gmobno = request.POST.get("st_guardian_mobile_no")
            st_healthissues = request.POST.get("st_health_issues")
            st_gemail = request.POST.get("st_guardian_email")
            Mothertongue = request.POST.get("st_mother_tongue")
            Nationality = int(request.POST.get("st_nationality"))
            mother_mobile_no = request.POST.get("st_mother_mobile_no")
            parent_pan = request.POST.get("st_father_pan")
            mother_pan = request.POST.get("st_mother_pan")
            parent_email = request.POST.get("st_father_email_id")
            mother_email = request.POST.get("st_mother_email_id")
            fatherjob = request.POST.get("st_father_occupation")
            motherjob = request.POST.get("st_mother_occupation")
            # FOR OFFICE USE ONLY
            SubCaste = request.POST.get("st_subcaste")
            BirthPlace = request.POST.get("st_pob") 
        except:
            if quota is None:
                quota = 0
            if gender is None:
                gender = 0
            if locality is None:
                locality = 0
            if Nationality is None:
                Nationality = 0
            if religion is None:
                religion = 0
            if ActualCategory is None:
                ActualCategory = 0
            if pmtaddress_state is None:
                pmtaddress_state = 0
            if postaladdress_state is None:
                postaladdress_state = 0
            if parent_income is None:
                parent_income  = 0
            if TotalFeePaid is None:
                TotalFeePaid = 0
            if RtChallanNo is None:
                RtChallanNo = 0

        try:
            bld_grp = int(request.POST.get("st_bld_group"))
        except Exception as e:
            print(e)
            if bld_grp is None:
                bld_grp = 0
        try:
            aadhar_no = int(request.POST.get("st_aadhar_no")) #O
        except Exception as e:
            print(e)
            if aadhar_no is None:
                aadhar_no = None
        try:
            mother_income = int(request.POST.get("st_mother_income")) #O
        except Exception as e:
            print(e)
            if mother_income is None:
                mother_income = None

        try:        
            # Previous Academic Details UG
            x_board = request.POST.get("ug_pacad_10th_board")
            x_schoolname = request.POST.get("ug_pacad_10th_schoolname")
            x_pass_month = int(request.POST.get("ug_pacad_10th_pass_month"))
            x_pass_year = request.POST.get("ug_pacad_10th_pass_year")
            x_state = request.POST.get("ug_pacad_10th_pass_state")
            x_medium = request.POST.get("ug_pacad_10th_medium")
            x_regno = request.POST.get("ug_pacad_10th_reg_no")
            x_marks = float(request.POST.get("ug_pacad_10th_total_marks_cgpa"))
            x_percentage = float(request.POST.get("ug_pacad_10th_percentage_cgpa"))
            xii_board = request.POST.get("ug_pacad_12th_board")
            xii_school_name = request.POST.get("ug_pacad_12th_schoolname")
            xii_month = int(request.POST.get("ug_pacad_12th_pass_month"))
            xii_passyr = request.POST.get("ug_pacad_12th_pass_year")
            xii_pass_state = request.POST.get("ug_pacad_12th_pass_state")
            xii_medium = request.POST.get("ug_pacad_12th_medium")
            xii_regno = request.POST.get("ug_pacad_12th_reg_no")
            xii_marks = int(request.POST.get("ug_pacad_12th_total_marks"))
            xii_percentage = float(request.POST.get("ug_pacad_12th_percentage"))
            xii_pmarks = int(request.POST.get("ug_pacad_12th_physics_marks"))
            xii_cmarks = int(request.POST.get("ug_pacad_12th_chemistry_marks"))
            xii_mmarks = int(request.POST.get("ug_pacad_12th_maths_marks"))
            xii_biocsmarks = int(request.POST.get("ug_pacad_12th_bio_cs_marks"))
            xii_pcmmakrs = int(request.POST.get("ug_pacad_12th_pcm_total_marks"))
            xii_pcmpercentage = float(request.POST.get("ug_pacad_12th_pcm_percentage"))

        except:
            if x_marks is None:
                x_marks = 0
            if x_percentage is None:
                x_percentage = 0
            if xii_marks is None:
                xii_marks = 0
            if xii_percentage is None:
                xii_percentage = 0
            if xii_pmarks is None:
                xii_pmarks = 0
            if xii_cmarks is None:
                xii_cmarks = 0
            if xii_mmarks is None:
                xii_mmarks = 0
            if xii_pcmmakrs is None:
                xii_pcmmakrs = 0
            if xii_pcmpercentage is None:
                xii_pcmpercentage = 0
            if xii_biocsmarks is None:
                xii_biocsmarks = 0

        try:
            # Details for students admitted under MANAGEMENT quota
            MGMTRank = int(request.POST.get("mgmt_rank"))

            MGMTcet = request.POST.getlist("mgmt_exam[]")

            for m in MGMTcet:
                mg_ug=int(mg_ug)+int(m)

            MGMTCollegeFeedPaid = int(request.POST.get("mgmt_college_fees_paid"))
            MGMTChallandate = request.POST.get("mgmt_challan_date")
            MGMTChallanNo = int(request.POST.get("mgmt_challan_no"))

        except:
            if MGMTRank is None:
                MGMTRank = 0
            if MGMTCollegeFeedPaid is None:
                MGMTCollegeFeedPaid = 0
            if MGMTChallanNo is None:
                MGMTChallanNo = 0

        try:
            # Documents submitted by the applicant
            AllotmentOrdCopy = int(request.POST.get("alt_order_copy"))
            x_MarksCardCopy = request.POST.get("st_10th_marks_card")
            xii_MarksCardCopy = request.POST.get("st_12th_marks_card")
            dip_MarksCardCopy = request.POST.get("st_dip_marks_card")
            deg_certCopy = request.POST.get("st_degree_certificate")
            StudyCertificate = request.POST.get("st_study_cerfiticate")
            IncomeCertificate = request.POST.get("st_income_certificate")
            LinguisticCertificate = request.POST.get("st_tulu_certificate")
            Eligcertificate = request.POST.get("st_eligibility_certificate")
            Migcertificate = request.POST.get("st_migration_certificate")
            TransferCertificate = request.POST.get("st_transfer_certificate")
            AadharCard = request.POST.get("st_aadhar_card")
            PanCard = request.POST.get("st_pan_card")
        except:
            if AllotmentOrdCopy is None:
                AllotmentOrdCopy = 0
        try:
            #Diploma Details (add_lateral.html)
            dip_board = request.POST.get("ug_pacad_dip_board")
            dip_school_name = request.POST.get("ug_pacad_dip_schoolname")
            dip_month = request.POST.get("ug_pacad_dip_pass_month")
            dip_passyr = request.POST.get("ug_pacad_dip_pass_year")
            dip_pass_state = request.POST.get("ug_pacad_dip_pass_state")
            dip_medium = request.POST.get("ug_pacad_dip_medium")
            dip_regno = request.POST.get("ug_pacad_dip_reg_no")
            dip_5marks = int(request.POST.get("ug_pacad_dip_5th_marks"))
            dip_6marks = int(request.POST.get("ug_pacad_dip_6th_marks"))
            dip_tmarks = int(request.POST.get("ug_pacad_dip_total_marks"))
            dip_tpercentage = float(request.POST.get("ug_pacad_total_percentage"))

        except:
            if dip_5marks is None:
                dip_5marks = 0
            if dip_6marks is None:
                dip_6marks = 0
            if dip_tmarks is None:
                dip_tmarks = 0
            if dip_tpercentage is None:
                dip_tpercentage = 0.0

        try:
            dip_admorder = request.POST.get("dip_adm_order_no")
            dip_dcetno = request.POST.get("dip_dcet_no")
            diprank = int(request.POST.get("dip_rank"))
            dipcatclaim = request.POST.get("dip_cat_claimed")
            dipcatallot = request.POST.get("dip_cat_allotted")
            dip_allotdate = request.POST.get("dip_allot_date")
            dip_feespaid = int(request.POST.get("dip_fees_paid"))
            dip_collfeepaid = int(request.POST.get("dip_college_fees_paid"))
            dip_tfeespaid = int(request.POST.get("dip_total_fees_paid"))
            dip_cdate = request.POST.get("dip_challan_date")
            dip_cno = int(request.POST.get("dip_challan_no"))

        except:
            if diprank is None:
                diprank = 0
            if dip_feespaid is None:
                dip_feespaid = 0
            if dip_collfeepaid is None:
                dip_collfeepaid = 0
            if dip_tfeespaid is None:
                dip_tfeespaid = 0
            if dip_cno is None:
                dip_cno = 0
                
        
            if dip_allotdate == '':
                dip_allotdate = None
                
            if dip_cdate == '':
                dip_cdate = None

        btn_value = request.POST["btn_clicked"]
        if btn_value == "register":

            snap = request.POST.get("snap")
            up_snap = request.POST.get("up_snap")
            if snap:
                img = snap
            else:
                img = up_snap

            with transaction.atomic():
                CustomUser.objects.create_user(email = StudentMailID, username = StudentUID, password=dob, user_type=3)
                student =   Student_Details.objects.create(st_profile_pic=get_image_from_data_url(img), st_acad_year_id = admit_year, adm_date = admis_date, st_branch_applied_id = branch, 
                st_name=name, st_adm_applied = admis_allot, st_adm_quota_id = quota, st_dob = dob, st_medium = medium , st_gender = gender, st_locality = locality, 
                st_bld_group_id = bld_grp, st_pob = BirthPlace, st_mother_tongue = Mothertongue, st_nationality = Nationality, 
                st_religion_id = religion, st_caste = Caste, st_subcaste = SubCaste, st_category_id = ActualCategory, 
                st_mobile_no = StudentMobileNo, st_email_id = StudentMailID, st_aadhar_no=aadhar_no, st_extracurr_activity = st_eactivity, st_father_name = father_name, 
                st_mother_name = mother_name, st_father_occupation = fatherjob, st_mother_occupation = motherjob, 
                st_father_income = parent_income, st_mother_income = mother_income, st_father_mobile_no = parent_mobile_no, 
                st_mother_mobile_no = mother_mobile_no, st_father_pan = parent_pan, st_mother_pan = mother_pan, 
                st_father_email_id = parent_email, st_mother_email_id = mother_email, st_parent_address = pmtaddress, 
                st_parent_address_city = pmtaddress_city, st_parent_address_district = pmtaddress_district, 
                st_parent_address_state_id = pmtaddress_state, st_parent_address_pincode = pmtaddress_pincode, 
                st_postal_address = postaladdress, st_postal_address_city = postaladdress_city, 
                st_postal_address_district = postaladdress_district, st_postal_address_state_id = postaladdress_state, 
                st_postal_address_pincode = postaladdress_pincode, st_local_guardian_addr = st_gaddress, st_guardian_mobile_no = st_gmobno, 
                st_health_issues = st_healthissues, st_guardian_email = st_gemail, st_total_fees = TotalFeePaid, st_rt_no = RtChallanNo, 
                st_adm_date = RtChallanDate, created_by = request.user.username, created_time = datetime.datetime.now(),last_edited_by = request.user.username,last_edited_time = datetime.datetime.now(), st_uid = StudentUID)

                pacad_dip  = Previous_dip_Academic_Details.objects.create(ug_pacad_dip_board = dip_board, ug_pacad_dip_schoolname = dip_school_name, 
                ug_pacad_dip_pass_month = dip_month, ug_pacad_dip_pass_year = dip_passyr, ug_pacad_dip_pass_state_id = dip_pass_state, ug_pacad_dip_medium = dip_medium,
                ug_pacad_dip_reg_no = dip_regno, ug_pacad_dip_5th_marks = dip_5marks, ug_pacad_dip_6th_marks = dip_6marks, ug_pacad_dip_total_marks = dip_tmarks, ug_pacad_total_percentage = dip_tpercentage, dip_uid = student)

                pacad_10th  = Previous_10th_Academic_Details.objects.create(ug_pacad_10th_board = x_board, ug_pacad_10th_schoolname = x_schoolname, ug_pacad_10th_pass_month_id = x_pass_month, ug_pacad_10th_pass_year = x_pass_year,
                ug_pacad_10th_pass_state_id= x_state , ug_pacad_10th_medium = x_medium, ug_pacad_10th_reg_no = x_regno, ug_pacad_10th_total_marks_cgpa = x_marks,
                ug_pacad_10th_percentage_cgpa = x_percentage, sslc_uid = student)

                pacad_12th = Previous_12th_Academic_Details.objects.create(ug_pacad_12th_board = xii_board, ug_pacad_12th_schoolname = xii_school_name,
                ug_pacad_12th_pass_month_id = xii_month, ug_pacad_12th_pass_year = xii_passyr, ug_pacad_12th_pass_state_id = xii_pass_state, ug_pacad_12th_medium = xii_medium, 
                ug_pacad_12th_reg_no = xii_regno, ug_pacad_12th_total_marks = xii_marks, ug_pacad_12th_percentage = xii_percentage, 
                ug_pacad_12th_physics_marks = xii_pmarks, ug_pacad_12th_chemistry_marks = xii_cmarks, ug_pacad_12th_maths_marks = xii_mmarks,
                ug_pacad_12th_bio_cs_marks = xii_biocsmarks, ug_pacad_12th_pcm_total_marks = xii_pcmmakrs, ug_pacad_12th_pcm_percentage = xii_pcmpercentage,puc_uid = student)
                

                mgmt_admission_ug = MGMT_Admission_Details_UG.objects.create(mgmt_rank = MGMTRank, mgmt_exam = mg_ug,
                mgmt_college_fees_paid = MGMTCollegeFeedPaid , mgmt_challan_date = MGMTChallandate , mgmt_challan_no = MGMTChallanNo, mgmt_uid = student)

                dip_admission_ug = Lateralentry_Admission_Details_UG.objects.create(dip_adm_order_no = dip_admorder, dip_dcet_no = dip_dcetno,
                dip_rank = diprank, dip_cat_claimed = dipcatclaim, dip_cat_allotted = dipcatallot,
                dip_allot_date = dip_allotdate, dip_fees_paid = dip_feespaid, dip_college_fees_paid = dip_collfeepaid,
                dip_total_fees_paid = dip_tfeespaid, dip_challan_date = dip_cdate, dip_challan_no = dip_cno, dip_uid = student)

                doc_details = Document_Details.objects.create(alt_order_copy = AllotmentOrdCopy, st_10th_marks_card  = x_MarksCardCopy, st_12th_marks_card = xii_MarksCardCopy,
                st_study_cerfiticate = StudyCertificate, st_income_certificate =  IncomeCertificate, st_dip_marks_card = dip_MarksCardCopy, st_degree_certificate = deg_certCopy,
                st_tulu_certificate = LinguisticCertificate, st_eligibility_certificate = Eligcertificate, 
                st_migration_certificate = Migcertificate, st_transfer_certificate = TransferCertificate,
                st_aadhar_card = AadharCard, st_pan_card = PanCard, doc_uid = student) 
  
            
            messages.success(request, "Student Admitted Successfully with UID" + StudentUID)
            context={"st_id": student.st_id, "st_uid": student.st_uid}
            return render(request,"add_lateral.html",context=context)



        elif btn_value == "update":
            dirty = 0
            st_id = request.POST.get('st_id')
            student = Student_Details.objects.get(st_id = st_id)
            snap = request.POST.get("snap")
            up_snap = request.POST.get("up_snap")
            data_pic = student.st_profile_pic
            print(data_pic)
            user = CustomUser.objects.update_user(email = StudentMailID, username = student.st_uid, password=dob)
            if snap:
                student.st_profile_pic = get_image_from_data_url(snap)
            elif up_snap:
                student.st_profile_pic = get_image_from_data_url(up_snap)
            else:
                student.st_profile_pic = data_pic
            
            student.st_name = name
            student.st_acad_year_id = admit_year
            student.st_branch_applied = dept
            student.st_adm_quota_id = quota
            student.st_dob = dob
            student.st_medium = medium 
            student.st_gender = gender
            student.st_locality = locality
            student.st_bld_group_id = bld_grp
            student.adm_date = admis_date
            student.st_adm_applied = admis_allot
            student.st_pob  = BirthPlace
            student.st_mother_tongue = Mothertongue
            student.st_nationality = Nationality
            student.st_religion_id = religion
            student.st_caste = Caste
            student.st_subcaste = SubCaste
            student.st_category_id = ActualCategory
            student.st_mobile_no = StudentMobileNo
            student.st_email_id = StudentMailID
            student.st_aadhar_no = aadhar_no
            student.st_extracurr_activity = st_eactivity
            student.st_father_name = father_name
            student.st_mother_name = mother_name
            student.st_father_occupation = fatherjob
            student.st_mother_occupation = motherjob
            student.st_father_income = parent_income
            student.st_mother_income = mother_income
            student.st_father_mobile_no = parent_mobile_no
            student.st_mother_mobile_no = mother_mobile_no
            student.st_father_pan = parent_pan
            student.st_mother_pan = mother_pan
            student.st_father_email_id = parent_email
            student.st_mother_email_id = mother_email
            student.st_parent_address = pmtaddress
            student.st_parent_address_city = pmtaddress_city
            student.st_parent_address_district = pmtaddress_district
            student.st_parent_address_state_id = pmtaddress_state
            student.st_parent_address_pincode = pmtaddress_pincode
            student.st_postal_address = postaladdress
            student.st_postal_address_city = postaladdress_city
            student.st_postal_address_district = postaladdress_district
            student.st_postal_address_state_id = postaladdress_state
            student.st_postal_address_pincode = postaladdress_pincode
            student.st_local_guardian_addr = st_gaddress
            student.st_guardian_mobile_no = st_gmobno
            student.st_health_issues = st_healthissues
            student.st_guardian_email = st_gemail
            student.st_total_fees = TotalFeePaid
            student.st_rt_no = RtChallanNo
            student.st_adm_date = RtChallanDate
            student.last_edited_by = request.user.username
            student.last_edited_time = datetime.datetime.now()
            student.save()
        

            ug_uid = request.POST.get('st_id')
            pacad_10th = Previous_10th_Academic_Details.objects.get(sslc_uid_id = ug_uid)
            pacad_10th.ug_pacad_10th_board = x_board
            pacad_10th.ug_pacad_10th_schoolname = x_schoolname
            pacad_10th.ug_pacad_10th_pass_month_id = x_pass_month
            pacad_10th.ug_pacad_10th_pass_year = x_pass_year
            pacad_10th.ug_pacad_10th_pass_state_id = x_state
            pacad_10th.ug_pacad_10th_medium = x_medium
            pacad_10th.ug_pacad_10th_reg_no = x_regno
            pacad_10th.ug_pacad_10th_total_marks_cgpa = x_marks
            pacad_10th.ug_pacad_10th_percentage_cgpa = x_percentage
            pacad_10th.save()

            pacad_12th = Previous_12th_Academic_Details.objects.get(puc_uid = ug_uid)
            pacad_12th.ug_pacad_12th_board = xii_board
            pacad_12th.ug_pacad_12th_schoolname = xii_school_name
            pacad_12th.ug_pacad_12th_pass_month_id = xii_month
            pacad_12th.ug_pacad_12th_pass_year = xii_passyr
            pacad_12th.ug_pacad_12th_pass_state_id = xii_pass_state
            pacad_12th.ug_pacad_12th_medium = xii_medium
            pacad_12th.ug_pacad_12th_reg_no = xii_regno
            pacad_12th.ug_pacad_12th_total_marks = xii_marks
            pacad_12th.ug_pacad_12th_percentage = xii_percentage
            pacad_12th.ug_pacad_12th_physics_marks = xii_pmarks
            pacad_12th.ug_pacad_12th_chemistry_marks = xii_cmarks
            pacad_12th.ug_pacad_12th_maths_marks = xii_mmarks
            pacad_12th.ug_pacad_12th_bio_cs_marks = xii_biocsmarks
            pacad_12th.ug_pacad_12th_pcm_total_marks = xii_pcmmakrs
            pacad_12th.ug_pacad_12th_pcm_percentage = xii_pcmpercentage
            pacad_12th.save()

            pacad_dip = Previous_dip_Academic_Details.objects.get(dip_uid_id = ug_uid)          
            pacad_dip.ug_pacad_dip_board = dip_board
            pacad_dip.ug_pacad_dip_schoolname = dip_school_name
            pacad_dip.ug_pacad_dip_pass_month = dip_month
            pacad_dip.ug_pacad_dip_pass_year = dip_passyr
            pacad_dip.ug_pacad_dip_pass_state_id = dip_pass_state
            print("-----------------")
            print(dip_pass_state)

            pacad_dip.ug_pacad_dip_medium = dip_medium
            pacad_dip.ug_pacad_dip_reg_no = dip_regno
            pacad_dip.ug_pacad_dip_5th_marks = dip_5marks
            pacad_dip.ug_pacad_dip_6th_marks = dip_6marks
            pacad_dip.ug_pacad_dip_total_marks = dip_tmarks
            pacad_dip.ug_pacad_total_percentage = dip_tpercentage
            pacad_dip.save()

    
            try:              
                mgmt_uid = request.POST.get('st_id')
                mgmt_admission_ug = MGMT_Admission_Details_UG.objects.get(mgmt_uid = mgmt_uid)
                mgmt_admission_ug.mgmt_rank = MGMTRank 
                mgmt_admission_ug.mgmt_exam = mg_ug
                mgmt_admission_ug.mgmt_college_fees_paid = MGMTCollegeFeedPaid
                mgmt_admission_ug.mgmt_challan_date = MGMTChallandate
                mgmt_admission_ug.mgmt_challan_no = MGMTChallanNo
                mgmt_admission_ug.save()
            except:
                    pass

            try: 
                doc_uid = request.POST.get('st_id')
                doc_details = Document_Details.objects.get(doc_uid = doc_uid)
                doc_details.alt_order_copy = AllotmentOrdCopy
                doc_details.st_10th_marks_card = x_MarksCardCopy
                doc_details.st_12th_marks_card = StudyCertificate
                doc_details.st_income_certificate = IncomeCertificate
                doc_details.st_dip_marks_card = dip_MarksCardCopy
                doc_details.st_degree_certificate = deg_certCopy
                doc_details.st_tulu_certificate = LinguisticCertificate
                doc_details.st_eligibility_certificate = Eligcertificate
                doc_details.st_migration_certificate = Migcertificate
                doc_details.st_transfer_certificate = TransferCertificate
                doc_details.st_aadhar_card = AadharCard
                doc_details.st_pan_card = PanCard
                doc_details.save()
            except:
                    pass           
            try: 
                dip_uid = request.POST.get('st_id')
                dip_admission_ug = Lateralentry_Admission_Details_UG.objects.get(dip_uid = dip_uid)
                dip_admission_ug.dip_adm_order_no = dip_admorder
                dip_admission_ug.dip_dcet_no = dip_dcetno
                dip_admission_ug.dip_rank = diprank
                dip_admission_ug.dip_cat_claimed = dipcatclaim
                dip_admission_ug.dip_cat_allotted = dipcatallot
                dip_admission_ug.dip_allot_date = dip_allotdate
                dip_admission_ug.dip_fees_paid = dip_feespaid
                dip_admission_ug.dip_challan_date = dip_cdate
                dip_admission_ug.dip_challan_no = dip_cno
                dip_admission_ug.save()
            except:
                    pass

            with transaction.atomic():
                    if student.is_dirty(check_relationship=True):
                        dirty = 1
                        dirty_fields = student.get_dirty_fields(check_relationship=True).keys()
                        student.save(update_fields=dirty_fields)

                    if pacad_10th.is_dirty(check_relationship=True):
                        dirty = 1
                        dirty_fields = pacad_10th.get_dirty_fields(check_relationship=True).keys()
                        pacad_10th.save(update_fields=dirty_fields)

                    if pacad_12th.is_dirty(check_relationship=True):
                        dirty = 1
                        dirty_fields = pacad_12th.get_dirty_fields(check_relationship=True).keys()
                        pacad_12th.save(update_fields=dirty_fields)

                    if pacad_dip.is_dirty(check_relationship=True):
                        dirty = 1
                        dirty_fields = pacad_dip.get_dirty_fields(check_relationship=True).keys()
                        pacad_dip.save(update_fields=dirty_fields)

                    if mgmt_admission_ug.is_dirty(check_relationship=True):
                        dirty = 1
                        dirty_fields = mgmt_admission_ug.get_dirty_fields(check_relationship=True).keys()
                        mgmt_admission_ug.save(update_fields=dirty_fields)

                    if doc_details.is_dirty(check_relationship=True):
                        dirty = 1
                        dirty_fields = doc_details.get_dirty_fields(check_relationship=True).keys()
                        doc_details.save(update_fields=dirty_fields)
            

            if dirty : 
                messages.success(request, "Student Updated Successfully with UID" + student.st_uid)
            else:
                messages.success(request, "No changes were made with UID" + student.st_uid)
        
        context={"st_id": student.st_id, "st_uid": student.st_uid}
        return render(request,"add_lateral.html",context=context)

def admitClgtrstudent(request):
    if request.method!="POST":
        return HttpResponseRedirect('AddTransferOfCollege')
    else:
        parent_income = None; mother_income = None; admit_year = None; admis_date = None; admis_allot = None; name = None; course = None; branch = None
        dept = None; quota = None; dob = None; gender = None; locality = None; bld_grp = None; BirthPlace = None; Mothertongue = None; Nationality = None
        rlg = None; Caste = None; SubCaste = None; ActualCategory = None; StudentMobileNo = None; StudentMailID = None; aadhar_no = None;
        st_eactivity = None; father_name = None; mother_name = None; fatherjob = None; motherjob = None; parent_mobile_no = None; mother_mobile_no = None;
        parent_pan = None; mother_pan = None; parent_email = None; mother_email =None; pmtaddress = None; pmtaddress_city = None;
        pmtaddress_district = None; pmtaddress_state = None; pmtaddress_pincode = None; postaladdress = None; postaladdress_city = None; 
        postaladdress_district = None; postaladdress_state = None; postaladdress_pincode = None; st_gaddress = None; st_gmobno = None; st_healthissues = None; 
        st_gemail = None; x_board = None; x_schoolname = None; x_pass_month = None; x_pass_year = None; x_state = None; x_medium = None; x_regno = None; x_marks = None
        x_percentage = None; xii_board = None; xii_school_name = None; xii_month =None; xii_passyr = None; xii_pass_state = None; xiipassState = None; xii_medium = None; 
        xii_regno = None; xii_marks = None; xii_percentage = None; xii_pmarks = None; xii_cmarks = None; xii_mmarks = None; xii_biocsmarks = None;
        xii_pcmmakrs = None; xii_pcmpercentage = None; TotalFeePaid = None; RtChallanNo = None; RtChallanDate = None;  

        exam_adm_ord_no = None; clg_trns_exam_type = None; exam_rgd_no = None; dip_5marks = None; dip_6marks = None; dip_tmarks = None; dip_tpercentage = None; 
        diprank = None; dip_feespaid = None; dip_collfeepaid = None; dip_tfeespaid = None; dip_cno = None; dip_allotdate = None; dip_cdate = None; dipcatclaim = None;
        dipcatallot = None; dip_pass_state = None; dip_medium = None; dip_regno = None; prv_clgtrns_details = None;
        
        exam_rank = None; exam_cat_claimed = None; exam_cat_allot = None; total_fee_paid = None; exam_challan_date = None
        fee_paid_to_college = None; exam_fee_paid = None; exam_allot_date = None; dip_challan_no = None


        MGMTRank = None; MGMTcet = None;MGMTcomedk = None; MGMTCollegeFeedPaid = None; MGMTChallandate = None; MGMTChallanNo = None;

        AllotmentOrdCopy = None; x_MarksCardCopy = None; xii_MarksCardCopy = None; dip_MarksCardCopy = None; deg_certCopy = None; StudyCertificate = None;
        IncomeCertificate = None; LinguisticCertificate = None; Eligcertificate = None; Migcertificate = None; TransferCertificate = None; AadharCard = None;
        PanCard = None; take_photo = None; StudentID = None; StudentUID = None; mg_ug=0; mg_pg=0; st_year_of_adm = None; Yr_of_admsn = None
        
        dip_admission_ug = None; mgmt_admission_ug = None;comedk_clgtrns = None;cet_clgtrns = None;dippassState = None;
        
        bld_grp = None;rlgn = None; bldgrp = None;

        try:   
            # Student details (add_student.html)
            take_photo = request.POST.get("take-photo")
            # # Generating Student UID code
            name = request.POST.get("st_name") 
            admit_year_id = request.POST.get("st_acad_year")
            admit_year = AcademicYear.objects.get(id=admit_year_id).acayear
            branch = request.POST.get("st_branch_applied")
            # # Generating Student UID code
            admis_allot = request.POST.get("st_adm_applied")
            Slice_year = admit_year[2:4]
            if admis_allot == "mtech":
                course = 'MT'
            elif admis_allot == "mba":
                course = 'MB'
            else:
                course = request.POST.get("st_course")

            with transaction.atomic():
                StudentSet = Student_Details.objects.select_for_update().filter(st_uid__contains=Slice_year + course).order_by('-st_id')[0]
            
            st_uid_sl_no = int(StudentSet.st_uid[4:])+1
                #st_uid_sl_no must be converted to string type else it cannot be concatenated
            if(st_uid_sl_no < 10):
                st_uid = Slice_year+course+'000'+str(st_uid_sl_no)
            elif(st_uid_sl_no > 9 and st_uid_sl_no <100):
                st_uid = Slice_year+course+'00'+str(st_uid_sl_no)
            elif(st_uid_sl_no > 99 and st_uid_sl_no <1000):
                st_uid = Slice_year+course+'0'+str(st_uid_sl_no)
            elif(st_uid_sl_no > 999 and st_uid_sl_no <10000):
                    st_uid = Slice_year+course+str(st_uid_sl_no)
            StudentUID = st_uid   
            
        except IndexError:
            st_uid = Slice_year+course+'0001'
            StudentUID = st_uid

        try:
            TotalFeePaid = int(request.POST.get("st_total_fees"))
            RtChallanNo = int(request.POST.get("st_rt_no"))
            admis_date = request.POST.get("adm_date")
            RtChallanDate = request.POST.get("st_adm_date")
            postaladdress = request.POST.get("st_postal_address")
            postaladdress_city = request.POST.get("st_postal_address_city")
            postaladdress_district= request.POST.get("st_postal_address_district")
            postaladdress_pincode = request.POST.get("st_postal_address_pincode")
            pmtaddress_pincode = request.POST.get("st_parent_address_pincode") 
            pmtaddress_district= request.POST.get("st_parent_address_district")
            pmtaddress_city = request.POST.get("st_parent_address_city")
            parent_mobile_no = request.POST.get("st_father_mobile_no")
            pmtaddress = request.POST.get("st_parent_address") 
            
            quota = int(request.POST.get("st_adm_quota"))
            Yr_of_admsn = request.POST.get("st_year_of_adm")
            dob = request.POST.get("st_dob")
            gender = int(request.POST.get("st_gender"))
            locality = int(request.POST.get("st_locality"))
            Nationality = int(request.POST.get("st_nationality"))
            rlgn = int(request.POST.get("st_religion"))
            Caste = request.POST.get("st_caste")
            ActualCategory = int(request.POST.get("st_category"))
            StudentMobileNo = request.POST.get("st_mobile_no")         
            father_name = request.POST.get("st_father_name")
            mother_name = request.POST.get("st_mother_name")
            fatherjob = request.POST.get("st_father_occupation")
            motherjob = request.POST.get("st_mother_occupation")
            parent_income = request.POST.get("st_father_income")
            mother_income = int(request.POST.get("st_mother_income"))
            mother_mobile_no = request.POST.get("st_mother_mobile_no")
            parent_pan = request.POST.get("st_father_pan")
            mother_pan = request.POST.get("st_mother_pan")
            parent_email = request.POST.get("st_father_email_id")
            mother_email = request.POST.get("st_mother_email_id")
            

            
           
            
            st_gaddress = request.POST.get("st_local_guardian_addr")
            st_gmobno = request.POST.get("st_guardian_mobile_no")
            st_healthissues = request.POST.get("st_health_issues")
            st_gemail = request.POST.get("st_guardian_email")

            # FOR OFFICE USE ONLY
            aadhar_no = int(request.POST.get("st_aadhar_no"))

        except: 
            if aadhar_no is None:
                aadhar_no = None
            if parent_income is None:
                parent_income  = None
            if mother_income is None:
                mother_income  = None
            if TotalFeePaid is None:
                TotalFeePaid = None
            if RtChallanNo is None:
                RtChallanNo = None
            if mother_income is '':
                mother_income = None
            if parent_email is '':
                parent_email is 0 

        try:
            StudentMailID = request.POST.get("st_email_id")
        except Exception as e:
            print(e)
            if StudentMailID is None:
                StudentMailID = None
        
        
        try:
            SubCaste = request.POST.get("st_subcaste")
        except Exception as e:
            print(e)
            if SubCaste is None:
                SubCaste = None
        try:
            Mothertongue = request.POST.get("st_mother_tongue")
        except Exception as e:
            print(e)
            if Mothertongue is None:
                Mothertongue = None
        
        try:
            BirthPlace = request.POST.get("st_pob")
        except Exception as e:
            print(e)
            if BirthPlace is None:
                BirthPlace = None
        
        try:
            bldgrp = int(request.POST.get("st_bld_group"))
            bld_grp = BloodGroup.objects.get(id = bldgrp)
        except Exception as e:
            print(e)
            if bldgrp is None:
                bldgrp = 0


        try:    
            pmtaddress_state = int(request.POST.get("st_parent_address_state"))
        except Exception as e:
            print(e)
            if pmtaddress_state is None:
                pmtaddress_state = None
        
        try:
            postaddr_state = int(request.POST.get("st_postal_address_state"))
            postaladdress_state = States.objects.get(id = postaddr_state)
        except Exception as e:
            print(e)
            if postaladdress_state is None:
                postaladdress_state = None
        
        try:
            pg_xii_board = request.POST.get("pg_pacad_12th_board")
        except:
            if pg_xii_board is None:
                pg_xii_board = None

        try:
            st_eactivity = request.POST.get("st_extracurr_activity")
        except Exception as e:
            print(e)
            if st_eactivity is None:
                st_eactivity = None
        
        try:        
            # Previous Academic Details UG
            x_board = request.POST.get("ug_pacad_10th_board")
            x_schoolname = request.POST.get("ug_pacad_10th_schoolname")
            x_pass_month = request.POST.get("ug_pacad_10th_pass_month")
            x_pass_year = request.POST.get("ug_pacad_10th_pass_year")
            xStates = int(request.POST.get("ug_pacad_10th_pass_state"))
            x_medium = request.POST.get("ug_pacad_10th_medium")
            x_regno = request.POST.get("ug_pacad_10th_reg_no")
            x_marks = float(request.POST.get("ug_pacad_10th_total_marks_cgpa"))
            x_percentage = float(request.POST.get("ug_pacad_10th_percentage_cgpa"))
            xii_board = request.POST.get("ug_pacad_12th_board")
            xii_school_name = request.POST.get("ug_pacad_12th_schoolname")
            xii_month = request.POST.get("ug_pacad_12th_pass_month")
            xii_passyr = request.POST.get("ug_pacad_12th_pass_year")
            xiipassState = int(request.POST.get("ug_pacad_12th_pass_state"))
            xii_pass_state = States.objects.get(id = xiipassState)
            xii_medium = request.POST.get("ug_pacad_12th_medium")
            xii_regno = request.POST.get("ug_pacad_12th_reg_no")
            xii_marks = int(request.POST.get("ug_pacad_12th_total_marks"))
            xii_percentage = float(request.POST.get("ug_pacad_12th_percentage"))
            xii_pmarks = int(request.POST.get("ug_pacad_12th_physics_marks"))
            xii_cmarks = int(request.POST.get("ug_pacad_12th_chemistry_marks"))
            xii_mmarks = int(request.POST.get("ug_pacad_12th_maths_marks"))
            xii_biocsmarks = int(request.POST.get("ug_pacad_12th_bio_cs_marks"))
            xii_pcmmakrs = int(request.POST.get("ug_pacad_12th_pcm_total_marks"))
            xii_pcmpercentage = float(request.POST.get("ug_pacad_12th_pcm_percentage"))

        except:
            if x_board is None:
                x_board = None
            if x_marks is None:
                x_marks = None
            if x_percentage is None:
                x_percentage = None
            if xii_marks is None:
                xii_marks = None
            if xii_percentage is None:
                xii_percentage = None
            if xii_pmarks is None:
                xii_pmarks = None
            if xii_cmarks is None:
                xii_cmarks = None
            if xii_mmarks is None:
                xii_mmarks = None
            if xii_pcmmakrs is None:
                xii_pcmmakrs = None
            if xii_pcmpercentage is None:
                xii_pcmpercentage = None
            if xii_biocsmarks is None:
                xii_biocsmarks = None
            if xiipassState is None:
                xiipassState = None
            if xii_pass_state is None:
                xii_pass_state = None
            if xii_passyr is '':
                xii_passyr = None

        try:
            # Details for students admitted under MANAGEMENT quota
            
            MGMTRank = int(request.POST.get("exam_rank"))

            # MGMTcet = request.POST.getlist("mgmt_exam[]")

            # for m in MGMTcet:
            #     mg_ug=int(mg_ug)+int(m)

            MGMTCollegeFeedPaid = int(request.POST.get("mgmt_college_fees_paid"))
            MGMTChallandate = request.POST.get("mgmt_challan_date")
            MGMTChallanNo = int(request.POST.get("mgmt_challan_no"))

        except:
            if MGMTRank is None:
                MGMTRank = None
            if MGMTCollegeFeedPaid is None:
                MGMTCollegeFeedPaid = None
            if MGMTChallanNo is None:
                MGMTChallanNo = None
        
        exam_order_copy = None

         #College transfer exam type selection
        try:
            clg_trns_exam_type = int(request.POST.get("clg_trns_exam_type"))
        except:
            if clg_trns_exam_type is None:
                clg_trns_exam_type = 0

        try:
            # Documents submitted by the applicant
            exam_order_copy = int(request.POST.get("exam_order_copy"))
            x_MarksCardCopy = request.POST.get("st_10th_marks_card")
            xii_MarksCardCopy = request.POST.get("st_12th_marks_card")
            dip_MarksCardCopy = request.POST.get("st_dip_marks_card")
            AllotmentOrdCopy = request.POST.get("exam_order_copy")
            # deg_certCopy = request.POST.get("st_degree_certificate")
            StudyCertificate = request.POST.get("st_study_cerfiticate")
            IncomeCertificate = request.POST.get("st_income_certificate")
            LinguisticCertificate = request.POST.get("st_tulu_certificate")
            Eligcertificate = request.POST.get("st_eligibility_certificate")
            Migcertificate = request.POST.get("st_migration_certificate")
            TransferCertificate = request.POST.get("st_transfer_certificate")
            AadharCard = request.POST.get("st_aadhar_card")
            PanCard = request.POST.get("st_pan_card")
        except:
            if AllotmentOrdCopy is None:
                AllotmentOrdCopy = None
            if exam_order_copy is None:
                exam_order_copy = None

        try:
            #Diploma Details (add_lateral.html)
            dip_board = request.POST.get("ug_pacad_dip_board")
            dip_school_name = request.POST.get("ug_pacad_dip_schoolname")
            dip_month = request.POST.get("ug_pacad_dip_pass_month")
            dip_passyr = request.POST.get("ug_pacad_dip_pass_year")
            dippassState= int(request.POST.get("ug_pacad_dip_pass_state"))
            #dip_pass_state = States.objects.get(id = dippassState)
            dip_medium = request.POST.get("ug_pacad_dip_medium")
            dip_regno = request.POST.get("ug_pacad_dip_reg_no")
            dip_5marks = int(request.POST.get("ug_pacad_dip_5th_marks"))
            dip_6marks = int(request.POST.get("ug_pacad_dip_6th_marks"))
            dip_tmarks = int(request.POST.get("ug_pacad_dip_total_marks"))
            dip_tpercentage = float(request.POST.get("ug_pacad_total_percentage"))

        except:
            if dip_5marks is None:
                dip_5marks = None
            if dip_6marks is None:
                dip_6marks = None
            if dip_tmarks is None:
                dip_tmarks = None
            if dip_tpercentage is None:
                dip_tpercentage = None

        #Gathering Previous College Academic Details 
        ug_prv_clgtr_name = None
        ug_prv_clgtr_name = request.POST.get("ug_prv_clgtr_name")
        ug_prv_clgtr_crd = None
        ug_prv_clgtr_crd_balance = None
        ug_prv_clgtr_cur_cgpa = None
        try:
            ug_prv_clgtr_crd = int(request.POST.get("ug_prv_clgtr_crd"))
            ug_prv_clgtr_crd_balance = int(request.POST.get("ug_prv_clgtr_crd_balance"))
            ug_prv_clgtr_cur_cgpa = float(request.POST.get("ug_prv_clgtr_cur_cgpa"))

        except:
            if ug_prv_clgtr_crd is None:
                ug_prv_clgtr_crd = None
            if ug_prv_clgtr_crd_balance is None:
                ug_prv_clgtr_crd_balance = None   
            if ug_prv_clgtr_cur_cgpa is None:
                ug_prv_clgtr_cur_cgpa = None
        try:
            dip_allotdate = request.POST.get("exam_allot_date")
            dip_cdate = request.POST.get("exam_challan_date")
            dip_admorder = request.POST.get("exam_adm_ord_no")
            dip_dcetno = request.POST.get("exam_rgd_no")
            diprank = int(request.POST.get("exam_rank"))
            dipcatclaim = request.POST.get("exam_cat_claimed")
            dipcatallot = request.POST.get("exam_cat_allot")
            dip_feespaid = int(request.POST.get("exam_fee_paid"))
            dip_collfeepaid = int(request.POST.get("fee_paid_to_college"))
            dip_tfeespaid = int(request.POST.get("total_fee_paid"))
            dip_cno = int(request.POST.get("exam_challan_no"))

        except:
            if diprank is None:
                diprank = None
            if dip_feespaid is None:
                dip_feespaid = None
            if dip_collfeepaid is None:
                dip_collfeepaid = None
            if dip_tfeespaid is None:
                dip_tfeespaid = None
            if dip_cno is None:
                dip_cno = None
            if dip_cdate == '' or dip_cdate is None:
                dip_cdate = None

        try:
            exam_adm_ord_no = request.POST.get("exam_adm_ord_no")
            print(exam_adm_ord_no)
        except:
            if exam_adm_ord_no is None:
                exam_adm_ord_no = None
        try:
            exam_rgd_no = request.POST.get("exam_rgd_no")
        except:
            if exam_rgd_no is None:
                exam_rgd_no = None
        try:
            exam_rank = int(request.POST.get("exam_rank"))
        except:
            if exam_rank is None:
                exam_rank = None
        try:
            exam_cat_claimed = request.POST.get("exam_cat_claimed")
        except:
            if exam_cat_claimed is None:
                exam_cat_claimed = None
        try:
            exam_cat_allot = request.POST.get("exam_cat_allot")
        except:
            if exam_cat_allot is None:
                exam_cat_allot = None
        try:
            exam_allot_date = date(request.POST.get("exam_allot_date"))
        except:
            if exam_allot_date is None:
                exam_allot_date = None
        try:
            exam_fee_paid = int(request.POST.get("exam_fee_paid"))
        except:
            if exam_fee_paid is None:
                exam_fee_paid = None            
        try:
            total_fee_paid = int(request.POST.get("total_fee_paid"))
        except:
            if total_fee_paid is None:
                total_fee_paid =  None
        
        try:
            exam_challan_date = date(request.POST.get("exam_challan_date"))
        except:
            if exam_challan_date is None:
                exam_challan_date = None
        try:
            dip_challan_no = request.POST.get("dip_challan_no")
        except:
            if dip_challan_no is None:
                dip_challan_no = None
        
        if dip_allotdate == '':
            dip_allotdate = None
            
        # if dip_cdate is '':
        #     dip_cdate = None

        btn_value = request.POST["btn_clicked"]
        if btn_value == "register":

            snap = request.POST.get("snap")
            up_snap = request.POST.get("up_snap")
            if snap:
                img = snap
            else:
                img = up_snap
        

            with transaction.atomic():
                CustomUser.objects.create_user(email = StudentMailID, username = StudentUID, password=dob, user_type=3)
                student =   Student_Details.objects.create(st_profile_pic=get_image_from_data_url(img), st_acad_year_id=admit_year_id, adm_date = admis_date, st_branch_applied_id = branch, 
                st_name=name, st_adm_applied = admis_allot, st_adm_quota_id = quota, st_dob = dob, st_gender = gender, st_locality = locality, 
                st_bld_group_id = bldgrp, st_pob = BirthPlace, st_mother_tongue = Mothertongue, st_nationality = Nationality, 
                st_religion_id = rlgn, st_caste = Caste, st_subcaste = SubCaste, st_category_id = ActualCategory, 
                st_mobile_no = StudentMobileNo, st_email_id = StudentMailID, st_aadhar_no=aadhar_no, st_extracurr_activity = st_eactivity, st_father_name = father_name, 
                st_mother_name = mother_name, st_father_occupation = fatherjob, st_mother_occupation = motherjob, 
                st_father_income = parent_income, st_mother_income = mother_income, st_father_mobile_no = parent_mobile_no, 
                st_mother_mobile_no = mother_mobile_no, st_father_pan = parent_pan, st_mother_pan = mother_pan, 
                st_father_email_id = parent_email, st_mother_email_id = mother_email, st_parent_address = pmtaddress, 
                st_parent_address_city = pmtaddress_city, st_parent_address_district = pmtaddress_district, 
                st_parent_address_state_id =  pmtaddress_state, st_parent_address_pincode = pmtaddress_pincode, 
                st_postal_address = postaladdress, st_postal_address_city = postaladdress_city, 
                st_postal_address_district = postaladdress_district, st_postal_address_state_id = postaddr_state , 
                st_postal_address_pincode = postaladdress_pincode, st_local_guardian_addr = st_gaddress, st_guardian_mobile_no = st_gmobno, 
                st_health_issues = st_healthissues, st_guardian_email = st_gemail, st_total_fees = TotalFeePaid, st_rt_no = RtChallanNo, 
                st_adm_date = RtChallanDate, created_by = request.user.username, created_time = datetime.datetime.now(),last_edited_by = request.user.username,last_edited_time = datetime.datetime.now() ,st_uid = StudentUID)

                pacad_dip  = Previous_dip_Academic_Details.objects.create(ug_pacad_dip_board = dip_board, ug_pacad_dip_schoolname = dip_school_name, 
                ug_pacad_dip_pass_month = dip_month, ug_pacad_dip_pass_year = dip_passyr, ug_pacad_dip_pass_state_id =  dippassState, ug_pacad_dip_medium = dip_medium,
                ug_pacad_dip_reg_no = dip_regno, ug_pacad_dip_5th_marks = dip_5marks, ug_pacad_dip_6th_marks = dip_6marks, ug_pacad_dip_total_marks = dip_tmarks, ug_pacad_total_percentage = dip_tpercentage, dip_uid = student)

                pacad_10th  = Previous_10th_Academic_Details.objects.create(ug_pacad_10th_board = x_board, ug_pacad_10th_schoolname = x_schoolname, ug_pacad_10th_pass_month_id = x_pass_month, ug_pacad_10th_pass_year = x_pass_year,
                ug_pacad_10th_pass_state_id = xStates, ug_pacad_10th_medium = x_medium, ug_pacad_10th_reg_no = x_regno, ug_pacad_10th_total_marks_cgpa = x_marks,
                ug_pacad_10th_percentage_cgpa = x_percentage, sslc_uid = student)

                pacad_12th = Previous_12th_Academic_Details.objects.create(ug_pacad_12th_board = xii_board, ug_pacad_12th_schoolname = xii_school_name,
                ug_pacad_12th_pass_month_id = xii_month, ug_pacad_12th_pass_year = xii_passyr, ug_pacad_12th_pass_state_id = xiipassState, ug_pacad_12th_medium = xii_medium, 
                ug_pacad_12th_reg_no = xii_regno, ug_pacad_12th_total_marks = xii_marks, ug_pacad_12th_percentage = xii_percentage, 
                ug_pacad_12th_physics_marks = xii_pmarks, ug_pacad_12th_chemistry_marks = xii_cmarks, ug_pacad_12th_maths_marks = xii_mmarks,
                ug_pacad_12th_bio_cs_marks = xii_biocsmarks, ug_pacad_12th_pcm_total_marks = xii_pcmmakrs, ug_pacad_12th_pcm_percentage = xii_pcmpercentage,puc_uid = student)
                

                
                if clg_trns_exam_type == 4:
                    mgmt_admission_ug = MGMT_Admission_Details_UG.objects.create(mgmt_rank = MGMTRank, mgmt_exam = mg_ug,
                    mgmt_college_fees_paid = MGMTCollegeFeedPaid , mgmt_challan_date = MGMTChallandate , mgmt_challan_no = MGMTChallanNo, mgmt_uid = student)

                elif clg_trns_exam_type == 3:    
                    dip_admission_ug = Lateralentry_Admission_Details_UG.objects.create(dip_adm_order_no = dip_admorder, dip_dcet_no = dip_dcetno,
                    dip_rank = diprank, dip_cat_claimed = dipcatclaim, dip_cat_allotted = dipcatallot,
                    dip_allot_date = dip_allotdate, dip_fees_paid = dip_feespaid, dip_college_fees_paid = dip_collfeepaid,
                    dip_total_fees_paid = dip_tfeespaid, dip_challan_date = dip_cdate, dip_challan_no = dip_cno, dip_uid = student)

                elif clg_trns_exam_type == 2:
                    comedk_clgtrns = COMEDK_Admission_Details_UG.objects.create(comedk_sl_no = exam_adm_ord_no, comedk_tat_no = exam_rgd_no,comedk_rank = exam_rank, comedk_cat_allotted = exam_cat_allot, 
                    comedk_allot_date = dip_allotdate, comedk_fees_paid = exam_fee_paid, comedk_college_fees_paid = dip_collfeepaid, comedk_challan_date = dip_cdate, 
                    comedk_challan_no = dip_cno, comedk_uid = student)
                
                elif clg_trns_exam_type == 1:
                    cet_clgtrns = CET_Admission_Details_UG.objects.create(cet_order_no = exam_adm_ord_no, cet_rank = exam_rank, cet_cat_claimed = exam_cat_claimed, cet_cat_allotted = exam_cat_allot,
                    cet_allot_date = dip_allotdate, cet_kea_fees_paid = exam_fee_paid, cet_college_fees_paid = dip_collfeepaid, cet_total_fees_paid = total_fee_paid,
                    cet_challan_date = dip_cdate, cet_challan_no = dip_cno,cet_uid = student)

                doc_details = Document_Details.objects.create(alt_order_copy = exam_order_copy, st_10th_marks_card  = x_MarksCardCopy, st_12th_marks_card = xii_MarksCardCopy,
                st_study_cerfiticate = StudyCertificate, st_income_certificate =  IncomeCertificate, st_dip_marks_card = dip_MarksCardCopy, st_degree_certificate = deg_certCopy,
                st_tulu_certificate = LinguisticCertificate, st_eligibility_certificate = Eligcertificate, 
                st_migration_certificate = Migcertificate, st_transfer_certificate = TransferCertificate,
                st_aadhar_card = AadharCard, st_pan_card = PanCard, doc_uid = student)

                prv_clgtrns_details = Previous_Transfer_College_Details.objects.create(clgtrns_st_uid = student,clg_trns_exam_type=clg_trns_exam_type,ug_ptcd_college_name = ug_prv_clgtr_name, ug_ptcd_admitted_sem=Yr_of_admsn, 
                ug_ptcd_credits_earned=ug_prv_clgtr_crd, ug_ptcd_credits_remaining=ug_prv_clgtr_crd_balance, ug_ptcd_admitted_cgpa= ug_prv_clgtr_cur_cgpa) 
  
            
            messages.success(request, "Student Admitted Successfully with UID" + StudentUID)
            context={"st_id": student.st_id, "st_uid": student.st_uid}
            return render(request,"add_transfercollege.html",context=context)

        elif btn_value == "update":
            dirty = 0
            st_id = request.POST.get('st_id')
            student = Student_Details.objects.get(st_id = st_id)
            snap = request.POST.get("snap")
            up_snap = request.POST.get("up_snap")
            data_pic = student.st_profile_pic
            print(data_pic)
            user = CustomUser.objects.update_user(email = StudentMailID, username = student.st_uid, password=dob)
            if snap:
                student.st_profile_pic = get_image_from_data_url(snap)
            elif up_snap:
                student.st_profile_pic = get_image_from_data_url(up_snap)
            else:
                student.st_profile_pic = data_pic
            
            #Code to Populate Admission year
            st_year_of_adm = int(request.POST.get("st_year_of_adm"))
            if (st_year_of_adm == "3"):
                Yr_of_admsn = 3
            elif (st_year_of_adm == "5"):
                Yr_of_admsn = 5
            elif (st_year_of_adm == "7"):
                Yr_of_admsn = 7
            print(Yr_of_admsn)
            
            student.st_name = name
            student.st_acad_year_id = admit_year
            student.st_branch_applied_id = branch
            student.st_adm_quota_id = quota
            student.st_dob = dob
            student.st_gender = gender
            student.st_locality = locality
            student.st_bld_group_id = bld_grp
            student.adm_date = admis_date
            student.st_adm_applied = admis_allot
            student.st_pob  = BirthPlace
            student.st_mother_tongue = Mothertongue
            student.st_nationality = Nationality
            student.st_religion_id = rlgn
            student.st_caste = Caste
            student.st_subcaste = SubCaste
            student.st_category_id = ActualCategory
            student.st_mobile_no = StudentMobileNo
            student.st_email_id = StudentMailID
            student.st_aadhar_no = aadhar_no
            student.st_extracurr_activity = st_eactivity
            student.st_father_name = father_name
            student.st_mother_name = mother_name
            student.st_father_occupation = fatherjob
            student.st_mother_occupation = motherjob
            student.st_father_income = parent_income
            student.st_mother_income = mother_income
            student.st_father_mobile_no = parent_mobile_no
            student.st_mother_mobile_no = mother_mobile_no
            student.st_father_pan = parent_pan
            student.st_mother_pan = mother_pan
            student.st_father_email_id = parent_email
            student.st_mother_email_id = mother_email
            student.st_parent_address = pmtaddress
            student.st_parent_address_city = pmtaddress_city
            student.st_parent_address_district = pmtaddress_district
            student.st_parent_address_state_id = pmtaddress_state
            student.st_parent_address_pincode = pmtaddress_pincode
            student.st_postal_address = postaladdress
            student.st_postal_address_city = postaladdress_city
            student.st_postal_address_district = postaladdress_district
            student.st_postal_address_state_id = postaladdress_state
            student.st_postal_address_pincode = postaladdress_pincode
            student.st_local_guardian_addr = st_gaddress
            student.st_guardian_mobile_no = st_gmobno
            student.st_health_issues = st_healthissues
            student.st_guardian_email = st_gemail
            student.st_total_fees = TotalFeePaid
            student.st_rt_no = RtChallanNo
            student.st_adm_date = RtChallanDate
            student.last_edited_by = request.user.username
            student.last_edited_time = datetime.datetime.now()

            ug_uid = request.POST.get('st_id')
            pacad_10th = Previous_10th_Academic_Details.objects.get(sslc_uid_id = ug_uid)
            pacad_10th.ug_pacad_10th_board = x_board
            pacad_10th.ug_pacad_10th_schoolname = x_schoolname
            pacad_10th.ug_pacad_10th_pass_month_id = x_pass_month
            pacad_10th.ug_pacad_10th_pass_year = x_pass_year
            pacad_10th.ug_pacad_10th_pass_state_id = xStates
            pacad_10th.ug_pacad_10th_medium = x_medium
            pacad_10th.ug_pacad_10th_reg_no = x_regno
            pacad_10th.ug_pacad_10th_total_marks_cgpa = x_marks
            pacad_10th.ug_pacad_10th_percentage_cgpa = x_percentage

            pacad_12th = Previous_12th_Academic_Details.objects.get(puc_uid_id = ug_uid)
            pacad_12th.ug_pacad_12th_board = xii_board
            pacad_12th.ug_pacad_12th_schoolname = xii_school_name
            pacad_12th.ug_pacad_12th_pass_month_id = xii_month
            pacad_12th.ug_pacad_12th_pass_year = xii_passyr
            pacad_12th.ug_pacad_12th_pass_state_id = xiipassState
            pacad_12th.ug_pacad_12th_medium = xii_medium
            pacad_12th.ug_pacad_12th_reg_no = xii_regno
            pacad_12th.ug_pacad_12th_total_marks = xii_marks
            pacad_12th.ug_pacad_12th_percentage = xii_percentage
            pacad_12th.ug_pacad_12th_physics_marks = xii_pmarks
            pacad_12th.ug_pacad_12th_chemistry_marks = xii_cmarks
            pacad_12th.ug_pacad_12th_maths_marks = xii_mmarks
            pacad_12th.ug_pacad_12th_bio_cs_marks = xii_biocsmarks
            pacad_12th.ug_pacad_12th_pcm_total_marks = xii_pcmmakrs
            pacad_12th.ug_pacad_12th_pcm_percentage = xii_pcmpercentage

            pacad_dip = Previous_dip_Academic_Details.objects.get(dip_uid_id = ug_uid)          
            pacad_dip.ug_pacad_dip_board = dip_board
            pacad_dip.ug_pacad_dip_schoolname = dip_school_name
            pacad_dip.ug_pacad_dip_pass_month = dip_month
            pacad_dip.ug_pacad_dip_pass_year = dip_passyr
            pacad_dip.ug_pacad_dip_pass_state_id =  dippassState
            pacad_dip.ug_pacad_dip_medium = dip_medium
            pacad_dip.ug_pacad_dip_reg_no = dip_regno
            pacad_dip.ug_pacad_dip_5th_marks = dip_5marks
            pacad_dip.ug_pacad_dip_6th_marks = dip_6marks
            pacad_dip.ug_pacad_dip_total_marks = dip_tmarks
            pacad_dip.ug_pacad_total_percentage = dip_tpercentage
    
            try:              
                mgmt_uid = request.POST.get('st_id')
                mgmt_admission_ug = MGMT_Admission_Details_UG.objects.get(mgmt_uid = mgmt_uid)
                mgmt_admission_ug.mgmt_rank = MGMTRank 
                mgmt_admission_ug.mgmt_exam = mg_ug
                mgmt_admission_ug.mgmt_college_fees_paid = MGMTCollegeFeedPaid
                mgmt_admission_ug.mgmt_challan_date = MGMTChallandate
                mgmt_admission_ug.mgmt_challan_no = MGMTChallanNo
            except:
                pass
            
            try: 
                dip_uid = request.POST.get('st_id')
                dip_admission_ug = Lateralentry_Admission_Details_UG.objects.get(dip_uid = dip_uid)
                dip_admission_ug.dip_adm_order_no = dip_admorder
                dip_admission_ug.dip_dcet_no = dip_dcetno
                dip_admission_ug.dip_rank = diprank
                dip_admission_ug.dip_cat_claimed = dipcatclaim
                dip_admission_ug.dip_cat_allotted = dipcatallot
                dip_admission_ug.dip_allot_date = dip_allotdate
                dip_admission_ug.dip_fees_paid = dip_feespaid
                dip_admission_ug.dip_challan_date = dip_cdate
                dip_admission_ug.dip_challan_no = dip_cno
            except:
                pass

            try:
                cet_clgtrns = CET_Admission_Details_UG.objects.get(cet_uid_id = student.st_id)
                cet_clgtrns.cet_order_no = exam_adm_ord_no 
                cet_clgtrns.cet_rank = exam_rank 
                cet_clgtrns.cet_cat_claimed = exam_cat_claimed 
                cet_clgtrns.cet_cat_allotted = exam_cat_allot
                cet_clgtrns.cet_allot_date = dip_allotdate 
                cet_clgtrns.cet_kea_fees_paid = exam_fee_paid 
                cet_clgtrns.cet_college_fees_paid = dip_collfeepaid
                cet_clgtrns.cet_total_fees_paid = total_fee_paid
                cet_clgtrns.cet_challan_date = dip_cdate 
                cet_clgtrns.cet_challan_no = dip_cno
            except:
                pass
            
            try:
                comedk_clgtrns = COMEDK_Admission_Details_UG.objects.get(comedk_uid_id = student.st_id)
                comedk_clgtrns.comedk_sl_no = exam_adm_ord_no 
                comedk_clgtrns.comedk_tat_no = exam_rgd_no
                comedk_clgtrns.comedk_rank = exam_rank
                comedk_clgtrns.comedk_cat_allotted = exam_cat_allot 
                comedk_clgtrns.comedk_allot_date = dip_allotdate
                comedk_clgtrns.comedk_fees_paid = exam_fee_paid
                comedk_clgtrns.comedk_college_fees_paid = dip_collfeepaid 
                comedk_clgtrns.comedk_challan_date = dip_cdate 
                comedk_clgtrns.comedk_challan_no = dip_cno
                comedk_clgtrns.save()
            except:
                pass

            try:
                clgtrns_uid = request.POST.get('st_id')
                prv_clgtrns_details = Previous_Transfer_College_Details.objects.get(clgtrns_st_uid = clgtrns_uid)
                prv_clgtrns_details.ug_ptcd_college_name = ug_prv_clgtr_name
                prv_clgtrns_details.ug_ptcd_admitted_sem = Yr_of_admsn
                prv_clgtrns_details.ug_ptcd_credits_earned = ug_prv_clgtr_crd
                prv_clgtrns_details.ug_ptcd_credits_remaining = ug_prv_clgtr_crd_balance
                prv_clgtrns_details.ug_ptcd_admitted_cgpa = ug_prv_clgtr_cur_cgpa

            except:
                pass

            try: 
                doc_uid = request.POST.get('st_id')
                doc_details = Document_Details.objects.get(doc_uid = doc_uid)
                doc_details.alt_order_copy = exam_order_copy
                doc_details.st_10th_marks_card = x_MarksCardCopy
                doc_details.st_12th_marks_card = StudyCertificate
                doc_details.st_income_certificate = IncomeCertificate
                doc_details.st_dip_marks_card = dip_MarksCardCopy
                doc_details.st_degree_certificate = deg_certCopy
                doc_details.st_tulu_certificate = LinguisticCertificate
                doc_details.st_eligibility_certificate = Eligcertificate
                doc_details.st_migration_certificate = Migcertificate
                doc_details.st_transfer_certificate = TransferCertificate
                doc_details.st_aadhar_card = AadharCard
                doc_details.st_pan_card = PanCard
            except:
                    pass           
            

            with transaction.atomic():
                    if student.is_dirty():
                        dirty = 1
                        dirty_fields = student.get_dirty_fields().keys()
                        student.save(update_fields=dirty_fields)

                    if pacad_10th.is_dirty():
                        dirty = 1
                        dirty_fields = pacad_10th.get_dirty_fields().keys()
                        pacad_10th.save(update_fields=dirty_fields)
                    
                    if pacad_12th.is_dirty():
                        dirty = 1
                        dirty_fields = pacad_12th.get_dirty_fields().keys()
                        pacad_12th.save(update_fields=dirty_fields)

                    if pacad_dip.is_dirty():
                        dirty = 1
                        dirty_fields = pacad_dip.get_dirty_fields().keys()
                        pacad_dip.save(update_fields=dirty_fields)


                    if dip_admission_ug is not None:
                        if dip_admission_ug.is_dirty():
                            dirty = 1
                            dirty_fields = dip_admission_ug.get_dirty_fields().keys()
                            dip_admission_ug.save(update_fields=dirty_fields)

                    if mgmt_admission_ug is not None:
                        if mgmt_admission_ug.is_dirty():
                            dirty = 1
                            dirty_fields = mgmt_admission_ug.get_dirty_fields().keys()
                            mgmt_admission_ug.save(update_fields=dirty_fields)

                    if doc_details.is_dirty():
                        dirty = 1
                        dirty_fields = doc_details.get_dirty_fields().keys()
                        doc_details.save(update_fields=dirty_fields)
                    
                    if prv_clgtrns_details.is_dirty():
                        dirty = 1
                        dirty_fields = prv_clgtrns_details.get_dirty_fields().keys()
                        prv_clgtrns_details.save(update_fields = dirty_fields)
                    
                    if cet_clgtrns is not None:
                        if cet_clgtrns.is_dirty():
                            dirty = 1
                            dirty_fields = cet_clgtrns.get_dirty_fields().keys()
                            cet_clgtrns.save(update_fields = dirty_fields)

                    if comedk_clgtrns is not None:
                        if comedk_clgtrns.is_dirty():
                            dirty = 1
                            dirty_fields = comedk_clgtrns.get_dirty_fields().keys()
                            comedk_clgtrns.save(update_fields=dirty_fields)
         
            if dirty : 
                messages.success(request, "Student Updated Successfully with UID" + student.st_uid)
            else:
                messages.success(request, "No changes were made with UID" + student.st_uid)
        
        context={"st_id": student.st_id, "st_uid": student.st_uid}
        return render(request,"add_transfercollege.html",context=context)

def admitStudent_ug(request):
    if request.method!="POST":
        return HttpResponseRedirect('AddStudent')
    else:
        parent_income = None
        mother_income = None
        admit_year = None
        admis_date = None
        admis_allot = None
        name = None
        course = None
        branch = None
        dept = None
        quota = None
        dob = None
        medium = None
        gender = None
        locality = None
        bld_grp = None
        BirthPlace = None
        Mothertongue = None
        Nationality = None
        religion = None
        Caste = None
        SubCaste = None
        ActualCategory = None
        StudentMobileNo = None
        StudentMailID = None
        aadhar_no = None
        st_eactivity = None
        father_name = None
        mother_name = None
        fatherjob = None
        motherjob = None
        parent_mobile_no = None
        mother_mobile_no = None
        parent_pan = None
        mother_pan = None
        parent_email = None
        mother_email =None
        pmtaddress = None
        pmtaddress_city = None
        pmtaddress_district = None
        pmtaddress_state = None
        pmtaddress_pincode = None
        postaladdress = None
        postaladdress_city = None
        postaladdress_district = None
        postaladdress_state = None
        postaladdress_pincode =None
        st_gaddress = None
        st_gmobno = None
        st_healthissues = None
        st_gemail = None
        x_board = None
        x_schoolname = None
        x_pass_month = None
        x_pass_year = None
        x_state = None
        x_medium = None
        x_regno = None
        x_marks = None
        x_percentage = None
        xii_board = None
        xii_school_name = None
        xii_month =None
        xii_passyr = None
        xii_pass_state = None
        xii_medium = None
        xii_regno = None
        xii_marks = None
        xii_percentage = None
        xii_pmarks = None
        xii_cmarks = None
        xii_mmarks = None
        xii_biocsmarks = None
        xii_pcmmakrs = None
        xii_pcmpercentage = None
        TotalFeePaid = None
        RtChallanNo = None
        RtChallanDate = None

        # dip_board = None
        # dip_school_name = None
        # dip_month =None
        # dip_passyr = None
        # dip_pass_state = None
        # dip_medium = None
        # dip_regno = None
        # dip_5marks = 0
        # dip_6marks = 0
        # dip_tmarks = 0
        # dip_tpercentage = 0.0

        AdmissionNo = None
        CETNo = None
        CETRank = None
        CategoryClaimed = None
        CategoryAllotted = None
        altdate = None
        cet_kea_feepaid = None
        cet_college_feepaid = None
        cet_totalfee = None
        cet_challandate = None
        cet_challanno = None

        COMEDKNo = None
        TATNumber = None
        COMEDKRank = None
        COMEDKCategoryAllotted = None
        COMEDKallottedDate = None
        COMEDKFeedPaid = None
        COMEDKCollegeFeedPaid = None
        COMEDKChallandate = None
        COMEDKChallanNo = None

        MGMTRank = None
        MGMTcet = None
        MGMTcomedk = None
        MGMTCollegeFeedPaid = None
        MGMTChallandate = None
        MGMTChallanNo = None

        AllotmentOrdCopy = None
        x_MarksCardCopy = None
        xii_MarksCardCopy = None
        dip_MarksCardCopy = None
        deg_certCopy = None
        StudyCertificate = None
        IncomeCertificate = None
        LinguisticCertificate = None
        Eligcertificate = None
        Migcertificate = None
        TransferCertificate = None
        AadharCard = None
        PanCard = None
        take_photo = None
        StudentID = None
        StudentUID = None

        mg_ug=0
        mg_pg=0


        try:   
            # Student details (add_student.html)
            take_photo = request.POST.get("take-photo")
            # # Generating Student UID code
            name = request.POST.get("st_name") 
            admit_year_id = request.POST.get("st_acad_year")
            admit_year = AcademicYear.objects.get(id=admit_year_id).acayear
            branch = request.POST.get("st_branch_applied")
            dept = Department.objects.get(dept_id=branch)  
            # # Generating Student UID code
            admis_allot = request.POST.get("st_adm_applied")
            st_similar_uid_set_count = 0
            Slice_year = admit_year[2:4]
            if admis_allot == "mtech":
                course = 'MT'
            elif admis_allot == "mba":
                course = 'MB'
            else:
                course = request.POST.get("st_course")

            with transaction.atomic():
                StudentSet = Student_Details.objects.select_for_update().filter(st_uid__contains=Slice_year + course).order_by('-st_id')[0]
            
            st_uid_sl_no = int(StudentSet.st_uid[4:])+1
                #st_uid_sl_no must be converted to string type else it cannot be concatenated
            if(st_uid_sl_no < 10):
                st_uid = Slice_year+course+'000'+str(st_uid_sl_no)
            elif(st_uid_sl_no > 9 and st_uid_sl_no <100):
                st_uid = Slice_year+course+'00'+str(st_uid_sl_no)
            elif(st_uid_sl_no > 99 and st_uid_sl_no <1000):
                st_uid = Slice_year+course+'0'+str(st_uid_sl_no)
            elif(st_uid_sl_no > 999 and st_uid_sl_no <10000):
                    st_uid = Slice_year+course+str(st_uid_sl_no)
            StudentUID = st_uid   
            
        except IndexError:
            st_uid = Slice_year+course+'0001'
            StudentUID = st_uid

        try:  
            admis_date = request.POST.get("adm_date") #C
            quota = int(request.POST.get("st_adm_quota")) #C
            # quota = Admission_Quota.objects.get(id=quota) #C
            dob = request.POST.get("st_dob") #C
            # medium = int(request.POST.get("st_medium"))
            medium = 2
            gender = int(request.POST.get("st_gender")) #C
            locality = int(request.POST.get("st_locality")) #C
            Nationality = int(request.POST.get("st_nationality")) #C
            religion = int(request.POST.get("st_religion")) #C
            Caste = request.POST.get("st_caste") #C
            ActualCategory = int(request.POST.get("st_category")) #C
            # ActualCategory = Category.objects.get(id=ActualCategory)
            StudentMobileNo = request.POST.get("st_mobile_no") #C
            father_name = request.POST.get("st_father_name") #C
            mother_name = request.POST.get("st_mother_name") #C
            parent_income = request.POST.get("st_father_income") #C
            parent_mobile_no = request.POST.get("st_father_mobile_no") #C
            pmtaddress = request.POST.get("st_parent_address") #C
            pmtaddress_city = request.POST.get("st_parent_address_city") #C
            pmtaddress_district = request.POST.get("st_parent_address_district") #C
            pmtaddress_state = int(request.POST.get("st_parent_address_state")) #C
            pmtaddress_pincode = request.POST.get("st_parent_address_pincode") #C
            postaladdress = request.POST.get("st_postal_address") #C
            postaladdress_city = request.POST.get("st_postal_address_city") #C
            postaladdress_district= request.POST.get("st_postal_address_district") #C
            postaladdress_state = int(request.POST.get("st_postal_address_state")) #C
            postaladdress_pincode = request.POST.get("st_postal_address_pincode") #C

        except:
            if quota is None:
                quota = 0
            if gender is None:
                gender = 0
            if medium is None:
                medium = 0
            if locality is None:
                locality = 0
            if Nationality is None:
                Nationality = 0
            if religion is None:
                religion = 0
            if ActualCategory is None:
                ActualCategory = 0
            if pmtaddress_state is None:
                pmtaddress_state = 0
            if postaladdress_state is None:
                postaladdress_state = 0
            if parent_income is None:
                parent_income  = 0

        try:
            # FOR OFFICE USE ONLY
            TotalFeePaid = int(request.POST.get("st_total_fees")) #C
            RtChallanNo = int(request.POST.get("st_rt_no")) #C
            RtChallanDate = request.POST.get("st_adm_date") #C
        except:
            if TotalFeePaid is None:
                TotalFeePaid = 0
            if RtChallanNo is None:
                RtChallanNo = 0
        #Optional non-string fields needs special attention
        #Hence they should be enclosed in try-catch blocks individually
        try:
            #in future unknown values from HTML to be validated
            bld_grp = int(request.POST.get("st_bld_group")) #O
        except Exception as e:
            print(e)
            if bld_grp is None:
                bld_grp = None
        try:
            aadhar_no = int(request.POST.get("st_aadhar_no")) #O
        except Exception as e:
            print(e)
            if aadhar_no is None:
                aadhar_no = None
        try:
            mother_income = int(request.POST.get("st_mother_income")) #O
        except Exception as e:
            print(e)
            if mother_income is None:
                mother_income = None

        #Optional string fields don't need special attention
        #Hence they can be clubbed in a single try-catch block
        try: 
            BirthPlace = request.POST.get("st_pob") #O
            Mothertongue = request.POST.get("st_mother_tongue") #O
            SubCaste = request.POST.get("st_subcaste") #O 
            StudentMailID = request.POST.get("st_email_id") #O
            st_eactivity = request.POST.get("st_extracurr_activity") #O
            fatherjob = request.POST.get("st_father_occupation") #O
            motherjob = request.POST.get("st_mother_occupation") #O
            mother_mobile_no = request.POST.get("st_mother_mobile_no") #O
            parent_pan = request.POST.get("st_father_pan") #O
            mother_pan = request.POST.get("st_mother_pan") #O
            parent_email = request.POST.get("st_father_email_id") #O
            mother_email = request.POST.get("st_mother_email_id") #O
            st_gaddress = request.POST.get("st_local_guardian_addr") #O
            st_gmobno = request.POST.get("st_guardian_mobile_no") #O
            st_healthissues = request.POST.get("st_health_issues") #O
            st_gemail = request.POST.get("st_guardian_email") #O
        except Exception as e:
            print(e)

        try:        
            # Previous Academic Details UG
            x_board = request.POST.get("ug_pacad_10th_board") #C
            x_schoolname = request.POST.get("ug_pacad_10th_schoolname") #C
            x_pass_month = int(request.POST.get("ug_pacad_10th_pass_month")) #C
            x_pass_month = Months.objects.get(id=x_pass_month)
            x_pass_year = request.POST.get("ug_pacad_10th_pass_year") #C
            x_state = int(request.POST.get("ug_pacad_10th_pass_state")) #C
            x_medium = request.POST.get("ug_pacad_10th_medium") #C
            x_regno = request.POST.get("ug_pacad_10th_reg_no") #C
            x_marks = float(request.POST.get("ug_pacad_10th_total_marks_cgpa")) #C
            x_percentage = float(request.POST.get("ug_pacad_10th_percentage_cgpa")) #C
            xii_board = request.POST.get("ug_pacad_12th_board") #C
            xii_school_name = request.POST.get("ug_pacad_12th_schoolname") #C
            xii_month = int(request.POST.get("ug_pacad_12th_pass_month")) #C
            xii_month = Months.objects.get(id=xii_month)
            xii_passyr = request.POST.get("ug_pacad_12th_pass_year") #C
            xii_pass_state = int(request.POST.get("ug_pacad_12th_pass_state")) #C
            xii_medium = request.POST.get("ug_pacad_12th_medium") #C
            xii_regno = request.POST.get("ug_pacad_12th_reg_no") #C
            xii_marks = int(request.POST.get("ug_pacad_12th_total_marks")) #C
            xii_percentage = float(request.POST.get("ug_pacad_12th_percentage")) #C
            xii_pmarks = int(request.POST.get("ug_pacad_12th_physics_marks")) #C
            xii_cmarks = int(request.POST.get("ug_pacad_12th_chemistry_marks")) #C
            xii_mmarks = int(request.POST.get("ug_pacad_12th_maths_marks")) #C
            xii_pcmmakrs = int(request.POST.get("ug_pacad_12th_pcm_total_marks")) #C
            xii_pcmpercentage = float(request.POST.get("ug_pacad_12th_pcm_percentage")) #C
        except Exception as e:
            print(e)
            if x_marks is None:
                x_marks = 0.0
            if x_percentage is None:
                x_percentage = 0.0
            if xii_marks is None:
                xii_marks = 0
            if xii_percentage is None:
                xii_percentage = 0.0
            if xii_pmarks is None:
                xii_pmarks = 0
            if xii_cmarks is None:
                xii_cmarks = 0
            if xii_mmarks is None:
                xii_mmarks = 0
            if xii_pcmmakrs is None:
                xii_pcmmakrs = 0
            if xii_pcmpercentage is None:
                xii_pcmpercentage = 0

        try:
            xii_biocsmarks = int(request.POST.get("ug_pacad_12th_bio_cs_marks")) #O
        except Exception as e:
            print(e)
            if xii_biocsmarks is None:
                xii_biocsmarks = None

        try:
            # Details for students admitted under CET quota
            AdmissionNo = request.POST.get("cet_order_no") #O
            CETNo = request.POST.get("cet_no") #O
            CategoryClaimed = request.POST.get("cet_cat_claimed") #O
            CategoryAllotted = request.POST.get("cet_cat_allotted") #O
            altdate = request.POST.get("cet_allot_date") #O
            cet_challandate = request.POST.get("cet_challan_date")
        except Exception as e:
            print(e)

        try:
            CETRank = int(request.POST.get("cet_rank")) #O
        except Exception as e:
            print(e)
            if CETRank is None:
                CETRank = None
        try:
            cet_kea_feepaid = int(request.POST.get("cet_kea_fees_paid")) #O
        except Exception as e:
            print(e)
            if cet_kea_feepaid is None:
                cet_kea_feepaid = None
        try:
            cet_college_feepaid = int(request.POST.get("cet_college_fees_paid")) #O
        except Exception as e:
            print(e)
            if cet_college_feepaid is None:
                cet_college_feepaid = None
        try:
            cet_totalfee = int(request.POST.get("cet_total_fees_paid")) #O
        except Exception as e:
            print(e)
            if cet_totalfee is None:
                cet_totalfee = None
        try:
            cet_challanno = int(request.POST.get("cet_challan_no")) #O
        except Exception as e:
            print(e)
            if cet_challanno is None:
                cet_challanno = None

        try:
            # Details for students admitted under COMEDK quota
            COMEDKNo = request.POST.get("comedk_sl_no") #O
            TATNumber = request.POST.get("comedk_tat_no") #O
            COMEDKCategoryAllotted = request.POST.get("comedk_cat_allotted") #O
            COMEDKallottedDate = request.POST.get("comedk_allot_date") #O
            COMEDKChallandate = request.POST.get("comedk_challan_date") #O
        except Exception as e:
            print(e)

        try:
            COMEDKRank = int(request.POST.get("comedk_rank")) #O
        except Exception as e:
            print(e)
            if COMEDKRank is None:
                COMEDKRank = None
        try:
            COMEDKFeedPaid = int(request.POST.get("comedk_fees_paid")) #O
        except Exception as e:
            print(e)
            if COMEDKFeedPaid is None:
                COMEDKFeedPaid = None
        try:
            COMEDKCollegeFeedPaid = int(request.POST.get("comedk_college_fees_paid")) #O
        except Exception as e:
            print(e)
            if COMEDKCollegeFeedPaid is None:
                COMEDKCollegeFeedPaid = None
        try:
            COMEDKChallanNo = int(request.POST.get("comedk_challan_no")) #O
        except Exception as e:
            print(e)
            if COMEDKChallanNo is None:
                COMEDKChallanNo = None

        try:
            # Details for students admitted under MANAGEMENT quota
            MGMTcet = request.POST.getlist("mgmt_exam[]") #C
            for m in MGMTcet:
                mg_ug=int(mg_ug)+int(m)
            MGMTChallandate = request.POST.get("mgmt_challan_date")
        except Exception as e:
            print(e)
        try:
            MGMTRank = int(request.POST.get("mgmt_rank")) #O
        except Exception as e:
            if MGMTRank is None:
                MGMTRank = None
        try:
            MGMTCollegeFeedPaid = int(request.POST.get("mgmt_college_fees_paid")) #O
        except Exception as e:
            print(e)
            if MGMTCollegeFeedPaid is None:
                MGMTCollegeFeedPaid = None
        try:
            MGMTChallanNo = int(request.POST.get("mgmt_challan_no")) #O
        except Exception as e:
            print(e)
            if MGMTChallanNo is None:
                MGMTChallanNo = None

        if COMEDKallottedDate == '':
            COMEDKallottedDate=None

        if COMEDKChallandate == '':
            COMEDKChallandate=None

        if MGMTChallandate == '':
            MGMTChallandate=None

        if altdate == '':
            altdate = None

        if cet_challandate == '':
            cet_challandate =  None

        try:
            # Documents submitted by the applicant
            AllotmentOrdCopy = int(request.POST.get("alt_order_copy")) #C
            x_MarksCardCopy = request.POST.get("st_10th_marks_card") #C
            xii_MarksCardCopy = request.POST.get("st_12th_marks_card") #C
            dip_MarksCardCopy = request.POST.get("st_dip_marks_card") #NA
            deg_certCopy = request.POST.get("st_degree_certificate") #NA
            StudyCertificate = request.POST.get("st_study_cerfiticate") #C
            IncomeCertificate = request.POST.get("st_income_certificate") #O
            LinguisticCertificate = request.POST.get("st_tulu_certificate") #O
            Eligcertificate = request.POST.get("st_eligibility_certificate") #O
            Migcertificate = request.POST.get("st_migration_certificate") #O
            TransferCertificate = request.POST.get("st_transfer_certificate") #C
            AadharCard = request.POST.get("st_aadhar_card") #O
            PanCard = request.POST.get("st_pan_card") #O
        except:
            if AllotmentOrdCopy is None:
                AllotmentOrdCopy = 0

        btn_value = request.POST["btn_clicked"]

        if btn_value == "register":
            snap = request.POST.get("snap")
            up_snap = request.POST.get("up_snap")
            if snap:
                img = snap
            else:
                img = up_snap

            with transaction.atomic():
                CustomUser.objects.create_user(email = StudentMailID, username = StudentUID, password=dob, user_type=3)
                student =  Student_Details.objects.create(st_profile_pic=get_image_from_data_url(img), st_acad_year=AcademicYear.objects.get(id=admit_year_id), adm_date = admis_date, st_branch_applied = dept, 
                st_name=name, st_adm_applied = admis_allot, st_adm_quota = Admission_Quota.objects.get(id=quota), st_dob = dob, st_medium = medium, st_gender = gender, st_locality = locality, 
                st_bld_group = BloodGroup.objects.get(id=bld_grp), st_pob = BirthPlace, st_mother_tongue = Mothertongue, st_nationality = Nationality, 
                st_religion = Religion.objects.get(id=religion), st_caste = Caste, st_subcaste = SubCaste, st_category = Category.objects.get(id=ActualCategory), 
                st_mobile_no = StudentMobileNo, st_email_id = StudentMailID, st_aadhar_no=aadhar_no, st_extracurr_activity = st_eactivity, st_father_name = father_name, 
                st_mother_name = mother_name, st_father_occupation = fatherjob, st_mother_occupation = motherjob, 
                st_father_income = parent_income, st_mother_income = mother_income, st_father_mobile_no = parent_mobile_no, 
                st_mother_mobile_no = mother_mobile_no, st_father_pan = parent_pan, st_mother_pan = mother_pan, 
                st_father_email_id = parent_email, st_mother_email_id = mother_email, st_parent_address = pmtaddress, 
                st_parent_address_city = pmtaddress_city, st_parent_address_district = pmtaddress_district, 
                st_parent_address_state = States.objects.get(id=pmtaddress_state), st_parent_address_pincode = pmtaddress_pincode, 
                st_postal_address = postaladdress, st_postal_address_city = postaladdress_city, 
                st_postal_address_district = postaladdress_district, st_postal_address_state = States.objects.get(id=postaladdress_state), 
                st_postal_address_pincode = postaladdress_pincode, st_local_guardian_addr = st_gaddress, st_guardian_mobile_no = st_gmobno, 
                st_health_issues = st_healthissues, st_guardian_email = st_gemail, st_total_fees = TotalFeePaid, st_rt_no = RtChallanNo, 
                st_adm_date = RtChallanDate, created_by = request.user.username, created_time = datetime.datetime.now(),last_edited_by = request.user.username,last_edited_time = datetime.datetime.now(), st_uid = StudentUID)

                pacad_10th  = Previous_10th_Academic_Details.objects.create(ug_pacad_10th_board = x_board, ug_pacad_10th_schoolname = x_schoolname, ug_pacad_10th_pass_month = x_pass_month, ug_pacad_10th_pass_year = x_pass_year,
                ug_pacad_10th_pass_state = States.objects.get(id=x_state), ug_pacad_10th_medium = x_medium, ug_pacad_10th_reg_no = x_regno, ug_pacad_10th_total_marks_cgpa = x_marks,
                ug_pacad_10th_percentage_cgpa = x_percentage, sslc_uid = student)

                pacad_12th = Previous_12th_Academic_Details.objects.create(ug_pacad_12th_board = xii_board, ug_pacad_12th_schoolname = xii_school_name,
                ug_pacad_12th_pass_month = xii_month, ug_pacad_12th_pass_year = xii_passyr, ug_pacad_12th_pass_state = States.objects.get(id=xii_pass_state), ug_pacad_12th_medium = xii_medium, 
                ug_pacad_12th_reg_no = xii_regno, ug_pacad_12th_total_marks = xii_marks, ug_pacad_12th_percentage = xii_percentage, 
                ug_pacad_12th_physics_marks = xii_pmarks, ug_pacad_12th_chemistry_marks = xii_cmarks, ug_pacad_12th_maths_marks = xii_mmarks,
                ug_pacad_12th_bio_cs_marks = xii_biocsmarks, ug_pacad_12th_pcm_total_marks = xii_pcmmakrs, ug_pacad_12th_pcm_percentage = xii_pcmpercentage,puc_uid = student)

                if quota == 1 or quota == 2: #CET or SNQ
                    cet_admission_ug = CET_Admission_Details_UG.objects.create(cet_order_no = AdmissionNo,
                    cet_no = CETNo, cet_rank= CETRank, cet_cat_claimed = CategoryClaimed, cet_cat_allotted = CategoryAllotted,
                    cet_allot_date = altdate, cet_kea_fees_paid = cet_kea_feepaid, cet_college_fees_paid = cet_college_feepaid, 
                    cet_total_fees_paid = cet_totalfee, cet_challan_date = cet_challandate,
                    cet_challan_no = cet_challanno, cet_uid = student)

                if quota == 4: #COMEDK
                    comedk_admission_ug = COMEDK_Admission_Details_UG.objects.create(comedk_sl_no = COMEDKNo,
                    comedk_tat_no = TATNumber,comedk_rank = COMEDKRank, comedk_cat_allotted = COMEDKCategoryAllotted, 
                    comedk_allot_date = COMEDKallottedDate, comedk_fees_paid = COMEDKFeedPaid,
                    comedk_college_fees_paid = COMEDKCollegeFeedPaid, comedk_challan_date = COMEDKChallandate, 
                    comedk_challan_no = COMEDKChallanNo, comedk_uid = student)

                if quota == 3: #MGMT
                    mgmt_admission_ug = MGMT_Admission_Details_UG.objects.create(mgmt_rank = MGMTRank, mgmt_exam = mg_ug,
                    mgmt_college_fees_paid = MGMTCollegeFeedPaid , mgmt_challan_date = MGMTChallandate , mgmt_challan_no = MGMTChallanNo, mgmt_uid = student)

                doc_details = Document_Details.objects.create(alt_order_copy = AllotmentOrdCopy, st_10th_marks_card  = x_MarksCardCopy, st_12th_marks_card = xii_MarksCardCopy,
                st_study_cerfiticate = StudyCertificate, st_income_certificate =  IncomeCertificate, st_dip_marks_card = dip_MarksCardCopy, st_degree_certificate = deg_certCopy,
                st_tulu_certificate = LinguisticCertificate, st_eligibility_certificate = Eligcertificate, 
                st_migration_certificate = Migcertificate, st_transfer_certificate = TransferCertificate,
                st_aadhar_card = AadharCard, st_pan_card = PanCard, doc_uid = student) 
            messages.success(request, "Student Admitted Successfully with UID" + StudentUID)
            context={"st_id": student.st_id, "st_uid": student.st_uid}
            return render(request,"add_student.html",context=context)

        elif btn_value == "update":
            print("Inside update")
            dirty = 0
            st_id = request.POST.get('st_id')
            student = Student_Details.objects.get(st_id = st_id)
            snap = request.POST.get("snap")
            up_snap = request.POST.get("up_snap")
            data_pic = student.st_profile_pic
            user = CustomUser.objects.update_user(email = StudentMailID, username = student.st_uid, password=dob)
            if snap:
                student.st_profile_pic = get_image_from_data_url(snap)
            elif up_snap:
                student.st_profile_pic = get_image_from_data_url(up_snap)
            else:
                student.st_profile_pic = data_pic

            student.st_name = name
            student.st_acad_year = AcademicYear.objects.get(id=admit_year_id)
            student.st_branch_applied = dept
            student.st_adm_quota = Admission_Quota.objects.get(id=quota)
            student.st_dob = dob
            student.st_medium = medium  
            student.st_gender = gender
            student.st_locality = locality
            student.st_bld_group = BloodGroup.objects.get(id=bld_grp)
            #### Debug #####
            print("Blood grp")
            print(student.st_bld_group)
            #### Debug #####
            student.adm_date = admis_date
            student.st_adm_applied = admis_allot
            student.st_pob  = BirthPlace
            student.st_mother_tongue = Mothertongue
            student.st_nationality = Nationality
            student.st_religion = Religion.objects.get(id=religion)
            student.st_caste = Caste
            student.st_subcaste = SubCaste
            student.st_category = Category.objects.get(id=ActualCategory)
            student.st_mobile_no = StudentMobileNo
            student.st_email_id = StudentMailID
            student.st_aadhar_no = aadhar_no
            student.st_extracurr_activity = st_eactivity
            student.st_father_name = father_name
            student.st_mother_name = mother_name
            student.st_father_occupation = fatherjob
            student.st_mother_occupation = motherjob
            student.st_father_income = parent_income
            student.st_mother_income = mother_income
            student.st_father_mobile_no = parent_mobile_no
            student.st_mother_mobile_no = mother_mobile_no
            student.st_father_pan = parent_pan
            student.st_mother_pan = mother_pan
            student.st_father_email_id = parent_email
            student.st_mother_email_id = mother_email
            student.st_parent_address = pmtaddress
            student.st_parent_address_city = pmtaddress_city
            student.st_parent_address_district = pmtaddress_district
            student.st_parent_address_state = States.objects.get(id=pmtaddress_state)
            student.st_parent_address_pincode = pmtaddress_pincode
            student.st_postal_address = postaladdress
            student.st_postal_address_city = postaladdress_city
            student.st_postal_address_district = postaladdress_district
            student.st_postal_address_state = States.objects.get(id=postaladdress_state)
            student.st_postal_address_pincode = postaladdress_pincode
            student.st_local_guardian_addr = st_gaddress
            student.st_guardian_mobile_no = st_gmobno
            student.st_health_issues = st_healthissues
            student.st_guardian_email = st_gemail
            student.st_total_fees = TotalFeePaid
            student.st_rt_no = RtChallanNo
            student.st_adm_date = RtChallanDate
            student.last_edited_by = request.user.username
            student.last_edited_time = datetime.datetime.now()

            print(student.is_dirty(check_relationship=True))

            ug_uid = request.POST.get('st_id')
            pacad_10th = Previous_10th_Academic_Details.objects.get(sslc_uid = ug_uid)
            pacad_10th.ug_pacad_10th_board = x_board
            pacad_10th.ug_pacad_10th_schoolname = x_schoolname
            pacad_10th.ug_pacad_10th_pass_month = x_pass_month
            pacad_10th.ug_pacad_10th_pass_year = x_pass_year
            pacad_10th.ug_pacad_10th_pass_state = States.objects.get(id=x_state)
            pacad_10th.ug_pacad_10th_medium = x_medium
            pacad_10th.ug_pacad_10th_reg_no = x_regno
            pacad_10th.ug_pacad_10th_total_marks_cgpa = x_marks
            pacad_10th.ug_pacad_10th_percentage_cgpa = x_percentage

            pacad_12th = Previous_12th_Academic_Details.objects.get(puc_uid = ug_uid)
            pacad_12th.ug_pacad_12th_board = xii_board
            pacad_12th.ug_pacad_12th_schoolname = xii_school_name
            pacad_12th.ug_pacad_12th_pass_month = xii_month
            pacad_12th.ug_pacad_12th_pass_year = xii_passyr
            pacad_12th.ug_pacad_12th_pass_state = States.objects.get(id=xii_pass_state)
            pacad_12th.ug_pacad_12th_medium = xii_medium
            pacad_12th.ug_pacad_12th_reg_no = xii_regno
            pacad_12th.ug_pacad_12th_total_marks = xii_marks
            pacad_12th.ug_pacad_12th_percentage = xii_percentage
            pacad_12th.ug_pacad_12th_physics_marks = xii_pmarks
            pacad_12th.ug_pacad_12th_chemistry_marks = xii_cmarks
            pacad_12th.ug_pacad_12th_maths_marks = xii_mmarks
            pacad_12th.ug_pacad_12th_bio_cs_marks = xii_biocsmarks
            pacad_12th.ug_pacad_12th_pcm_total_marks = xii_pcmmakrs
            pacad_12th.ug_pacad_12th_pcm_percentage = xii_pcmpercentage

            try:
                cet_uid = request.POST.get('st_id')
                cet_admission_ug = CET_Admission_Details_UG.objects.get(cet_uid = cet_uid)
                cet_admission_ug.cet_order_no = AdmissionNo
                cet_admission_ug.cet_no = CETNo
                cet_admission_ug.cet_rank = CETRank
                cet_admission_ug.cet_cat_claimed = CategoryClaimed
                cet_admission_ug.cet_cat_allotted = CategoryAllotted
                cet_admission_ug.cet_allot_date = altdate
                cet_admission_ug.cet_kea_fees_paid = cet_kea_feepaid
                cet_admission_ug.cet_total_fees_paid = cet_totalfee
                cet_admission_ug.cet_college_fees_paid = cet_college_feepaid
                cet_admission_ug.cet_challan_date = cet_challandate
                cet_admission_ug.cet_challan_no = cet_challanno
            except:
                cet_admission_ug = None

            try:
                comedk_uid = request.POST.get('st_id')
                comedk_admission_ug = COMEDK_Admission_Details_UG.objects.get(comedk_uid = comedk_uid)
                comedk_admission_ug.comedk_sl_no  = COMEDKNo
                comedk_admission_ug.comedk_tat_no = TATNumber
                comedk_admission_ug.comedk_rank = COMEDKRank
                comedk_admission_ug.comedk_cat_allotted = COMEDKCategoryAllotted
                comedk_admission_ug.comedk_allot_date = COMEDKallottedDate
                comedk_admission_ug.comedk_fees_paid = COMEDKFeedPaid
                comedk_admission_ug.comedk_college_fees_paid = COMEDKCollegeFeedPaid
                comedk_admission_ug.comedk_challan_date = COMEDKChallandate
                comedk_admission_ug.comedk_challan_no = COMEDKChallanNo 
            except:
                    comedk_admission_ug = None
            try:              
                mgmt_uid = request.POST.get('st_id')
                mgmt_admission_ug = MGMT_Admission_Details_UG.objects.get(mgmt_uid = mgmt_uid)
                mgmt_admission_ug.mgmt_rank = MGMTRank 
                mgmt_admission_ug.mgmt_exam = mg_ug
                mgmt_admission_ug.mgmt_college_fees_paid = MGMTCollegeFeedPaid
                mgmt_admission_ug.mgmt_challan_date = MGMTChallandate
                mgmt_admission_ug.mgmt_challan_no = MGMTChallanNo
            except:
                    mgmt_admission_ug = None

            try: 
                doc_uid = request.POST.get('st_id')
                doc_details = Document_Details.objects.get(doc_uid = doc_uid)
                doc_details.alt_order_copy = AllotmentOrdCopy
                doc_details.st_10th_marks_card = x_MarksCardCopy
                doc_details.st_12th_marks_card = StudyCertificate
                doc_details.st_income_certificate = IncomeCertificate
                doc_details.st_dip_marks_card = dip_MarksCardCopy
                doc_details.st_degree_certificate = deg_certCopy
                doc_details.st_tulu_certificate = LinguisticCertificate
                doc_details.st_eligibility_certificate = Eligcertificate
                doc_details.st_migration_certificate = Migcertificate
                doc_details.st_transfer_certificate = TransferCertificate
                doc_details.st_aadhar_card = AadharCard
                doc_details.st_pan_card = PanCard
            except:
                    doc_details = None           
            
            with transaction.atomic():
                    if student.is_dirty(check_relationship=True):
                        dirty = 1
                        dirty_fields = student.get_dirty_fields(check_relationship=True).keys()
                        print(dirty_fields)
                        student.save(update_fields=dirty_fields)

                    if pacad_10th.is_dirty(check_relationship=True):
                        dirty = 1
                        dirty_fields = pacad_10th.get_dirty_fields(check_relationship=True).keys()
                        pacad_10th.save(update_fields=dirty_fields)

                    if pacad_12th.is_dirty(check_relationship=True):
                        dirty = 1
                        dirty_fields = pacad_12th.get_dirty_fields(check_relationship=True).keys()
                        pacad_12th.save(update_fields=dirty_fields)

                    try:
                        if cet_admission_ug.is_dirty(check_relationship=True):
                            dirty = 1
                            dirty_fields = cet_admission_ug.get_dirty_fields(check_relationship=True).keys()
                            cet_admission_ug.save(update_fields=dirty_fields)
                    except:
                        pass

                    try:
                        if comedk_admission_ug.is_dirty(check_relationship=True):
                            dirty = 1
                            dirty_fields = comedk_admission_ug.get_dirty_fields(check_relationship=True).keys()
                            comedk_admission_ug.save(update_fields=dirty_fields)
                    except:
                        pass

                    try:
                        if mgmt_admission_ug.is_dirty(check_relationship=True):
                            dirty = 1
                            dirty_fields = mgmt_admission_ug.get_dirty_fields(check_relationship=True).keys()
                            mgmt_admission_ug.save(update_fields=dirty_fields)
                    except:
                        pass

                    if doc_details.is_dirty(check_relationship=True):
                        dirty = 1
                        dirty_fields = doc_details.get_dirty_fields(check_relationship=True).keys()
                        doc_details.save(update_fields=dirty_fields)


            if dirty : 
                messages.success(request, "Student Updated Successfully with UID" + student.st_uid)
            else:
                messages.success(request, "No changes were made with UID" + student.st_uid)
        return HttpResponseRedirect('ViewStudent')

def admitStudent_pg(request):
    if request.method!="POST":
        return HttpResponseRedirect('AddPGStudent')
    
    else:

        parent_income = None
        mother_income = None
        admit_year = None
        admis_date = None
        admis_allot = None
        name = None
        course = None
        branch = None
        dept = None
        quota = None
        dob = None
        gender = None
        locality = None
        BirthPlace = None
        Mothertongue = None
        Nationality = None
        Caste = None
        SubCaste = None
        ActualCategory = None
        StudentMobileNo = None
        StudentMailID = None
        aadhar_no = None
        st_eactivity = None
        father_name = None
        mother_name = None
        fatherjob = None
        motherjob = None
        parent_mobile_no = None
        mother_mobile_no = None
        parent_pan = None
        mother_pan = None
        parent_email = None
        mother_email =None
        pmtaddress = None
        pmtaddress_city = None
        pmtaddress_district = None
        pmtaddress_state = None
        pmtaddress_pincode = None
        postaladdress = None
        postaladdress_city = None
        postaladdress_district = None
        postaladdress_state = None
        postaladdress_pincode =None
        st_gaddress = None
        st_gmobno = None
        st_healthissues = None
        st_gemail = None
        TotalFeePaid = None
        RtChallanNo = None
        RtChallanDate = None
        bld_grp=None

        AllotmentOrdCopy = None
        x_MarksCardCopy = None
        xii_MarksCardCopy = None
        dip_MarksCardCopy = None
        deg_certCopy = None
        StudyCertificate = None
        IncomeCertificate = None
        LinguisticCertificate = None
        Eligcertificate = None
        Migcertificate = None
        TransferCertificate = None
        AadharCard = None
        PanCard = None

        pg_x_board = None 
        pg_x_regno = None
        pg_x_pass_month = None 
        pg_x_pass_year= None
        pg_x_marks = None
        pg_x_percentage = None 
        pg_10th_class = None
        pg_xii_board = None
        pg_xii_regno = None
        pg_xii_month = None
        pg_xii_passyr = None
        pg_xii_marks = None
        pg_xii_percentage = None 
        pg_12th_class = None
        pg_degree = None
        pg_degreeregno = None 
        pg_degreepass_month = None 
        pg_degreepass_year = None
        pg_degreepercent = None
        pg_deg_5_8_percent = None
        pg_degree_class = None

        pg_AdmissionNo = None
        pg_CETNo = None
        pg_CETRank = None
        pg_CategoryClaimed = None  
        pg_CategoryAllotted = None
        pg_altdate = None 
        pg_cet_kea_feepaid = None  
        pg_cet_college_feepaid = None 
        pgcet_totalfees = None
        pgcet_challandate = None 
        pg_challanno = None 

        pg_MGMTRank = None
        pg_MGMTcet = None
        pg_MGMTCollegeFeedPaid = None 
        pg_MGMTChallandate = None
        pg_MGMTChallanNo = None

        take_photo = None
        StudentID = None
        StudentUID = None

        mg_ug=0
        mg_pg=0
        bldgrp = None


        try:   
            # Student details (add_student.html)
            take_photo = request.POST.get("take-photo")
            # # Generating Student UID code
            name = request.POST.get("st_name") 
            admit_year_id = request.POST.get("st_acad_year")
            admit_year = AcademicYear.objects.get(id=admit_year_id).acayear
            branch = request.POST.get("st_branch_applied")
            dept = Department.objects.get(dept_id=branch)  
            # # Generating Student UID code
            admis_allot = request.POST.get("st_adm_applied")
            st_similar_uid_set_count = 0
            Slice_year = admit_year[2:4]
            if admis_allot == "mtech":
                course = 'MT'
            elif admis_allot == "mba":
                course = 'MB'
            else:
                course = request.POST.get("st_course")

            with transaction.atomic():
                StudentSet = Student_Details.objects.select_for_update().filter(st_uid__contains=Slice_year + course).order_by('-st_id')[0]
            
            st_uid_sl_no = int(StudentSet.st_uid[4:])+1
                #st_uid_sl_no must be converted to string type else it cannot be concatenated
            if(st_uid_sl_no < 10):
                st_uid = Slice_year+course+'000'+str(st_uid_sl_no)
            elif(st_uid_sl_no > 9 and st_uid_sl_no <100):
                st_uid = Slice_year+course+'00'+str(st_uid_sl_no)
            elif(st_uid_sl_no > 99 and st_uid_sl_no <1000):
                st_uid = Slice_year+course+'0'+str(st_uid_sl_no)
            elif(st_uid_sl_no > 999 and st_uid_sl_no <10000):
                    st_uid = Slice_year+course+str(st_uid_sl_no)
            StudentUID = st_uid   
            
        except IndexError:
            st_uid = Slice_year+course+'0001'
            StudentUID = st_uid

        try:  
            admis_date = request.POST.get("adm_date")
            quota = int(request.POST.get("st_adm_quota"))
            dob = request.POST.get("st_dob")
            gender = int(request.POST.get("st_gender"))
            locality = int(request.POST.get("st_locality"))
            Nationality = int(request.POST.get("st_nationality"))
            rlgn = int(request.POST.get("st_religion"))
            Caste = request.POST.get("st_caste")
            parent_income = request.POST.get("st_father_income")
            parent_mobile_no = request.POST.get("st_father_mobile_no")
            ActualCategory = int(request.POST.get("st_category"))
            StudentMobileNo = request.POST.get("st_mobile_no")
            pmtaddress = request.POST.get("st_parent_address")
            pmtaddress_city = request.POST.get("st_parent_address_city")
            pmtaddress_district= request.POST.get("st_parent_address_district")
            RtChallanNo = int(request.POST.get("st_rt_no"))
            pmtaddress_pincode = request.POST.get("st_parent_address_pincode")
            postaladdress = request.POST.get("st_postal_address")
            postaladdress_city = request.POST.get("st_postal_address_city")
            postaladdress_district= request.POST.get("st_postal_address_district")
            postaladdress_pincode = request.POST.get("st_postal_address_pincode")
            RtChallanDate = request.POST.get("st_adm_date")

            father_name = request.POST.get("st_father_name")
            mother_name = request.POST.get("st_mother_name")
            fatherjob = request.POST.get("st_father_occupation")
            motherjob = request.POST.get("st_mother_occupation")
            mother_mobile_no = request.POST.get("st_mother_mobile_no")
            parent_pan = request.POST.get("st_father_pan")
            mother_pan = request.POST.get("st_mother_pan")
            parent_email = request.POST.get("st_father_email_id")
            mother_email = request.POST.get("st_mother_email_id")
            st_gaddress = request.POST.get("st_local_guardian_addr")
            st_gmobno = request.POST.get("st_guardian_mobile_no")
            st_healthissues = request.POST.get("st_health_issues")
            st_gemail = request.POST.get("st_guardian_email")

            TotalFeePaid = int(request.POST.get("st_total_fees"))
            mother_income = int(request.POST.get("st_mother_income"))          
            aadhar_no = int(request.POST.get("st_aadhar_no"))
             

        except: 
            if aadhar_no is None:
                aadhar_no = 0
            if TotalFeePaid is None:
                TotalFeePaid = None
            if RtChallanNo is None:
                RtChallanNo = None  

        try:
            StudentMailID = request.POST.get("st_email_id")
        except Exception as e:
            print(e)
            if StudentMailID is None:
                StudentMailID = None
        
        
        try:
            SubCaste = request.POST.get("st_subcaste")
        except Exception as e:
            print(e)
            if SubCaste is None:
                SubCaste = None
        try:
            Mothertongue = request.POST.get("st_mother_tongue")
        except Exception as e:
            print(e)
            if Mothertongue is None:
                Mothertongue = None
        
        try:
            BirthPlace = request.POST.get("st_pob")
        except Exception as e:
            print(e)
            if BirthPlace is None:
                BirthPlace = None
        
        try:
            bldgrp = int(request.POST.get("st_bld_group"))
            bld_grp = BloodGroup.objects.get(id = bldgrp)
        except Exception as e:
            print(e)
            if bld_grp is None:
                bld_grp = None


        try:    
            pmtaddress_state = int(request.POST.get("st_parent_address_state"))
        except Exception as e:
            print(e)
            if pmtaddress_state is None:
                pmtaddress_state = None
        
        try:
            postaddr_state = int(request.POST.get("st_postal_address_state"))
            postaladdress_state = States.objects.get(id = postaddr_state)
        except Exception as e:
            print(e)
            if postaladdress_state is None:
                postaladdress_state = None
        
        try:
            pg_xii_board = request.POST.get("pg_pacad_12th_board")
        except:
            if pg_xii_board is None:
                pg_xii_board = None

        try:
            st_eactivity = request.POST.get("st_extracurr_activity")
        except Exception as e:
            print(e)
            if st_eactivity is None:
                st_eactivity = None
        
        try:        
            # Previous Academic Details PG
            pg_12th_class = request.POST.get("pg_pacad_12th_class_obtained")
            pg_deg_5_8_percent = float(request.POST.get("pg_pacad_be_percentage_5_8"))
            pg_degree_class = request.POST.get("pg_pacad_degree_class_obtained")
            pg_x_board =  request.POST.get("pg_pacad_10th_board")
            pg_x_regno =  request.POST.get("pg_pacad_10th_reg_no")
            pg_x_pass_month = request.POST.get("pg_pacad_10th_pass_month")
            pg_x_pass_year= request.POST.get("pg_pacad_10th_pass_year")
            pg_x_marks = request.POST.get("pg_pacad_10th_total_marks_cgpa")
            pg_x_percentage = request.POST.get("pg_pacad_10th_percentage_cgpa")
            pg_10th_class =  request.POST.get("pg_pacad_10th_class_obtained")
            pg_degree = request.POST.get("pg_pacad_degree_university")
            pg_degreeregno = request.POST.get("pg_pacad_degree_reg_no")
            pg_degreepass_month = request.POST.get("pg_pacad_degree_pass_month")
            pg_degreepass_year = request.POST.get("pg_pacad_degree_pass_year")
            pg_degreepercent = float(request.POST.get("pg_pacad_degree_percentage_cgpa"))
            pg_xii_passyr = request.POST.get("pg_pacad_12th_pass_year")
            pg_xii_month = request.POST.get("pg_pacad_12th_pass_month")
            pg_xii_regno = request.POST.get("pg_pacad_12th_reg_no")
            pg_xii_percentage = int(request.POST.get("pg_pacad_12th_percentage"))
            pg_xii_marks = int(request.POST.get("pg_pacad_12th_total_marks"))
           
            

        except:
            if pg_x_marks is None:
                pg_x_marks = 0
            if pg_x_percentage is None:
                pg_x_percentage = 0
            if pg_xii_percentage is '':
                pg_xii_percentage = None
            if pg_degreepercent is None:
                pg_degreepercent = 0
            if  pg_deg_5_8_percent is None:
                pg_deg_5_8_percent = 0
        
        try:
            pg_CategoryClaimed =  request.POST.get("pgcet_cat_claimed")
            pg_CategoryAllotted =  request.POST.get("pgcet_cat_allotted")
            pg_AdmissionNo = request.POST.get("pgcet_order_no")
            pg_challanno =  request.POST.get("pgcet_challan_no")
            pg_CETNo = request.POST.get("pgcet_no")
            pg_altdate =  request.POST.get("pgcet_allot_date")
            pgcet_challandate =  request.POST.get("pgcet_challan_date")
            pg_CETRank = int(request.POST.get("pgcet_rank"))
            pg_cet_kea_feepaid =  int(request.POST.get("pgcet_kea_fees_paid"))
            pg_cet_college_feepaid =  int(request.POST.get("pgcet_college_fees_paid"))
            pgcet_totalfees =  int(request.POST.get("pgcet_total_fees_paid")) 

        except:
            if pg_CETRank is None:
                pg_CETRank = None
            if pg_cet_kea_feepaid is None:
                pg_cet_kea_feepaid = 0
            if pg_cet_college_feepaid is None:
                pg_cet_college_feepaid = 0
            if pgcet_totalfees is None:
                pgcet_totalfees = None
            if pg_challanno is None:
                pg_challanno= None
            if pg_AdmissionNo is None:
                pg_AdmissionNo = None
            if  pg_cet_kea_feepaid is None:
                pg_cet_kea_feepaid = None 
            if pg_cet_college_feepaid is None:
                pg_cet_college_feepaid = None

        try:
            pg_MGMTChallandate = request.POST.get("mgmt_pg_challan_date") 
            pg_MGMTcet = request.POST.getlist("mgmt_exampg[]")
            for m in pg_MGMTcet:
                mg_pg=int(mg_pg)+int(m)
            pg_MGMTCollegeFeedPaid = int(request.POST.get("mgmt_pg_college_fees_paid"))
             
        except:
            if pg_MGMTChallanNo is None:
                pg_MGMTChallanNo = 0 

        try:
            pg_MGMTChallanNo = int(request.POST.get("mgmt_pg_challan_no"))
        except:
            if pg_MGMTChallanNo is None:
                pg_MGMTChallanNo = 0

        try:
            pg_MGMTRank = int(request.POST.get("mgmt_pg_rank"))
        except:
            if pg_MGMTRank is None:
                pg_MGMTRank =0

        try:
            # Documents submitted by the applicant
            AllotmentOrdCopy = int(request.POST.get("alt_order_copy"))
            x_MarksCardCopy = request.POST.get("st_10th_marks_card")
            xii_MarksCardCopy = request.POST.get("st_12th_marks_card")
            dip_MarksCardCopy = request.POST.get("st_dip_marks_card")
            deg_certCopy = request.POST.get("st_degree_certificate")
            StudyCertificate = request.POST.get("st_study_cerfiticate")
            IncomeCertificate = request.POST.get("st_income_certificate")
            LinguisticCertificate = request.POST.get("st_tulu_certificate")
            Eligcertificate = request.POST.get("st_eligibility_certificate")
            Migcertificate = request.POST.get("st_migration_certificate")
            TransferCertificate = request.POST.get("st_transfer_certificate")
            AadharCard = request.POST.get("st_aadhar_card")
            PanCard = request.POST.get("st_pan_card")
        except:
            if AllotmentOrdCopy is None:
                AllotmentOrdCopy = 0

        btn_value = request.POST["btn_clicked"]
        if btn_value == "register":

            snap = request.POST.get("snap")
            up_snap = request.POST.get("up_snap")
            if snap:
                img = snap
            else:
                img = up_snap

            with transaction.atomic():
                CustomUser.objects.create_user(email = StudentMailID, username = StudentUID, password=dob, user_type=3)
                student =   Student_Details.objects.create(st_profile_pic=get_image_from_data_url(img), st_acad_year_id=admit_year_id, adm_date = admis_date, st_branch_applied_id = branch, 
                st_name=name, st_adm_applied = admis_allot, st_adm_quota_id = quota, st_dob = dob, st_gender = gender, st_locality = locality, 
                st_bld_group_id = bldgrp, st_pob = BirthPlace, st_mother_tongue = Mothertongue, st_nationality = Nationality, 
                st_religion_id = rlgn, st_caste = Caste, st_subcaste = SubCaste, st_category_id = ActualCategory, 
                st_mobile_no = StudentMobileNo, st_email_id = StudentMailID, st_aadhar_no=aadhar_no, st_extracurr_activity = st_eactivity, st_father_name = father_name, 
                st_mother_name = mother_name, st_father_occupation = fatherjob, st_mother_occupation = motherjob, 
                st_father_income = parent_income, st_mother_income = mother_income, st_father_mobile_no = parent_mobile_no, 
                st_mother_mobile_no = mother_mobile_no, st_father_pan = parent_pan, st_mother_pan = mother_pan, 
                st_father_email_id = parent_email, st_mother_email_id = mother_email, st_parent_address = pmtaddress, 
                st_parent_address_city = pmtaddress_city, st_parent_address_district = pmtaddress_district, 
                st_parent_address_state_id =  pmtaddress_state, st_parent_address_pincode = pmtaddress_pincode, 
                st_postal_address = postaladdress, st_postal_address_city = postaladdress_city, 
                st_postal_address_district = postaladdress_district, st_postal_address_state_id = postaddr_state , 
                st_postal_address_pincode = postaladdress_pincode, st_local_guardian_addr = st_gaddress, st_guardian_mobile_no = st_gmobno, 
                st_health_issues = st_healthissues, st_guardian_email = st_gemail, st_total_fees = TotalFeePaid, st_rt_no = RtChallanNo, 
                st_adm_date = RtChallanDate, created_by = request.user.username, created_time = datetime.datetime.now(),last_edited_by = request.user.username,last_edited_time = datetime.datetime.now() ,st_uid = StudentUID)

                doc_details = Document_Details.objects.create(alt_order_copy = AllotmentOrdCopy, st_10th_marks_card  = x_MarksCardCopy, st_12th_marks_card = xii_MarksCardCopy,
                st_study_cerfiticate = StudyCertificate, st_income_certificate =  IncomeCertificate, st_dip_marks_card = dip_MarksCardCopy, st_degree_certificate = deg_certCopy,
                st_tulu_certificate = LinguisticCertificate, st_eligibility_certificate = Eligcertificate, 
                st_migration_certificate = Migcertificate, st_transfer_certificate = TransferCertificate,
                st_aadhar_card = AadharCard, st_pan_card = PanCard, doc_uid = student) 

                pacad_pg = Previous_Academic_Details_PG.objects.create(pg_pacad_10th_board = pg_x_board, pg_pacad_10th_reg_no = pg_x_regno, pg_pacad_10th_pass_month = pg_x_pass_month, pg_pacad_10th_pass_year = pg_x_pass_year,
                pg_pacad_10th_total_marks_cgpa = pg_x_marks, pg_pacad_10th_percentage_cgpa = pg_x_percentage, pg_pacad_10th_class_obtained = pg_10th_class, pg_pacad_12th_board = pg_xii_board, pg_pacad_12th_reg_no = pg_xii_regno,
                pg_pacad_12th_pass_month = pg_xii_month, pg_pacad_12th_pass_year = pg_xii_passyr, pg_pacad_12th_total_marks = pg_xii_marks, pg_pacad_12th_percentage = pg_xii_percentage, pg_pacad_12th_class_obtained = pg_12th_class,
                pg_pacad_degree_university = pg_degree , pg_pacad_degree_reg_no = pg_degreeregno, pg_pacad_degree_pass_month = pg_degreepass_month, pg_pacad_degree_pass_year = pg_degreepass_year,
                pg_pacad_degree_percentage_cgpa = pg_degreepercent, pg_pacad_be_percentage_5_8 = pg_deg_5_8_percent , pg_pacad_degree_class_obtained = pg_degree_class, pg_uid = student)

                pgcet_admission_pg = PGCET_Admission_Details_PG.objects.create(pgcet_order_no = pg_AdmissionNo, pgcet_no = pg_CETNo, pgcet_rank= pg_CETRank, pgcet_cat_claimed = pg_CategoryClaimed, 
                pgcet_cat_allotted = pg_CategoryAllotted, pgcet_allot_date = pg_altdate, pgcet_kea_fees_paid = pg_cet_kea_feepaid, pgcet_college_fees_paid = pg_cet_college_feepaid, 
                pgcet_total_fees_paid = pgcet_totalfees, pgcet_challan_date = pgcet_challandate ,pgcet_challan_no = pg_challanno ,pgcet_uid = student)

                mgmt_admission_pg = MGMT_Admission_Details_PG.objects.create(mgmt_pg_rank = pg_MGMTRank, mgmt_exampg = mg_pg,
                mgmt_pg_college_fees_paid = pg_MGMTCollegeFeedPaid , mgmt_pg_challan_date = pg_MGMTChallandate , mgmt_pg_challan_no = pg_MGMTChallanNo, mgmt_pg_uid = student)       
            
            messages.success(request, "Student Admitted Successfully with UID" + StudentUID)
            context={"st_id": student.st_id, "st_uid": student.st_uid}
            return render(request,"add_pg.html",context=context)


        elif btn_value == "update":
            print("Inside update")
            dirty = 0
            st_id = request.POST.get('st_id')
            student = Student_Details.objects.get(st_id = st_id)
            snap = request.POST.get("snap")
            up_snap = request.POST.get("up_snap")
            data_pic = student.st_profile_pic
            user = CustomUser.objects.update_user(email = StudentMailID, username = student.st_uid, password=dob)
            if snap:
                student.st_profile_pic = get_image_from_data_url(snap)
            elif up_snap:
                student.st_profile_pic = get_image_from_data_url(up_snap)
            else:
                student.st_profile_pic = data_pic

            student.st_name = name
            student.st_acad_year_id = admit_year_id
            student.st_branch_applied_id = dept
            student.st_adm_quota_id = quota
            student.st_dob = dob
            student.st_gender = gender
            student.st_adm_applied = admis_allot
            student.st_locality = locality
            student.st_bld_group_id = bld_grp
            student.adm_date = admis_date
            student.st_pob  = BirthPlace
            student.st_mother_tongue = Mothertongue
            student.st_nationality = Nationality
            student.st_religion_id = rlgn
            student.st_caste = Caste
            student.st_subcaste = SubCaste
            student.st_category_id = ActualCategory
            student.st_mobile_no = StudentMobileNo
            student.st_email_id = StudentMailID
            student.st_aadhar_no = aadhar_no
            student.st_extracurr_activity = st_eactivity
            student.st_father_name = father_name
            student.st_mother_name = mother_name
            student.st_father_occupation = fatherjob
            student.st_mother_occupation = motherjob
            student.st_father_income = parent_income
            student.st_mother_income = mother_income
            student.st_father_mobile_no = parent_mobile_no
            student.st_mother_mobile_no = mother_mobile_no
            student.st_father_pan = parent_pan
            student.st_mother_pan = mother_pan
            student.st_father_email_id = parent_email
            student.st_mother_email_id = mother_email
            student.st_parent_address = pmtaddress
            student.st_parent_address_city = pmtaddress_city
            student.st_parent_address_district = pmtaddress_district
            student.st_parent_address_state_id = pmtaddress_state
            student.st_parent_address_pincode = pmtaddress_pincode
            student.st_postal_address = postaladdress
            student.st_postal_address_city = postaladdress_city
            student.st_postal_address_district = postaladdress_district
            student.st_postal_address_state_id = postaladdress_state
            student.st_postal_address_pincode = postaladdress_pincode
            student.st_local_guardian_addr = st_gaddress
            student.st_guardian_mobile_no = st_gmobno
            student.st_health_issues = st_healthissues
            student.st_guardian_email = st_gemail
            student.st_total_fees = TotalFeePaid
            student.st_rt_no = RtChallanNo
            student.st_adm_date = RtChallanDate
            student.last_edited_by = request.user.username
            student.last_edited_time = datetime.datetime.now()
            student.save()

            try: 
                doc_uid = request.POST.get('st_id')
                doc_details = Document_Details.objects.get(doc_uid = doc_uid)
                doc_details.alt_order_copy = AllotmentOrdCopy
                doc_details.st_10th_marks_card = x_MarksCardCopy
                doc_details.st_12th_marks_card = StudyCertificate
                doc_details.st_income_certificate = IncomeCertificate
                doc_details.st_dip_marks_card = dip_MarksCardCopy
                doc_details.st_degree_certificate = deg_certCopy
                doc_details.st_tulu_certificate = LinguisticCertificate
                doc_details.st_eligibility_certificate = Eligcertificate
                doc_details.st_migration_certificate = Migcertificate
                doc_details.st_transfer_certificate = TransferCertificate
                doc_details.st_aadhar_card = AadharCard
                doc_details.st_pan_card = PanCard
                doc_details.save()
            except:
                pass           
            try: 
                pg_uid = request.POST.get('st_id')
                pacad_pg = Previous_Academic_Details_PG.objects.get(pg_uid_id = pg_uid)
                pacad_pg.pg_pacad_10th_board = pg_x_board
                pacad_pg.pg_pacad_10th_reg_no = pg_x_regno
                pacad_pg.pg_pacad_10th_pass_month = pg_x_pass_month
                pacad_pg.pg_pacad_10th_pass_year = pg_x_pass_year
                pacad_pg.pg_pacad_10th_total_marks_cgpa = pg_x_marks
                pacad_pg.pg_pacad_10th_percentage_cgpa = pg_x_percentage
                pacad_pg.pg_pacad_10th_class_obtained = pg_10th_class
                pacad_pg.pg_pacad_12th_board = pg_xii_board
                pacad_pg.pg_pacad_12th_reg_no = pg_xii_regno
                pacad_pg.pg_pacad_12th_pass_month = pg_xii_month
                pacad_pg.pg_pacad_12th_pass_year = pg_xii_passyr    
                pacad_pg.pg_pacad_12th_total_marks = pg_xii_marks
                pacad_pg.pg_pacad_12th_percentage = pg_xii_percentage
                pacad_pg.pg_pacad_12th_class_obtained = pg_12th_class
                pacad_pg.pg_pacad_degree_university = pg_degree
                pacad_pg.pg_pacad_degree_reg_no = pg_degreeregno
                pacad_pg.pg_pacad_degree_pass_month = pg_degreepass_month
                pacad_pg.pg_pacad_degree_pass_year = pg_degreepass_year
                pacad_pg.pg_pacad_degree_percentage_cgpa = pg_degreepercent
                pacad_pg.pg_pacad_be_percentage_5_8 = pg_deg_5_8_percent
                pacad_pg.pg_pacad_degree_class_obtained = pg_degree_class

                pacad_pg.save()

            except:
                pass

            try:
                pgcet_uid = request.POST.get('st_id')
                pgcet_admission_pg = PGCET_Admission_Details_PG.objects.get(pgcet_uid = pgcet_uid)
                pgcet_admission_pg.pgcet_order_no = pg_AdmissionNo
                pgcet_admission_pg.pgcet_no = pg_CETNo
                pgcet_admission_pg.pgcet_rank = pg_CETRank
                pgcet_admission_pg.pgcet_cat_claimed = pg_CategoryClaimed
                pgcet_admission_pg.pgcet_cat_allotted = pg_CategoryAllotted
                pgcet_admission_pg.pgcet_allot_date = pg_altdate
                pgcet_admission_pg.pgcet_kea_fees_paid = pg_cet_kea_feepaid
                pgcet_admission_pg.pgcet_college_fees_paid = pg_cet_college_feepaid
                pgcet_admission_pg.pgcet_total_fees_paid = pgcet_totalfees
                pgcet_admission_pg.pgcet_challan_date = pgcet_challandate
                pgcet_admission_pg.pgcet_challan_no = pg_challanno
                pgcet_admission_pg.save()
            except:
                pass

            try:
                mgmt_pg_uid = request.POST.get('st_id')
                mgmt_admission_pg = MGMT_Admission_Details_PG.objects.get(mgmt_pg_uid = mgmt_pg_uid)
                mgmt_admission_pg.mgmt_pg_rank = pg_MGMTRank
                mgmt_admission_pg.mgmt_exampg = mg_pg
                mgmt_admission_pg.mgmt_pg_college_fees_paid = pg_MGMTCollegeFeedPaid
                mgmt_admission_pg.mgmt_pg_challan_date = pg_MGMTChallandate
                mgmt_admission_pg.mgmt_pg_challan_no = pg_MGMTChallanNo
                mgmt_admission_pg.save()
            except:
                pass
                
            with transaction.atomic():
                    if student.is_dirty():
                        dirty = 1
                        dirty_fields = student.get_dirty_fields().keys()
                        student.save(update_fields=dirty_fields)
                        print(student._dirty_fields())

                    if doc_details.is_dirty():
                        dirty = 1
                        dirty_fields = doc_details.get_dirty_fields().keys()
                        doc_details.save(update_fields=dirty_fields)

                    if pacad_pg.is_dirty():
                        dirty = 1
                        dirty_fields = pacad_pg.get_dirty_fields().keys()
                        pacad_pg.save(update_fields=dirty_fields)

                    if pgcet_admission_pg.is_dirty():
                        dirty = 1
                        dirty_fields = pgcet_admission_pg.get_dirty_fields().keys()
                        pgcet_admission_pg.save(update_fields=dirty_fields)

                    if mgmt_admission_pg.is_dirty():
                        dirty = 1
                        dirty_fields = mgmt_admission_pg.get_dirty_fields().keys()
                        mgmt_admission_pg.save(update_fields=dirty_fields)
            

            if dirty : 
                messages.success(request, "Student Updated Successfully with UID" + student.st_uid)
            else:
                messages.success(request, "No changes were made with UID" + student.st_uid)
        context={"st_id": student.st_id}
        return render(request,"add_pg.html",context=context)

def about_us(request):
    return render(request,"about_us.html")

def admindashboard(request):
    return render(request,"admin_home.html")

def StudentHome(request): 
    return render(request,"StudentHomePage.html")

def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        print("kkk")
        username=request.POST.get("txtusrname")
        password=request.POST.get("txtpasswd")
        print(username,password)
        user=EmailBackEnd.authenticate(request,username=request.POST.get("txtusrname"),password=request.POST.get("txtpasswd"))
        if user!=None:
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect(reverse('LoginDashBoard'))
        else:
            messages.error(request,"Invalid User Name or Password")
            return redirect('/')
            
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

def SearchStudent(request):
    department = Department.objects.all()
    rel_tbl = Religion.objects.all()
    if request.POST:
        Branch = request.POST['st_branch']
        Uid = request.POST['st_uid']
        Name = request.POST['st_name']
        Usn = request.POST['st_usn']
        if Branch == "0" and Uid == "" and Name == "" and Usn == "":
            messages.error(request, "Please Enter Atleast One Field to Search")
        else:
            SearchParm1 = Student_Details.objects.filter(Q(st_name__icontains = Name) & Q(st_uid__icontains = Uid))
            SearchParm2 = Student_Details.objects.filter(st_branch_applied_id = int(Branch))
            if Name == '':
                c1 = ~Q(st_name__icontains = Name)
            else:
                c1 = Q(st_name__icontains = Name)
            
            if Uid == '':
                c2 = ~Q(st_uid__icontains = Uid)
            else:
                c2 = Q(st_uid__icontains = Uid)    

            c3 = Q(st_branch_applied_id = int(Branch))
            SearchParm = Student_Details.objects.filter(c1 | c2 | c3)
            if not SearchParm.exists():
                messages.error(request,"Student Details Not Found")
            return render(request,"view_student.html",{'student':SearchParm,'department':department,'rel_tbl':rel_tbl})
        return render(request,"view_student.html",{'department':department,'rel_tbl':rel_tbl})
        
    else:
        return render(request,"view_student.html",{'department':department,'rel_tbl':rel_tbl})
def reportPage(request):
    if request.method != 'POST':
        student_details = Student_Details.objects.all()
        field_names = [
            "ID", "Profile pic", "UID", "USN Old", "USN New",
            "Name", "Branch", "Academic Year", "Admission Date", "Admission Quota", "Medium",
            "DOB", "Gender", "Locality", "Blood Group", "Place of Birth",
            "Mother Tongue", "Nationality", "Religion", "Caste", "Sub Caste",
            "Category", "Mobile No", "Email ID", "Aadhar No", "Extracurricular Activity",
            "Father Name", "Mother Name", "Father Occupation", "Mother Occupation", "Father Income",
            "Mother Income", "Father Mobile No", "Mother Mobile No", "Father PAN", "Mother PAN",
            "Father Email ID", "Mother Email ID", "Parent Address", "Parent Address City", "Parent Address District",
            "Parent Address State", "Parent Address Pincode", "Postal Address", "Postal Address City", "Postal Address District",
            "Postal Address State", "Postal Address Pincode", "Local Guardian Address", "Guardian Mobile No", "Health Issues",
            "Guardian Email", "Admission Date", "Total Fees", "RT No", "Created by",
            "Created Time", "Last Edited By", "Last Edited Time"
        ]
        return render(request, "report.html", {"student_details": student_details, "field_names": field_names})
    
    else:
        print("kkkk")
        selected_columns = []
        for key, value in request.POST.items():
            if key.startswith('column_'):
                selected_columns.append(value)
        
        # Convert selected_columns to a tuple to use with values() method in queryset
        selected_columns = tuple(selected_columns)

        # Query to fetch data based on selected columns
        student_details = Student_Details.objects.values(*selected_columns)
        
        # You can further process the fetched data as needed
        
        return render(request, "report.html", {"student_details": student_details})
def mapUSNPage(request):
    userName=CustomUser.objects.get(id=request.user.id)
    return render(request,"student_usn_mapping.html",{'department':Department.objects.all() ,'st_list':Student_Details.objects.all(),'username':userName,'academic_year_tbl': AcademicYear.objects.all()})

# For USN mapping - code to handle ajax request
def load_st_uid(request):
    st_list = None
    acadyear= request.GET.get('acad_year')
    print(acadyear,"pppppppppppppppppppppppp")
    branch = request.GET.get("branch")
    sem = request.GET.get("sem")
    print(acadyear)
    st_list = Student_Details.objects.filter(st_acad_year_id=acadyear,st_branch_applied_id=branch).order_by('st_uid').values('st_uid','st_name')[:30]
    
    return render(request, "student_usn_mapping.html",{'st_list':st_list})
    

def allot_usn(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        acadyear = None
        pendling_list = None
        branch = None
        sem = None
        try:
            acadyear = request.POST.get("acad_year")
            branch = request.POST.get("st_branch_applied")
            sem = request.POST.get("sem")
            uid_usn_list = request.POST.getlist("st_uid")
            mapped_usn = request.POST.getlist('mapped_usn')
        except Academic_Calendar.DoesNotExist:
            messages.error(request, "Please check Academic Year and Semester")
            return render(request,"student_usn_mapping.html") 
        except Exception as e:
            print(e)
            messages.error(request, "Mapping of USN failed. Please Retry!")
            return render(request,"student_usn_mapping.html")  
        
        try:
            btn_value = request.POST["btn_clicked"]
            allot_failed_list = []
            if btn_value == "register":   
                count = 0
                i=0
                for st in uid_usn_list:
                    st_uid = st
                    usn = mapped_usn[i]
                    if len(usn)==10: # placeholder for regex check
                        cnt = Student_Details.objects.filter(st_uid=st_uid).update(st_usn_new=usn,st_usn_old=usn)
                    else:
                        cnt = 0
                        allot_failed_list.append(st_uid)
                    count = count+cnt
                    i=i+1
                pendling_list = Student_Details.objects.filter(st_acad_year=acadyear,st_sem_admitted=sem,st_usn_old__isnull=True,st_branch_applied=branch)
                if count>0:
                    if allot_failed_list: # if allot_failed_list is NOT empty
                        messages.warning(request, "Allotted USN for "+str(count)+" students! "+str(len(allot_failed_list))+" failed.")
                    else:
                        messages.success(request, "Allotted USN for "+str(count)+" students! "+str(pendling_list.count())+" pending.")
                else:
                    messages.error(request,"USN Allotment failed!")
                return mapUSNPage(request)    
        except IntegrityError:
            messages.error(request, "Error! USN needs to be unique.")
            return mapUSNPage(request)
        except Exception as e:                
            return mapUSNPage(request)
from .forms import UploadFileForm
import pandas as pd
def handle_uploaded_file(file):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(file)
    
    # Ensure the column names match the headers in your Excel file
    for index, row in df.iterrows():
        name = row['name']
        usn = row['usn']
        try:
            # Find the student by name
            student = Student_Details.objects.get(st_name=name)
            # Update the st_uid with usn value
            student.st_uid = usn
            student.save()
        except Student_Details.DoesNotExist:
            # Handle the case where the student does not exist
            print(f"Student with name {name} not found")

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            messages.success(request, 'File uploaded and processed successfully.')
            return redirect('upload_file') 
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

