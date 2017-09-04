from django.http import HttpResponse
from django.shortcuts import render_to_response, render


def index(request):
    """index 首页"""
    return render(request, 'index.html')


def hello(request):
    """HttpResponse示例"""
    return HttpResponse("hello Andy")

def python(request):
    """python笔记"""
    return render(request, 'python.html')

def examples(request):
    """实例"""
    from mywebsite.models import web_user
    tlist = web_user.objects.all()
    return render(request, 'examples.html', {'td_list':tlist})
