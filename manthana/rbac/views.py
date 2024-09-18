from django.shortcuts import render
from django.contrib import messages
from django.urls.base import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from rbac.context_processors import categories_processor
from .forms import EditRightDetailsForm, RightDetailsForm, UserRightsForm
from .models import RightCategory, RightDetails, RightType, UserRights
from admission.models import CustomUser
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import redirect, render


# Create your views here.
@login_required
def add_rights(request):
    form=RightDetailsForm()
    RightsInfo = RightDetails.objects.all()
    return render(request,"add_rights.html",{"form":form,'RightsInfo':RightsInfo})

def assignRights(request):
    form=UserRightsForm()
    return render(request,"assign_rights.html",{"form":form})


def CreateRights(request):
    if request.method!="POST":
        return render(request,"add_rights.html")
    else:
        form=RightDetailsForm(request.POST)
        if form.is_valid():
            abbr=form.cleaned_data["abbr"]
            desc=form.cleaned_data["desc"]
            category=form.cleaned_data["category"]
            type=form.cleaned_data["type"]

            category=RightCategory.objects.get(category=int(category))
            type=RightType.objects.get(type=int(type))

            admin_pk_id=CustomUser.objects.get(username="admin")
            try:
                checkrights=RightDetails.objects.filter(abbr=abbr,details=desc,category=category,type=type).count()
                if checkrights == 0:
                    right=RightDetails.objects.create(abbr=abbr,details=desc,category=category,type=type)
                    admin=UserRights.objects.create(user=admin_pk_id,right=right)
                    messages.success(request,"Right Added Successfully")
                else:
                    messages.error(request,"Right Already Exists")
                return HttpResponseRedirect(reverse("AddRights"))
            except Exception as e:
                messages.error(request,"Failed to Add Rights")
                print(e)
                return HttpResponseRedirect(reverse("AddRights"))
        else:
            return render(request,"add_rights.html")

@login_required
def edit_rights(request,right_id):
    rights=RightDetails.objects.get(id=right_id)
    form=EditRightDetailsForm()
    form.fields['abbr']=rights.abbr
    form.fields['desc'].initial=rights.details
    form.fields['category'].initial=rights.category
    form.fields['type'].initial=rights.type
    context={'form':form,'right_id':right_id}
    return render(request,"edit_rights.html", context=context)
   

@login_required
def EditRights(request):
    right_id = int(request.POST.get('right_id'))
    if request.method!="POST":
        return render(request,"add_rights.html")
    else:
        form=EditRightDetailsForm(request.POST)
        if form.is_valid():
            abbr=form.cleaned_data["abbr"]
            desc=form.cleaned_data["desc"]
            category=form.cleaned_data["category"]
            type=form.cleaned_data["type"]

            category = RightCategory.objects.get(desc=category)
            type = RightType.objects.get(desc=type)
            
            try:
                rightcnt=RightDetails.objects.filter(abbr=abbr,details=desc,category=category.category,type=type.type).count()
                if rightcnt == 0:
                    right = RightDetails.objects.get(id = right_id)
                    right.abbr = abbr
                    right.details = desc
                    right.category = category.category
                    right.type = type.type
                    right.save()
                    messages.success(request,"Right Updated Successfully")
                    return HttpResponseRedirect(reverse("EditRights",kwargs={'right_id':right_id}))
                else:
                    messages.error(request,"Right Already Exists")
                    return HttpResponseRedirect(reverse("EditRights", kwargs={'right_id':right_id}))
            except Exception as e:
                
                messages.error(request,"Failed to Update Right")
                return HttpResponseRedirect(reverse("EditRights",kwargs={'right_id':right_id}))
        else:
            context={'right_id':right_id}
            return render(request,"edit_rights.html",context=context)

def AssignRights (request):
    if request.method!="POST":
        return render(request,"assign_rights.html")
    else:
        form=UserRightsForm(request.POST)
        if form.is_valid():
            user=form.cleaned_data["user"]
            right=form.cleaned_data["right"]
            try:
                checkrights=UserRights.objects.filter(user=user,right=right).count()
                if checkrights == 0:
                    right=UserRights.objects.create(user=user,right=right)
                    messages.success(request,"Right Assigned Successfully")
                else:
                    messages.error(request,"Right Already Exists")
                return HttpResponseRedirect(reverse("assignRights"))
            except Exception as e:
                messages.error(request,"Failed to Assign Rights")
                print(e)
                return HttpResponseRedirect(reverse("assignRights"))
        else:
            return render(request,"assign_rights.html")

@login_required
def LoginDashBoard(request):  
    return render(request,"admin_home.html")
   

@login_required
def change_password(request):
    form=PasswordChangeForm(request.user, request.POST)
    return render(request,"change_password.html",{"form":form})

@login_required
def ChangePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user, request.POST)
    return render(request, 'change_password.html', {'form': form})

