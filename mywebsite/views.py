from django.http import HttpResponse

def index(request):
    """index 首页"""
    return HttpResponse("hello Andy")
