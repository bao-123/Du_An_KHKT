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



