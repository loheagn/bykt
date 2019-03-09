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
