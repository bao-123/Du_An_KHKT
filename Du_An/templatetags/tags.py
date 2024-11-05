from django import template
from django.utils.html import format_html
from django.urls import reverse
from django.core.exceptions import MultipleObjectsReturned
from ..views import *
#** No need to import models.py because it's already imported in views.py

register = template.Library()

@register.simple_tag
def get_student_by_role(classroom: Class, role, porpery: str, year: int = this_year): #** classroom is a Class object
    try:
        return getattr(classroom.profiles.get(year=year).students.get(role=role), porpery, None)
    except StudentYearProfile.DoesNotExist:
        return f"Lớp chưa có {get_role_name(role)}"


@register.simple_tag
def get_student_page_link(classroom: Class, role: str, tagclass: str, year: int = this_year) -> str:
    try:
        student: StudentYearProfile = classroom.profiles.get(year=year).students.get(role=role)
        #* HTML code
        href = reverse("view_student", args=(student.student.id, ))
        return format_html(tag("a", attribute='href="{}" class="{}"', content=student.student.full_name), href, tagclass)
    except StudentYearProfile.DoesNotExist:
        return f"Lớp chưa có {get_role_name(role)}"
    except ClassYearProfile.DoesNotExist:
        return "Năm học không hợp lệ"
    except: 
        #! Shouldn't return None
        return '' #* Return None may raise Error when Django render template

# -I this function will return the id of a 'Subject' instance
@register.simple_tag
def get_subject(classroom: ClassYearProfile, teacher: Teacher, attribute: str ):
    try:
        # -W A teacher can teach more than 1 subject in a class
        #TODO: Ensure that if the teacher teach more than 1 subject everything still working. (take a look at HTML)
        subject_teacher: ClassSubjectTeacher = classroom.subject_teachers.get(teacher=teacher).subject
        return getattr(subject_teacher, attribute, None)
    except MultipleObjectsReturned:
        return None #TODO

@register.simple_tag
def get_teacher_subject_options(profile: ClassYearProfile, teacher: Teacher):
    teaching_subjects = [teacher_subject.subject for teacher_subject in profile.subject_teachers.filter(teacher=teacher)]

    html_options = [format_html(tag("option", attribute='value={}', content=subject.name), subject.id) for subject in teaching_subjects]

    return '\n'.join(html_options)


@register.simple_tag
def get_teaching_subjects(class_profile: ClassYearProfile, teacher: Teacher) -> str:
    return ', '.join([subject_teacher.subject.name for subject_teacher in class_profile.subject_teachers.filter(teacher=teacher)])


@register.simple_tag
def get_profile(classroom: Class, porperty: str, year: int = this_year): #* 'this_year' Declared in 'models.py'
    try:
        return getattr(classroom.profiles.get(year=year), porperty, None)
    except Class.DoesNotExist:
        return None
    

@register.simple_tag
def get_role_name(role: str) -> str | None:
    if role not in STUDENT_ROLE:
        return 
    for role_name in role_choices:
        if role in role_name:
            return role_name[-1] #* get the vietnamese name of the role
        

def tag(tagname: str, attribute: str = '', content: str = ''):
    return f"<{tagname} {attribute}> {content} </{tagname}>"