#from openai import OpenAI
from .models import *
from django.http import JsonResponse, HttpResponseNotAllowed
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
from openai import OpenAI
import os
#TODO:
load_dotenv()
#-i API
API_KEY = os.getenv("API_KEY")
API_BASE_URL = "https://api.aimlapi.com/v1"

if not API_KEY:
    raise Exception("API KEY not found")

api = OpenAI(api_key=API_KEY, base_url=API_BASE_URL)
system_prompt = "Answer in Vietnamese"

#-i APIs
def get_class_marks(request, id):
    if request.method != "GET":
        return HttpResponseNotAllowed(request.method)
    
    profile = Class.objects.get(pk=id).get_profile()

    return [ student_profile.get_subject_marks(serialize=True) for student_profile in profile.students.all()]


@login_required(login_url="login")
def get_student_advice(request=None, id=None):
    if request.method != "GET":
        return JsonResponse({"message": "Invalid method"}, status=402)
    
    AI_advice = get_advice("Give some advice about studying, learning")

    return JsonResponse({"advice": AI_advice}, status=400)
    


#TODO: Debug this function and research read excel file function.


def get_advice(prompt):
    completions = api.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
            {"role": "system", "content": system_prompt}
        ],
        temperature=1,
        max_tokens=200
    )

    return completions.choices[0].message.content


#-i For create student profile
@login_required(login_url='login')
def create_profile(request, student_id: int):
    if request.method != "POST":
        return HttpResponseNotAllowed(request.method)
    
    try:
        student = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        print("student not found")
        return JsonResponse({"message": "student not found"}, status=404)
    
    #* Authorization
    if not hasattr(request.user, "teacher"):
        return JsonResponse({"message": "unauthorized"}, status=403)
    elif request.user.teacher != student.get_profile().classroom.form_teacher: #*Check if the user is the current form teacher of the student
        return JsonResponse({"message": "only form teacher of this student can do this!"}, status=403)
    
    year = request.POST.get('year')
    classroom_name = request.POST.get('classroom_name')#* classroom name is unique

    try:
        classroom = Class.objects.get(name=classroom_name)
    except Class.DoesNotExist:
        print("classroom not found")
        return JsonResponse({"message": "classroom not found"}, status=404)
    
    role = request.POST.get("role", "student") #* default is student

    try:
        profile = StudentYearProfile.create_profile(student, role, classroom, year=year)
        return JsonResponse({"message": "profile created successfully", "profile": profile.serialize()}, status=200)
    except ValidationError:
        return JsonResponse({"message": "invalid data"}, status=400)


