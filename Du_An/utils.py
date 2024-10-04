from .models import *

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
        class_list = []*classes_count
        for i in range(classes_count):
            classroom = Class.objects.create(name=names[i])
            class_list[i] = classroom
        return class_list
    
    #TODO
    @staticmethod
    def create_student(name: str, classroom: Class, role: str | None = None, is_boy: bool | None = None):
        pass

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
                teacher = Teacher(full_name=full_name, username=email, password=password)

                if subjects:
                    teacher.subject.set(subjects)
                
                teacher.save()
                return teacher
            elif type == "parent":
                parent = Parent(full_name=full_name, username=email, password=password)

                if children:
                    parent.children.set(children)

                parent.save()

                return parent
            else:
                raise Exception("Unknow user type")
        except Exception as e:
            print(e)
            return None