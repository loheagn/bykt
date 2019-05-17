from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import *
from .forms import LoginForm, RegisterForm, VisitForm
from .face_recognation import *
import time
import numpy
from gensim import corpora, models, similarities
from urllib.request import quote, urlopen
import lxml.html
import jieba
import re
import datetime
from .ocr import *


# Create your views here.
etree = lxml.html.etree


def test(request):
    return render(request, 'main/test.html')


def search(request):
    key_word = request.POST.get('key')
    if not key_word:
        key_word = ""
    return redirect('https://www.google.com.hk/search?q=' + key_word)


def volunteer(request):
    if not request.session.get('id'):
        request.session.flush()
        return redirect('/login/')
    student = Student.objects.get(pk=request.session.get('id'))
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            tt = image.name.split('.')[-1]
            image.name = str(time.time()).replace('.', '-') + '.' + tt
            new_tmp_image = TmpImage(image=image)
            new_tmp_image.save()
            file_name = "/home/loheagn/boyasite/uploads/images/tmp/" + image.name
            try:
                number, name = get_number_and_name_from_single_picture(file_name)
                number = float(number)
                name = str(name)
                if student.name != name:
                    message = "所上传截图与注册姓名不符，请重新确认！"
                    return render(request, 'main/volunteer.html', locals())
                vol_image = VolunteerImage()
                vol_image.student = student
                vol_image.image = image
                vol_image.time_number = number
                vol_image.save()
                student.volunteer = number - student.old_volunteer
                if student.volunteer >= 16:
                    flag = True
                else:
                    flag = False
                student.save()
                return redirect('/volunteer_show/')
            except:
                message = "图片检测失败，请稍后刷新重试！"
                return render(request, 'main/volunteer.html', locals())
    return render(request, 'main/volunteer.html', locals())


def volunteer_show(request):
    if not request.session.get('id'):
        request.session.flush()
        return redirect('/login/')
    student = Student.objects.get(pk=request.session.get('id'))
    if student.volunteer >= 16:
        flag = True
    else:
        flag = False
    return render(request, 'main/volunteer_show.html', locals())



def sport_show(request):
    if not request.session.get('id'):
        request.session.flush()
        return redirect('/login/')
    student = Student.objects.get(pk=request.session.get('id'))
    return render(request, 'main/sport_show.html', locals())


def sport(request):
    if not request.session.get('id'):
        request.session.flush()
        return redirect('/login/')
    student = Student.objects.get(pk=request.session.get('id'))
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            tt = image.name.split('.')[-1]
            image.name = str(time.time()).replace('.', '-') + '.' + tt
            new_tmp_image = TmpImage(image=image)
            new_tmp_image.save()
            file_name = "/home/loheagn/boyasite/uploads/images/tmp/" + image.name
            try:
                number, s_time = get_number_and_time_from_single_picture(file_name)
                s_time = datetime.datetime.strptime(s_time, '%Y-%m-%d%H：%M')
                number = float(number)
                test_sport_image = SportImage.objects.filter(s_time=s_time)
                if test_sport_image:
                    message = "图片疑似已被使用，请尝试其他有效截图！"
                    return render(request, 'main/sport.html', locals())
                sport_image = SportImage()
                sport_image.image = image
                sport_image.s_time = s_time
                sport_image.student = student
                sport_image.number = number
                sport_image.save()
                student.sport = student.sport + number
                student.save()
                return redirect('/sport_show/')
            except:
                message = "检测失败或图片疑似已被使用，请稍后刷新重试！"
                return render(request, 'main/sport.html', locals())

    return render(request, 'main/sport.html', locals())














def index(request):
    is_login = request.session.get('is_login', None)
    if is_login:
        student = Student.objects.get(pk=request.session.get('id'))
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
            sp = image.name.split('.')[-1]
            image.name = 'profile' + str(time.time()).replace('.', '')[0] + '.' + sp
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
            new_student.face_array = '/home/loheagn/boyasite/uploads/face_arrays/' + str(time.time()).replace('.', '')[0] + '.npy'
            try:
                numpy.save(new_student.face_array, get_src_vectors_from_someone_single_image(file_name))
                new_student.save()
                return redirect('/login/')
            except:
                message = '文件非法，请刷新页面并重试！'
                return render(request, 'main/register.html', locals())
        else:
            message = '文件非法，请刷新页面并重试！'
            return render(request, 'main/register.html', locals())
    register_form = RegisterForm()
    return render(request, 'main/register.html', locals())


def logout(request):
    request.session.flush()
    return render(request, 'main/logout.html')


def profile(request):
    if not request.session.get('id'):
        request.session.flush()
        return redirect('/login/')
    student = Student.objects.get(pk=request.session.get('id'))
    return render(request, 'main/profile.html', locals())


def change_password(request):
    if not request.session.get('id'):
        request.session.flush()
        return redirect('/login/')
    student = Student.objects.get(pk=request.session.get('id'))
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 and password2:
            if password2 != password1:
                message = "两次输入的密码不同！"
                return render(request, 'main/change_password.html', locals())
            else:
                student.password = password1
                student.save()
                return redirect('/profile/')
    return render(request, 'main/change_password.html', locals())


def visit_show(request):
    if not request.session.get('id'):
        request.session.flush()
        return redirect('/login/')
    alert = request.session.get('visit_alert')
    student = Student.objects.get(pk=request.session.get('id'))
    visit_images = VisitImage.objects.filter(student=student)
    return render(request, 'main/visit_show.html', locals())


def visit(request):
    if not request.session.get('id'):
        request.session.flush()
        return redirect('/login/')
    form_flag = False
    student = Student.objects.get(pk=request.session.get('id'))
    visit_images = VisitImage.objects.filter(student=student)
    if request.method == 'POST':
        # 获取上传的表格数据
        time_value = request.POST.get('v_time')
        v_time = datetime.datetime.strptime(time_value, '%Y-%M-%d').date()
        location = request.POST.get('location')
        image = request.FILES.get('image')
        if v_time and location and image:
            sp = image.name.split('.')[-1]
            image.name = 'profile' + str(time.time()).replace('.', '')[0] + '.' + sp
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
            if 0.5 > min_distance > 0.1:
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
            response = render(request, 'main/visit_show.html', locals())
            while response is None:
                response = render(request, 'main/visit_show.html', locals())
            return render(request, 'main/visit_show.html', locals())
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
    lines = cut_text(lines, 40)
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
    #authorName = request.GET['authorname']
    articletitle = request.GET['articletitle']
    articlesim = len(cc_text)/len(org_text)
    student = Student.objects.get(pk=request.session.get('id'))
    if articlesim < 0.4:
        student.my_article = True
        student.save()
    Article.objects.create(articleTitle=articletitle, articleContent=org_text, articlecopyContent=cc_text, article_copy_rate=articlesim, student=student)

    context = {
        'similarity_rates': similarity_rates,
        'org_text': org_text,
        'org_index': repeat_index,
        'simi_r': articlesim
    }
    return render(request, 'main/article.html', context=context)


def article_input(request):
    if not request.session.get('id'):
        request.session.flush()
        return redirect('/login/')
    stuID = request.session['id']
    objs = Article.objects.filter(student_id=stuID).values()
    return render(request, 'main/article_input.html', locals())


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
    objs = Article.objects.filter(articleID=id).values()
    articleid = objs[0]['articleID']
    title = objs[0]['articleTitle']
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
        'articleid': articleid,
        'title': title,
        'org_text': org_text,
        'org_index': repeat_index
    }
    return render(request, 'main/show_detail.html', context)


def delete(request):
    article_id = request.GET['article_id']
    article = Article.objects.filter(articleID=article_id).delete()
    return render(request, 'main/delete.html')
