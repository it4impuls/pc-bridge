from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from urllib.parse import urlencode
from os import path
from .models import Pc

# Sites
def index(request:WSGIRequest):
    pcList = Pc.objects.all()
    context = {"pcList": pcList}
    return render(request, 'PC_bridge/index.html', context)

def addPC(request):
    name = request.GET.get("name")
    if name == None: name = ""
    ip = request.GET.get("ip")
    if ip == None: ip = ""
    mac = request.GET.get("mac")
    if mac == None: mac = ""
    context = {"name": name, "ip":ip, "mac":mac}
    return render(request, 'PC_bridge/addPC.html', context)

def detail(request, pcId):
    pc = get_object_or_404(Pc, pk=pcId)
    context = {"pc": pc}
    return render(request, 'PC_bridge/pcDetails.html', context)


# nur per Post-request ansprechbar
def _submit(request:WSGIRequest):            # PC hinzufügen
    if request.method == 'POST':
        try:
            name= request.POST["name"]
            ip = request.POST["ip"]
            mac = request.POST["mac"]
            if name == "" or ip == "" or mac == "":
                return redirect_args("addPC", {"name": name, "ip":ip, "mac":mac})
            else:
                pc = Pc.objects.create(name=name, ip=ip, mac=mac)
                context = {'pc': pc}
                return render(request, 'PC_bridge/submit.html', context)
        except:
            return redirect("addPC")
    else:
        return redirect("addPC")

def _remove(request, pcId:int):     # PC entfernen
    if request.method == 'POST':
        try:
            print("remove")
            pk= request.POST["id"]
            Pc.objects.filter(id=pk).delete()
            return redirect('index')
        except Exception as e:
            print(e)
            return redirect("detail", pcId)
    else:
        return redirect("detail", pcId)

def _update(request:WSGIRequest, pcId):     # PC Eigenschaften ändern
    if request.method == 'POST':
        try:
            name= request.POST["name"]
            ip = request.POST["ip"]
            mac = request.POST["mac"]
            Pc.objects.filter(id=pcId).update(name=name, ip=ip, mac=mac)
            return redirect('index')
        except:
            return redirect("detail", pcId)
    else:
        return redirect("detail", pcId)

@csrf_exempt
def _restartPc(request:WSGIRequest):
    if request.method == 'POST':
        try:
            pcId = request.POST["id"]
        except Exception as e:
            print(e)
            return HttpResponse(status=400)
            
        # pc = get_object_or_404(Pc, pk=pcId)
        if Pc.objects.filter(pk=pcId).exists():
            print("Restarting: " + str(pcId))
            return redirect("detail", pcId)
        else:
            print("PC " + str(pcId) + " not in db")
            return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)

@csrf_exempt
def _shutdownPC(request:WSGIRequest):
    if request.method == 'POST':
        try:
            pcId = request.POST["id"]
            print("Shutting Down: " + str(pcId))
            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse(status=400)
    else:
        return redirect("index")

@csrf_exempt
def _getStatus(request:WSGIRequest):
    if request.method == 'GET':
        try:
            pcId = request.GET["id"]
        except Exception as e:
            print(e)
            return HttpResponse(status=400)


        if Pc.objects.filter(pk=pcId).exists():
            if True:        # zukunft statusabfrage
                print("status of " + str(pcId) + ": Online")
                return HttpResponse(status=200)
            else:
                print("status of " + str(pcId) + ": Offline")
                return HttpResponse(status=406)
        else:
            print("PC " + str(pcId) + " not in db")
            return HttpResponse(content=str(pcId) + " not in db", status=200)
    else:
        return HttpResponse(status=400)
        

# helper functions
def redirect_args(view:str, args:dict):
    ...
    base_url = reverse(view)  # 1 /products/
    query_string =  urlencode(args)  # 2 category=42
    url = '{}?{}'.format(base_url, query_string)  # 3 /products/?category=42
    return redirect(url)