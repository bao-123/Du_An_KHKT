from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponseNotAllowed
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from .models import *

# Create your views here.

def index(request):
    if request.method == "GET":
        return render(request, "Du_An/welcome.html")
    else:
        return HttpResponseNotAllowed("method not allowed.")

def dashboard(request):
    if request.method == "GET":
        return render(request, "Du_An/dashboard.html")
    else:
        return HttpResponseNotAllowed("method not allowed")

def login_view(request):
    if request.method == "GET":
        return render(request, "Du_An/login.html")
    elif request.method == "POST":
        email: str = request.POST["email"]
        password = request.POST["password"]

        if "role" not in list(request.POST.keys()):
            #replace this
            return HttpResponseBadRequest("please choose either teacher or parent")
        

        user_type = request.POST["role"]
        user_auth = authenticate(email=email, password=password)

        if not user_auth:
            return render(request, "Du_An/login.html", {
                "error": "Invalid password or email",
                "error_message": "Please re-check your email and password"
            })
        
        if user_type == "teacher":
            try:
                user = Teacher.objects.get(pk=user_auth.pk)
            except Teacher.DoesNotExist:
                return render(request, "Du_An/login.html", {
                    "error": "Failed to login",
                    "error_message": "Doesn't found any account with this email and password, please ensure that your account is registered as teacher"
                })
        elif user_type == "parent":
            try:
                user = Parent.objects.get(pk=user_auth.pk)
            except Parent.DoesNotExist:
                return render(request, "Du_An/login.html", {
                    "error": "Failed to login",
                    "error_message": "Doesn't found any account with this email and password, please ensure that your account is registered as parent"
                })
        else:
            return HttpResponseBadRequest("Unknow user type")
        
        #log user in
        login(request, user)

        return HttpResponseRedirect(reverse("dashboard"))
    
    else:
        return HttpResponseNotAllowed("method not allowed.")
            

def logout_view(request):

    logout(request)

    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "GET":
        return render(request, "Du_An/register.html", {
            "subjects": [ subject.serialize() for subject in Subject.objects.all() ],
            "children": [ student.serialize() for student in Student.objects.all() ]
        })
    
    elif request.method == "POST":
        full_name: str = request.POST["full_name"]
        email: str = request.POST["email"]
        raw_password = request.POST["password"]
        #? is_boy = request.POST["is_boy"]


        if "user_type" not in list(request.POST.keys()):
            return render(request, "Du_An/register.html", {
                "error": "",
                "error_message": "" #TODO
            })
        user_type = request.POST["user_type"]

        if user_type == "teacher":
            subjects_id = request.POST.getlist("subjects[]")

            if not subjects_id:
                return render(request, "Du_An/login.html", {
                    "error": "require at lease 1 subject",
                    "error": "Please choose at lease 1 subject"
                })
            
            subjects = Subject.objects.filter(pk__in=subjects_id)


            if Teacher.objects.filter(email=email).exists():
                return render(request, "Du_An/login.html", {
                    "error": "Email already registered",
                    "error_message": "your email already registered as a teacher, please enter another email."
                })
            
            teacher = Teacher.objects.create(
                full_name=full_name, #** Use full_name instead of username
                email=email,
                password = make_password(raw_password),
                #is_boy=is_boy
                  #TODO: add some needed information.       
            )
            teacher.subject.set(subjects)
            teacher.save()
            login(request, teacher)

        elif user_type == "parent":
            children_id = request.POST.getlist("children[]")
            children = Student.objects.filter(pk__in=children_id)

            if Parent.objects.filter(email=email).exists():
                return render(request, "Du_An/login.html", {
                    "error": "Email already registered",
                    "error_message": "your email already registered as a parent, please enter another email."
                })
            
            parent = Parent.objects.create(
                username=full_name,
                email=email,
                password = make_password(raw_password)
            )
            parent.children.set(children)

            parent.save()

            login(request, parent)
        else:
            return HttpResponseBadRequest("Unnknow user type")
        return HttpResponseRedirect(reverse("dashboard"))
    else:
        return HttpResponseNotAllowed("method not allowed.")
    


