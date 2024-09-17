from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Subject(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
    
    def get_teachers(self) -> list:
        return [teacher.serialize for teacher in self.teachers.all()]
    
    def teacher_count(self):
        return self.teachers.count()
    

class Teacher(User):
    full_name = models.CharField(max_length=200, unique=False)
    subject = models.ManyToManyField(Subject, related_name="teachers")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.username,
            "email": self.email,
            "is_boy": self.is_boy
        }


class Parent(User):
    full_name = models.CharField(max_length=200, unique=False)
    children = models.ManyToManyField("Student", related_name="parent")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.username,
            "email": self.email,
        }

    
class Student(models.Model):
    full_name = models.CharField(max_length=200)
    birthday = models.DateField(blank=False)
    is_boy = models.BooleanField()
    main_subjects = models.ManyToManyField("MainSubject", related_name="student")


    def serialize(self):
        return {
            "name": self.full_name,
            "birthday": self.birthday.strftime("%d/%m/%Y"),
            "is_boy": self.is_boy,
            "math": self.math.serialize()
        }



class Class(models.Model):
    form_teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, related_name="form_class")
    name = models.CharField(max_length=3)
    students = models.ManyToManyField(Student, blank=True, related_name="classroom")
    math_teacher = models.ForeignKey(Teacher, blank=True, on_delete=models.DO_NOTHING, related_name="math_classes")

    def student_count(self) -> int:
        return self.students.count()
    
    
    def remove_teacher(self, subject, teacher: Teacher) -> None:
        match(subject):
            case "math":
                self.math_teacher = None
                self.save()
            #TODO

class MainSubject(models.Model):
    name = models.CharField(max_length=20)
    diem_thuong_xuyen1 = models.FloatField(null=True)
    diem_thuong_xuyen2 = models.FloatField(null=True)
    diem_thuong_xuyen3 = models.FloatField(null=True)
    diem_thuong_xuyen4 = models.FloatField(null=True)
    diem_giua_ki = models.FloatField(null=True)
    diem_cuoi_ki = models.FloatField(null=True)
    comment = models.TextField()

    def serialize(self):
        return {
            "thuong_xuyen1": self.diem_thuong_xuyen1,
            "thuong_xuyen2": self.diem_thuong_xuyen2,
            "thuong_xuyen3": self.diem_thuong_xuyen3,
            "thuong_xuyen4": self.diem_thuong_xuyen4,
            "giua_ki": self.diem_giua_ki,
            "cuoi_ki": self.diem_cuoi_ki,
            "teacher_comment": self.comment
        }
    

#function to create a Subject
def create_main_subject(name: str):
    subject = MainSubject.objects.create(name=name)

    return subject

#function to get a student
def get_student(student_name: str, class_name) -> Student | None: #Shouldn't let two students have the same name into a class.
    student = Student.objects.filter().first()
    return student


