from .models import *
from datetime import date
from typing import Iterable

#Utils functions for views
class ViewUtils():

    @staticmethod
    def get_form_class(teacher: Teacher):
        try:
            return teacher.form_class
        except Teacher.form_class.RelatedObjectDoesNotExist:
            return None
        

#TODO:!
#** functions for testing purpose
class TestUtils():

    #! Only use these functions for testing purpose!
    @staticmethod
    def create_subjects(names: list[str]):
        subjects = []
        for name in names:
            subjects.append(Subject.objects.create(name=name))
        return subjects
    
    @staticmethod
    def create_classroom(name: str, form_teacher: Teacher | None = None, subject_teachers: Iterable[Teacher] = [], year: int = this_year ):
        classroom = Class.objects.create(name=name)
        profile = ClassYearProfile.objects.create(classroom=classroom, form_teacher=form_teacher, year=year)

        for teacher in subject_teachers:
            #*Subject of teachers should be different, this just for testing purpose!
            class_subject_teacher = ClassSubjectTeacher.objects.create(subject=teacher.subject.first(), teacher=teacher) 
            profile.subject_teachers.add(class_subject_teacher)
        
        profile.save(force_update=True)
        return {"classroom": classroom, "profile": profile}
    

    @staticmethod
    def create_student(name: str, classroom: Class,
                       role: str | None = None, is_boy: bool | None = None,
                       birthday: date | None = None
                       ) -> Student:
        student = Student.objects.create(full_name=name, is_boy=is_boy, birthday=birthday)

        student_profile = StudentYearProfile.create_profile(student, role, classroom)

        return {"student": student, "profile": student_profile}


    @staticmethod
    def create_user(type: str | None = None, 
                    email: str | None = None, 
                    password: str | None = None, 
                    full_name: str | None = None,
                    children: list[Student] | None = None,
                    subjects: list[Subject] | None = None
                    ) -> Parent | Teacher | None:
        try:
            if type == "teacher":
                #** We not user 'make_password' just for testing purpose
                teacher = Teacher.objects.create(username=email, children=children, full_name=full_name)

                if subjects:
                    teacher.subject.set(subjects)
                
                teacher.save(force_update=True)
                return teacher
            elif type == "parent":
                parent = Parent.objects.create(username=email, full_name=full_name, password=password)

                if children:
                    parent.children.set(children)

                parent.save(force_update=True)

                return parent
            else:
                raise Exception("Unknow user type")
        except Exception as e:
            print(e)
            return None