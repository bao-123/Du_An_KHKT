from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponseNotAllowed
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from .models import *

# Create your views here.

def index(request):
    pass

def login_view(request):
    if request.method == "GET":
        return render(request, "Du_An/login.html")
    elif request.method == "POST":
        username: str = request.POST["username"]
        password = request.POST["password"]

        if "role" not in list(request.POST.keys()):
            #replace this
            return HttpResponseBadRequest("please choose either teacher or parent")
        
        user_type = request.POST["role"]

        try:
            if user_type == "teacher":
                user = Teacher.objects.get(username=username, password=password)
            elif user_type == "parent":
                user = Parent.objects.get(username=username, password=password)
            user = authenticate(request, username=username, password=password)

        except:
            user = None
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            #replace this
            return HttpResponseBadRequest("Invalid password or username")
    else:
        return HttpResponseNotAllowed("method not allowed.")
            

def register(request):
    if request.method == "GET":
        return render(request, "Du_An/register.html")
    elif request.method == "POST":
        pass
    else:
        return HttpResponseNotAllowed("method not allowed.")