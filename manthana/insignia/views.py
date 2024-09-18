import tempfile
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
from insignia.models import *
from django.db import transaction
from django.template.loader import render_to_string
from django.db.models import Max
from django.shortcuts import render
import datetime
#from .forms import UploadFileForm

def hello():
    pass
def hello1(request):

    return render(request,"ADD.html",{'eve': Event.objects.all()})  
    

def reg1(request):
    if request.method!="POST":
        return HttpResponseRedirect('addforevents')
        
    else:
        print("bjhdfjjh")
        email=request.POST.get("email")  
        College = request.POST.get("CName")
        competet = request.POST.get("cars")
        nop = request.POST.get("nop")
        namepart = request.POST.get("nameop")
        leader = request.POST.get("headp")
        phone = request.POST.get("phone")
        pay = request.POST.get("payment")
        type1 = Event.objects.get(id=competet).type
        name1 = Event.objects.get(id=competet).name
        pay_id=request.POST.get("ho")
        
        with transaction.atomic():
            reg =   List.objects.create(eventid="0", email = email, college = College, names = namepart, 
            leader=leader, number = phone, event = Event.objects.get(id=competet), numberofpar = nop, payment = pay ,pay_id=pay_id)
        
        number=reg.id
        x=str(datetime.datetime.now())
        x=x[2:4]
        print(x)
        if type1==1:
            id=x+"_INS_ON_CENT"+name1[0:3].upper()+"-"+str(number)
        elif type1==2:
            id=x+"_INS_ON_DEP_"+name1[0:3].upper()+"-"+str(number)
        else:
            id=x+"_INS_ON_CUL_"+name1[0:3].upper()+"-"+str(number)
        stu=List.objects.get(id=number)
        stu.eventid=id
        stu.save()
        messages.success(request, "Registration successful with id "+id)
        

        return render(request,"ADD.html")   
def part(request):
    
    return render(request,"partgui.html",{'eve': Event.objects.all()}) 
def reglist(request):
    num=request.POST.get("eventName") 
    name=Event.objects.get(id=num).name
    hello=List.objects.filter(event=Event.objects.get(id=num))
    day=Event.objects.get(id=num).day
    return render(request,"participatlist.html",{'num':hello,'name':name,'day':day})       
def WINNER(request):
    return render(request,"WINNERS.html",{'eve': Event.objects.all()}) 
def win(request):
    event=request.POST.get("eventName")
    eve=Event.objects.get(id=event)
    no=request.POST.get("numberOfWinners")
    win=request.POST.get("winnersContainer")
    print(win)
    for i in range (1,int(no)+1):
        hello=request.POST.get("winner"+str(i))
        stu=List.objects.get(eventid=hello,event=Event.objects.get(id=event))
        reg =   winners.objects.create(college = stu.college, names = stu.names, number = stu.number, 
        event = eve, now = no, winner = i ,inid=hello)
    messages.success(request, "Winners added successful")

    return render(request,"WINNERS.html",{'eve': Event.objects.all()}) 
    
def winl(request):
    x=Department.objects.all()
    
    print(x)
    return render(request,"winnerlist.html",{'eve': Department.objects.all()})    
def win_list(request):
    temp=0
    day_printed=0
    depo=request.POST.get("eventName")
    if depo=="13":
        temp=1
    if depo=="14":
        temp=3
    if depo == "13" or depo == "14":
        depo=0
        stu=Event.objects.filter(dep=depo,type=temp)
    else:
        stu=Event.objects.filter(dep=depo)

    print(stu)
    listo=[]
    event=[]
    days=[]
    for i in stu:
        print("")
        print(i.type)
        if i.type=="2":

            print("i am here")
            print(i.id)
            hello=list(winners.objects.filter(event=i.id))
            if(winners.objects.filter(event=i.id)):
                print(hello)
                listo.append(hello)
                event.append(i)
                days.append(i.day)

        elif i.type=="1":

            print("i am here")
            print(i.id)
            hello=list(winners.objects.filter(event=i.id))
            if(winners.objects.filter(event=i.id)):
                print(hello)
                listo.append(hello)
                event.append(i)
                days.append(i.day) 

        elif i.type=="3":

            print("i am here")
            print(i.id)
            hello=list(winners.objects.filter(event=i.id))
            if(winners.objects.filter(event=i.id)):
                print(hello)
                listo.append(hello)
                event.append(i)
                days.append(i.day)   
    print(listo)
    length=len(listo)
   


    if temp==1:
        return render(request,"winn_list.html",{'eve':"Centralized",'list':zip(listo,event),"l":int(length),'list2':zip(listo,event)}) 
    elif temp==3:
        return render(request,"winn_list.html",{'eve':"Cultural",'list':zip(listo,event),"l":int(length),'list2':zip(listo,event)}) 
    else:
        return render(request,"winn_list.html",{'eve':Department.objects.get(dept_id=depo).dept_abbr,'list':zip(listo,event),"l":int(length),'list2':zip(listo,event),"day_printed":day_printed}) 
 
def addev(request):
    return render(request,"Addevent.html",{'eve': Department.objects.all()})  
def addeven(request):
    if request.method!="POST":
        return HttpResponseRedirect('addeven')
        
    else:
        
        name=request.POST.get("eventName")  
        type=request.POST.get("eventType")  
        dep=request.POST.get("departmentName") 
        day=request.POST.get("day") 
        print(name)
        if dep == None:
            dep=0
        reg =   Event.objects.create(name = name, type = type, dep = dep,day=day )
        messages.success(request, "Event added successful")
        return render(request,"Addevent.html") 
def feedback1(request):
    if request.method!="POST":
        return render(request,"FEEDBACK.html",{'eve': Event.objects.all()})
    else:
        name=request.POST.get("Name")  
        email=request.POST.get("email") 
        overall=request.POST.get("overall_rating")
        eve=request.POST.get("eventName")
        q1=request.POST.get("question1")
        q2=request.POST.get("question2")
        q3=request.POST.get("question3")
        q4=request.POST.get("question4")
        q5=request.POST.get("question5")
        q62=request.POST.get("question6")
        q7=request.POST.get("question7")
        q8=request.POST.get("question8")
        full=request.POST.get("feedback")

        print(name,type)
        feedback.objects.create(names=name, email = email, event = Event.objects.get(id=eve), overall = overall, 
        q1 = q1, q2 = q2, q3 = q3, q4 = q4, q5 = q5 ,q6 = q62, q7 = q7, q8 = q8, response = full)
        messages.success(request, " Thank you for your valuable feedback.")
        return render(request,"FEEDBACK.html",{'eve': Event.objects.all()})
def dump123(request):
    if request.method!="POST":
        return render(request,"dump.html",{'eve': Event.objects.all()})
    else:
            file = request.FILES['excel_file']
            df1 = pd.read_excel(file,skiprows=1)
            df1 = df1.dropna()
            df=df1.values.tolist()
            print(type(df[0]))
            event=request.POST.get("cars")
            #print(df1)s
            #print (df)
            grouped_data={} 
            hello=List.objects.filter(event=Event.objects.get(id=event))
            id_values_list = hello.values_list('eventid', flat=True)

            # Convert values to strings
            id_values_list = [int(value) for value in id_values_list]
            print(id_values_list)
            print(df)
            for row in df:
                group_id, name, *_ = row
                if group_id not in id_values_list:
                    
                    if group_id not in grouped_data:
                        grouped_data[group_id]={'names':[],'college':None,'phone':None,'event':None}
                        grouped_data[group_id]['college'] = row[5]
                        grouped_data[group_id]['phone']= row[4]
                        grouped_data[group_id]['event']=event

                    grouped_data[group_id]['names'].append(name)
                    
                    #print(grouped_data)
                    
                else:
                    pass
            final_result=[]
            for group_id, group_info in grouped_data.items():
                names=','.join(group_info['names'])
                final_result.append([group_id, names, group_info['college'],group_info['phone'],group_info['event']])
              
            for i in final_result: 
                reg =   List.objects.create(eventid=i[0], email = 'none', college = i[2], names = i[1],leader='none', number = i[3], event = Event.objects.get(id=i[4]), numberofpar = 'none', payment = 'none' ,pay_id='none')       
            messages.success(request, "done")
            return render(request, 'dump.html', {'df': df})
# Create your views here.
def addev(request):
    return render(request,"Addevent.html",{'eve': Department.objects.all()})  
def report(request):
        list=[0]*14
        other=[0]*14
        h=0
        alllist=[0,0]
        centre=[0,0]
        culture=[0,0]
        winn=[0,0]
        all=List.objects.all()
        for i in all:
            sto=i.college
            sub="sdm"
            if sub.casefold() in sto.casefold():
                alllist[0]=alllist[0]+1
            else:
                alllist[1]=alllist[1]+1

        for i in range(1,13):
            h=h+1
            if i==8:
                continue
            else:
                hu=Event.objects.filter(type="2",dep=str(i))
                print("hu",hu)
               
                for i in hu:
                    li=List.objects.filter(event=Event.objects.get(id=i.id))
                    print(li)
                    for j in li:
                        sto=j.college
                        sub="sdm"
                        if sub.casefold() in sto.casefold():
                            list[h]=list[h]+1
                        else:
                            other[h]=other[h]+1
        hu1=Event.objects.filter(type="1")
        print("hu",hu)
               
        for i in hu1:
            li=List.objects.filter(event=Event.objects.get(id=i.id))
            print(li)
            for j in li:
                sto=j.college
                sub="sdm"
                if sub.casefold() in sto.casefold():
                    centre[0]=centre[0]+1
                else:
                    centre[1]=centre[1]+1
        hu2=Event.objects.filter(type="3")
        print("hu",hu)
               
        for i in hu2:
            li=List.objects.filter(event=Event.objects.get(id=i.id))
            print(li)
            for j in li:
                sto=j.college
                sub="sdm"
                if sub.casefold() in sto.casefold():
                    culture[0]=culture[0]+1
                else:
                    culture[1]=culture[1]+1
        
        hu3=winners.objects.all()
               
        for i in hu3:
            sto=i.college
            sub="sdm"
            if sub.casefold() in sto.casefold():
                winn[0]=winn[0]+1
            else:
                winn[1]=winn[1]+1

        return render(request,"report.html",{'list': list,'other':other,'all':alllist,'cul':culture,'cen':centre,'winn':winn}) 


