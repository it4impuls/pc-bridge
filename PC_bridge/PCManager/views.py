from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, Http404
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
    pc = get_object_or_404(Pc, pk=pcId)
    context = {"pc": pc}
    return render(request, 'pcDetails.html', context)

def submit(request):
    if request.method == 'POST':
        name= request.POST["name"]
        ip = request.POST["ip"]
        mac = request.POST["mac"]
        Pc.objects.create(name=name, ip=ip, mac=mac)
        dic = {
            'name': name,
            'ip': ip,
            'mac': mac
        }
        return render(request, 'submit.html', dic)   
        # return redirect('index')