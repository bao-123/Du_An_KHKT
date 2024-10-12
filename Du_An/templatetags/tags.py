from django import template
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
def get_student_page_link(classroom: Class, role: str, tagclass: str, year: int = this_year) -> str | None:
    try:
        student = classroom.profiles.get(year=year).students.get(role=role)
        #* HTML code
        href = "{%" + f"url 'view_student' {student.id}" + "%}"
        return tag("a", attribute=f"href={href} class={tagclass}", content=student.full_name)
    except StudentYearProfile.DoesNotExist:
        return f"Lớp chưa có {get_role_name(role)}"
    except: 
        return None

# -I this function will return the id of a 'Subject' instance
@register.simple_tag
def get_subject(classroom: Class, teacher: Teacher, attribute: str ) -> int | None:
    try:
        # -W A teacher can teach more than 1 subject in a class
        #TODO: Ensure that if the teacher teach more than 1 subject everything still working. (take a look at HTML)
        subject_teacher: ClassSubjectTeacher = classroom.subject_teachers.get(teacher=teacher) # * This will return a 'ClassSubjectTeacher' instance
        return getattr(subject_teacher, attribute, None)
    except MultipleObjectsReturned:
        return None #TODO


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