from django.shortcuts import render
from django.http import HttpResponse
from os import path
from .models import Pc




def index(request):
    pcList = Pc.objects.all()
    context = {"pcList": pcList}
    return render(request, 'index.html', context)


def addPC(request):
    pcList = Pc.objects.all()
    return render(request, 'addPC.html')

def detail(request, pcId):
    pc = Pc.objects.get(pk=pcId)
    context = {"pc": pc}
    return render(request, 'pcDetails.html')