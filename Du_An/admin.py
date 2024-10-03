from django.contrib import admin
from .models import *

#TODO: Tim hieu them
# Register your models here.
class StudentAdminModel(admin.ModelAdmin):
    list_display = ("id", "full_name", "classroom", "is_boy", "role")

class ParentAdmin(admin.ModelAdmin):
    filter_horizontal = ("children", )

class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

class SubjectTeacherAdmin(admin.ModelAdmin):
    filter_horizontal = ("subject_teachers", )

admin.site.register(Student, StudentAdminModel)
admin.site.register(Class, SubjectTeacherAdmin)
admin.site.register(Teacher)
admin.site.register(Parent, ParentAdmin)
admin.site.register(MainSubject, SubjectAdmin)
admin.site.register(SecondSubject, SubjectAdmin)
admin.site.register(EvaluateByCommentSubject, SubjectAdmin)
admin.site.register(ClassSubjectTeacher)


"""
    SUPER USER:
    USERNAME: baobao
    password: Bao12345#
"""