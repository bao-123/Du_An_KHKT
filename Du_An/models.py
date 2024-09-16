from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Teacher(User):
    subject = models.CharField(max_length=200)
    is_boy = models.BooleanField()


class Parent(User):
    children = models.ManyToManyField("Student", related_name="parent")

    
class Student(models.Model):
    full_name = models.CharField(max_length=200)
    birthday = models.DateField(blank=False)
    is_boy = models.BooleanField()
    math = models.ForeignKey("MainSubject", on_delete=models.PROTECT, related_name="student")


class Class(models.Model):
    form_teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, related_name="form_class")
    name = models.CharField(max_length=3)
    students = models.ManyToManyField(Student, blank=True, related_name="Class")
    math_teacher = models.ForeignKey(Teacher, blank=True, on_delete=models.DO_NOTHING, related_name="math_teaching_class")

    def student_count(self) -> int:
        return self.students.count()
    
    def remove_teacher(self, subject, teacher: Teacher) -> None:
        match(subject):
            case "math":
                self.math_teacher = None
            #TODO

class MainSubject(models.Model):
    diem_thuong_xuyen1 = models.FloatField(blank=True)
    diem_thuong_xuyen2 = models.FloatField(blank=True)
    diem_thuong_xuyen3 = models.FloatField(blank=True)
    diem_thuong_xuyen4 = models.FloatField(blank=True)
    diem_giua_ki = models.FloatField(blank=True)
    diem_cuoi_ki = models.FloatField(blank=True)
    comment = models.TextField()
    

