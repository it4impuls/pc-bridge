from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, Http404
from os import path
from .models import Pc




def index(request):
    pcList = Pc.objects.all()
    context = {"pcList": pcList}
    return render(request, 'index.html', context)


def addPC(request):
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
        pc = Pc.objects.create(name=name, ip=ip, mac=mac)
        dic = {
            'name': name,
            'ip': ip,
            'mac': mac
        }
        return render(request, 'submit.html', dic)
    else:
        return redirect("addPC")
        # return redirect('index')

def remove(request, pcId):
    print("test")
    if request.method == 'POST':
        pk= request.POST["id"]
        print(pk)
        Pc.objects.filter(id=pk).delete()
        return redirect('index')
        # return render(request, 'pcDetails.html', dic)   
    else:
        return redirect("detail", pcId)