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

@admin.action(description="Create profiles for students")
def create_profiles(modeladmin, request, query_set):
    for student in query_set:
        student_profiles = student.profiles.all()     
        for i in range(2015, 2024):
            #profile = StudentYearProfile(year=i, student=student, clas)
            pass #TODO:

@admin.action(description="Check subjects")
def check_subjects(modeladmin, request, query_set):
    for obj in query_set:
        if obj.name not in (MAIN_SUBJECTS + SECOND_SUBJECTS + COMMENT_SUBJECTS):
            print(obj.name)
            raise Exception("Invalid subject!!!")
        
@admin.action(description="Create default subject")
def create_subjects(modeladmin, request, query_set):
    for subject_name in (MAIN_SUBJECTS + SECOND_SUBJECTS + COMMENT_SUBJECTS):
        if subject_name not in [subject.name for subject in query_set]:
            Subject.objects.create(name=subject_name)
    

    
@admin.action(description="create profiles")
def create_profiles(modeladmin, request, query_set):
    for obj in query_set:
        for i in range(2010, 2025):
            ClassYearProfile.objects.create(year=i, classroom=obj)

    
# Register your models here.
class StudentAdminModel(admin.ModelAdmin):
    list_display = ("id", "full_name", "is_boy")

class ParentAdmin(admin.ModelAdmin):
    filter_horizontal = ("children", )

class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

class ClassAdmin(admin.ModelAdmin):
    list_display = ("name", )
    actions = [create_profiles, ]

class SubjectAdmin(admin.ModelAdmin):
    actions = [check_subjects, create_subjects]

    list_display = ("id", "name")

class StudentSubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

class ClassYearProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "classroom", "year")

admin.site.register(Student, StudentAdminModel)
admin.site.register(Class, ClassAdmin)
admin.site.register(Teacher)
admin.site.register(Parent, ParentAdmin)
admin.site.register(MainSubject, StudentSubjectAdmin)
admin.site.register(SecondSubject, StudentSubjectAdmin)
admin.site.register(EvaluateByCommentSubject, StudentSubjectAdmin)
admin.site.register(ClassSubjectTeacher)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(ClassYearProfile, ClassYearProfileAdmin)
admin.site.register(StudentYearProfile)


"""
    SUPER USER:
    USERNAME: baobao
    password: Bao12345#
"""