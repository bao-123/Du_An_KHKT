from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponseNotAllowed, HttpRequest
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
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
        #** store user's email in username field
        user_auth = authenticate(request, username=email, password=password)

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

def register(request: HttpRequest):
    if request.method == "GET":
        return render_register(request)
    
    elif request.method == "POST":
        full_name: str = request.POST["full_name"]
        email: str = request.POST["email"]
        raw_password = request.POST["password"]
        #? is_boy = request.POST["is_boy"]


        if "user_type" not in list(request.POST.keys()):
            return render_register(request, error={
                "error": "Error occurs",
                "error_message": "Please choose either teacher or parent"
            })
        user_type = request.POST["user_type"]

        if user_type == "teacher":
            subjects_id = request.POST.getlist("subjects[]")

            if not subjects_id:
                return render_register(request, error={
                    "error": "require at lease 1 subject",
                    "error": "Please choose at lease 1 subject"
                })
            
            subjects = Subject.objects.filter(pk__in=subjects_id)

            #* we have stored user's email in 'username' and it is unique so we don't need to check if a email is exists

            try:
                teacher = Teacher.objects.create(
                    full_name=full_name, #** Use full_name instead of username
                    username=email,
                    password = make_password(raw_password),
                    #is_boy=is_boy
                    #TODO: add some needed information.       
                )
            except IntegrityError:
                return render_register(request,  error={
                    "error": "Email already exists",
                    "error_message": "Your email already registered as a teacher, please choose another email."
                })
            
            teacher.subject.set(subjects)
            form_class_id = request.POST.get("form_class", default=None)
            if form_class_id:
                try:
                    form_class = Class.objects.get(pk=int(form_class_id))
                    if form_class.form_teacher:
                        return render_register(request, error={
                            "error": f"{form_class.name} already have a form teacher!",
                            "error_message": "Check if you choose the wrong class or if you are not a form teacher you don't have to choose a form class."
                        })
                    form_class.form_teacher = teacher
                    form_class.save(force_update=True)
                except Class.DoesNotExist:
                    return HttpResponseRedirect(reverse("register"))

            teacher.save()
            login(request, teacher)

        elif user_type == "parent":
            children_id = request.POST.getlist("children[]")
            children = Student.objects.filter(pk__in=children_id)

            try:
                parent = Parent.objects.create(
                    full_name=full_name,
                    username=email,
                    password = make_password(raw_password)
                )
            except IntegrityError:
                return render_register(request,  error={
                    "error": "Email already register as a parent, please choose another email"
                })
            
            parent.children.set(children)

            parent.save()

            login(request, parent)
        else:
            return HttpResponseBadRequest("Unnknow user type")
        return HttpResponseRedirect(reverse("dashboard"))
    else:
        return HttpResponseNotAllowed("method not allowed.")
    


def view_classes(request):
    if request.method != "GET":
        return HttpResponseNotAllowed("Method not allowed")
    classes = Class.objects.all()

    return render(request, "Du_An/classes.html", {
        "classes": classes
    })



def view_teacher(request, teacher_id):
    if request.method != "GET":
        return HttpResponseNotAllowed("method not allowed")
    try:
        teacher = Teacher.objects.get(pk=teacher_id)

        return render(request, "Du_An/teacher.html", {
            "teacher": teacher
        })
    
    except Teacher.DoesNotExist:
        return render_error(request, error="Not found", 
                            error_message="Doesn't found any teacher with this id") #* Add error_image (a path to a image in static) if wish.
    
    
def view_student(request, id):
    pass


def view_class(request, id):
    try:
        request_class = Class.objects.get(pk=id)

        return render(request, "Du_An/class_profile.html", {
            "classroom": request_class
        })
    except Class.DoesNotExist:
        return render_error(error="Not found", error_message="Doesn't found any teacher with this id")




def render_register(request: HttpRequest, error: dict | None = None):
    DEFAULT_DICT: dict = {
        "subjects": [ subject.serialize() for subject in Subject.objects.all() ],
        "children": [ student.serialize() for student in Student.objects.all() ],
        "classes":  [ classroom.serialize() for classroom in Class.objects.all() ]
    }

    return render(request, "Du_An/register.html", DEFAULT_DICT | error if error else DEFAULT_DICT)


def render_error(request: HttpRequest, error: str | None = None, error_message: str | None = None, error_image: str | None = None):
    return render(request, "Du_An/error.html", {
        "error": error,
        "error_message": error_message,
        "error_image": error_image
    })

