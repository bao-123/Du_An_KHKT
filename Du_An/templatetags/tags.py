from django import template
from ..views import *
#** No need to import models.py because it's already imported in views.py

register = template.Library()

@register.simple_tag
def get_student_by_role(classroom: Class, role): #** classroom is a Class object
    try:
        return classroom.students.get(role=role)
    except Class.DoesNotExist:
        return None


# -I this function will return the id of the subject that the teacher are teaching the class.
@register.simple_tag
def get_subject(classroom: Class, teacher: Teacher) -> int:
    # @@classroom is the class
    # @@teacher is the teacher
    try:
        return classroom.subject_teachers.get(teacher=teacher).subject
    except ClassSubjectTeacher.DoesNotExist:
        return 
