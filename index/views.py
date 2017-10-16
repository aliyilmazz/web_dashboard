from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from Application import Application
from .models import *

a = Application()

# Create your views here.

def edit(request):
    if request.method == 'POST':
        r_type = request.POST.get('request_type')
        if r_type == 'available':
            return HttpResponse(str(a.available()))
        elif r_type == 'add-component':
            comp_name = request.POST.get('comp_name')
            responseHTML = a.load(comp_name)().execute()
            return JsonResponse({"html" : responseHTML})
        elif r_type == 'save-to-user':
            response = {}
            username = request.POST.get('username')
            password = request.POST.get('password')
            height = request.POST.get('height')
            width = request.POST.get('width')
            component_names = request.POST.getlist('component_names[]')
            component_xs = request.POST.getlist('component_xs[]')
            component_ys = request.POST.getlist('component_ys[]')
            print("sov basliyor")
            print(component_names)
            print(component_xs)
            print(component_ys)
            try:
                User.objects.get(username=username)
            except:
                User.objects.create_user(username = username, password = password)
                Dashboard.objects.create(user=User.objects.get(username=username),width=width,height=height)
            user = authenticate(username = username, password = password)
            if user is not None:
                Components.objects.filter(user__username=username).delete()
                Dashboard.objects.filter(user__username=username).update(
                    width=width, height=height
                )
                for c in range(len(component_names)):
                    Components.objects.create(
                        user = User.objects.get(username=username),
                        name = component_names[c],
                        x=component_xs[c], y=component_ys[c])
                response['result'] = 'success'
            else:
                response['result'] = 'fail'
            return JsonResponse(response)
        return HttpResponse(r_type)
    context = {'bok': '42'}
    return render(request, 'index/edit.html', context)

def display(request, username):
    context = {}
    context['username'] = username
    if request.method == 'POST':
        r_type = request.POST.get('request_type')
        if r_type == 'add-component':
            comp_name = request.POST.get('comp_name')
            responseHTML = a.load(comp_name)().execute()
            return JsonResponse({"html" : responseHTML})
    try:
        dashboard = Dashboard.objects.get(user__username=username)
        status = 1
        context['width'] = dashboard.width
        context['height'] = dashboard.height
    except:
        status = 0
        context['width'] = 0
        context['height'] = 0

    context['status'] = status

    if context['status'] == 1:
        components = Components.objects.filter(user__username=username)
        context['len'] = len(components)
    elif context['status'] == 0:
        context['len'] = 0
    else:
        context['len'] = 0
        print("internal error occurred")
    dumpstr = []
    for i in range(context['len']):
        dumpstr.append(components[i].name)
        dumpstr.append(str(components[i].x))
        dumpstr.append(str(components[i].y))
    dumpstr = ",".join(dumpstr)
    context["dumpstr"] = dumpstr
    print(str(context))
    return render(request, 'index/display.html', context)
