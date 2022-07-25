from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from django.urls import exceptions, reverse
from urllib.parse import urlencode
from os import path
from .models import Pc

# Sites
def index(request:WSGIRequest):
    msg = request.GET.get("msg")
    pcList = Pc.objects.all()
    context = {"pcList": pcList, "msg":msg}
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
        except exceptions as e:
            print(e)
            return redirect("addPC")
    else:
        return redirect("addPC")

def _remove(request:WSGIRequest, pcId:int):     # PC entfernen
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

def _update(request:WSGIRequest, pcId:int):     # PC Eigenschaften ändern
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

def _pc_action(request:WSGIRequest):
    msg = ""
    if "restart" in request.POST:
        response = _restartPc(request)
    elif "shutdown" in request.POST:
        response =  _shutdownPC(request)
    elif "getStatus" in request.POST:
        request.method = "GET"
        tempdict = request.POST.copy()
        request.GET = tempdict
        response =  _getStatus(request)
    else:
        response = HttpResponse("something went wrong", status=404)
    msg = response.content.decode()
    return redirect_args("index", {"msg":msg})
    

# ansprechbar ohne Tokens
@csrf_exempt
def _restartPc(request:WSGIRequest):
    if request.method == 'POST':
        try:
            pcId = request.POST["id"]
        except Exception as e:
            print(e)
            return HttpResponse("something went wrong", status=400)
            
        pc = get_object_or_404(Pc, pk=pcId)
        print("Restarting: " + str(pcId))
        if True:
            return HttpResponse("successfully restarted " + pc.name, status=200)
        else:
            return HttpResponse("could not restart " + pc.name, status=400)
    else:
        return HttpResponse("not a POST request", status=400)

@csrf_exempt
def _shutdownPC(request:WSGIRequest):
    if request.method == 'POST':
        pcId = request.POST.get("id")
        
        if pcId != None:
            pc = get_object_or_404(Pc, pk=pcId)
            print("Shutting Down: " + pc.name)
            if True:
                return HttpResponse("successful shutdown " + pc.name, status=200)
            else:
                return HttpResponse("could not shutdown " + pc.name, status=400)
        else:
            return HttpResponse("no id in request", status=400)
    else:
        return HttpResponse("not a POST request", status=200)

@csrf_exempt
def _getStatus(request:WSGIRequest):
    if request.method == 'GET':
        pcId = request.GET.get("id")
        if pcId != None:
            pc = get_object_or_404(Pc, pk=pcId)
            print("Shutting Down: " + pc.name)
            if True:
                print("status of " + pc.name + ": Online")
                return HttpResponse("status of " + pc.name + ": Online", status=200)
            else:
                print("status of " + pc.name + ": Offline")
                return HttpResponse("status of " + pc.name + ": Offline", status=406)
        else:
            return HttpResponse("no id in request", status=200)
    else:
        return HttpResponse("not a GET request", status=400)
        

# helper functions
def redirect_args(view:str, args:dict):
    base_url = reverse(view)  # 1 /products/
    query_string =  urlencode(args)  # 2 category=42
    url = '{}?{}'.format(base_url, query_string)  # 3 /products/?category=42
    return redirect(url)