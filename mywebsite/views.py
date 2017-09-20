# -*- coding=utf-8 -*-
"""
    视图
"""

# from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    """index 首页"""
    return render(request, 'index.html')

def python(request):
    """python笔记"""
    return render(request, 'python.html')

def examples(request):
    """实例"""
    from mywebsite.models import web_html
    clist = web_html.objects(typeval="example")
    typeval = request.GET.get("type", "")
    print(typeval)
    if typeval:
        return render(request, "example/%s.html" % request.GET.get("id"))
    else:
        return render(request, 'example.html', {'clist':clist})

def children(request):
    """视图"""
    from mywebsite.models import web_homework
    from time import time
    urlid = request.GET.get("urlid")
    if urlid:
        clist = web_homework.objects.filter(urlid=urlid, classof=0)
        return render(request, "hwcontent.html", {"clist":clist})
    else:
        clist = web_homework.objects.filter(classof=0, urlid__gte=(time()-86400*7)).order_by("-orderid", "-urlid")
        return render(request, "children.html", {"clist":clist})

def syllabus(request):
    """课程表"""
    return render(request, "children/syllabus.html")

def schedule(request):
    """作息时间表"""
    return render(request, "children/schedule.html")

def booklist(request):
    """书目"""
    from mywebsite.models import chi_booklist
    clist = chi_booklist.objects.all()
    return render(request, "children/booklist.html", {"clist":clist})

def chisearch(request):
    """学校附近搜索"""
    qword = request.GET.get("query")
    from mywebsite.API.SearchAPI import SearchAPI
    if qword == "":
        clist = ""
    else:
        r = SearchAPI()
        r.s_library(qword)
        clist = r.result
        print(clist)
    return render(request, "children/search.html", {"clist":clist})

def hwsubmit(request):
    """提交"""
    from mywebsite.models import web_homework
    from mywebsite.models import web_user
    from time import time, localtime, strftime
    tlist = web_user.objects.all().order_by("tid")
    today = strftime("%Y-%m-%d", localtime(time()))
    postlist = web_homework()
    errmsg = []
    if request.method == "POST":
        pd = request.POST.getlist("homework")
        postlist.urlid = str(int(time()))
        postlist.classof = int(pd[1])
        postlist.title = pd[2]
        postlist.author = pd[0].split(',')[1]
        postlist.course = pd[0].split(',')[0]
        postlist.content = "<p>%s</p>" % pd[3].replace("\r\n","</br>")
        postlist.urllink = pd[4]
        postlist.datestr = today
        try:
            postlist.validate()
            postlist.save()
            clist = web_homework.objects.filter(urlid=postlist.urlid)
            return render(request, "hwcontent.html", {"clist":clist})
        except Exception as e:
            for i in e.errors: errmsg.append("%s : %s" % (i, e.errors[i]))
            print(errmsg)
    else:
        postlist.urlid = str(0)
        postlist.title = ""
        postlist.author = ""
        postlist.course = ""
        postlist.urllink = ""
        postlist.content = ""
        postlist.datestr = today        
    return render(request, "hwsubmit.html", {"tlist":tlist, "today":today, "postlist":postlist, "errmsg":errmsg})

def pinyin(request):
    """"""
    from mywebsite.models import web_homework
    from xpinyin import Pinyin
    pinyin = Pinyin()
    urlid = request.GET.get("urlid")
    if not urlid:
        clist = list(web_homework.objects.filter(classof=3).order_by("-orderid", "-urlid"))
        print(type(clist))
        for item in clist:
            item.title = [{"word":j, "pinyin":pinyin.get_pinyin(j, show_tone_marks=True)} for j in item.title]
        ctype = False
    else:
        clist = list(
            web_homework.objects.filter(classof=3, urlid=urlid).order_by("-orderid", "-urlid")
            )[0]
        clist.title = [
            {"word":j,
             "pinyin":pinyin.get_pinyin(j, show_tone_marks=True)}
            for j in clist.title
        ]
        tmp = clist.content[3:-4].split("</br>")
        clist.author = [{"word":j, "pinyin":pinyin.get_pinyin(j, show_tone_marks=True)} for j in tmp[0]]
        clist.content = [
            [{"word":j, "pinyin":pinyin.get_pinyin(j, show_tone_marks=True)} for j in i]
            for i in tmp[1:]
            ]
        ctype = True
    return render(request, 'children/pinyin.html', {"ctype":ctype, "clist":clist})

