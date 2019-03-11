from django import forms
from captcha.fields import CaptchaField

form_style = {'class': 'form-control'}


class LoginForm(forms.Form):
    studentID = forms.IntegerField(label='学号', widget=forms.TextInput(attrs=form_style))
    password = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput(attrs=form_style))
    captcha = CaptchaField(label='验证码')


class RegisterForm(forms.Form):
    studentID = forms.IntegerField(label='学号', widget=forms.TextInput(attrs=form_style))
    name = forms.CharField(label='姓名', max_length=256, widget=forms.TextInput(attrs=form_style))
    password1 = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput(attrs=form_style))
    password2 = forms.CharField(label='确认密码', max_length=256, widget=forms.PasswordInput(attrs=form_style))
    image = forms.ImageField(label='照片')
    captcha = CaptchaField(label='验证码')


class VisitForm(forms.Form):
    location = forms.IntegerField(label='位置', widget=forms.TextInput(attrs={"id": "location", "type": "text", "class": "form-control", "placeholder": "请输入参观地点", "style": "width: 40%"}))
    image = forms.ImageField(label='照片', widget=forms.FileInput(attrs={"style": "display:none"}))
    v_time = forms.DateField(label='参观时间', widget=forms.TextInput(attrs={"type": "text", "class": "form-control", "placeholder": "请选择参观日期", "style": "width: 25%", "readonly": "readonly"}))
