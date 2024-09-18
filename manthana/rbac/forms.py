from admission.models import CustomUser
from .models import RightCategory, RightDetails, RightType
from django import forms
from django.forms import ChoiceField

class RightDetailsForm(forms.Form):
    abbr=forms.CharField(label="Right Abbreviation", max_length=50,widget=forms.TextInput(attrs={"class":"form-control "}))
    desc=forms.CharField(label="Right Description", max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))

    cat_list = []
    try:
        cat = RightCategory.objects.all()
        for c in cat:
            small_cat = (c.category,c.desc)
            cat_list.append(small_cat)
    except:
        cat_list = []

    category=forms.ChoiceField(label="Right Category",choices=cat_list,widget=forms.Select(attrs={"class":"form-control"}))
    
    type_list = []
    try:
        type = RightType.objects.all()
        for t in type:
            small_type = (t.type,t.desc)
            type_list.append(small_type)
    except:
        type_list = []

    type=forms.ChoiceField(label="Right Type",choices=type_list,widget=forms.Select(attrs={"class":"form-control"}))

class EditRightDetailsForm(forms.Form):
    abbr=forms.CharField(label="Right Abbreviation", max_length=50,widget=forms.TextInput(attrs={"class":"form-control "}))
    desc=forms.CharField(label="Right Description", max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))

    cat_list = []
    try:
        cat = RightCategory.objects.all()
        for c in cat:
            small_cat = (c.category,c.desc)
            cat_list.append(small_cat)
        
    except Exception as e:
        cat_list = []
    
    category=forms.ChoiceField(label="Right Category",choices=cat_list,widget=forms.Select(attrs={"class":"form-control"}))
    
    type_list = []
    try:
        type = RightType.objects.all()
        for t in type:
            small_type = (t.type,t.desc)
            type_list.append(small_type)
    except:
        type_list = []

    type=forms.ChoiceField(label="Right Type",choices=type_list,widget=forms.Select(attrs={"class":"form-control"}))

class UserRightsForm(forms.Form):
    cuser_list = []
    try:
        cuser = CustomUser.objects.all()
        for c in cuser:
            small_cuser = (c.id,c.username)
            cuser_list.append(small_cuser)
    except:
        cuser_list = []

    user=forms.ModelChoiceField(label="User Name",queryset=CustomUser.objects.all(),widget=forms.Select(attrs={"class":"form-control"}))
    
    rdesc_list = []
    try:
        rdesc = RightDetails.objects.all()
        for r in rdesc:
            small_rdesc = (r.id,r.desc)
            rdesc_list.append(small_rdesc)
    except:
        rdesc_list = []
    right=forms.ModelChoiceField(label="Role Type",queryset=RightDetails.objects.all(),widget=forms.Select(attrs={"class":"form-control"}))