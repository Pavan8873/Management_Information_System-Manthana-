from django import forms
from captcha.fields import CaptchaField

class CaptchaForm(forms.Form):
   captcha=CaptchaField()

class UploadFileForm(forms.Form):
    file = forms.FileField()