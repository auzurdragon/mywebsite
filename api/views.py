
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from mycoupon import coupon
from django.http import JsonResponse
# Create your views here.

def weixin(request):
    echostr = request.GET.get('echostr')
    print(echostr)
    print(dir(request.GET))
    return HttpResponse(echostr)
