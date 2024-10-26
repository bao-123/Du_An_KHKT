from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponseNotAllowed, HttpRequest, JsonResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from datetime import date
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import json
from .models import *
from .utils import ViewUtils

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


def about(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(request.method)
    return render(request, "Du_An/about.html")
    

def login_view(request):
    if request.method == "GET":
        return render(request, "Du_An/login.html")
    elif request.method == "POST":
        email: str = request.POST["email"]
        password = request.POST["password"]

        if "role" not in request.POST:
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
        return HttpResponseNotAllowed(request.method)
            

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
        contact_info = request.POST["contact_info"]

        #? is_boy = request.POST["is_boy"]
        if not email or not full_name or not raw_password:
            return render_register(request, error={
                "error": "Error occurs",
                "error_message": "Please fill all the input field"
            })
        
        try:
            validate_email(email)
        except ValidationError:
            return render_register(request, error={
                "error": "Invalid email",
                "error_message": "Please enter a valid email"
            })


        user_type = request.POST.get("user_type", None)
        if not user_type:
            return render_register(request, error={"error": "Failed to register", "error_message": "Please choose your account's type (either parent or teacher)"})

        if user_type == "teacher":
            subjects_id = request.POST.getlist("subjects[]")

            if not subjects_id:
                return render_register(request, error={
                    "error": "require at lease 1 subject",
                    "error_message": "Please choose at lease 1 subject"
                })
            
            subjects = Subject.objects.filter(pk__in=subjects_id)

            #* we have stored user's email in 'username' and it is unique so we don't need to check if a email is exists

            try:
                teacher = Teacher.objects.create(
                    full_name=full_name, #** Use full_name instead of username
                    username=email,
                    password = make_password(raw_password),
                    contact_information=contact_info
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
                    class_profile = form_class.get_profile()
                    if class_profile.form_teacher:
                        return render_register(request, error={
                            "error": f"{form_class.name} already have a form teacher!",
                            "error_message": "Check if you choose the wrong class or if you are not a form teacher you don't have to choose a form class."
                        })
                    
                    class_profile.form_teacher = teacher
                    class_profile.save(force_update=True)
                except (Class.DoesNotExist, ClassYearProfile.DoesNotExist):
                    return HttpResponseRedirect(reverse("register"))

            teacher.save(force_update=True)
            login(request, teacher)

        elif user_type == "parent":
            children_id = request.POST.getlist("children[]")
            children = Student.objects.filter(pk__in=children_id)

            try:
                parent = Parent.objects.create(
                    full_name=full_name,
                    username=email,
                    password = make_password(raw_password),
                    contact_information=contact_info
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
    if request.method == "GET":
        classes = Class.objects.all()

        return render(request, "Du_An/classes.html", {
            "classes": [ {"class": classroom, "profile": classroom.get_profile()} for classroom in classes ]
        })
    
    #** API to add class's subject teacher
    elif request.method == "PUT":
        if not hasattr(request.user, "teacher"):
            return HttpResponseNotAllowed("Only teachers can do this")
        
        body: dict = json.loads(request.body)
        class_id = body.get("class_id")
        subject_id = body.get("subject_id") #** id of a 'Subject' instance
        year = body.get("year") if body.get("year") else this_year

        try:
            classroom = Class.objects.get(pk=class_id)
            class_profile = classroom.profiles.get(year=year)

            subject = Subject.objects.get(pk=subject_id)

            if ClassSubjectTeacher.get_subject_teacher(subject, class_profile):
                return JsonResponse({"message": f"This class already have a {subject.name} teacher"}, status=400)

            classroom_subject_teacher = ClassSubjectTeacher(subject=subject, teacher=request.user.teacher, classroom=class_profile)
            classroom_subject_teacher.save()

            return JsonResponse({"message": "Successfully"}, status=200)

        except Class.DoesNotExist:
            return JsonResponse({"message": "Lỗi, Không tìm thấy lớp học này"}, status=400)
        except Subject.DoesNotExist:
            return JsonResponse({"message": "Lỗi, không tìm thấy môn học này"}, status=400)


def view_teaching_classes(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(request.method)
    
    if not hasattr(request.user, "teacher"):
        return HttpResponseBadRequest("Only teachers can access this page")
    
    classes = request.user.teacher.get_teaching_classes()

    return render(request, "Du_An/teaching_classes.html", {
        "classes": classes
    })

    
@login_required(login_url="login")
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
    

@login_required(login_url="login")
def view_teachers(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(request.method)
    
    teachers = Teacher.objects.all()

    return render(request, "Du_An/teachers.html", {
        "teachers": teachers
    })


@login_required(login_url="login")
def view_student(request, id):
    if request.method == "GET":
        try:
            student = Student.objects.get(pk=id)
            return render(request, "Du_An/student.html", {
                "student": student,
                "student_profile": student.get_profile(),
                "subjects": Subject.objects.all()
            })
        except Student.DoesNotExist:
            return render_error(request, error="Not found", error_message="Can't found any student with this id")
        
    elif request.method == "PUT":
        if not hasattr(request.user, "teacher"):
            return JsonResponse({"message": "Only teachers can do this!"}, status=401)
        
        #** body should be a dict
        body: dict = json.loads(request.body)
        subject_id: int = body.get("subject_id")
        #** new mark
        new_mark: float = body.get("new_mark")
        #** 'mark_type' should be a str with some possible values like 'thuong_xuyen1', 'thuong_xuyen2', ...
        mark_type: str = body.get("mark_type")
        #** semester: 1 or 2
        semester: int = body.get("semester")
        

        if not body or not subject_id or \
           not new_mark or not mark_type:
            print("missing information")
            return JsonResponse({"message": "Missing information"},
                                status=400)
        
        try:
            subject = Subject.objects.get(pk=subject_id)
            student_profile = Student.objects.get(pk=id).get_profile() #TODO: Update so we can update marks for other years
            if not ClassSubjectTeacher.is_teaching(subject, request.user.teacher, student_profile.classroom):
                return JsonResponse({"message": "Permission denied"}, status=401)
            
            if semester not in [1, 2]:
                print("Invalid semester")
                return JsonResponse({"message": "Invalid semester"}, status=400)
            
            if subject.name in MAIN_SUBJECTS:
                student_subject = student_profile.main_subjects.get(name=subject.name) if semester == 1 else student_profile.second_term_main_subjects.get(name=subject.name)
                
            elif subject.name in SECOND_SUBJECTS:
                student_subject = student_profile.second_subjects.get(name=subject.name) if semester == 1 else student_profile.second_term_second_subjects.get(name=subject.name)
                
            elif subject.name in COMMENT_SUBJECTS:
                student_subject = student_profile.comment_subjects.get(name=subject.name) if semester == 1 else student_profile.second_term_comment_subjects.get(name=subject.name)
                    
            else:
                return JsonResponse({"message": "Unknow subject"}, status=400)
            
            match(mark_type):
                case "tx1":
                    student_subject.diem_thuong_xuyen1 = new_mark
                    
                case "tx2":
                        student_subject.diem_thuong_xuyen2 = new_mark
                
                case "tx3":
                        student_subject.diem_thuong_xuyen3 = new_mark #* student_subject must be a 'MainSuject' instance
                    
                case "tx4":
                        student_subject.diem_thuong_xuyen4 = new_mark #* student_subject must be a 'MainSuject' instance

                case "gk":
                        student_subject.diem_giua_ki = new_mark
                
                case "ck":
                        student_subject.diem_cuoi_ki = new_mark
                
                #** for eveluate-by-comment subject
                case "is_passed":
                        #** Set the 'is_passed' to True if the mark is one, otherwise set it to False
                        student_subject.is_passed = new_mark == 1
                
                case _:
                    print("Invalid mark type")
                    return JsonResponse({"message": "Unknow attribute"}, status=400)
                
            student_subject.save(force_update=True)

            return JsonResponse({"message": "Update successfully"}, status=200)

        except:
            return JsonResponse({"message": "Failed to update student's marks"}, status=400)

    else:
        return HttpResponseNotAllowed("method not allowed.")


#-i API for get a particular subject's marks
def get_marks(request: HttpRequest, id):
    if request.method != "GET":
        return HttpResponseNotAllowed("method not allowed.")
    
    try:
        student = Student.objects.get(pk=id)
        year = request.GET.get("year", this_year)
        student_profile = student.profiles.get(year=year)
        subject_id = request.GET.get("subject_id")
        subject = Subject.objects.get(pk=subject_id)


        if subject.name in MAIN_SUBJECTS:
            student_subject = {"first_term": student_profile.main_subjects.get(name=subject.name).serialize(),
                                "second_term": student_profile.second_term_main_subjects.get(name=subject.name).serialize(), "subject": subject.name}
        elif subject.name in SECOND_SUBJECTS:
            student_subject = {"first_term": student_profile.second_subjects.get(name=subject.name).serialize(),
                                "second_term": student_profile.second_term_second_subjects.get(name=subject.name).serialize(), "subject": subject.name}
        elif subject.name in COMMENT_SUBJECTS:
            student_subject = {"first_term": student_profile.comment_subjects.get(name=subject.name).serialize(),
                                "second_term": student_profile.second_term_comment_subjects.get(name=subject.name).serialize(), "subject": subject.name}
        else:
            return JsonResponse({"message": "Unknow subject"}, status=400)
        
        return JsonResponse(student_subject, status=200)
    except Student.DoesNotExist:
        return JsonResponse({"message": "Invalid student id"}, status=400)
    except StudentYearProfile.DoesNotExist:
        return JsonResponse({"message": "Invalid year"}, status=400)
    except Subject.DoesNotExist:
        return JsonResponse({"message": "Invalid subject id"}, status=400)


#-i API for searching students
def search_student(request: HttpRequest):
    if request.method != "GET":
        return HttpResponseNotAllowed(request.method)
    
    student_name = request.GET.get("name", '')
    classroom_id = request.GET.get("classroom_id", None)

    if classroom_id:
        try:
            classroom = Class.objects.get(pk=classroom_id)
        except Class.DoesNotExist:
            return JsonResponse({"message": "Invalid classroom id"}, status=400)
    else:
        classroom = None

    if classroom:
        students = [profile.student for profile in classroom.get_profile().students.all() if student_name.lower() in profile.student.full_name.lower()]
    else:
        students = Student.objects.filter(full_name__icontains=student_name)
        
    student_profiles = [ student.get_profile() for student in students ]


    return JsonResponse({"search_result": [ {"student": profile.student.serialize(), "profile": profile.serialize()} for profile in student_profiles ] }, status=200)
        
         
@login_required(login_url="login")
def view_class(request, id):
    if request.method != "GET":
        return HttpResponseNotAllowed("method not allowed")
    try:
        request_class = Class.objects.get(pk=id)
        class_profile = request_class.get_profile() #TODO: Update to get others year

        return render(request, "Du_An/class_profile.html", {
            "classroom": request_class,
            "class_profile": class_profile
        })
    except Class.DoesNotExist:
        return render_error(request, error="Not found", error_message="Doesn't found any teacher with this id")
    except ClassYearProfile.DoesNotExist:
        return render_error(request, error="NVALID YEAR", error_message="Doesn't found any profile in this year")


@login_required(login_url="login")
def view_parent(request: HttpRequest, id: int):
    if request.method != "GET":
        return HttpResponseNotAllowed("method not allowed")
    
    try:
        parent = Parent.objects.get(pk=id)
        #TODO: code parent.html
        return render(request, "Du_An/parent.html", {
            "parent": parent
        })
    
    except Parent.DoesNotExist:
        return render_error(request, error="Not found", error_message="Doesn't found any parent with this id")
    

@login_required(login_url="login")
def create_student(request: HttpRequest):
    classes = Class.objects.all()
    if request.method == "GET":
        return render(request, "Du_An/create_student.html", {
            "classes": classes,
            "role": STUDENT_ROLE #* list  of student's roles
        })
    elif request.method == "POST":
        full_name = request.POST.get("full_name", None)
        classroom_id = request.POST.get("class", None)
        birthday = request.POST.get("birthday", None)
        gender = request.POST.get("gender", None)
        role = request.POST.get("role", None)
        if not full_name or not classroom_id or not birthday \
        or not gender or not role:
            return render(request, "Du_An/create_student.html", {
                "error": "MISSING INFORMATION",
                "error_message": "Please fill all the input fields",
                "classes": classes
            })
        
        try:
            #-I if the format of the date in html form changed, remember to change this also.
            birthday = birthday.split("-") #-W the first element is month, second is day and the last is year
            year, month, day = int(birthday[0]), int(birthday[1]), int(birthday[-1])
            if len(birthday) != 3:
                return render(request, "Du_An/create_student.html", {
                "error": "INVALID DATE FORMAT",
                "error_message": "Please use a valid date format",
                "classes": classes
            })
            #* get selected class
            student_classroom = Class.objects.get(pk=classroom_id)
            classroom_profile = student_classroom.get_profile() #* Tam thoi

            #** ensure that there is only a monitor in a class
            if classroom_profile.get_student_by_role("monitor") and role == "monitor":
                return render(request, "Du_An/create_student.html", {
                    "error": "Fail to create student",
                    "error_message": "This class already have a monitor"
                })
            
            new_student = Student(
                full_name=full_name,
                is_boy= (gender == "boy"),
                birthday=date(year, month, day)
            )

            new_student.full_clean()
            new_student.save()
            
            try:
                StudentYearProfile.create_profile(new_student, role, student_classroom) 
            except ValidationError:
                pass #TODO

            #//new_student.save(force_update=True)

            
            return HttpResponseRedirect(reverse("view_class", args=(student_classroom.id, )))
        except Exception as e:
            print(e.with_traceback())
            return render(request, "Du_An/create_student.html", {
                "error": "INVALID INFORMATION",
                "error_message": "PLease enter valid information.",
                "classes": classes
            })
    else:
        return HttpResponseNotAllowed("method not allowed")
    

@login_required(login_url="login")
#* set the class's form teacher
def update_class(request: HttpRequest):
    if request.method != "POST":
        return HttpResponseNotAllowed("method not allowed.")
    
    classroom_id = int(request.POST.get("classroom_id", -1)) #* If there are not class's id, 'classroom_id' will be -1
    year = int(request.POST.get("year", this_year))

    if not hasattr(request.user, "teacher"):
        return render_error(request, error="Permisson denied", error_message="ONly teachers can do this!")
    
    #ensure that a teacher only have a form class at a time
    if ViewUtils.get_form_class(request.user.teacher):
        return render_error(request, error="Lỗi", error_message="Bạn đã có 1 lớp chủ nhiệm!")

    try:
        classroom = Class.objects.get(pk=classroom_id)
        class_profile: ClassYearProfile = classroom.profiles.get(year=year)
        if class_profile.form_teacher:
          return render_error(request, error="Error occurs", error_message="This class already have a form teacher!")
        
        class_profile.form_teacher = request.user.teacher

        class_profile.save(force_update=True)

        return HttpResponseRedirect(reverse("view_class", args=(classroom_id, )))
    except Class.DoesNotExist:
        return render_error(request, error="Not found", error_message="Doesn't found any class with this id")
    except ClassYearProfile.DoesNotExist:
        return render_error(request, error="Invalid year", error_message="Doesn't found any profile of this class in this year")


def render_register(request: HttpRequest, error: dict | None = None):
    DEFAULT_DICT: dict = {
        "subjects": [ subject.serialize() for subject in Subject.objects.all() ],
        "children": Student.objects.all(),
        "classes":  [ classroom.serialize() for classroom in Class.objects.all() ]
    }

    return render(request, "Du_An/register.html", DEFAULT_DICT | error if error else DEFAULT_DICT)


def render_error(request: HttpRequest, error: str | None = None, error_message: str | None = None, error_image: str | None = None):
    return render(request, "Du_An/error.html", {
        "error": error,
        "error_message": error_message,
        "error_image": error_image
    })


