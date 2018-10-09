from django.shortcuts import render, render_to_response
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage as fs

# Create your views here.

def index(request):
    return render(request, 'mynote.html')

    
