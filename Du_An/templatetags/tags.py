from django import template
from django.core.exceptions import MultipleObjectsReturned
from ..views import *
#** No need to import models.py because it's already imported in views.py

register = template.Library()

@register.simple_tag
def get_student_by_role(classroom: Class, role): #** classroom is a Class object
    try:
        return classroom.students.get(role=role)
    except Class.DoesNotExist:
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

