from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from django.urls import exceptions, reverse
from urllib.parse import urlencode
from os import path
from .models import Pc
from sys import platform

if platform == "linux" or platform == "linux2":
    from . import gpio_reader

# Sites
def index(request:WSGIRequest):
    msg = request.GET.get("msg")
    pcList = Pc.objects.all()
    context = {"pcList": pcList, "msg":msg}
    return render(request, 'PC_bridge/index.html', context)

def addPC(request:WSGIRequest):
    name = request.GET.get("name")
    if name == None: name = ""
    ip = request.GET.get("ip")
    if ip == None: ip = ""
    mac = request.GET.get("mac")
    if mac == None: mac = ""
    pcie_power = request.GET.get("pcie_power")
    if pcie_power == None: pcie_power = ""
    pcie_status = request.GET.get("pcie_status")
    if pcie_status == None: pcie_status = ""
    msg = request.GET.get("msg")

    context = {"name": name, "ip":ip, "mac":mac, "pcie_power":pcie_power, "pcie_status":pcie_status, "msg": msg}
    return render(request, "PC_bridge/addPC.html", context)

def detail(request:WSGIRequest, pcId:int):
    msg = request.GET.get("msg")
    pc = get_object_or_404(Pc, pk=pcId)
    context = {"pc": pc, "msg":msg}
    return render(request, 'PC_bridge/pcDetails.html', context)


# nur per Post-request ansprechbar
def _submit(request:WSGIRequest):            # PC hinzufügen
    if request.method == 'POST':
        # try:
        name= request.POST["name"]
        ip = request.POST["ip"]
        mac = request.POST["mac"]
        pcie_power = request.POST["pcie_power"]
        pcie_status = request.POST["pcie_status"]
        if name != "" and pcie_power != "" and pcie_status != "":
            if isinstance(pcie_power, str) and isinstance(pcie_status, str) and pcie_power.isnumeric() and pcie_status.isnumeric():
                pc = Pc.objects.create(name=name, ip=ip, mac=mac, pcie_power=pcie_power, pcie_status=pcie_status)
                context = {"pc": pc}
                return render(request, "PC_bridge/submit.html", context)
            else:
                msg = "gpio_power und gpio_status müssen Nummern sein"
                context = {"msg": msg, "name": name, "ip":ip, "mac":mac, "pcie_power":pcie_power, "pcie_status":pcie_status}
                return redirect_args("addPC", context)
        else:
            msg = "Name, gpio_power und gpio_status müssen angegeben werden"
            context = {"msg": msg, "name": name, "ip":ip, "mac":mac, "pcie_power":pcie_power, "pcie_status":pcie_status}
            return redirect_args("addPC", context)
    else:
        return redirect("addPC")

def _remove(request:WSGIRequest, pcId:int):     # PC entfernen
    if request.method == 'POST':
        try:
            print("remove")
            pk= request.POST["id"]
            Pc.objects.filter(id=pk).delete()
            return redirect("index")
        except Exception as e:
            print(e)
            return redirect("detail", pcId)
    else:
        return redirect("detail", pcId)

def _update(request:WSGIRequest, pcId:int):     # PC Eigenschaften ändern
    if request.method == 'POST':
        # try:
        name= request.POST["name"]
        ip = request.POST.get("ip")
        mac = request.POST.get("mac")
        pcie_power = request.POST["pcie_power"]
        pcie_status = request.POST["pcie_status"]

        if name != "" and pcie_power != "" and pcie_status != "":
            if isinstance(pcie_power, str) and isinstance(pcie_status, str) and pcie_power.isnumeric() and pcie_status.isnumeric():
                Pc.objects.filter(id=pcId).update(name=name, ip=ip, mac=mac, pcie_power=pcie_power, pcie_status=pcie_status)
                return redirect_args("index", {"msg": "PC erfolgreich geändert"})
            else:
                msg = "gpio_power und gpio_status müssen Nummern sein"
                context = {"msg": msg}
                return redirect_args("detail", context, r_arg=pcId)
        else:
            msg = "Name, gpio_power und gpio_status müssen angegeben werden"
            context = {"msg": msg}
            return redirect_args("detail", context, r_arg=pcId)
        # except:
        #     return redirect("detail", pcId)
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
            return HttpResponse("no id in request", status=400)
            
        pc = get_object_or_404(Pc, pk=pcId)
        if not 0 < pc.pcie_power < 40 or not 0 < pc.pcie_status < 40:
            return HttpResponse("invalid gpio", status=400)
        print(platform)
        if platform == "linux" or platform == "linux2":
            print(f"status_gpio = {pc.pcie_status}, power_gpio = {pc.pcie_power}")
            gpio_reader.startPc(status_gpio = pc.pcie_status, power_gpio = pc.pcie_power)
        print("Restarting: " + str(pcId))
        if gpio_reader.waitForChange(1, pc.pcie_status):
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
            if not 0 < pc.pcie_power < 40 or not 0 < pc.pcie_status < 40:
                return HttpResponse("invalid gpio", status=400)
            if platform == "linux" or platform == "linux2":
                gpio_reader.shutdownPc(status_gpio = pc.pcie_status, power_gpio = pc.pcie_power)
            print("Shutting Down: " + pc.name)
            if gpio_reader.waitForChange(0, pc.pcie_status):
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
            if platform == "linux" or platform == "linux2":
                status = gpio_reader.getStatus(status_gpio = pc.pcie_status)
                if status == 1:
                    print("status of " + pc.name + ": Online")
                    return HttpResponse("status of " + pc.name + ": Online", status=200)
                elif status == 0:
                    print("status of " + pc.name + ": Offline")
                    return HttpResponse("status of " + pc.name + ": Offline", status=406)
                else:
                    print("status of " + pc.name + ": gpio out of range")
                    return HttpResponse("status of " + pc.name + ": gpio out of range", status=406)
            else:
                print("status of " + pc.name + ": no gpio")
                return HttpResponse("status of " + pc.name + ": Online", status=200)
            
        else:
            return HttpResponse("no id in request", status=200)
    else:
        return HttpResponse("not a GET request", status=400)
        
# helper functions
def redirect_args(view:str, args:dict, r_arg=None):
    print(r_arg)
    print("test")
    if r_arg:
        base_url = reverse(view, args= (r_arg,))
    else:
        base_url = reverse(view)  # 1 /products/
    query_string =  urlencode(args)  # 2 category=42
    url = '{}?{}'.format(base_url, query_string)  # 3 /products/?category=42
    
    return redirect(url)