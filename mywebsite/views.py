# -*- coding=utf-8 -*-
"""
    视图
"""

from django.http import HttpResponse
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
    from mywebsite.models import web_html
    clist = web_html.objects(typeval="children").order_by("-orderid", "-urlid")
    typeval = request.GET.get("type", "")
    if typeval:
        return render(request, "children/%s.html" % request.GET.get("id"))
    else:
        return render(request, "children.html", {'clist':clist})
