from openai import OpenAI
from .models import *
from django.http import JsonResponse, HttpResponseNotAllowed

#-i APIs
def get_class_marks(request, id):
    if request.method != "GET":
        return HttpResponseNotAllowed(request.method)
    
    profile = Class.objects.get(pk=id).get_profile()

    return [ student_profile.get_subject_marks(serialize=True) for student_profile in profile.students.all()]


#TODO: Debug this function and research read excel file function.


