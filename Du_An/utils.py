from .models import *
from datetime import date

#Utils functions for views
class ViewUtils():

    @staticmethod
    def get_form_class(teacher: Teacher):
        try:
            return teacher.form_class
        except Teacher.form_class.RelatedObjectDoesNotExist:
            return None
        
    
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
    def create_classes(names: list[str]) -> list[Class]:
        classes_count = len(names)
        class_list = [None]*classes_count
        for i in range(classes_count):
            classroom = Class.objects.create(name=names[i])
            class_list[i] = classroom
        return class_list
    

    @staticmethod
    def create_student(name: str, classroom: Class,
                       role: str | None = None, is_boy: bool | None = None,
                       birthday: date | None = None
                       ) -> Student:
        student = Student.objects.create(full_name=name, classroom=classroom, role=role, is_boy=is_boy, birthday=birthday)

        student.main_subjects.set(MainSubject.generate_main_subjects())
        student.second_term_main_subjects.set(MainSubject.generate_main_subjects())
        student.second_subjects.set(SecondSubject.generate_second_subjects())
        student.second_term_second_subjects.set(SecondSubject.generate_second_subjects())
        student.comment_subjects.set(EvaluateByCommentSubject.generate_comment_subject())
        student.second_term_comment_subjects.set(EvaluateByCommentSubject.generate_comment_subject())

        return student


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