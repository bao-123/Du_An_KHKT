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


# Register your models here.
class StudentAdminModel(admin.ModelAdmin):
    list_display = ("id", "full_name", "classroom", "is_boy", "role")
    filter_horizontal = ("main_subjects", "second_subjects", "second_term_main_subjects", "second_term_second_subjects",
                         "comment_subjects", "second_term_comment_subjects")

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
admin.site.register(Subject)


"""
    SUPER USER:
    USERNAME: baobao
    password: Bao12345#
"""