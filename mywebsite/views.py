# -*- coding=utf-8 -*-
"""
    视图
"""

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt

def login(request):
    from mywebsite.models import web_user
    if request.method == "POST":
        # 获取表单用户密码
        username = request.POST["username"]
        password = request.POST["password"]
        print(username, password)
        # 获取表单数据与数据进行比较
        user = web_user.objects.filter(username__exact = username, pwd__exact = password )
        if user:
            # 比较成功，跳转首页
            response = HttpResponseRedirect('/hwsubmit')
            # 将username写入浏览器cookie，失效时间为3600
            response.set_cookie("username", username, 3600)
            return response
        else:
            # 比较失败，停止在login
            return HttpResponseRedirect("/login")
    return render(request, "login.html")


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
    if not request.COOKIES.get("username", ""):
        print(request.COOKIES.get("username", ""))
        return HttpResponseRedirect("/login")
    else:
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

@csrf_exempt
def test(request):
    """get和post测试接口"""
    import json
    request_data = {}
    request_data['request_class'] = list(dir(request))
    request_data['path'] = request.path
    request_data['method'] = request.method
    if request.method == 'POST':
        request_data['body'] = request.body
        print(request_data, sep='\n')
        print(request.POST)
        return HttpResponse(json.dumps(request_data), content_type='application/json')
    else:
        request_data['parameter'] = request.GET
        return HttpResponse(json.dumps(request_data), content_type='application/json')
    
def wxopen(request):
    """微信公众号接口验证""" 
    echostr = request.GET.get('echostr')
    print(dir(request.GET))
    return HttpResponse(echostr)

def applications(request):
    """加载应用列表页面"""
    return render(request, 'applications.html')

def mycase(request, casename):
    """
        加载实例网页
        使用get请求eid加载指定文件名.html的实例
    """
    import os
    from time import localtime, strftime
    from mywebsite.models import my_case
    casename = casename.lower()
    clist = list(my_case.objects())
    print(clist)
    urllist = [i.urllink for i in clist]
    # 如果实例文件存在，则返回实例文件
    if casename in urllist:
        return render(request, 'mycase/%s' % casename)
    else:
        return render(request, 'tablelist.html', {'clist':clist})
    # # 获得实例文件名
    # caselist = [i.lower() for i in os.listdir(casepath)]
    # ·print(caselist)
    # 如eid文件名存在则加载实例文件，否则加载实例列表。
    # if casename in caselist:
    #   return render(request, casename.lower())
    # else:
    #     caselist = [{'casename':i} for i in caselist]
    #     for item in caselist:
    #         # 获得文件最近修改时间
    #         casefile = casepath + item['casename']
    #         ctime = os.path.getmtime(casefile)
    #         item['caseupdate'] = strftime('%Y-%m-%d', localtime(ctime))
    #         with open(casefile, encoding='utf8') as reader:
    #             item['caseinfo'] = reader.readline()[5:-5]    # 读取文件第一行中<!-- --> 中的内容作为说明
    #     print(caselist)
    #     return render(request, 'caselist.html', {'caselist':caselist})

def rootauth(request):
    """ 阿里验证 """
    with open('root.txt', 'rb') as reader:
        root = reader.read()
    return HttpResponse(root)
