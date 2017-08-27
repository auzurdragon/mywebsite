from django.http import HttpResponse


def index(request):
    """
        render_to_response()方法
        index 首页
    """
    from django.shortcuts import render_to_response
    return render_to_response('index.html')


def hello(request):
    """HttpResponse示例"""
    return HttpResponse("hello Andy")
