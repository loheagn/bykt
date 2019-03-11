from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import Student, ProfileImage, TmpImage, VisitImage
from .forms import LoginForm, RegisterForm, VisitForm
from .face_recognation import *
import time
import numpy
from gensim import corpora, models, similarities
from urllib.request import quote, urlopen
import lxml.html
import jieba
import re
from . import models as Models
import datetime


# Create your views here.
etree = lxml.html.etree


def test(request):
    return render(request, 'main/test.html')


def index(request):
    is_login = request.session.get('is_login', None)
    sid = request.session['id']
    student = Student.objects.get(pk=sid)
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
            image.name = image.name + str(time.time()).replace('.', '')
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




def profile(request):
    pass


def visit_show(request):
    alert = request.session.get('visit_alert')
    student = Student.objects.get(pk=request.session.get('id'))
    visit_images = VisitImage.objects.filter(student=student)
    return render(request, 'main/visit_show.html', locals())


def visit(request):
    form_flag = False
    student = Student.objects.get(pk=request.session.get('id'))
    visit_images = VisitImage.objects.filter(student=student)
    if request.method == 'POST':
        # 获取上传的表格数据
        time_value = request.POST.get('v_time')
        v_time = datetime.datetime.strptime(time_value, '%Y-%M-%d').date()
        location = request.POST.get('location')
        image = request.FILES.get('image')
        # image.name = image.name + str(time.time()).replace('.', '')
        if v_time and location and image:
            test_v_time = VisitImage.objects.filter(v_time=v_time)
            if test_v_time:
                message = "请勿上传同一天的参观照片！"
                form_flag = True
                visit_form = VisitForm()
                return render(request, 'main/visit.html', locals())
            test_location = VisitImage.objects.filter(location=location)
            if test_location:
                message = "请勿上传同一地点的参观照片！"
                form_flag = True
                visit_form = VisitForm()
                return render(request, 'main/visit.html', locals())

            old_face_array = numpy.load(student.face_array)

            new_tmp_image = TmpImage(image=image)
            new_tmp_image.save()
            file_name = "/home/loheagn/boyasite/uploads/images/tmp/" + image.name
            new_face_array = get_dst_vectors_from_single_image(file_name)
            tmp_new_string_array = VisitImage.objects.filter(string_array=str(new_face_array.tolist()))
            if tmp_new_string_array:
                message = "请勿上传同一张照片！"
                form_flag = True
                visit_form = VisitForm()
                return render(request, 'main/visit.html', locals())
            temp = new_face_array - old_face_array
            e = numpy.linalg.norm(temp, axis=1, keepdims=True)
            min_distance = e.min()
            alert = False
            if min_distance > 0.1 and min_distance < 0.5:
                new_visit_image = VisitImage()
                new_visit_image.image = image
                new_visit_image.similar = min_distance
                new_visit_image.v_time = v_time
                new_visit_image.location = location
                new_visit_image.student = student
                new_visit_image.is_ok = True
                new_visit_image.string_array = str(new_face_array.tolist())
                new_visit_image.save()
                student.visit = student.visit + 1
                student.save()
                alert = True
            else:
                alert = False
            request.session['visit_alert'] = alert
            return redirect('/visit_show/')
        else:
            form_flag = True
            message = "请再次仔细检查所填写的内容！"
            visit_form = VisitForm()
            return render(request, 'main/visit.html', locals())
    else:
        form_flag = True
        visit_form = VisitForm()
        return render(request, 'main/visit.html', locals())

















def cut_text(text, lenth):
    textArr = re.findall('.{'+str(lenth)+'}', text)
    textArr.append(text[(len(textArr)*lenth):])
    return textArr


def get_html(url1):
    ret1 = quote(url1, safe=";/?:@&=+$,", encoding="utf-8")
    res = urlopen(ret1)
    html = res.read().decode('utf-8')
    return html


def get_similarity_rate(all_doc, doc_test):
    p = ',.＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～?????\u3000、〃〈〉《》「」『』【】〔〕〖〗?????〝〞????–—‘’?“”??…?﹏﹑﹔·！？?。''＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～?????\u3000、〃〈〉《》「」『』【】〔〕〖〗?????〝〞????–—‘’?“”??…?﹏﹑﹔·！？?。'
    _doc_test = re.sub("[%s]+" % p, "", doc_test)
    _all_doc = [re.sub("[%s]+" % p, "", doc) for doc in all_doc]
    all_doc_list = []
    for doc in _all_doc:
        doc_list = [word for word in jieba.cut(doc)]
        all_doc_list.append(doc_list)
    doc_test_list = [word for word in jieba.cut(_doc_test)]
    dictionary = corpora.Dictionary([doc_test_list])
    corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]
    doc_test_vec = dictionary.doc2bow(doc_test_list)
    tfidf = models.TfidfModel(corpus)
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))
    sim = index[tfidf[doc_test_vec]]
    if max(sim) < 1e-5 and _all_doc[sim.tolist().index(max(sim))] in _doc_test:
        return [doc_test, all_doc[sim.tolist().index(max(sim))],
                round(len(_all_doc[sim.tolist().index(max(sim))]) / len(_doc_test), 3)]
    return [doc_test, all_doc[sim.tolist().index(max(sim))], round(max(sim), 3)]


def article(request):
    global similarity_rates
    lines = request.GET['article_name']
    org_text = lines
    cc_text = ""
    lines = cut_text(lines, 20)
    header = "http://www.baidu.com/s?wd="
    similarity_rates = []
    for line in lines:
        if (len(line) == 0):
            continue
        html = get_html(header + line)
        et_html = etree.HTML(html)
        # match_texts = et_html.xpath("//*[@id]/div[1]/em")
        urls = et_html.xpath('//*[@id]/h3/a/@href')
        url_no = len(urls)
        match_texts = {}
        for No in range(1, url_no+1):
            matchs = et_html.xpath('//*[@id="%d"]/div[1]/em' % No)
            for m in matchs:
                match_texts[m.text] = No-1
        ems = []
        for m_txt in match_texts:
            ems.append(m_txt)
        try:
            tmp = get_similarity_rate(ems, line)
            match_em = tmp[1]
            tmp.insert(2, urls[match_texts[match_em]])
            similarity_rates.append(tmp)
        except:
            similarity_rates.append([line, str(ems), "无匹配链接", 0])
    for similarity_rate in similarity_rates:
        cc_text += similarity_rate[1]
    c, flag = lcs(org_text, cc_text)
    len_org = len(org_text)
    len_cc = len(cc_text)
    repeat_index = []

    while len_org > 0 and len_cc > 0:
        if flag[len_org][len_cc] == "up":
            len_org = len_org-1
        elif flag[len_org][len_cc] == "left":
            len_cc = len_cc-1
        elif flag[len_org][len_cc] == "ok":
            len_org = len_org - 1
            len_cc = len_cc - 1
            repeat_index.append(len_org)
    authorName = request.GET['authorname']
    articletitle = request.GET['articletitle']
    articlesim = 0.0
    for similarity_rate in similarity_rates:
        articlesim += similarity_rate[3]
    articlesim /= len(similarity_rates)

    Models.Article.objects.create(authorName=authorName, articleTitle=articletitle, articleContent=org_text, articlecopyContent=cc_text, article_copy_rate=articlesim, student_id=request.session['id'] + 1)

    context = {
        'similarity_rates': similarity_rates,
        'org_text': org_text,
        'org_index': repeat_index
    }
    return render(request, 'main/article.html', context=context)


def article_input(request):
    stuID = request.session['id'] + 1
    objs = Models.Article.objects.filter(student_id=stuID).values()
    context = {
       'objs': objs
    }
    return render(request, 'main/article_input.html', context)


def lcs(a, b):
    lena = len(a)
    lenb = len(b)
    c = [[0 for i in range(lenb+1)] for j in range(lena+1)]
    flag = [[0 for i in range(lenb+1)] for j in range(lena+1)]
    for i in range(lena):
        for j in range(lenb):
            if a[i] == b[j]:
                c[i+1][j+1] = c[i][j]+1
                flag[i+1][j+1] = "ok"
            elif c[i+1][j] > c[i][j+1]:
                c[i+1][j+1] = c[i+1][j]
                flag[i+1][j+1] = "left"
            else:
                c[i+1][j+1] = c[i][j+1]
                flag[i+1][j+1] = "up"
    return c, flag


def show_detail(request):
    id = request.GET['id']
    objs = Models.Article.objects.filter(articleID=id).values()
    org_text = objs[0]['articleContent']
    cc_text = objs[0]['articlecopyContent']
    c, flag = lcs(org_text, cc_text)
    len_org = len(org_text)
    len_cc = len(cc_text)
    repeat_index = []

    while len_org > 0 and len_cc > 0:
        if flag[len_org][len_cc] == "up":
            len_org = len_org - 1
        elif flag[len_org][len_cc] == "left":
            len_cc = len_cc - 1
        elif flag[len_org][len_cc] == "ok":
            len_org = len_org - 1
            len_cc = len_cc - 1
            repeat_index.append(len_org)
    context = {
        'org_text': org_text,
        'org_index': repeat_index
    }
    return render(request, 'main/show_detail.html', context)

