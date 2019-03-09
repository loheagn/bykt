from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import Student, ProfileImage
from .forms import LoginForm, RegisterForm
from .face_recognation import *
import time
import numpy


# Create your views here.


def index(request):
    is_login = request.session.get('is_login', None)
    return render(request, 'main/index.html', locals())


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        message = ""
        if login_form.is_valid():
            studentID = login_form.cleaned_data['studentID']
            password = login_form.cleaned_data['password']
            try:
                student = Student.objects.get(studentID=studentID)
                if password == student.password:
                    request.session['studentID'] = student.studentID
                    request.session['id'] = student.id
                    request.session['name'] = student.name
                    request.session['is_login'] = True
                    return redirect('/index/')
                else:
                    message = "密码错误！"
            except:
                message = "学号错误！"
    login_form = LoginForm(request.POST)
    return render(request, 'main/login.html', locals())


def register(request):
    request.session.flush()
    if request.method == 'POST':
        register_form = RegisterForm(request.POST, request.FILES)
        message = "请再次仔细检查要填写的内容！"
        if register_form.is_valid():
            studentID = register_form.cleaned_data['studentID']
            name = register_form.cleaned_data['name']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            image = register_form.files['image']
            same_id = Student.objects.filter(studentID=studentID)
            if same_id:
                jump_to_login = True
                request.session.flush()
                return render(request, 'main/register.html', locals())
            if password2 != password1:
                message = "两次输入的密码不同！"
                return render(request, 'main/register.html', locals())

            # 如果一切OK，那么创建用户并保存
            new_student = Student()
            new_student.studentID = int(studentID)
            new_student.name = name
            new_student.password = password1
            new_profile_image = ProfileImage(image=image)
            new_profile_image.save()
            file_name = "/home/loheagn/boyasite/uploads/images/profile/" + image.name
            new_student.face_array = '/home/loheagn/boyasite/uploads/face_arrays/' + str(time.time()).split('.')[0] + '.npy'
            numpy.save(new_student.face_array, get_src_vectors_from_someone_single_image(file_name))
            new_student.save()
            return redirect('/login/')
        else:
            return HttpResponse("校验失败")
    register_form = RegisterForm()
    return render(request, 'main/register.html', locals())


def logout(request):
    request.session.flush()
    return render(request, 'main/logout.html')
