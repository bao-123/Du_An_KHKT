from django.contrib import admin
from .models import *

#TODO: Tim hieu them
#* Action to rename subjects
"""
@admin.action(description="Correct name Main subjects")
def correct_name(modeladmin, request, query_set):
    for obj in query_set:
        if obj.name == "Lịch sử & địa lí":
            obj.name = "Lịch Sử & Địa Lí"
            obj.save(force_update=True)

"""
@admin.action(description="Check subjects")
def check_subjects(modeladmin, request, query_set):
    for obj in query_set:
        if obj.name not in (MAIN_SUBJECTS + SECOND_SUBJECTS + COMMENT_SUBJECTS):
            print(obj.name)
            raise Exception("Invalid subject!!!")
    

# Register your models here.
class StudentAdminModel(admin.ModelAdmin):
    list_display = ("id", "full_name", "is_boy")

class ParentAdmin(admin.ModelAdmin):
    filter_horizontal = ("children", )

class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

class SubjectTeacherAdmin(admin.ModelAdmin):
    pass

class SubjectAdmin(admin.ModelAdmin):
    actions = [check_subjects, ]

admin.site.register(Student, StudentAdminModel)
admin.site.register(Class, SubjectTeacherAdmin)
admin.site.register(Teacher)
admin.site.register(Parent, ParentAdmin)
admin.site.register(MainSubject, SubjectAdmin)
admin.site.register(SecondSubject, SubjectAdmin)
admin.site.register(EvaluateByCommentSubject, SubjectAdmin)
admin.site.register(ClassSubjectTeacher)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(ClassYearProfile)
admin.site.register(StudentYearProfile)


"""
    SUPER USER:
    USERNAME: baobao
    password: Bao12345#
"""